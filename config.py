# -*- coding: utf-8 -*-
#
# File: Eldis.py
#
#
# GNU General Public License (GPL)
#
__version__ = '$Id: config.py 159 2012-05-29 08:26:46Z subhendu $'
__author__ = """Subhendu Kumar Giri <subhendu.giri@oneworld.net>"""
__docformat__ = 'plaintext'

from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = "Eldis"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))
ADD_CONTENT_PERMISSIONS = {
    'EldisArticle': 'Eldis: Add EldisArticle',
}

setDefaultRoles('Eldis: Add EldisArticle', ('Manager','Owner'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []


eldis_states = (('publish','submit','draft'))
PROPERTIES = (('ELDIS_GUID', 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxx-xx', 'string'),
              ('ELDIS_HOST', 'http://api.ids.ac.uk/', 'string'),
              ('ELDIS_FORMAT', 'full', 'string'),							
              ('ELDIS_DATATYPE', '', 'string'),
              ('ELDIS_NO_RECORDS', '20', 'string'),							
              ('ELDIS_START_RECORDS', '0', 'string'),								
              ('ELDIS_PUBLISHED_AFTER', '', 'string'),
              ('ELDIS_PUBLISHED_BEFORE', '', 'string'),	
              ('ELDIS_PUBLISHED_YEAR', '', 'string'),
              ('ELDIS_FOLDER', 'ids-document', 'string'),
              ('ELDIS_OBJECT', 'documents', 'string'),
              ('ELDIS_STATE', 'submit', 'string'),
              ('ELDIS_AUTHOR', '', 'string'),
              ('ELDIS_PUBLISHER', '', 'string'),
              ('ELDIS_LANGUAGE', '', 'string'),
              ('ELDIS_COUNTRY', '', 'string'),
              ('ELDIS_KEYWORD', '', 'string'),
              ('ELDIS_THEME', '', 'string'))

try:
    from Products.Eldis.AppConfig import *
except ImportError:
    pass
