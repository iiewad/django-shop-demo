from django.db import models
from datetime import datetime


class Types(models.Model):
    name = models.CharField(max_length=32)
    pid = models.IntegerField(default=0)
    path = models.CharField(max_length=255)

    class Meta:
        db_table = "type"
    

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=32)
    name = models.CharField(max_length=16)
    password = models.CharField(max_length=32)
    sex = models.IntegerField(default=1)
    address = models.CharField(max_length=255)
    code = models.CharField(max_length=6)
    phone = models.CharField(max_length=16)
    email = models.CharField(max_length=50)
    state = models.IntegerField(default=1)
    addtime = models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {
            'id':self.id,
            'username':self.username,
            'name':self.name,
            'password':self.password,
            'address':self.address,
            'phone':self.phone,
            'email':self.email,
            'state':self.state,
            'addtime':self.addtime
        }

    class Meta:
        db_table = "users"
