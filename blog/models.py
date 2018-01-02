# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=80)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("blog:post_detail", kwargs={'idx':self.id})