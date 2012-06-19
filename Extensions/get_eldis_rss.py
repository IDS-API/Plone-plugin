# -*- coding: utf-8 -*-
#
# File: get_eldis_rss.py
#
__version__ = '$Id: get_eldis_rss.py 159 2012-05-29 08:26:46Z subhendu $'
__author__ = """Subhendu Kumar Giri <subhendu.giri@oneworld.net>"""
__docformat__ = 'plaintext'

import urllib2
#from standards import url_quote
from xml.dom import minidom, Node
import gc
gc.enable()
""" Get the XML """

def get_eldis_article(xml_host_url,xml_info):
    #xml_url = xml_host_url+url_quote(xml_info)
    xml_url = xml_host_url+xml_info	
    url_info = urllib2.urlopen(xml_url)
    del xml_url

    if (url_info):
        xmldoc = minidom.parse(url_info)
        eldis_data=[]
        if (xmldoc):
            rootNode = xmldoc.documentElement
            resultNode = rootNode.childNodes[0]
            metaNode = rootNode.childNodes[1]
            #Iterate the child nodes
            for node in resultNode.childNodes:
                headline=""
                title=""
                if (node.nodeName == "list-item"):
                    dict_xml={}
                    #Now iterate through all of the <list-item>s children
                    for item_node in node.childNodes:
                        if (item_node.nodeName == "object_id"):
                            object_id = ""
                            for text_node in item_node.childNodes:
                                if (text_node.nodeType == node.TEXT_NODE):
                                    object_id += text_node.nodeValue
                            dict_xml['object_id'] = object_id
  
                        if (item_node.nodeName == "title"):
                            title= ""
                            for text_node in item_node.childNodes:
                                if (text_node.nodeType == node.TEXT_NODE):
                                    title+= text_node.nodeValue
                            dict_xml['title'] = title
                            
                        if (item_node.nodeName == "urls"):
                            listing = []
                            for list_node in item_node.childNodes:
                                if (list_node.nodeName == "list-item"):
                                    #Now iterate through all of the <list-item>s children
                                    for list_item in list_node.childNodes:
                                        if (list_item.nodeType == node.TEXT_NODE):
                                            listing.append('<li><a target="_blank" class="external" href="'+list_item.nodeValue+'">'+list_item.nodeValue+'</a></li>')
                            dict_xml['listing'] = '<ul>'+"".join(listing)+'</ul>'

                        if (item_node.nodeName == "category_theme_array"):
                            keyword = []
                            for list_node in item_node.childNodes: # theme
                                for node_list in list_node.childNodes: # list-item
                                    for item_list in node_list.childNodes: # object_name
                                        if (item_list.nodeName == "object_name"):
                                            for list_item in item_list.childNodes:
                                                if (list_item.nodeType == node.TEXT_NODE):
                                                    keyword.append(list_item.nodeValue)
                            dict_xml['keyword'] = ", ".join(keyword)
                            
                        if (item_node.nodeName == "website_url"):
                            website_url = ""
                            for text_node in item_node.childNodes:
                                if (text_node.nodeType == node.TEXT_NODE):
                                    website_url += text_node.nodeValue
                            dict_xml['website_url'] = website_url

                        if (item_node.nodeName == "description"):
                            long_abstract = ""
                            for text_node in item_node.childNodes:
                                if (text_node.nodeType == node.TEXT_NODE):
                                    long_abstract += text_node.nodeValue
                            dict_xml['description'] = long_abstract

                    eldis_data.append(dict_xml)
                    del dict_xml

        else:
            return "Error getting XML document!"
    else:
        return "Error! Getting URL"
    del xmldoc
    return eldis_data