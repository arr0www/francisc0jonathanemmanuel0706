from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null = True, unique=True)
    bio = models.TextField(null=True)

    USERNAME_FIELD =  'email'
    REQUIRED_FIELDS = ['username']


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    serialnumber = models.CharField(max_length=200)
    date_published = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    status = models.IntegerField(default = 0)
    description = models.TextField(max_length=200)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']


    def __str__(self):
        return self.name





class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]


class Reservation(models.Model):
    room = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    requestdate = models.DateField()
    returndate = models.DateField()
    bstatus = models.IntegerField(default = 1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-created', '-updated' ]
        


class Reservation2(models.Model):
    room = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    requestdate = models.DateField()
    returndate = models.DateField()
    bstatus = models.IntegerField(default = 1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created', '-updated']
        

class Reservation3(models.Model):
    room = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    requestdate = models.DateField()
    returndate = models.DateField()
    bstatus = models.IntegerField(default = 1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created', '-updated']
        

class Reservation4(models.Model):
    room = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    requestdate = models.DateField()
    returndate = models.DateField()
    bstatus = models.IntegerField(default = 1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created', '-updated']
        




