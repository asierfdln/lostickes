# import string, random, hashlib
import uuid
from django.db import models
from django.forms import ModelForm
from django.core import validators as vals

# Create your models here.

"""

Operamos bajo el supuesto de que el user2 nunca ha pagado nada, por lo que debe pagar siempre

"""

class User(models.Model):

    name = models.CharField(max_length=55, blank=False)
    email = models.EmailField(max_length=105, unique=True, blank=False)

    """
    -------------------------------------------------------
    SOBRE MI CABEZONERIA Y LAS PRIMARY KEYS UNICAS A MANIJA
    -------------------------------------------------------

    Intentar definir una primkey que dependa de name + email + _random_noise tiene dos problemas:
        - (1) no puedes acceder al texto de name/email tal y como esta definido ahora mismo
        - (2) necesitas que la utilizacion de todas las funciones del modulo de random sean utilizadas
              dentro del metodo __init__ de la clase, ya que si no todos los objetos de la clase User
              tendran el mismo _random_noise, cosa que no nos interesa a la hora de generar primkeys unicas.
              Y, aunque puedas tener _random_noise disponible, tampoco puedes definir un 
              UUIDField dentro del constructor __init__ porque Django se rompe...
    """

    # _random_noise = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(10)))
    # _string_key = f'{_random_noise}' # TODO añadir name y email
    # _key = hashlib.sha256(bytes(_string_key, 'utf-8')).hexdigest()
    # primkey = models.UUIDField(primary_key=True, editable=False, default=_key[:16])
    primkey = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return self.name


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class UserGroup(models.Model):

    name = models.CharField(max_length=55, blank=False)
    desc = models.TextField(max_length=280, blank=False)

    primkey = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    users = models.ManyToManyField(User, blank=False, help_text="Usuarios pertenecientes al grupo.")

    def user_balance(self, user="user2"):
        balance = 0
        for transaction in Transaction.objects.filter(user_group=self):
            balance = balance + transaction.user_account(user=user)

        return balance

    def __str__(self):
        return self.name


class UserGroupForm(ModelForm):
    class Meta:
        model = UserGroup
        fields = "__all__"


class Element(models.Model):

    name = models.CharField(max_length=55, blank=False)
    desc = models.TextField(max_length=280, blank=False)
    price = models.IntegerField(validators=[vals.MinValueValidator(limit_value=0, message="Only positive integers allowed")])

    primkey = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return self.name


class ElementForm(ModelForm):
    class Meta:
        model = Element
        fields = "__all__"


class Transaction(models.Model):

    name = models.CharField(max_length=55, blank=False)
    desc = models.TextField(max_length=280, blank=False)

    primkey = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    user_group = models.ForeignKey(UserGroup, blank=False, on_delete=models.CASCADE, help_text="Grupo al cual pertenence la transaccion.")
    payers = models.ManyToManyField(User, blank=False, help_text="Usuarios entre los que pagar la transaccion.")
    elements = models.ManyToManyField(Element, blank=False, help_text="Introduce elementos de la transaccion.")

    # 1,2;3,4 --> el producto1 es compartido por los payers 1 y 2, el producto2 es compartido por los payers 3 y 4...
    mapping = models.CharField(max_length=55, blank=False, help_text="Para definir que paga cada usuario seguir el siguiente formato: 1,2;2,3,4. ; por cada producto. , por cada usuario responsable.")

    preciototal = None
    payers_elements_mapping = None

    def total_price(self):
        if self.preciototal == None:
            self.preciototal = 0
            for element in self.elements.all():
                self.preciototal = self.preciototal + element.price

        return self.preciototal

    def accounts(self):
        if self.payers_elements_mapping == None:
            payer_counter = 1
            self.payers_elements_mapping = {}
            for payer in self.payers.all():
                element_counter = 0
                self.payers_elements_mapping[payer.name] = 0
                for product in self.elements.all():
                    if str(payer_counter) in self.mapping.split(";")[element_counter]:
                        self.payers_elements_mapping[payer.name] = self.payers_elements_mapping[payer.name] + product.price/len(self.mapping.split(";")[element_counter].split(","))
                    element_counter = element_counter + 1
                payer_counter = payer_counter + 1

        return self.payers_elements_mapping

    def user_account(self, user="user2"):
        if self.payers_elements_mapping == None:
            self.accounts()

        return self.payers_elements_mapping[user]

    def __str__(self):
        return self.name


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'