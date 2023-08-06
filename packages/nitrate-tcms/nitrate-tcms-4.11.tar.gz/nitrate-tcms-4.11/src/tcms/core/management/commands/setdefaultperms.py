# -*- coding: utf-8 -*-

import logging

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

logger = logging.getLogger(__name__)

# flake8: noqa

DEFAULT_PERMS = {
    'Tester': {
        'classification':               {'add': 1, 'change': 1, 'delete': 0},
        'comment':                      {'add': 1, 'change': 1, 'delete': 0},
        'commentflag':                  {'add': 1, 'change': 0, 'delete': 0},
        'component':                    {'add': 1, 'change': 1, 'delete': 0},
        'contenttype':                  {'add': 1, 'change': 0, 'delete': 0},
        'groups':                       {'add': 1, 'change': 1, 'delete': 0},
        'logentry':                     {'add': 1, 'change': 1, 'delete': 0},
        'milestone':                    {'add': 1, 'change': 1, 'delete': 0},
        'priority':                     {'add': 1, 'change': 1, 'delete': 0},
        'product':                      {'add': 1, 'change': 1, 'delete': 0},
        'profiles':                     {'add': 1, 'change': 1, 'delete': 0},
        'session':                      {'add': 1, 'change': 1, 'delete': 0},
        'tcmsenvgroup':                 {'add': 1, 'change': 1, 'delete': 0},
        'tcmsenvgrouppropertymap':      {'add': 1, 'change': 1, 'delete': 0},
        'tcmsenvplanmap':               {'add': 1, 'change': 1, 'delete': 0},
        'tcmsenvproperty':              {'add': 1, 'change': 1, 'delete': 0},
        'tcmsenvrunvaluemap':           {'add': 1, 'change': 1, 'delete': 1},
        'tcmsenvvalue':                 {'add': 1, 'change': 1, 'delete': 0},
        'tcmslogmodel':                 {'add': 1, 'change': 1, 'delete': 0},
        'testattachment':               {'add': 1, 'change': 1, 'delete': 0},
        'testattachmentdata':           {'add': 1, 'change': 1, 'delete': 0},
        'testbuild':                    {'add': 1, 'change': 1, 'delete': 0},
        'testcase':                     {'add': 1, 'change': 1, 'delete': 0},
        'testcaseattachment':           {'add': 1, 'change': 1, 'delete': 0},
        'issue':                        {'add': 1, 'change': 1, 'delete': 1},
        'issuetracker':                 {'add': 0, 'change': 1, 'delete': 0},
        'testcasecategory':             {'add': 1, 'change': 1, 'delete': 0},
        'testcasecomponent':            {'add': 1, 'change': 1, 'delete': 1},
        'testcaseplan':                 {'add': 1, 'change': 1, 'delete': 1},
        'testcaserun':                  {'add': 1, 'change': 1, 'delete': 1},
        'testcaserunstatus':            {'add': 1, 'change': 1, 'delete': 0},
        'testcasestatus':               {'add': 1, 'change': 1, 'delete': 0},
        'testcasetag':                  {'add': 1, 'change': 1, 'delete': 1},
        'testcasetext':                 {'add': 1, 'change': 1, 'delete': 0},
        'testenvironment':              {'add': 1, 'change': 1, 'delete': 0},
        'testenvironmentcategory':      {'add': 1, 'change': 1, 'delete': 0},
        'testenvironmentelement':       {'add': 1, 'change': 1, 'delete': 0},
        'testenvironmentmap':           {'add': 1, 'change': 1, 'delete': 0},
        'testenvironmentproperty':      {'add': 1, 'change': 1, 'delete': 0},
        'testplan':                     {'add': 1, 'change': 1, 'delete': 0},
        'testplanattachment':           {'add': 1, 'change': 1, 'delete': 0},
        'testplancomponent':            {'add': 1, 'change': 1, 'delete': 1},
        'testplantag':                  {'add': 1, 'change': 1, 'delete': 1},
        'testplantext':                 {'add': 1, 'change': 1, 'delete': 0},
        'testplantype':                 {'add': 1, 'change': 1, 'delete': 0},
        'testrun':                      {'add': 1, 'change': 1, 'delete': 1},
        'testruncc':                    {'add': 1, 'change': 1, 'delete': 1},
        'testruntag':                   {'add': 1, 'change': 1, 'delete': 1},
        'testtag':                      {'add': 1, 'change': 1, 'delete': 1},
        'usergroupmap':                 {'add': 1, 'change': 1, 'delete': 0},
        'version':                      {'add': 1, 'change': 1, 'delete': 0},
        'xmlrpclog':                    {'add': 1, 'change': 1, 'delete': 0},
        'can_moderate':                 1
    },
    'System Admin': {
        'user':                         {'add': 0, 'change': 1, 'delete': 0},
    },
    'Administrator': {
        'classification':               {'add': 1, 'change': 1, 'delete': 0},
        'comment':                      {'add': 1, 'change': 1, 'delete': 0},
        'commentflag':                  {'add': 1, 'change': 1, 'delete': 0},
        'component':                    {'add': 1, 'change': 1, 'delete': 0},
        'contenttype':                  {'add': 1, 'change': 1, 'delete': 0},
        'logentry':                     {'add': 1, 'change': 1, 'delete': 0},
        'milestone':                    {'add': 1, 'change': 1, 'delete': 0},
        'priority':                     {'add': 1, 'change': 1, 'delete': 0},
        'product':                      {'add': 1, 'change': 1, 'delete': 0},
        'profiles':                     {'add': 1, 'change': 1, 'delete': 0},
        'session':                      {'add': 1, 'change': 1, 'delete': 0},
        'site':                         {'add': 1, 'change': 1, 'delete': 0},
        'tcmsenvgroup':                 {'add': 1, 'change': 1, 'delete': 0},
        'tcmsenvgrouppropertymap':      {'add': 1, 'change': 1, 'delete': 0},
        'tcmsenvplanmap':               {'add': 1, 'change': 1, 'delete': 0},
        'tcmsenvproperty':              {'add': 1, 'change': 1, 'delete': 0},
        'tcmsenvrunvaluemap':           {'add': 1, 'change': 1, 'delete': 1},
        'tcmsenvvalue':                 {'add': 1, 'change': 1, 'delete': 0},
        'tcmslogmodel':                 {'add': 1, 'change': 1, 'delete': 0},
        'testattachment':               {'add': 1, 'change': 1, 'delete': 0},
        'testattachmentdata':           {'add': 1, 'change': 1, 'delete': 0},
        'testbuild':                    {'add': 1, 'change': 1, 'delete': 0},
        'testcase':                     {'add': 1, 'change': 1, 'delete': 0},
        'testcaseattachment':           {'add': 1, 'change': 1, 'delete': 0},
        'issue':                        {'add': 1, 'change': 1, 'delete': 1},
        'issuetracker':                 {'add': 0, 'change': 1, 'delete': 0},
        'testcasecategory':             {'add': 1, 'change': 1, 'delete': 0},
        'testcasecomponent':            {'add': 1, 'change': 1, 'delete': 1},
        'testcaseplan':                 {'add': 1, 'change': 1, 'delete': 1},
        'testcaserun':                  {'add': 1, 'change': 1, 'delete': 1},
        'testcaserunstatus':            {'add': 1, 'change': 1, 'delete': 0},
        'testcasestatus':               {'add': 1, 'change': 1, 'delete': 0},
        'testcasetag':                  {'add': 1, 'change': 1, 'delete': 1},
        'testcasetext':                 {'add': 1, 'change': 1, 'delete': 0},
        'testenvironment':              {'add': 1, 'change': 1, 'delete': 0},
        'testenvironmentcategory':      {'add': 1, 'change': 1, 'delete': 0},
        'testenvironmentelement':       {'add': 1, 'change': 1, 'delete': 0},
        'testenvironmentmap':           {'add': 1, 'change': 1, 'delete': 0},
        'testenvironmentproperty':      {'add': 1, 'change': 1, 'delete': 0},
        'testplan':                     {'add': 1, 'change': 1, 'delete': 0},
        'testplanattachment':           {'add': 1, 'change': 1, 'delete': 0},
        'testplancomponent':            {'add': 1, 'change': 1, 'delete': 1},
        'testplantag':                  {'add': 1, 'change': 1, 'delete': 1},
        'testplantext':                 {'add': 1, 'change': 1, 'delete': 0},
        'testplantype':                 {'add': 1, 'change': 1, 'delete': 0},
        'testrun':                      {'add': 1, 'change': 1, 'delete': 1},
        'testruncc':                    {'add': 1, 'change': 1, 'delete': 1},
        'testruntag':                   {'add': 1, 'change': 1, 'delete': 1},
        'testtag':                      {'add': 1, 'change': 1, 'delete': 1},
        'version':                      {'add': 1, 'change': 1, 'delete': 0},
        'xmlrpclog':                    {'add': 1, 'change': 1, 'delete': 0},
        'can_moderate':                 1,
    }
}


class Command(BaseCommand):
    help = (
        'Set permissions to default groups. Generally, this command should run'
        ' just after database migration.'
    )

    def handle(self, *args, **options):
        for group, perms_config in DEFAULT_PERMS.items():
            logger.debug('Set permissions to group %s: %r', group, perms_config)
            for model_name, capabilities in perms_config.items():
                if not isinstance(capabilities, (dict, int)):
                    raise TypeError(
                        'Permission capabilities {} does not have either type '
                        'dict or int.'.format(capabilities))

                group = Group.objects.get(name=group)
                if isinstance(capabilities, dict):
                    for action, is_enabled in capabilities.items():
                        codename = f'{action}_{model_name}'
                        perm = Permission.objects.get(codename=codename)
                        if is_enabled:
                            group.permissions.add(perm)
                        else:
                            group.permissions.remove(perm)
                else:
                    perm = Permission.objects.get(codename=model_name)
                    if capabilities:
                        group.permissions.add(perm)
                    else:
                        group.permissions.remove(perm)
