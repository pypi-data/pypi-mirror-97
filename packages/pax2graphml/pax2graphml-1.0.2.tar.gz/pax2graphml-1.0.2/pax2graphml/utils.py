"""This module contains utilitary functions related to graph and file manipulation, package management and execution."""


__license__ = "MIT"
__docformat__ = 'reStructuredText'


import sys,os
import logging
from decimal import Decimal
from subprocrunner import SubprocessRunner
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import graph_tool.all as gt
import graph_tool.centrality as centrality
import pandas as pd
import argparse
from os import path
import logging
import xml
import tempfile, shutil
import lxml.etree as et


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def resource_path():
    """return the resources  path

        :return:  a string representing the resource \
        path containing additional files like template and  jar
 
    """


    pa = __relPath('resources')

    logger.info("resource_path:%s" % (pa))
    return pa

def data_path():
    """return the data folder  path with example datasets

        :return:  a string representing the data folder \
        path  containing example data files like BIOPAX
 
    """
    pa = __relPath('data')
    logger.info("data_path:%s" % (pa))
    return pa





def node_list(g ):
    """return a  simple  list of all nodes of a graph (without iterator)

        :return:  a list of nodes
 
    """    
    ar=list()
    for el in g.vertices():  
        ar.append(el)

    return ar


def edge_list( g ):

    """return a  simple  list of all edges of a graph (without iterator)

       :return:  a list of edges
 
    """    
    ar=list()
    for el in g.edges():  
        ar.append(el)
 
    return ar 

 


def node_to_string(gh, n, sep="\n"):

    """return a string representing all the properties values from a node

        :return:  a string
    """ 
    s=""  
    for prop in gh.vertex_properties.keys():
        s=s+str(prop)+"="+str(gh.vp[prop][n])+sep
    return s


def to_string(gh, n, sep="\n"):
  """alias of node_to_string

     :return:  a string
  """  
  return node_to_string(gh, n, sep )


def edge_to_string(gh, e, sep="\n"):

    """return a string representing all the properties values from an edge

        :return:  a string
    """ 
    s=""
    for prop in gh.edge_properties.keys():
        s=s+str(prop)+"="+str(gh.ep[prop][e])+sep
    return s


def edge_description(g,e):

    """return a string giving al details from an edge, incuding source an target description

        :return:  a string
    """ 
    ep=edge_to_string(g,e,',')
    sp=node_to_string(g,e.source(),',')
    tp=node_to_string(g,e.target(),',')   
    
    return "edge:%s \n\tsource: %s  \n\ttarget: %s"%(ep,sp,tp)

                        




 
def count_edge(n,mode="all"):

        """compute edges count from a selected node

        :param n: graph node
        :param mode: count mode. values :"all","in", "out"
        :return:  the edges count
        :rtype: int 
        """ 
        ect=0
        if mode=="all":
          for e in n.neighbors():
            ect+=1
        if mode=="in":
          for e in n.in_neighbors():
            ect+=1
        if mode=="out":
          for e in n.out_neighbors():
            ect+=1

        return ect




def cc_by_node_count(g,min,max):

        """select a sub graph from a graph, using the minimum and maximum node number
           of each connected component as as a filter

        :param g: a graph 
        :param min: minimum node count of each connected component
        :param max: maximum node count of each connected component
        :return:  a subgraph
        :rtype: graph 
        """ 

        mccid=dict()
        v2cc = g.new_vertex_property('int');
        ccomp, hist  = gt.label_components(g, directed=None, attractors=False)

        for v in g.vertices():
           ccid=ccomp[v]
           ccidct=0
           if ccid in mccid.keys():
               ccidct=mccid[ccid]

           ccidct+=1
           mccid[ccid]=ccidct
           v2cc[v]=ccid

         
        selectedccid=None
        for ccid in mccid.keys():
             ccidct=  mccid[ccid]
             logging.info("cc id:%s=>%s nodes" %(ccid,ccidct))
             if ccidct>=min and ccidct<=max:
                logging.info("cc id:%s=>%s nodes %s %s " %(ccid,ccidct,min,max))
                selectedccid=ccid
                break
        if selectedccid is not None:
          vfilter = g.new_vertex_property("bool");
          for v in g.vertices():
             cval=v2cc[v]
             vindex=g.vertex_index[v]
             if cval is not None and cval==selectedccid:
                 vfilter[vindex] = True

             else:
                 vfilter[vindex] = False


          u = gt.GraphView(g, vfilt=vfilter)
          u=gt.Graph(u, prune=True)
          return u
        else:
          logger.info("cc_by_node_count returns None" )
          return None 








def friendly_format_graphml(graphml_file,usetemp=False):

      """modify in place a graphml_file to have more human readable properties data key

        :param graphml_file: a graphml file file folling the graph.tools generation rules
      """ 
       
      if usetemp==True: 
        f = tempfile.NamedTemporaryFile(delete=False)
        tmpf=f.name
        #warning: issue with cross devide link
      else:
        tmpf=graphml_file+".work.tmp"


      gns='http://graphml.graphdrawing.org/xmlns'
      ns={'x': gns}
         
 
      root = et.parse(graphml_file)
       
      lst=root.xpath("./x:key", namespaces=ns)
 
      
      keymap=dict()
      for el in lst: 
 
          fv=el.get('for')
          iv=el.get('id')
          v=el.get('attr.name')
          k="%s@%s" %(fv,iv)
          keymap[k]=v
          el.set('id', v)
          
      
      for tag in ["node","edge"]:    
        lst=root.xpath("./x:graph/x:%s" %(tag) , namespaces=ns)
        for elm in lst :   
         for el in elm: 
           
           if el.tag=='{%s}data' %(gns):
            
               ktag="key"
               kv=el.get(ktag)
               k="%s@%s" %(tag,kv)
               v=keymap[k]
               el.set(ktag, v)
            
      root.write(tmpf,
                 pretty_print=True, xml_declaration=True,
                 encoding='UTF-8')

      shutil.move(tmpf, graphml_file)  



 
__P2GJAR="biopax2spaimgen.jar"
__P2GTEMPLATE="graphml.vm"
__P2GJMEM=" -Xmx48g  -XX:+UseConcMarkSweepGC  "
__P2GJVM="java" 

def __gdirEnv():
   """ return the value of an optional evironment variable for alternate resources directory definition""" 
   p2gjdir=os.getenv("P2GJDIR")
   if p2gjdir is None:
      p2gjdir="./"
   return p2gjdir

def __gdir():
   """ return the resources directory if exists else use an evironment variable """ 
   fname=resource_path()
   if (os.path.isdir(fname) ):
      return fname
   else:
      return __gdirEnv()


def __p2g():
    """ paxx2graphml java extension jar name """ 
    return __P2GJAR


def __template():
    """ path to the graphml template used to generate  reaction graph file from BIOPAX.
       this editable template is  processed by the velocity template engine.
       see http://velocity.apache.org
    """ 
    return __gdir()+"/"+__P2GTEMPLATE

def __jarpath():
    """ path to the jar containing the paxx2graphml java extension using paxtools""" 
    return __gdir()+"/"+__p2g()

def __jvm():
    """ java binary """ 
    return __P2GJVM

def __jvmopt():
    """ jvm option """ 
    mem=os.getenv("JVMMEM")
    if mem is None:
       mem=__P2GJMEM
    return mem


def __formatRes(st):
  """utility to find json data in a stdout  string""" 
  ct=""
  fd=0
  ln=st.split("\n")
  for l in ln:
    if l.startswith("{"):
      fd=1
    if fd==1:
      ct+=l

  return ct   

def __runCmd(cmd):
    """command line execution that expect a json output with a status code

        :param cmd: a command line
        :type cmd: string 
        :return:  the json command output
        :rtype: dict 
    """ 
    resp =None
    try:
      runner = SubprocessRunner(cmd)
      logging.info("command: {:s}".format(runner.command))
      logging.info("return code: {:d}".format(runner.run()))
      logging.info("stdout: {:s}".format(runner.stdout))
      logging.info("stderr: {:s}".format(runner.stderr))
      rs=__formatRes(runner.stdout)
      resp = json.loads(rs)
      if resp["status"] ==0:
          logging.info("%s" %(resp["message"]))
      else:
          logging.info("%s" %(resp["error"]))
    except:
        print("error occured! %s %s ." %(sys.exc_info()[0],sys.exc_info()[1]))
    return resp

def __relPath(relname):
    """utility to convert a relative path to current script, to an absolute path  """ 
    resDir = path.join(path.dirname(__file__), relname)
    return resDir


def __addArrayEl(mp,k,el):
    """utility to add element to an array representing the value of a dictionary key""" 
    if k in mp:
      ar=mp[k]
    else:
      ar=list()  
    ar.append(el)
    mp[k]=ar   


def __clean_rm(file):
  err=0
  try:
     shutil.rmtree(graphmlOutFile, False,  None)
  except: 
     err=1 


def __str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def __convertType(v,property_type):
 if property_type is None:
   return v 
 elif property_type=='int':
   v=int(v)
 elif property_type=='float':
   v=float(v)
 elif property_type=='double':
   v=Decimal(v)    
 elif property_type=='double':     
   v=__str2bool(v)
 return v



if __name__ == "__main__":
     print("no main defined")








