# -*- coding: utf-8 -*-
#
# File: EldisArticle.py
#
#
# GNU General Public License (GPL)
#
__version__ = '$Id: EldisArticle.py 159 2012-05-29 08:26:46Z subhendu $'
__author__ = """Subhendu Kumar Giri <subhendu.giri@oneworld.net>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.kupu.plone.ReftextField import ReftextField
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Eldis.config import *

schema = Schema((

    ReftextField(
        name='bodyText',
        widget=RichWidget(
            label='Bodytext',
            label_msgid='Eldis_label_bodyText',
            i18n_domain='Eldis',
            ),
        ),

    TextField(
        name='sourceUrl',
        widget=StringWidget(
            label='Eldis Article: Source URL',
            description='Auto generated',
            label_msgid='Eldis_label_sourceUrl',
            i18n_domain='Eldis',									
            size = 40,
            ),
        ),		

    TextField(
        name='sourceId',
        index='FieldIndex:schema',
        widget=StringWidget(
            label='Article: Source Unique Id',
            description='Auto generated',
            label_msgid='Eldis_label_sourceId',
            i18n_domain='Eldis',
            size = 40,
            ),
        ),

),
)

EldisArticle_schema = BaseSchema.copy() + \
    schema.copy()


class EldisArticle(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IEldisArticle)

    meta_type = 'EldisArticle'

    _at_rename_after_creation = True

    schema = EldisArticle_schema

 
registerType(EldisArticle, PROJECTNAME)
