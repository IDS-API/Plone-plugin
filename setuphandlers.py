# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
#
# GNU General Public License (GPL)
#
__version__ = '$Id: setuphandlers.py 159 2012-05-29 08:26:46Z subhendu $'
__author__ = """Subhendu Kumar Giri <subhendu.giri@oneworld.net>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('Eldis: setuphandlers')
from Products.Eldis.config import PROJECTNAME
from Products.Eldis.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction
##code-section HEAD
##/code-section HEAD

def isNotEldisProfile(context):
    return context.readDataFile("Eldis_marker.txt") is None



def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotEldisProfile(context): return 
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()


def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotEldisProfile(context): return 
    site = context.getSite()


##code-section FOOT
##/code-section FOOT
