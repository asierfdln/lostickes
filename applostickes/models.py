import uuid
from django.db import models

# Create your models here.


class User(models.Model):

    # TODO docu
    # TODO imagen,icono

    primkey = models.UUIDField(primary_key=True, editable=false, default=str(uuid.uuid4()))
    name = models.CharField(max_length=55)
    email = models.EmailField(max_length=105, unique=True)

    # TODO foreign keys y demás de grupos y usuarios


class UserGroup(models.Model):

    # TODO docu
    # TODO imagen,icono

    primkey = models.UUIDField(primary_key=True, editable=false, default=str(uuid.uuid4()))
    name = models.CharField(max_length=55)
    desc = models.TextField(max_length=280) # si esto peta, charfield con widget=forms.Textarea

    # TODO foreign keys y demás de grupos y usuarios


# TODO Deudosos, Elementos