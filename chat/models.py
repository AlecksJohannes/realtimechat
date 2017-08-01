# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.six import python_2_unicode_compatible
from django.db import models

@python_2_unicode_compatible
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Conversation(models.Model):
    sender_id = models.ForeignKey(User, related_name='%(class)s_sender')
    recipient_id = models.ForeignKey(User, related_name='%(class)s_receipient')



@python_2_unicode_compatible
class Message(models.Model):
    body = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    is_read = models.BooleanField(default=False)
    conversation = models.ForeignKey(Conversation)
    def __str__(self):
        return "%s" % (self.body)
