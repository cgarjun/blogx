# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urllib import quote_plus
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Post
from blog.form import PostForm
# Create your views here.


def post_create(request):
    if not request.user.is_staff or not request.user.superuser:
        raise Http404

    if not request.user.is_authenticated():
        raise Http404
        
    form = PostForm(request.POST or None, request.FILES or None)
    context = {'form': form}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully created post")
        return HttpResponseRedirect(instance.get_absolute_url())
    return render(request, "post_form.html", context)

def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    share_string = quote_plus(instance.content)
    context = {
        "title": "details",
        "instance":instance,
        "share_string":share_string
    }
    return render(request, "post_detail.html", context)

def post_list(request):
    queryset_all = Post.objects.all()
    paginator = Paginator(queryset_all, 3)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
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
        "title": "details",
        "page_request_var":page_request_var
    }
    return render(request, "index.html", context)

def post_update(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)

    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
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

def post_delete(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    return redirect("blog:list")