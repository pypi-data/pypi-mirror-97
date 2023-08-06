# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.dispatch import receiver
from django.db.models.signals import post_save
from . import models

# @receiver(post_save, sender=models.Party)
# def create_tenant(sender, **kwargs):
#     if kwargs['created']:
#         party = kwargs['instance']
#         from xyz_tenant.tasks import gen_tenant
#         data = dict(schema_name=party.uid, domain_url=party.slug, name=party.name)
#         gen_tenant.delay(data)
