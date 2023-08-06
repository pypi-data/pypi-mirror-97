# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from . import choices
from xyz_util import modelutils

class Party(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "团体"

    name = models.CharField("名称", max_length=128)
    logo = models.URLField("标识图Url", blank=True, null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    modify_time = models.DateTimeField("修改时间", auto_now=True)

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        self.name = self.name.replace(" ", "")
        return super(Party, self).save(**kwargs)


class Master(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "管理员"

    user = models.OneToOneField(User, verbose_name=User._meta.verbose_name, null=True, blank=True, related_name="as_saas_master")

    def __unicode__(self):
        return self.user.get_full_name()


class App(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "应用"

    name = models.CharField("名字", max_length=64, unique=True)
    title = models.CharField("标题", max_length=64, unique=True)
    status = models.PositiveSmallIntegerField("状态", choices=choices.CHOICES_APP_STATUS,
                                              default=choices.APP_STATUS_INSTALL)
    settings = modelutils.JSONField('配置信息', blank=True, default={})
    settings_meta = modelutils.JSONField('配置定义', blank=True, default={})
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    modify_time = models.DateTimeField("修改时间", auto_now=True)

    def __unicode__(self):
        return self.title


class Role(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "角色"

    name = models.CharField("名字", max_length=64, unique=True)
    permissions = modelutils.JSONField("权限", blank=True, default={})
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    modify_time = models.DateTimeField("修改时间", auto_now=True)
    users = models.ManyToManyField(User, blank=True, related_name="saas_roles")

    def __unicode__(self):
        return self.name
