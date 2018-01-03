# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Post
from blog.form import PostForm
# Create your views here.


def post_create(request):
    form = PostForm(request.POST)
    context = {'form': form}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully created post")
        return HttpResponseRedirect(instance.get_absolute_url())
    return render(request, "post_form.html", context)

def post_detail(request, idx=None):
    instance = get_object_or_404(Post, id=idx)
    context = {
        "title": "details",
        "instance":instance
    }
    return render(request, "post_detail.html", context)

def post_list(request):
    queryset_all = Post.objects.all()
    paginator = Paginator(queryset_all, 3)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
    "object_list":queryset,
        "title": "details"
    }
    return render(request, "index.html", context)

def post_update(request, idx=None):
    instance = get_object_or_404(Post, id=idx)

    form = PostForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "details",
        "instance":instance,
        "form": form
    }
    return render(request, "post_form.html", context)

def post_delete(request, idx):
    instance = get_object_or_404(Post, id=idx)
    instance.delete()
    return redirect("blog:list")