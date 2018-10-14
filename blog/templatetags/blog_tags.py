#!/usr/bin/env python
# encoding: utf-8
"""
@version: 1.0
@author: zhao
@contact: zhaoxinjie2016@gmail.com
@software: PyCharm
@file: blog_tags.py
@time: 2018/9/17 23:42
 自定义模板，可以在html中调用函数，取得它的返回值作为变量，渲染html
"""

from django import template
from django.db.models import Count

from ..models import Post, Category, Tag
from comments.models import Comment

register = template.Library()


# 获取最近文章
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


# 归档文章，按年月
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


# 列出最近的10条评论
@register.simple_tag
def comments():
    return Comment.objects.all()[:10]


# 获取所有分类
@register.simple_tag
def get_categories():
    # 记得在顶部引入 count 函数
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


# 获取标签
@register.simple_tag
def get_tags():
    # 记得在顶部引入 Tag model
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


# 查询某分类下的文章数量
@register.simple_tag
def get_count_of_category(category_pk):
    return Post.objects.filter(category=category_pk).count()


# 查询归档年月的文章数量
@register.simple_tag
def get_count_of_date(year, month):
    return Post.objects.filter(created_time__year=year, created_time__month=month).count()


@register.simple_tag
def get_most_views_host(num = 5):
    return Post.objects.all().order_by('-views')[:num]