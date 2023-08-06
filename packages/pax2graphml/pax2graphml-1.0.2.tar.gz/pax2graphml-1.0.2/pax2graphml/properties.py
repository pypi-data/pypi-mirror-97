"""This module contains function to manipulate edge and node properties"""


__license__ = "MIT"
__docformat__ = 'reStructuredText'


import sys
import logging
import copy
import pandas as pd
import numpy as np 

from graph_tool.all import random_graph, label_components
import graph_tool.all as gt

from pybiomart import  Server, Dataset
from pybiomart.dataset import   Filter


from pax2graphml import utils
from pax2graphml import extract



logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def property_values(g,annot_key):
    """ Alias of node_property_values"""

    return node_property_values(g,annot_key)

def node_property_values(g,annot_key):
    """Return a list of unique values corresponding to an existing node property:

    :param g: a graph
    :param annot_key: an existing propety name
    :return:  a list of node property values
    :rtype: list 
 
    """ 
  
    vset=set()
    pkprop= g.vertex_properties[annot_key]
    nid=0
    if str(pkprop.value_type())=="python::object":
      for v in   g.vertices():
         vaf=pkprop[nid]
         if isinstance(vaf, (list)) :    
            for va in vaf:
                 vset.add(va)  
         elif isinstance(vaf, (dict)) :    
            for k in vaf.keys():
                 vset.add(vaf[k])                      
         else:
            vaf=pkprop[nid]
            vset.add(vaf)  
            
         nid+=1  
    else:
      for v in   g.vertices():
         vset.add(pkprop[nid])  
         nid+=1
    
    pv=list(vset)
    return pv



def edge_property_values(g,annot_key):
    """Return a list of unique values corresponding to an existing edge property:

    :param g: a graph
    :param annot_key: an existing propety name
    :return:  a list of edge property values
    :rtype: list 
 
    """ 
  
    vset=set()
    pkprop= g.edge_properties[annot_key]
    nid=0
    if str(pkprop.value_type())=="python::object":
      for e in   g.edges():
         vaf=pkprop[e]
         if isinstance(vaf, (list)) :    
            for va in vaf:
                 vset.add(va)  
         elif isinstance(vaf, (dict)) :    
            for k in vaf.keys():
                 vset.add(vaf[k])                      
         else:
            vaf=pkprop[e]
            vset.add(vaf)  
            
         nid+=1  
    else:
      for e in   g.edges():
         vset.add(pkprop[e])  
         nid+=1
    
    pv=list(vset)
    return pv

def describe_properties(g, name=None):
    """Return a description of node and edge properties with names and types:

    :param g: a graph
    :param name: property name (optional). If None, all properties are described
    :return:  a description of edge and node properties
    :rtype: string 
 
    """ 
    strn=""
    stre=""

    for k, v in g.properties.items():
        nm=k[1]
        cstrn=""
        cstre=""        
        tp='' 
        if k[0] == 'v':
          tp='node'
          cstrn="%s, %s, %s \n"   % (tp,nm, v.value_type()) 
        elif k[0] == 'e':
          tp='edge'
          cstre="%s, %s, %s \n"   % (tp,nm, v.value_type()) 
        if name is not  None and name ==nm: 
           return cstrn+cstre
        else:
           strn+=cstrn
           stre+=cstre

    return strn+stre



def defaultNodeValue(gr,prop,default_val ):

    """asign a userdefined value to a node property when it is None ar equal to "":

    :param gr: a graph
    :param prop: an existing property name
    :param default_val: the  value to be used to replace None and "" string
    :return:  void
    :rtype: None 
 
    """      
    pkprop= gr.vertex_properties[prop]
    for v in   gr.vertices():
        xid=gr.vp[prop][v]
        if xid is None or str(xid) == "":
                 gr.vp[prop][v]=default_val   
   
def default_edge_value(gr,prop,default_val ):
    """asign a userdefined value to an edge property when it is None ar equal to "":

    :param gr: a graph
    :param prop: an existing property name
    :param default_val: the  value to be used to replace None and "" string
    :return:  void
    :rtype: None 
 
    """           
    pkprop= gr.edge_properties[prop]
    for e in   gr.edges():
        xid=gr.ep[prop][e]
        if xid is None or str(xid) == "":
                 gr.ep[prop][e]=default_val   








    
    



def define_biomart_server(url,mart_name):  
   """define a biomart server "":

   :param url: the url of the biomartserver
   :param mart_name: the mart name
   :return:  mart 
   :rtype: mart Object 
   """     
   server = Server(host=url)
   mart=server.marts[mart_name]
   return mart



def client_annot_impl( prot,conf=None):

  """Configure a mart for Uniprot to GO annotation "":

  :param prot:  list of Uniprot gene symbols
  :param conf: the configuration dictionary
  :return:  a dictionary of annotations 
  :rtype: dict 
 
  """    

  mart=define_biomart_server(conf['server'],conf['mart'])  
  dataset = (mart.datasets[conf['dataset']])
  attr=conf['attr']

  dataset.filters
 
  dataset._filters[conf['searchkey']]=Filter(conf['searchkey'], 'text')

  filt={conf['searchkey']: prot}

  unimap=dict()
  for p in prot:
      unimap[p] =set()
  



  uni_key=conf['uni_key']
  annot_key=conf['annot_key']  

  res=dataset.query(attributes=attr, filters=filt)
  i=0
  for index, row in res.iterrows() : 
    i=i+1
    maxIt=1000000
    if i<= maxIt:
        try:
          uni=str(row[uni_key])
          goterm=str(row[annot_key])
        except:
          print("error wrong/mission uni_key /annot_key in conf. missing row response key. row is  %s, conf is %s" %(row, conf))
          
          return None
        if uni != "nan":

           if uni in unimap:
              ma=unimap[uni]
           else:
              ma=set()
           if goterm != "nan":     
              ma.add(goterm)  
           unimap[uni]=ma
        
    else:
        break
  for k in unimap.keys():
     v= unimap[k]
     if v is not None and len(v)==0:
        unimap[k]=None
  return unimap


def __default_apî_conf():
     conf={
       'server':'http://www.ensembl.org',
       'mart':'ENSEMBL_MART_ENSEMBL',
       'dataset':'hsapiens_gene_ensembl',
       'attr':[
           'ensembl_gene_id',
           'external_gene_name',
           'uniprot_gn_symbol',
           'go_id'
          ],
       'searchkey' :'uniprot_gn_symbol',
       'uni_key' : 'UniProtKB Gene Name symbol',    
       'annot_key' :'GO term accession'
      }
     return conf

def __current_apî_conf(conf=None):
   confg=__default_apî_conf()
   if conf is not None:
      for k in conf.keys():
          confg[k]=conf[k]     
   return confg
   

def uniprot_to_go(protein_list,conf=None,chunck_size=50):

   """Configure a mart for Uniprot to GO annotation "":

   :param prot:  list of Uniprot gene symbols
   :param conf: the configuration dictionary
   :param chunck_size: the size of each chunk of inputs to be submitted in one time
   :return:  a dictionary of annotations 
   :rtype: dict 
  
   """   
   if  conf is None:
      conf=__default_apî_conf()
   

   return ensembl_api(protein_list,conf,chunck_size)

def ensembl_api(in_list,conf=None,chunck_size=50):    
   """Configure a mart for any annotation "":

   :param in_list:  list of inputs identifiers
   :param conf: the configuration dictionary
   :param chunck_size: the size of each chunk of inputs to be submitted in one time
   :return:  a dictionary of annotations 
   :rtype: dict 
  
   """ 
   confg=__current_apî_conf(conf)   
 
   chunks = [in_list[x:x+chunck_size] for x in range(0, len(in_list), chunck_size)]
   allM=dict()
   for inl in chunks:
     #print(prot)   
     annotmap=client_annot_impl(inl,confg)
     allM.update(annotmap) 
   return allM

 
def is_unique(g, key_prop, exclude_void=True):

  """Evaluate if a property contains one unique value for each node:

  :param g: a graph
  :param key_prop: the key node property to be evaluated
  :param exclude_void: define is we include None values 
  :rtype: boolean 
  
  """  
  ud=set()
  i=0
  vc=0
  for node in g.vertices():  
    key=g.vp[key_prop][node] 
    if exclude_void==True and  key is None :
      vc+=1
    else:
      i+=1
      ud.add(key)



  if i!=len(ud):
     return False
  else :
     return True 

def annot_node_to_file(g,output_prop_file,key_prop,annot_prop,defval=None,excluded_keys=[None,''],delimiter=','):

  """Export two properties to a tabular file. The first property act as a  key to identify the node, the second as an additionnal annotaion attribute. The Unicity of the key is not tested :

  :param g: a graph
  :param output_prop_file: the tabular output file
  :param key_prop: the key node property that will be present as a named column in the file. 'index' references the node index (from 0)
  :param annot_prop: the additionnal property to be exported as a named column in the file
  :param defval: value to replace None values in output
  :param excluded_keys: list of key_prop values that will be excluded 
  :param delimiter: tabular file delimiter
  :rtype: void 
  
  """  
  f = open(output_prop_file,"w") 
  endL="\n"
  f.write("%s%s%s%s" % (key_prop,delimiter,annot_prop,endL))
  idx=-1
  for node in g.vertices():
   
    idx+=1
    if key_prop=="index":
      key=str(idx)
    else:
      key=g.vp[key_prop][node]
    
    annot=g.vp[annot_prop][node]
    if key not in excluded_keys:
      if key is None:
         key='None'    
      if annot is None:
         annot=defval            
      f.write( "%s%s%s%s" % (key,delimiter,annot,endL))
  f.close()




def annot_edge_to_file(g,output_prop_file,key_prop,annot_prop,defval=None,excluded_keys=[None,''],delimiter=','):

  """Export two properties to a tabular file. The first property act as a  key to identify the edge, the second as an additionnal annotaion attribute. The Unicity of the key is not tested :

  :param g: a graph
  :param output_prop_file: the tabular output file
  :param key_prop: the key edge property that will be present as a named column in the file.  'index' references the edge index (from 0)
  :param annot_prop: the additionnal property to be exported as a named column in the file
  :param defval: value to replace None values in output
  :param excluded_keys: list of key_prop values that will be excluded 
  :param delimiter: tabular file delimiter
  :rtype: void 
  
  """  
  f = open(output_prop_file,"w") 
  endL="\n"
  f.write("%s%s%s%s" % (key_prop,delimiter,annot_prop,endL))
  idx=-1
  for edge in g.edges():
    idx+=1
    
    if key_prop=="index":
       key=str(idx)
    else:
       key=g.ep[key_prop][edge]

    annot=g.ep[annot_prop][edge]
    if key not in excluded_keys:
      if key is None:
         key='None'    
      if annot is None:
         annot=defval            
      f.write( "%s%s%s%s" % (key,delimiter,annot,endL))
  f.close()


def annot_node_from_file(g,annot_file,map_key,new_prop,new_prop_type="string",delimiter=","):

  """Populate the nodes with a new property. The values of the property are extract from a tabular file:

  :param g: a graph
  :param annot_file: the tabular annotation file
  :param map_key: the node property holding the primary key that must be present as a named column in the file.  'index' references the node index (from 0)
  :param new_prop: the new property to be created that must be present as a named column in the file
  :param new_prop_type: type of the new property ('string','int', 'float', 'long','bool')
  :param delimiter: tabular file delimiter
  :rtype: void 
  
  """  

  df = pd.read_csv(annot_file,   delimiter=delimiter)

  andict=dict(df.values)

  g.vp[new_prop]=g.new_vertex_property(new_prop_type)
 

  nodes=g.vertices()
  idx=-1
  for node in nodes:
    idx+=1
    if map_key=='index':
       key=idx

    else:
       key=g.vp[map_key][node]

    if key is not None:
      if key in andict.keys():   
         g.vp[new_prop][node]=andict[key]


 

           
def annot_edge_from_file(g,annot_file,map_key,new_prop,new_prop_type="string",delimiter=","):

  """Populate the edges with a new property. The values of the property are extract from a tabular file:

  :param g: a graph
  :param annot_file: the tabular annotation file
  :param map_key: the node property holding the primary key that must be present as a named column in the file.  'index' references the edge index (from 0)
  :param new_prop: the new property to be created that must be present as a named column in the file
  :param new_prop_type: type of the new property ('string','int', 'float', 'long','bool')
  :param delimiter: tabular file delimiter
  :rtype: void 
  
  """ 


  df = pd.read_csv(annot_file,  delimiter=delimiter)
  andict=dict(df.values)
  

  g.ep[new_prop]=g.new_edge_property(new_prop_type)
 

  edges=g.edges()
  idx=-1
  for edge in edges:
    idx+=1
    if map_key=='index':
       key=idx
    else:
       key=g.ep[map_key][edge]

    
    if key is not None:
      if key in andict.keys():   
         g.ep[new_prop][edge]=andict[key]








 
def copy_node_properties(g, sourceNode, targetNode):
    """Copy all properties of a source node to a target node:

    :param g: a graph
    :param sourceNode: source node
    :param targetNode:  target node
    :rtype: void 
  
    """ 
    for prop in g.vertex_properties.keys():
        g.vp[prop][targetNode]=g.vp[prop][sourceNode]

 
def copy_edge_properties(g, source_edge, target_edge):

    """Copy all properties of a source edge to a target edge:

    :param g: a graph
    :param source_edge: source node
    :param target_edge:  target node
    :rtype: void 
  
    """ 

    for prop in g.edge_properties.keys():
        g.ep[prop][target_edge]=g.ep[prop][source_edge]




def string_to_list_property(g, string_prop,new_property=None, sep=";", entity="node"):

  """Convert a string property to a property contains a list, for each node or edge:

    :param g: a graph
    :param string_prop: initial property
    :param new_property: new property name, is None, the intial property is replaced
    :param sep: string separator used in the string property
    :param entity: define is the properties are related to nodes or edges
    :return:  void
 
  """ 
  do_replace=False
  if new_property is None:
      do_replace=True

  if entity=="node":
    nprop = g.new_vertex_property("object")
    for n in g.vertices():
      st=g.vp[string_prop][n]
      ln=st.split(sep)
      nprop[n]=ln
  
    if do_replace==True:         
      del g.vp[string_prop]
      g.vp[string_prop] = nprop 
    else:
      g.vp[new_property] = nprop 
    
  if entity=="edge":  
    nprop = g.new_edge_property("object")
    for n in g.edges():
      st=g.ep[string_prop][n]
      ln=st.split(sep)
      nprop[n]=ln
  
    if do_replace==True:         
      del g.ep[string_prop]
      g.ep[string_prop] = nprop 
    else:
      g.ep[new_property] = nprop 
    
    
    
def list_to_string_property(g, string_prop,new_property=None, sep=";", entity="node"):
  """Convert a property contains a list  to a concatened string property, for each node or edge:

    :param g: a graph
    :param string_prop: initial property
    :param new_property: new property name, is None, the intial property is replaced
    :param sep: string separator used in the string property
    :param entity: define is the properties are related to nodes or edges
    :return:  void
 
  """   
  do_replace=False
  if new_property is None:
      do_replace=True

  if entity=="node": 
    nprop = g.new_vertex_property("string")
    for n in g.vertices():
      ln=g.vp[string_prop][n]
      if len(ln)>1:
        st=sep.join(ln)
      else:
        st=""
      nprop[n]=st
    
    if do_replace==True:         
      del g.vp[string_prop]
      g.vp[string_prop] = nprop 
    else:
      g.vp[new_property] = nprop 
    
    
  if entity=="edge": 
    nprop = g.new_edge_property("string")
    for n in g.vertices():
      ln=g.ep[string_prop][n]
      if len(ln)>1:
        st=sep.join(ln)
      else:
        st=""
      nprop[n]=st
    
    if do_replace==True:         
      del g.ep[string_prop]
      g.ep[string_prop] = nprop 
    else:
      g.ep[new_property] = nprop     
    
    



                
def change_property_type(g,property_name, property_type, entity="node"):
  """change a node or edge property type  :

    :param g: a graph
    :param property_name: the name of the property to be affected
    :param property_type: the new primitive property type (string,int,bool,float,double), is None, the intial property is replaced
    :param entity: define is the properties are related to nodes or edges
    :return:  void
 
  """  
  prop=None
  if entity=="node":
       prop=g.vp[property_name]
       nprop = g.new_vertex_property(property_type)
       for n in g.vertices():
           nprop[n]=utils.__convertType(prop[n],property_type)
       g.vp[property_name]=nprop  
 
    
  elif entity=="edge":        
       prop=g.ep[property_name]  
       nprop = g.new_edge_property(property_type)
       for e in g.edges():
           nprop[e]=utils.__convertType(prop[e],property_type)  
       g.ep[property_name]=nprop    
 
    

def create_property_from_map(g, annot_map,primary_key, new_property,case_sensitive=False):
    
  """Create a new node property from a dictionary "":

   :param g:  a graph
   :param annot_map:  a dictionary 
   :param primary_key: the primary key property (e.g. uri, uniprot...)
   :param new_property: the new property name. The expected type  is 'object'
   :param case_sensitive: define if the primary key mapping is case sensitive or not
   :return:  void  

  """

  g.vp[new_property]=g.new_vertex_property("object")
 
  for node in g.vertices() :
    pk=g.vp[primary_key][node]
    if pk is not None:
      for k in annot_map.keys(): 
        if case_sensitive==False:
          rk= pk.lower()    
          km=k.lower()
        else:
          rk= pk
          km=k       
        if rk ==km:
           val=annot_map[k]
           if val is not None: 
              g.vp[new_property][node]=val
              #print("%s-->%s" %(pk,annot_map[k]))


def count_edges_by_values(gr,att):

     """Count edges for each value of an input property:

     :param gr: a graph
     :param att: a  existing property name
     :return: a dictionnary (property value/count)
     :rtype: dict  

     """        
     avlist=edge_property_values(gr,att) 
     print(avlist) 
    
     mc=dict()
     for val in avlist:
         ct=0
         for e in gr.edges():
           cval=gr.ep[att][e]
           
           if cval is not None and cval==val:
             ct=ct+1
         mc[val]=ct  
     return mc


def count_nodes_by_values(gr,att):

     """Count nodes for each value of an input property:

     :param gr: a graph
     :param att: a  existing property name
     :return: a dictionnary (property value/count)
     :rtype: dict  

     """        
     avlist=node_property_values(gr,att) 
     
     mc=dict()
     for val in avlist:
         ct=0
         for n in gr.vertices():
           cval=gr.vp[att][n]
           
           if cval is not None and cval==val:
             ct=ct+1
         mc[val]=ct  
     return mc













