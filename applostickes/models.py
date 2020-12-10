# import string, random, hashlib
import uuid
from django.db import models
from django import forms
from django.core import validators as vals
import applostickes

# Create your models here.


class User(models.Model):

    name = models.CharField(max_length=55, blank=False)
    email = models.EmailField(max_length=105, unique=True, blank=False)


    # TODO @asier probar esto de __init__ con:
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)

    # _random_noise = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(10)))
    # _string_key = f'{_random_noise}' # TODO @asier añadir name y email
    # _key = hashlib.sha256(bytes(_string_key, 'utf-8')).hexdigest()
    # primkey = models.UUIDField(primary_key=True, editable=False, default=_key[:16])
    primkey = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    """
        -------------------------------------------------------
        SOBRE MI CABEZONERIA Y LAS PRIMARY KEYS UNICAS A MANIJA
        -------------------------------------------------------

        Intentar definir una primkey que dependa de name + email + _random_noise tiene dos problemas:
            - (1) no puedes acceder al texto de name/email tal y como esta definido ahora mismo porque son 
                fields que son creados en si al mismo tiempo que el propio valor de primkey...
            - (2) necesitas que la utilizacion de todas las funciones del modulo de random sean utilizadas
                dentro del metodo __init__ de la clase, ya que si no todos los objetos de la clase User
                tendran el mismo _random_noise, cosa que no nos interesa a la hora de generar primkeys unicas.
                Y, aunque puedas tener _random_noise disponible, tampoco puedes definir un 
                UUIDField dentro del constructor __init__ porque Django se rompe...

    """

    uidentifier = None

    def get_uidentifier(self):
        if self.uidentifier == None:
            self.uidentifier = str(self.primkey)[:8]

        return self.uidentifier

    def __str__(self):
        return self.name


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


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
        for transaction in Transaction.objects.filter(user_group=self):
            balance = balance + transaction.user_account(user_pk=user_pk)

        return balance

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
    price = models.IntegerField(validators=[vals.MinValueValidator(limit_value=0, message="Only positive integers allowed")])

    primkey = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

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

    preciototal = None
    payers_elements_mapping = None
    tridentifier = None

    def total_price(self):
        if self.preciototal == None:
            self.preciototal = 0
            for element in self.elements.all():
                self.preciototal = self.preciototal + element.price

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
                        # esta seria la parte donde metes el caso de el que paga pero que no tiene
                        # ningun elemento asignado a su nombre en la transaccion
                        # else:
                        #     pass
                    if str(payer_counter) in self.mapping.split("-")[1].split(";")[element_counter]:
                        self.payers_elements_mapping[payer.primkey] = round(self.payers_elements_mapping[payer.primkey], 2) + round(product.price/len(self.mapping.split(";")[element_counter].split(",")), 2)
                    element_counter = element_counter + 1
                payer_counter = payer_counter + 1

            # calculamos lo que se le debe al que paga la cuenta
            lista_payers_quedeben_primkeys = list(self.payers_elements_mapping.keys())
            print(payer_responsible_primkey)
            lista_payers_quedeben_primkeys.remove(payer_responsible_primkey)
            self.payers_elements_mapping[payer_responsible_primkey] = 0
            for payer_quedebe_primkey in lista_payers_quedeben_primkeys:
                self.payers_elements_mapping[payer_responsible_primkey] = round(self.payers_elements_mapping[payer_responsible_primkey], 2) - round(self.payers_elements_mapping[payer_quedebe_primkey], 2)

        return self.payers_elements_mapping

    def user_account(self, user_pk):
        if self.payers_elements_mapping == None:
            self.accounts()

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
        widget=forms.Select,
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
            primkey__contains=applostickes.from_group_to_createDebt_string.split('-')[1]
        )

        peoples_paying = User.objects.filter(
            usergroup__in=usergroup_tofilterwith
        )

        self.fields['user_group'].queryset = usergroup_tofilterwith
        self.fields['user_group'].initial = usergroup_tofilterwith[0]
        self.fields['user_group'].help_text = 'Grupo al cual pertenence la transaccion.'

        self.fields['payer'].queryset = peoples_paying