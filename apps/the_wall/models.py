from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
UpperCasePassword_REGEX=re.compile(r'^(?=.*?[A-Z])')
LowerCasePassword_REGEX=re.compile(r'^(?=.*?[a-z])')

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors["first_name"] = "Please enter a first name"
        if len(postData['first_name']) >= 1 and len(postData['first_name']) <= 2:
            errors["first_name"] = "First name must be longer than 2 characters"
        if str.isalpha(postData['first_name']) == False:
            errors["first_name"] = "First name must contain only letters"
        if len(postData['last_name']) < 1:
            errors["last_name"] = "Please enter a last name"
        if len(postData['last_name']) >= 1 and len(postData['first_name']) <= 2:
            errors["last_name"] = "Last name must be longer than 2 characters"
        if str.isalpha(postData['last_name']) == False:
            errors["last_name"] = "Last name must contain only letters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Please enter a valid email address ex. 'yourname@email.com'"
        if User.objects.filter(email=postData['email']).exists():
            errors["email"] = "Duplicate email detected! Please use a different email"
        if len(postData['password']) < 1:
            errors["password"] = "Please enter a password"
        if len(postData['password']) >= 1 and len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters longer"
        if not UpperCasePassword_REGEX.match(postData['password']):
            errors["password"] = "Password must containh at least  upper case character"
        if not LowerCasePassword_REGEX.match(postData['password']):
            errors["password"] = "Password must containh at least one lower case character"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class MessagePost(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message_poster = models.ForeignKey(User, related_name="posted_message")

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment_poster = models.ForeignKey(User, related_name="posted_comment")
    commented_on = models.ForeignKey(MessagePost, related_name="message_comment")


