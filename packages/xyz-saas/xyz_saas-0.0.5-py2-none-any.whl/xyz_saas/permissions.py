# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from rest_framework.permissions import DjangoModelPermissions

__author__ = 'denishuang'
import helper
from xyz_auth.permissions import RoleResPermissions as RRPermissions

class RoleResPermissions(RRPermissions):

    # def has_permission(self, request, view):
    #     b = super(RoleResPermissions, self).has_permission(request, view)
    #     if b:
    #         return b
    #     return helper

    def has_object_permission(self, request, view, obj):
        b = super(RoleResPermissions, self).has_object_permission(request, view, obj)
        if b:
            return b
        return helper.model_in_user_scope(obj, request.user)
