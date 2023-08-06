"""This module contains function to read and write graphml and compute topological statistics on graphs """

__license__ = "MIT"
__docformat__ = 'reStructuredText'


import sys
import logging
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import graph_tool.all as gt
import graph_tool.centrality as centrality
import pandas as pd
import argparse
from os import path

import xml
import tempfile,shutil
import lxml.etree as et


from pax2graphml import utils
from pax2graphml import properties

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

 
def load_graphml(graphml_file, directed=True):
    """Return a graph instance from a GRAPHML file :

    :param graphml_file: a graphml file
    :param directed: a boolean that defines if the edges of the graph are oriented 
    :return: graph
    :rtype: graph object
  
    """ 
    g=gt.load_graph(graphml_file)
    g.set_directed(directed)
    g=gt.Graph(g, prune=True)
    if g is None:
       logger.info("warning graph is None")
    try:
      logger.info("input graph order: %s" %len(list(g.vertices())))
      logger.info("input graph size: %s" %len(list(g.edges())))
    except:
      logger.error("error, no vertices or edges in graph")
 
    return g




def describe_graph(g):

    """Return a string describing the graph will all edges and nodes with properties values :

    :param g: a graph
    
    :rtype: string 
  
    """ 
    if g is None:
       logger.info("warning graph is None")
    desc="" 
    for v in g.vertices(): 
      desc+="  vertex %s (%s)\n" %(v,  utils.node_to_string(g,v,',') )
      for e in v.in_edges():
         desc+="     %s in_edge:%s (%s)\n" %(v,e, utils.edge_to_string(g,e,',') )  
      for e in v.out_edges():
         desc+="      %s out_edge:%s (%s)\n" %(v,e, utils.edge_to_string(g,e,',') ) 
      desc+="\n\n"
    print(desc)
    return desc



def summary(g):
    """Return a string with graph nodes count and edges count :

    :param g: a graph
    
    :rtype: string 
  
    """ 
    if g is None:
       logger.info("warning graph is None")
    s=""
    if g is not None:
      s=s+"nodes count: %s \n" %len( list(g.vertices())  )
      s=s+"edges count: %s \n" %len( list(g.edges() )   )
    return s




def graphml_xml_string(graphml_file,ids=1,entity="node" ):


  """Return the XML content extract of the graphml file:

  :param graphml_file: graphml file path
  :param ids:  an intger or  list or integers that correspondn to the id attribute values of the selected entities
  :param entity: "edge" or ""node" value to define which entity should be selected
  :return: an XML string
  :rtype: string
  
  """ 

  if not isinstance(ids, (list)):
        idl = [ids]
  else:
        idl = ids

  model = xml.dom.minidom.parse(graphml_file)
  xmlent=model.getElementsByTagName(entity)
 
  ret=list()
  for en in xmlent:
     ide=en.getAttribute("id")
     ide=int(str(ide))   
     if ide in idl:
 
       ret.append(en.toxml())
  return ret


def largest_cc_degree_dist(g):
  """Generate the distribution of degrees of the nodes of the largest connected component:

  :param g: a graph instance
  :return: distibution of the degrees of the nodes
  :rtype: DataFrame object
  
  """ 
  if g is None:
       logger.info("warning graph is None")

  lCCFilt = gt.label_largest_component(g, directed=False)
  lCC = gt.GraphView(g, vfilt=lCCFilt)
  lCC = gt.Graph(lCC, prune=True)
 
  dist = degree_distribution(lCC)
  return dist

def degree_distribution(g):
  """Generate the distribution of degrees of the node of the graph:

  :param g: a graph instance
  :return: distibution of the degrees of the nodes
  :rtype: DataFrame object
  
  """ 
  if g is None:
       logger.info("warning graph is None")

  degreeMap=g.degree_property_map("total")
  dist = pd.DataFrame(degreeMap.a, columns=["edge_count"])
  return dist



def compute_betweenness( g ):
    """Compute the graph Betweenness:

    :param g: a graph instance
    
    :return: dictionary holding the metrics data
    :rtype: dict
  
    """ 
    if g is None:
       logger.info("warning graph is None")
    return centrality.betweenness(g)  



def compute_page_rank( g ):
    """Compute the graph PageRank:

    :param g: a graph instance
    
    :return: dictionary holding the metrics data
    :rtype: dict
  
    """ 
    if g is None:
       logger.info("warning graph is None")
    return centrality.pagerank(g)  

def compute_closeness( g ):
    """Compute the graph Closeness:

    :param g: a graph instance
    
    :return: dictionary holding the metrics data
    :rtype: dict
    """   
    return centrality.closeness(g)  


def compute_graph_metrics( g ):
    """Compute multiple topological graph metrics (degree distribution, betweenness, pagerank, closeness):

    :param g: a graph instance
    
    :return: dictionary holding the metrics data
    :rtype: dict
    """   
    d=dict()
    try:
      stat1=centrality.betweenness(g)  
      d["betweenness"]=stat1
      stat2=centrality.pagerank(g)
      d["pagerank"]=stat2
      stat3=centrality.closeness(g)
      d["closeness"]=stat3
      d["ccomponent"]=largest_cc_degree_dist(g)
      d["degreedist"]=degree_distribution(g)

      d["error"]=None
    except:
      d["error"]= "%s,%s" %(sys.exc_info()[0],sys.exc_info()[1])

    return d





def save_graphml(g, graphml_file,friendly=False):
    """Save a graph instance as a graphml file:

    :param g: a graph instance
    :param graphml_file: graphml output file path
    :return: void
    :rtype: None
  
    """ 
    utils.__clean_rm(graphml_file)

    g=gt.Graph(g, prune=True)
    g.save(graphml_file)
     
    if friendly==True:
       utils.friendly_format_graphml(graphml_file)
  



 
def __saveOrPlot(g, output_graph=None, output_image=None):
   """Save a graph instance as a graphml file or save a graph image (png)"""

   logger.info("\noutput graph order: %s" %len(list(g.vertices())))
   logger.info("output graph size: %s" %len(list(g.edges())))
   if (output_graph is not None):
         g=gt.Graph(g, prune=True)
         utils.__clean_rm(output_graph)
         g.save(output_graph)
   if (output_image is not None):
        size=3000
        utils.__clean_rm(output_image)
        __saveGraphImage(g,output_image, size)





def save_image(g, image_file,  size=3000 ,conf=None):
  """Generate an image from a graph instance :

  :param g: a graph instance
  :param image_file: png file path
  :param size: image size
  :param conf: image configuration dictionary with nodelabel and edgelabel keys
  :return: void
  :rtype: None
  
  """ 
  __saveGraphImage(g,image_file, size)



def __saveGraphImage(g,image_file, size,conf=None):

  """Generate an image from a graph instance :

  :param g: a graph instance
  :param image_file: png file path
  :param size: image size
  :param conf: image configuration dictionary with nodelabel and edgelabel keys
  :return: void
  :rtype: None
  
  """ 

  ecolor=None
  for prop in g.edge_properties.keys():
      if prop =="color":
           ecolor=g.ep[prop]

  if conf is None:
     nodelabel="_graphml_vertex_id"
     edgelabel=None 
  else:
     nodelabel=conf["nodelabel"]
     edgelabel=conf["edgelabel"]
  vtext=None
  etext=None
  if  nodelabel is not None:
      vtext=g.vp[nodelabel]
  if  edgelabel is not None:
     etext=g.ep[edgelabel]

 
  gt.graph_draw(g, vertex_text=vtext, edge_text=etext, vertex_font_size=30, bg_color=[1.,1.,1.,1.], vertex_fill_color=g.vp.color, edge_color=ecolor, output_size=(size,size), output=image_file)
  




 
def color_nodes(g):

  """Generate a node color property that Differentiates the node entities (reaction, chemical):

  :param g: a graph instance
  :return: void
  :rtype: None
  
  """ 

  chemiColor='darkcyan'
  reactColor='indigo'
  g.vp.color = g.new_vertex_property("string")
  for v in g.vertices():
        if (g.vp.entityType[v]=="reaction"):
            g.vp.color[v]=reactColor
        elif (g.vp.entityType[v]=="chemical"):
            g.vp.color[v]=chemiColor
        else:
            g.vp.color[v]='k'
  return g

 
def color_edges(g):


    """Generate a edge color property that Differentiates the edge semantic (subtsrat, product, activator, inhibitor, modulator) using the spaim edge property (s,p,a,i,m):

    :param g: a graph instance
    :return: void
    :rtype: None
  
    """ 
    if g is None:
       logger.info("warning graph is None")
    g.ep.color = g.new_edge_property("string")
    def eColorMap(spaim):
        switcher={
            's':'mediumseagreen',
            'p':'orchid',
            'a':"darkred",
            'i':"purple",
            'm':"grey"
        }
        return switcher.get(spaim, 'k')

    for e in g.edges():
        g.ep.color[e]=eColorMap(g.ep.spaim[e])
        if (g.ep.color[e]=='k'):
            g.ep.spaim[e]="undef"
    return g










