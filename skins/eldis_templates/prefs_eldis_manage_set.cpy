## Controller Script (Python) "prefs_eldis_manage_set"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=ELDIS_STATE=None, ELDIS_FOLDER=None, RESPONSE=None
##title=Eldis Management Properties
##

from Products.CMFPlone import PloneMessageFactory as _
REQUEST=context.REQUEST

if ELDIS_FOLDER=='':
   ELDIS_FOLDER='ids-document'
   
obj = getattr(container, ELDIS_FOLDER, None)   
if obj is None:
   old_id = container.generateUniqueId('Folder')
   new_id = container.invokeFactory('Folder', id=old_id, title=ELDIS_FOLDER,description='The data were fetched from IDS web API a way to use the data and metadata contained in the datasets that IDS maintains - namely BRIDGE and ELDIS.')
   newobj = getattr(container, new_id)
   newobj.processForm()
   #newobj.unmarkCreationFlag()

ap = context.portal_properties.ELDISAPI_PROPERTIES
ap.manage_changeProperties(ELDIS_STATE= ELDIS_STATE, ELDIS_FOLDER=ELDIS_FOLDER)

context.plone_utils.addPortalMessage(_(u'Eldis Management Properties Updated'))
return state
