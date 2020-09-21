from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_no = models.IntegerField()
    address = models.CharField(max_length=200)
    sex = models.CharField(max_length=50)
    dob = models.DateField(null = True, blank=True,)
    age = models.IntegerField(blank=True, null = True)
    blood_group = models.CharField(max_length=3)
    photo = models.ImageField(upload_to = 'users/%Y/%m/%d', blank = True)
    archive = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
