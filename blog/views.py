# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response,get_object_or_404,render
from django.utils.text import slugify
import markdown
from markdown.extensions.toc import TocExtension
from .models import Post,Category
from comments.forms import CommentForm

def index(request):
    post_list = Post.objects.all()
    return render_to_response('blog/index.html',{'post_list':post_list})

def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    md = markdown.Markdown(extensions=[
	'markdown.extensions.extra',
	'markdown.extensions.codehilite',
	TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {'post':post,
               'toc':md.toc,
	       'form':form,
	       'comment_list':comment_list,
              }
    return render(request,'blog/detail.html',context)

def archives(request,year,month):
    post_list = Post.objects.filter(created_time__year=year,created_time__month=month)
    return render_to_response('blog/index.html',{'post_list':post_list})
 
def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render_to_response('blog/index.html',{'post_list':post_list})

def blog(request):
    post_list = Post.objects.all()
    return render_to_response('blog/blog.html',{'post_list':post_list})
    
def about(request):
    return render_to_response('blog/about.html',{})

def contact(request):
    return render_to_response('blog/contact.html',{})

def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
	error_msg = "请输入关键词"
	return render_to_response('blog/index.html',{'error_msg':error_msg})
    post_list = Post.objects.filter(title__icontains=q)
    return render_to_response('blog/index.html',{'error_msg':error_msg,
                                                 'post_list':post_list})
