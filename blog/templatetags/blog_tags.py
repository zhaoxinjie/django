#!/usr/bin/env python
# encoding: utf-8
"""
@version: 1.0
@author: zhao
@contact: zhaoxinjie2016@gmail.com
@software: PyCharm
@file: blog_tags.py
@time: 2018/9/17 23:42
"""

from django import template
from django.db.models import Count

from ..models import Post, Category, Tag
from comments.models import Comment

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def comments():
    return Comment.objects.all()[:10]


@register.simple_tag
def get_categories():
    # 记得在顶部引入 count 函数
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    # 记得在顶部引入 Tag model
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)