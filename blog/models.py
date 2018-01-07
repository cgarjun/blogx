# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.db import models

# Create your models here.

def upload_location(instance, filename):
	return "{0}/{1}".format(instance.id, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=80)
	content = models.TextField()
	cover_image = models.ImageField(null=True, blank=True, upload_to = upload_location)
	slug = models.SlugField(unique=True)
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("blog:post_detail", kwargs={'slug':self.slug})

	class Meta:
		ordering = ['-created_at']


def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug=new_slug

	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()

	if exists:
		new_slug = "{0}-{1}".format(slug, qs.first().id)
		return create_slug(instance, new_slug)

	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)