from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User,AbstractUser
import hashlib
from api.utility import sendTransaction

class CustomUser(AbstractUser):
    ip=models.CharField(max_length=200)
class PostBacheca(models.Model):
    author = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    hash=models.CharField(max_length=32,default=None,null=True)
    txId= models.CharField(max_length=66,default=None,null=True)

    def writeOnChain(self):
        self.hash=hashlib.sha256(self.text.encode('utf-8')).hexdigest()
        self.txId=sendTransaction(self.hash)
        self.save()
