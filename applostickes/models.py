import uuid
from django.db import models
from django.core import validators as vals

# Create your models here.


class User(models.Model):

    # TODO docu
    # TODO imagen,icono

    # hacer el tema este hashlib y sha256(name + email + ruido_random)
    primkey = models.UUIDField(primary_key=True, editable=False, default=str(uuid.uuid4()))
    name = models.CharField(max_length=55, blank=False)
    email = models.EmailField(max_length=105, unique=True, blank=False)

    def __str__(self):
        # TODO un poco mas mejor
        return self.name


class UserGroup(models.Model):

    # TODO docu
    # TODO imagen,icono

    primkey = models.UUIDField(primary_key=True, editable=False, default=str(uuid.uuid4()))
    name = models.CharField(max_length=55, blank=False)
    desc = models.TextField(max_length=280, blank=False) # si esto peta, charfield con widget=forms.Textarea

    users = models.ManyToManyField(User, help_text="Users belonging to this group")

    users_names = []

    def generate_list_of_users_names(self):
        # for user in self.users: # TODO ver como manejar objetos de fk
        #     users_names.append(user.name)
        pass

    def add_user(self, user):
        # self.users.add(user)
        pass

    def delete_user(self, user):
        # self.users.remove(user)
        pass

    def calc_user_balance(self, user):
        pass # la funxion de ver cuánto te deben / debes en este grupo

    def __init__(self, **kwargs):
        self.generate_list_of_users_names()

    def __str__(self):
        # TODO un poco mas mejor
        return self.name


class Transaction(models.Model):

    primkey = models.UUIDField(primary_key=True, editable=False, default=str(uuid.uuid4()))
    name = models.CharField(max_length=55, blank=False)
    desc = models.TextField(max_length=280, blank=False) # si esto peta, charfield con widget=forms.Textarea

    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    elements = models.ManyToManyField('Element', help_text="Enter thangz to pay for")

    preciototal = None # TODO...

    # FOREIGN KEY PERO LIMITADAAAAAAAAAAAAAAAAAAAAAAA
    owner = models.CharField(max_length=55)

    def calc_user_balance(self):
        pass

    def __str__(self):
        # TODO un poco mas mejor
        return self.name


class Element(models.Model):

    primkey = models.UUIDField(primary_key=True, editable=False, default=str(uuid.uuid4()))
    name = models.CharField(max_length=55, blank=False)
    desc = models.TextField(max_length=280, blank=False) # si esto peta, charfield con widget=forms.Textarea
    price = models.IntegerField(validators=[vals.MinValueValidator(limit_value=0, message="Only positive integers allowed")])