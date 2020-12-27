# import string, random, hashlib
import uuid
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as DjangoUser
from django.core import validators as vals
from django.db import models
from django.utils.translation import gettext_lazy as _
from picklefield.fields import PickledObjectField
import applostickes

# Create your models here.


class User(models.Model):

    # ver https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#extending-the-existing-user-model
    django_user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, null=True) # null=True == ñapa...
    primkey = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    uidentifier = None

    def get_uidentifier(self):
        if self.uidentifier == None:
            self.uidentifier = str(self.primkey)[:8]

        return self.uidentifier

    def __str__(self):
        return self.django_user.username


class UserForm(UserCreationForm):

    class Meta:
        model = DjangoUser
        fields = [
            'username',
            'password1',
            'password2',
        ]


class UserGroup(models.Model):

    name = models.CharField(max_length=55, blank=False) # _('ug_name')
    desc = models.TextField(max_length=280, blank=False) # _('ug_desc')

    primkey = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    users = models.ManyToManyField(User, blank=False, help_text=_("Users belonging to group."))

    ugidentifier = None

    """
        ------------------------------------------------------------------------------------------
        PENSAMIENTOS ACERCA DE ESTA MINIPRIMARYKEY DE ugidentifier (tb aplicable a Transaction...)
        ------------------------------------------------------------------------------------------

        Este identificador (como su nombre apunta) esta pensado para ser usado en la view de group(). La 
        idea es que, antes que hacer una query del grupo clickado en groups() en la view de group() con la 
        primkey del propio grupo (lo cual implicaria tener la primkey de los grupos por ahi en las 
        plantillas para que todo quisqui las vea, cosa mala...), es mejor pasar como parametro a la vista 
        group() un identificador no clave (es decir, a partir del cual no se pueda inferir todo el 
        importante campo de la clave primaria de uuid del grupo del cual proviene) que identifique 
        univocamente a un grupo de entre todos los demas, cosa que la fecha de creacion del grupo o su 
        nombre o el nombre+fechadecreacion no pueden hacer.

        Para ello, estamos "confiando" en que los campos primkey uuid de los grupos son robustos ante 
        colisiones parciales, es decir, que los (arbitrarios) primeros 8 caracteres de los campos de 
        primkey no se repiten de grupo a grupo y, por lo tanto, sirven como identificadores univocos de 
        los grupos sin llegar a ser una clara filtracion de como funciona nuestra base de datos por debajo. 
        Este acto de confianza ha conllevado algo de lectura de la literatura acerca de UUID, preguntar 
        a @asier sobre el tema...

    """

    def user_balance(self, user_pk):
        balance = 0
        user_to_filter_transactionsofgroup_with = User.objects.get(primkey=user_pk)
        for transaction in Transaction.objects.filter(user_group=self):
            if user_to_filter_transactionsofgroup_with in transaction.payers.all():
                balance = balance + transaction.user_account(user_pk=user_pk)

        return round(balance, 2)

    def get_ugidentifier(self):
        if self.ugidentifier == None:
            self.ugidentifier = str(self.primkey)[:8]

        return self.ugidentifier

    def __str__(self):
        return self.name


class UserGroupForm(forms.ModelForm):

    class Meta:
        model = UserGroup
        fields = '__all__'

    users = forms.ModelChoiceField(
        empty_label=None,
        queryset=None,
        widget=forms.Select
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.exclude(primkey=applostickes.user_primkey_exclude)
        self.fields['users'].help_text = _('Users to choose from...')


class Element(models.Model):

    name = models.CharField(max_length=55, blank=False)
    price = models.FloatField(validators=[vals.MinValueValidator(limit_value=0.009, message=_("Only positive integers allowed"))])

    primkey = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    creation_date = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        get_latest_by = 'creation_date'
        ordering = ['creation_date']

    def __str__(self):
        return self.name + ' - ' + str(self.price) + ' €'


class ElementForm(forms.ModelForm):

    class Meta:
        model = Element
        fields = '__all__'


class Transaction(models.Model):

    name = models.CharField(
        max_length=55,
        blank=False
    )
    desc = models.TextField(
        max_length=280,
        blank=False
    )

    primkey = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    user_group = models.ForeignKey(
        UserGroup,
        blank=False,
        on_delete=models.CASCADE
    )
    payers = models.ManyToManyField(
        User,
        blank=False,
        help_text=_('Users involved in transaction.')
    )
    elements = models.ManyToManyField(
        Element,
        blank=False,
        help_text=_('Elements involved in transaction.')
    )

    mapping = models.CharField(
        max_length=280,
        blank=False,
        help_text=_('Mapping of whose is what and such...')
    )

    score_settling_mapping = PickledObjectField(default=dict)

    creation_date = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        get_latest_by = 'creation_date'
        ordering = ['-creation_date']

    preciototal = None
    tridentifier = None
    payers_elements_mapping = None
    payer_responsible_primkey = None

    def generate_score_settling_mapping(self):

        if self.payers_elements_mapping == None:
            self.accounts()

        for payer in self.payers.all():
            self.score_settling_mapping[payer.primkey] = {
                'transaction_role': 'Rol del payer, en la transaccion: OWNER - DEBTER',
                'transaction_state': 'Estado de la deuda: PAYED - NOTPAYED',
            }
            if self.payers_elements_mapping[payer.primkey] < 0:
                self.score_settling_mapping[payer.primkey]['transaction_role'] = 'OWNER'
                self.score_settling_mapping[payer.primkey]['transaction_state'] = 'NOTPAYED'
            else:
                self.score_settling_mapping[payer.primkey]['transaction_role'] = 'DEBTER'
                self.score_settling_mapping[payer.primkey]['transaction_state'] = 'NOTPAYED'

    def get_score_role(self, user_primkey):
        return self.score_settling_mapping[user_primkey]['transaction_role']

    def get_score_state(self, user_primkey):
        return self.score_settling_mapping[user_primkey]['transaction_state']

    def pay_transaction(self, user_primkey):

        # "pagamos"
        self.score_settling_mapping[user_primkey]['transaction_state'] = 'PAYED'

        # miramos a ver si hemos pagado todos los DEBTERS
        emospagadotos = True
        for key in self.score_settling_mapping.keys():
            if self.get_score_state(key) == 'NOTPAYED' and self.get_score_role(key) == 'DEBTER':
                emospagadotos = False

        if emospagadotos:
            self.mark_as_payed()
        else:
            self.save()

    def mark_as_payed(self):

        # ponemos que todo el mundo ha "pagado" y que al OWNER le han "pagado"
        for key in self.score_settling_mapping.keys():
            self.score_settling_mapping[key]['transaction_state'] = 'PAYED'

        self.save()

    def total_price(self):
        if self.preciototal == None:
            self.preciototal = 0
            for element in self.elements.all():
                self.preciototal = round(self.preciototal, 2) + round(element.price, 2)

        return self.preciototal

    def accounts(self, i_have_payed_and_here_is_my_primkey=None):

        if self.payers_elements_mapping == None:

            #################################################################
            # calculamos lo que tiene que pagar cada payer (el que paga tb) #
            #################################################################

            # contador de usuarios en el string de mapping (arrays empiezan en 1)
            payer_counter = 1

            # iniciamos el diccionario de mappin vacio
            self.payers_elements_mapping = {}

            # en todos los payers de la transaccion...
            for payer in self.payers.all():

                # empezamos el contador de elementos (arrays empiezan en cero)
                element_counter = 0

                # precio que tiene que pagar el usuario de momento cero, ahora recorremos los elementos 
                # en los que esta involucrado para ver cuanto debe...
                self.payers_elements_mapping[payer.primkey] = 0

                # si todavia nohemos encontrado al que paga...
                if self.payer_responsible_primkey is None:

                    # ...y resulta que su numero es el del usuario pagador al principio de mapping...
                    if str(payer_counter) == self.mapping.split("-")[0]:

                        # hemos encontrado nuestro pagador
                        self.payer_responsible_primkey = payer.primkey

                # en todos los productos de la transaccion...
                for product in self.elements.all():

                    # si el usuario en el que estamos esta registrado en el elemento del bucle for...
                    if str(payer_counter) in self.mapping.split("-")[1].split(";")[element_counter]:

                        # actualizamos su deuda total con el que ha pagado
                        self.payers_elements_mapping[payer.primkey] = round(self.payers_elements_mapping[payer.primkey], 2) + round(product.price/len(self.mapping.split(";")[element_counter].split(",")), 2)
                    
                    # atualizamos el contador de elementos
                    element_counter = element_counter + 1

                # actualizamos el contador de pagadores
                payer_counter = payer_counter + 1

            ######################################################
            # calculamos lo que se le debe al que paga la cuenta #
            ######################################################

            lista_payers_quedeben_primkeys = list(self.payers_elements_mapping.keys())
            lista_payers_quedeben_primkeys.remove(self.payer_responsible_primkey)
            self.payers_elements_mapping[self.payer_responsible_primkey] = 0
            for payer_quedebe_primkey in lista_payers_quedeben_primkeys:
                self.payers_elements_mapping[self.payer_responsible_primkey] = round(self.payers_elements_mapping[self.payer_responsible_primkey], 2) - round(self.payers_elements_mapping[payer_quedebe_primkey], 2)

        return self.payers_elements_mapping

    def user_account(self, user_pk):
        if self.payers_elements_mapping == None:
            self.accounts()

        if self.get_score_state(user_pk) == 'PAYED':
            return 0
        elif self.get_score_state(user_pk) == 'NOTPAYED':
            if self.get_score_role(user_pk) == 'DEBTER':
                return self.payers_elements_mapping[user_pk]
            elif self.get_score_role(user_pk) == 'OWNER':
                owner_balance = self.payers_elements_mapping[user_pk]
                for key in self.score_settling_mapping.keys():
                    if self.get_score_state(key) == 'PAYED' and self.get_score_role(key) == 'DEBTER':
                        owner_balance = owner_balance + self.payers_elements_mapping[key]
                return owner_balance
        else:
            return self.payers_elements_mapping[user_pk]

    def is_payed(self):
        moroso_found = False
        for payer in self.payers.all():
            if self.get_score_state(payer.primkey) == 'NOTPAYED':
                moroso_found = True
                break
        return moroso_found

    def get_tridentifier(self):
        if self.tridentifier == None:
            self.tridentifier = str(self.primkey)[:8]

        return self.tridentifier

    def __str__(self):
        return self.name


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = [
            'name',
            'desc',
            'user_group',
            'payer',
            'elements',
        ]

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'textinput textInput form-control',
            }
        )
    )

    desc = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'textarea form-control',
            }
        )
    )

    user_group = forms.ModelChoiceField(
        empty_label=None,
        queryset=None,
        widget=forms.HiddenInput,
    )

    payer = forms.ModelChoiceField(
        empty_label=None,
        queryset=None,
        widget=forms.Select(
            attrs={
                'class': 'select form-control',
            }
        )
    )

    elements = forms.ModelMultipleChoiceField(
        queryset=Element.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        usergroup_tofilterwith = UserGroup.objects.filter(
            primkey__contains=applostickes.from_group_view_url_string.split('-')[1]
        )

        peoples_paying = User.objects.filter(
            usergroup__in=usergroup_tofilterwith
        )

        self.fields['name'].label = _('Name')
        self.fields['desc'].label = _('Description')

        self.fields['user_group'].queryset = usergroup_tofilterwith
        self.fields['user_group'].initial = usergroup_tofilterwith[0]

        self.fields['payer'].label = _('Payer')
        self.fields['payer'].queryset = peoples_paying
        self.fields['payer'].help_text = _('Member of group paying for the whole thing.')

        self.fields['elements'].label = _('Elements')