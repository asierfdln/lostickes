import uuid
from django.db import models
from django.core import validators as vals

## Create your models here.
#
#
#class User(models.Model):
#
#    # TODO docu
#    # TODO imagen,icono
#
#    primkey = models.UUIDField(primary_key=True, editable=False, default=str(uuid.uuid4()))
#    name = models.CharField(max_length=55)
#    email = models.EmailField(max_length=105, unique=True)
#
#    def __str__(self):
#        # TODO un poco mas mejor
#        return self.name
#
#
#class UserGroup(models.Model):
#
#    # TODO docu
#    # TODO imagen,icono
#
#    primkey = models.UUIDField(primary_key=True, editable=False, default=str(uuid.uuid4()))
#    name = models.CharField(max_length=55)
#    desc = models.TextField(max_length=280) # si esto peta, charfield con widget=forms.Textarea
#
#    users = models.ManyToManyField(User, help_text="Users belonging to this group")
#
#    users_names = []
#
#    def generate_list_of_users_names(self):
#        for user in self.user_set.all(): # TODO ver como manejar objetos de fk
#            users_names.append(user.name)
#
#    def add_user(self):
#        pass # TODO
#
#    def __init__(self):
#        self.generate_list_of_users_names()
#    
#    def __str__(self):
#        # TODO un poco mas mejor
#        return self.name
#
#
#class Transaction(models.Model):
#
#    primkey = models.UUIDField(primary_key=True, editable=False, default=str(uuid.uuid4()))
#    name = models.CharField(max_length=55)
#    desc = models.TextField(max_length=280) # si esto peta, charfield con widget=forms.Textarea
#
#    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
#    elements = models.ManyToManyField('Element', help_text="Enter thangz to pay for")
#
#    
#    preciototal = None # TODO...
#
#    def calc(self):
#        pass
#
#    def validate_owner(owner_string):
#        if owner_string not in self.user_group.users_names: # TODO ver como manejar objetos de fk
#            raise ValidationError("Owner not in user group")
#        else:
#            return owner_string
#
#    owner = models.CharField(max_length=55, validators=[validate_owner('')])
#
#
#    def __str__(self):
#        # TODO un poco mas mejor
#        return self.name
#
#
#class Element(models.Model):
#
#    primkey = models.UUIDField(primary_key=True, editable=False, default=str(uuid.uuid4()))
#    name = models.CharField(max_length=55)
#    desc = models.TextField(max_length=280) # si esto peta, charfield con widget=forms.Textarea
#    price = models.IntegerField(validators=[vals.MinValueValidator(limit_value=0, message="Only positive integers allowed")])