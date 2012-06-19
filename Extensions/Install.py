# -*- coding: utf-8 -*-
#
# File: Install.py
#
#
__version__ = '$Id: Install.py 159 2012-05-29 08:26:46Z subhendu $'
__author__ = """Subhendu Kumar Giri <subhendu.giri@oneworld.net>"""
__docformat__ = 'plaintext'


from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.Eldis.config import PROJECTNAME, PROPERTIES



# Configlets to be added to control panels or removed from them
configlets = (
		{ 'id'         : PROJECTNAME
		, 'name'       : 'Eldis Configuration'
		, 'action'     : 'string:${portal_url}/prefs_eldis_form'
		, 'condition'  : ''
		, 'category'   : 'Products'   # section to which the configlet should be added:
																	# (Plone,Products,Members)
		, 'visible'    : 1
		, 'appId'      : 'EldisMenuSection'
		, 'permission' : 'Manage portal'
		, 'imageUrl'   : 'eldis_icon.gif'
		},
)

def install(self, reinstall=False):
		"""External Method to install Eldis 

		This method to install a product is kept, until something better will get
		part of Plones front end, which utilize portal_setup.
		"""
		out = StringIO()
		print >> out, "Installation log of %s:" % PROJECTNAME

		setuptool = getToolByName(self, 'portal_setup')
		importcontext = 'profile-Products.%s:default' % PROJECTNAME
		setuptool.setImportContext(importcontext)
		#setuptool.runAllImportSteps() #dangerous in Plone 2.5
		setuptool.runImportStep(step_id="typeinfo")
		#setuptool.runImportStep(step_id="factorytool")
		setuptool.runImportStep(step_id="toolset")
		setuptool.runImportStep(step_id="rolemap")
		setuptool.runImportStep(step_id="workflow")
		setuptool.runImportStep(step_id="skins")
		setuptool.runImportStep(step_id="cssregistry")
		setuptool.runImportStep(step_id="controlpanel")
		setuptool.runImportStep(step_id="action-icons")
		setuptool.runImportStep(step_id="jsregistry")
		setuptool.runImportStep(step_id="content_type_registry")
		#setuptool.runImportStep(step_id="catalog_tool")		

		from Products.Eldis.setuphandlers import updateRoleMappings, postInstall
		context = setuptool._getImportContext(importcontext)
		updateRoleMappings(context)
		postInstall(context)
		print >> out, "Successfully imported steps."
		
		catalogTool = getToolByName(self, 'portal_catalog')
		if 'sourceId' not in catalogTool.indexes():
				catalogTool.addIndex('sourceId', 'FieldIndex')
		print >> out, "Successfully created indexes."

		# add Property sheet to portal_properies
		pp = getToolByName(self, 'portal_properties')
		if not 'ELDISAPI_PROPERTIES' in pp.objectIds():
				pp.addPropertySheet(id='ELDISAPI_PROPERTIES', title= '%s Properties' % 'ELDISAPI_PROPERTIES')
				out.write("Adding %s property sheet to portal_properies\n" % 'ELDISAPI_PROPERTIES' )

		props_sheet = pp['ELDISAPI_PROPERTIES']
		updateProperties(props_sheet, out, PROPERTIES)

		# add the configlets to the portal control panel
		configTool = getToolByName(self, 'portal_controlpanel', None)
		if configTool:
				for conf in configlets:
						configTool.registerConfiglet(**conf)
						out.write('Added configlet %s\n' % conf['id'])

		print >> out, "Successfully installed %s." % PROJECTNAME
		return out.getvalue()
		
def uninstall(self):
		out = StringIO()

		# remove the configlets from the portal control panel
		configTool = getToolByName(self, 'portal_controlpanel', None)
		if configTool:
				for conf in configlets:
						configTool.unregisterConfiglet(conf['id'])
						out.write('Removed configlet %s\n' % conf['id'])

		try:
				self.portal_controlpanel.unregisterApplication(PROJECTNAME)
		except:
				pass

		print >> out, "Successfully uninstalled %s." % PROJECTNAME
		return out.getvalue()	

def updateProperties(pp_ps, out, *args):
		for prop in args:
				for prop_id, prop_value, prop_type in prop:
						if not pp_ps.hasProperty(prop_id):
								pp_ps.manage_addProperty(prop_id, prop_value, prop_type)
								out.write("Adding %s property to %s property sheet\n" % (prop_id, 'ELDISAPI_PROPERTIES') )
