# import string, random, hashlib
import uuid
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as DjangoUser
from django.core import validators as vals
from django.db import models
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
            'email',
            'password1',
            'password2',
        ]


class UserGroup(models.Model):

    name = models.CharField(max_length=55, blank=False)
    desc = models.TextField(max_length=280, blank=False)

    primkey = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    users = models.ManyToManyField(User, blank=False, help_text="Usuarios pertenecientes al grupo.")

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


class Element(models.Model):

    name = models.CharField(max_length=55, blank=False)
    desc = models.TextField(max_length=280, blank=False)
    price = models.FloatField(validators=[vals.MinValueValidator(limit_value=0.009, message="Only positive integers allowed")])

    primkey = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        ordering = ['name', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = self.name + ' - ' + str(self.price) + ' €'

    def __str__(self):
        return self.name


class ElementForm(forms.ModelForm):

    class Meta:
        model = Element
        fields = '__all__'


class Transaction(models.Model):

    name = models.CharField(max_length=55, blank=False)
    desc = models.TextField(max_length=280, blank=False)

    primkey = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    user_group = models.ForeignKey(UserGroup, blank=False, on_delete=models.CASCADE, help_text="Grupo al cual pertenence la transaccion.")
    payers = models.ManyToManyField(User, blank=False, help_text="Usuarios entre los que pagar la transaccion.")
    elements = models.ManyToManyField(Element, blank=False, help_text="Introduce elementos de la transaccion.")

    # 1,2;3,4 --> el producto1 es compartido por los payers 1 y 2, el producto2 es compartido por los payers 3 y 4...
    mapping = models.CharField(max_length=280, blank=False, help_text="Para definir que paga cada usuario seguir el siguiente formato: 1,2;2,3,4. ; por cada producto. , por cada usuario responsable.")

    score_settling_mapping = PickledObjectField(default=dict)

    preciototal = None
    payers_elements_mapping = None
    tridentifier = None

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

    def accounts(self):
        if self.payers_elements_mapping == None:

            # calculamos lo que tiene que pagar cada payer (el que paga tb)
            payer_counter = 1
            payer_responsible_primkey = None
            self.payers_elements_mapping = {}
            for payer in self.payers.all():
                element_counter = 0
                self.payers_elements_mapping[payer.primkey] = 0
                for product in self.elements.all():
                    if payer_responsible_primkey is None:
                        if str(payer_counter) == self.mapping.split("-")[0]:
                            payer_responsible_primkey = payer.primkey
                    if str(payer_counter) in self.mapping.split("-")[1].split(";")[element_counter]:
                        self.payers_elements_mapping[payer.primkey] = round(self.payers_elements_mapping[payer.primkey], 2) + round(product.price/len(self.mapping.split(";")[element_counter].split(",")), 2)
                    element_counter = element_counter + 1
                payer_counter = payer_counter + 1

            # calculamos lo que se le debe al que paga la cuenta
            lista_payers_quedeben_primkeys = list(self.payers_elements_mapping.keys())
            lista_payers_quedeben_primkeys.remove(payer_responsible_primkey)
            self.payers_elements_mapping[payer_responsible_primkey] = 0
            for payer_quedebe_primkey in lista_payers_quedeben_primkeys:
                self.payers_elements_mapping[payer_responsible_primkey] = round(self.payers_elements_mapping[payer_responsible_primkey], 2) - round(self.payers_elements_mapping[payer_quedebe_primkey], 2)

        return self.payers_elements_mapping

    def user_account(self, user_pk):
        if self.payers_elements_mapping == None:
            self.accounts()

        if self.get_score_state(user_pk) == 'PAYED':
            return 0
        elif self.get_score_state(user_pk) == 'NOTPAYED':
            return self.payers_elements_mapping[user_pk]
        else:
            return self.payers_elements_mapping[user_pk]

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

    user_group = forms.ModelChoiceField(
        empty_label=None,
        queryset=None,
        widget=forms.HiddenInput,
    )

    payer = forms.ModelChoiceField(
        empty_label=None,
        queryset=None,
        widget=forms.Select,
        help_text='Miembro del grupo a pagar la transaccion.'
    )

    elements = forms.ModelMultipleChoiceField(
        queryset=Element.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        help_text='Introduce elementos de la transaccion.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        usergroup_tofilterwith = UserGroup.objects.filter(
            primkey__contains=applostickes.from_group_view_url_string.split('-')[1]
        )

        peoples_paying = User.objects.filter(
            usergroup__in=usergroup_tofilterwith
        )

        self.fields['user_group'].queryset = usergroup_tofilterwith
        self.fields['user_group'].initial = usergroup_tofilterwith[0]
        self.fields['user_group'].help_text = 'Grupo al cual pertenence la transaccion.'

        self.fields['payer'].queryset = peoples_paying