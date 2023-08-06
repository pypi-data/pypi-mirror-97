# -*- coding:utf-8 -*- 
__author__ = 'denishuang'


def get_user_scope_map(user):
    rsm = getattr(user, '_user_scope_map', None)
    if rsm:
        return rsm
    roles = list(user.saas_roles.all())
    if not roles:
        return
    rsm = {}
    for r in roles:
        rsm.update(r.permissions)
    setattr(user, '_user_scope_map', rsm)
    return rsm


def model_in_user_scope(model, user):
    mn = model._meta.label_lower
    sm = get_user_scope_map(user)
    if not sm:
        return False
    if sm.get(mn, {}).get('scope', None) == '@all':
        return True
    return False
