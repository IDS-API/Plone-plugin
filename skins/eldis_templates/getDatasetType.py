## Script (Python) "getDatasetType"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=actions=None
##title=
##
__version__ = '$Id: get_eldis_rss.py 19 2011-09-30 14:03:09Z subhendu $'
from Products.CMFCore.utils import getToolByName
import string
skinsTool = getToolByName(context, 'portal_skins')
default_skin = skinsTool.getDefaultSkin()
path = skinsTool.getSkinPath(default_skin)
path = map( string.strip, string.split( path,',' ) )

if 'eldis_templates/eldis' in path:
    return 'eldis'
elif 'eldis_templates/bridge' in path:
    return 'bridge'
else:
    return None