REQUEST=context.REQUEST
from Products.Eldis.Extensions.get_eldis_rss import get_eldis_article
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName
from Products.PythonScripts.standard import url_quote
import logging
import string
import re

portal_catalog = getToolByName(context, 'portal_catalog')
sourceIds= portal_catalog.Indexes['sourceId'].uniqueValues()
ap = context.portal_properties.ELDISAPI_PROPERTIES.propertyItems()
ap= dict((x, y) for x, y in ap)
ptype='EldisArticle'
pcont=ap['ELDIS_FOLDER'] #folder name
query = {}
sstr=''

if ap['ELDIS_HOST']=='':
    ap['ELDIS_HOST']='http://api.ids.ac.uk'
#if ap['ELDIS_OBJECT']=='':
#    ap['ELDIS_OBJECT']='document'
if ap['ELDIS_DATATYPE']=='':
    ap['ELDIS_DATATYPE']='eldis'
#if ap['ELDIS_FORMAT']=='':
#    ap['ELDIS_FORMAT']='full'
if ap['ELDIS_AUTHOR']!='':
    sstr=sstr + '&author=' + url_quote(string.strip(ap['ELDIS_AUTHOR']))
if ap['ELDIS_PUBLISHER']!='':
    sstr=sstr + '&publisher=' + url_quote(string.strip(ap['ELDIS_PUBLISHER']))
#if ap['ELDIS_LANGUAGE']!='':
#	sstr=sstr + '&language=' + ap['ELDIS_LANGUAGE']
if ap['ELDIS_COUNTRY']!='':
    sstr=sstr + '&country=' + url_quote(string.strip(ap['ELDIS_COUNTRY']))
if ap['ELDIS_KEYWORD']!='':
    sstr=sstr + '&keyword=' + url_quote(string.strip(ap['ELDIS_KEYWORD']))
if ap['ELDIS_THEME']!='':
    sstr=sstr + '&theme=' + url_quote(string.strip(ap['ELDIS_THEME']))	
if ap['ELDIS_PUBLISHED_AFTER']!='':
    sstr=sstr + '&document_published_after=' + url_quote(string.strip(ap['ELDIS_PUBLISHED_AFTER']))
if ap['ELDIS_PUBLISHED_BEFORE']!='':
    sstr=sstr + '&document_published_before=' + url_quote(string.strip(ap['ELDIS_PUBLISHED_BEFORE']))
if ap['ELDIS_PUBLISHED_YEAR']!='':
    sstr=sstr + '&document_published_year=' + url_quote(string.strip(ap['ELDIS_PUBLISHED_YEAR']))	
	 
xml_host_url=string.strip(ap['ELDIS_HOST']) + '/openapi/' + string.strip(ap['ELDIS_DATATYPE'])+ '/get_all/documents/full?' + 'num_results=' + url_quote(string.strip(ap['ELDIS_NO_RECORDS'])) 
xml_info='&_token_guid=' + url_quote(string.strip(ap['ELDIS_GUID'])) + sstr +'&_accept=application/xml'

logger = logging.getLogger("Plone")
logger.info(xml_host_url+''+xml_info)
xml_data =get_eldis_article(xml_host_url, xml_info)


if (xml_data):
    try:
        xml_data +' '
    except:
        for xd in xml_data:
            if xd.has_key('object_id'):
                if xd['object_id'] not in sourceIds:
                    title = ''
                    headline = ''
                    body = ''
                    asset_id = ''
                    subject = ''
                    website_url = ''
                    asset_id = xd['object_id']
                    if xd.has_key('title'):
                        title = xd['title']
                    if xd.has_key('description'):
                        headline = xd['description']
                    if xd.has_key('keyword'):
                        subject = xd['keyword']
                    if xd.has_key('listing'):
                        body = xd['listing']
                    if xd.has_key('website_url'):
                        website_url = xd['website_url']
                        website_url = website_url.replace('&amp;','&')
                    obj = getattr(container, pcont)
                    old_id = obj.generateUniqueId(ptype)
                    new_id = obj.invokeFactory(ptype, id=old_id, title=title)
                    newobj = getattr(obj, new_id)
                    newobj.processForm()
                    #newobj.unmarkCreationFlag()
                    mid=newobj.id
                    objx = getattr(obj, mid)
                    objx[mid].edit(description='',sourceId=asset_id,sourceUrl=website_url,subject=subject )
                    objx[mid].edit(bodyText=headline+'<br/>' +body,format='text/html')
                    if ap['ELDIS_STATE']=='publish' or ap['ELDIS_STATE']=='submit':
                        objx[mid].portal_workflow.doActionFor(objx[mid], ap['ELDIS_STATE'], comment="")
        return 'Content created successfully'
else:
    return 'Error getting XML document!'
