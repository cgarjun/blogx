# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from blog.models import Post
# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'created_at', 'updated_at']
	list_display_links = ['updated_at']
	list_filter = ['updated_at']
	search_fields = ['title', 'content']
	class Meta:
		model = Post


admin.site.register(Post, PostModelAdmin)