"""This module contains function to extract graph and connected components from a graph in graphml and assemble such graphs"""


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

 
from pax2graphml import utils, properties, graph_explore
 
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def sub_graph_by_value(g,targets,annot_keys,add_void=False,void_symbol=None):
    
  """Extract a subgraph list. Each graph contains nodes with properties matching provided values:


  :param g: a graph
  :param targets: a list of values that must match the values of the properties defined by annot_keys
  :param annot_keys: a list of properties
  :param add_void: a boolean defining if we  keeo void values
  :param void_symbol: void_symbol represents the void value symbol, used if add_void is true
  :return:  a list of dictionnary where the key "subgraph" represents the subgraph
  :rtype: list 
 
  """ 

  extend_to_cc=False     
  subgraphList=list()
  for tar in targets:
      pvset=set()
      if add_void==True:
        if void_symbol is not None and tar != void_symbol:   
           pvset.add(void_symbol)  
           pvset.add(tar)     
      else:
          pvset.add(tar)    
      pvlist=list(pvset)  
      if len(pvlist)>0:

         add_voidCC=True
         sg,targmap=connected_component_by_annotation(g,pvlist,annot_keys,add_voidCC,extend_to_cc)    
         d=dict()
         d["datasource"]=pvlist
         d["subgraph"]=sg
         d["ccomponent"]=targmap
         subgraphList.append(d)
    
  return subgraphList   


def subgraphs_by_datasource(g,add_void=False,void_symbol=""):

    """Extract a subgraph list. Each graph contains nodes with datasource/provider matching input values:

    :param g: a graph
    :param add_void: a boolean defining if we  keep void values
    :param void_symbol: void_symbol represents the void value symbol, used if add_void is true
    :return:  a list of dictionnary where the key "subgraph" represents the subgraph
    :rtype: list 
 
 
    """
    if g is None:
       logger.info("warning graph is None")
    annot_key="provider"
    providerList=properties.property_values(g,annot_key)
    annot_keys=[annot_key]
    return  sub_graph_by_value(g,providerList,annot_keys,add_void,void_symbol)
    
 

def connected_component_by_annotation(g,targ,annot_keys,add_void=False,extend_to_cc=True):

    """Extract a subgraph build by merging a subset of connected components of the original graph. Each connected component contains nodes with properties matching provided values:


    :param g: a graph
    :param targ: a list of values that must match the values of the properties defined by annot_keys
    :param annot_keys: a list of properties
    :param add_void: a boolean defining if we  keeo void values.void values will have the string value "" 
    :param extend_to_cc:   if true  add all members of a connectes compoenent which, \
    at least one node matches a properties value defined in targ 
    :return: a subgraph
    :rtype: graph 
 
    """ 


    targmap=dict()
    targmapcc=dict()
    revnidmap=dict()
    prop2nid=dict()
    selectedcc=dict()
    for annot_key in annot_keys:
      pkprop= g.vertex_properties[annot_key]
      nid=0
      vfilt =  g.new_vertex_property('bool'); 
      for v in   g.vertices():
          vfilt[nid] = False
          xid=pkprop[nid]
          revnidmap[xid]=nid
         
          if xid is not None and xid !="":
              utils.__addArrayEl(prop2nid,xid,nid)   
          else:
             if add_void==True:
                    if xid is None:
                       xid="" 
                    utils.__addArrayEl(prop2nid,xid,nid)   
             
          nid+=1
         
    if extend_to_cc==True:   
        ccomp, hist  = label_components(g, directed=None, attractors=False)
    mccid=dict()
     

            
    if targ!=None:        
      for nml in  targ:
         nm=nml
         ccidl=set()   
         if nm in  prop2nid.keys(): 
           for nid in prop2nid[nm]:
              v=  g.vertex(nid)
              vfilt[nid] = True
              if extend_to_cc==True: 
                ccid=ccomp[v]
                ccidl.add(ccid)
                selectedcc[ccid]=1
         else:
            nms=nml.split(";")
            for nm in nms: 
              if nm in  prop2nid.keys(): 
                for nid in prop2nid[nm]:                
                   v=  g.vertex(nid)
                   vfilt[nid] = True
                   if extend_to_cc==True: 
                      ccid=ccomp[v]
                      ccidl.add(ccid)
                      selectedcc[ccid]=1
                
         targmap[nml]=list(ccidl)   

    if extend_to_cc==True:
        for v in g.vertices():
           nid=int(v) 
           ccid=ccomp[v]
           ccidct=0
           if ccid in mccid.keys():
               ccidct=mccid[ccid]

           ccidct+=1
           mccid[ccid]=ccidct
           if ccid in selectedcc.keys(): 
               vfilt[nid] = True
            
            
    sgv = gt.GraphView(g, vfilt=vfilt)
    sg = gt.Graph(sgv, prune=True)        

    
    return sg,targmap




def define_boolean_filter(gr,att,val, usecase=True):

     """Create a boolean filter property:


     :param gr: a graph
     :param att: a  existing property name
     :param val: a value for the property att. Each node with this property value will be selected by the filter. Optionaly, val can be a list of values 
     :param usecase:if False, when val is a string, upper or lower strings will match     
     :return: a filter as a dictionnary (node index,True/False)
     :rtype: dict  
     """ 

     vfilter = gr.new_vertex_property("bool");
     lval  =list()
     if type(val) is list: 
        for v in val:
           lval.append(v) 
     else:
        lval.append(val)
    
     for v in gr.vertices():
         cval=gr.vp[att][v]
         vindex=gr.vertex_index[v]
         domatch=0
         for vl in lval:   
           if cval is not None:

             if usecase ==False:
                cval=cval.lower()
                vl=vl.lower()
               
             if cval==vl:   
                domatch=1
                
         if domatch==1   :
           vfilter[vindex] = True 
         else:
           vfilter[vindex] = False

                
     return vfilter
 

 
def filter_from_boolean_filter(gr,vfilter):
     """Create a subgraph using a filter:

     :param gr: a graph
     :param vfilter: a filter as a dictionnary (node index,True/False)
     :return: a subgraph
     :rtype: graph 
 
     """

     
     u = gt.GraphView(gr, vfilt=vfilter)
     u=gt.Graph(u, prune=True)
     return u


#filter a graph using a node property ( V2 with lambda)
def filter_by_node_attribute(gr,att,val):
     """Create a subgraph where the nodes matches a property value:

     :param gr: a graph
     :param att: an  existing property name
     :param val: a value for the property att. Each node with this property value will be selected by the filter 
     :return: a subgraph
     :rtype: graph 
 
     """
     u=gt.GraphView(gr, vfilt=lambda v: gr.vp[att][v]==val)
     u=gt.Graph(u, prune=True)
     if u is None:
       logger.info("warning graph is None")
     return u




def largest_connected_component(g, directed=False):

	"""Select the largest connected component:

	:param g: a graph
	:return: a subgraph
	:rtype: graph 
 
	"""

	lCCfilt = gt.label_largest_component(g, directed=directed)
	lCC = gt.GraphView(g, vfilt=lCCfilt)
	lCC=gt.Graph(lCC, prune=True)
	logger.info("\nlargest CC order: %s" %len(list(lCC.vertices())))
	logger.info("largest CC size: %s" %len(list(lCC.edges())))
	return lCC

 
def remove_largest_cc(g, directed=False):
	"""Remove the largest connected component:

	:param g: a graph
	:return: a subgraph
	:rtype: graph 
 
	"""

	woLCCfilt = gt.label_largest_component(g, directed=directed)
	for i in range(len(woLCCfilt.a)):
		woLCCfilt.a[i]= 1-woLCCfilt.a[i]
	woLCC = gt.GraphView(g, vfilt=woLCCfilt)
	woLCC=gt.Graph(woLCC, prune=True)
	logger.info("graph without largest CC order: %s" %len(list(woLCC.vertices())))
	logger.info("graph without largest CC size: %s" %len(list(woLCC.edges())))
	return woLCC




###########################



def merge_nodes(gr,first_node,second_node,remove_node=True):
    """Merge two nodes of a graph, presserving edges and properties:

    :param gr: a graph
    :param first_node: first node to ne merged
    :param second_node: second node to ne merged
    :param remove_node: if True, remove first_node
    :return: the modified graph
    :rtype: graph 
 
    """


    properties.copy_node_properties(gr,first_node,second_node)
    
    for e in first_node.in_edges():
         ee=gr.edge(e.source(),second_node)
         if ee is None:   
           newEdge=gr.add_edge(e.source(),second_node)
           properties.copy_edge_properties(gr, e, newEdge)
            
    for e in first_node.out_edges():
        ee=gr.edge(second_node,e.target())
        if ee is None:   
            newEdge=gr.add_edge(second_node,e.target()) 
            properties.copy_edge_properties(gr, e, newEdge)
           
    earr=list()            
    for e in first_node.in_edges():
        earr.append(e)
    for e in first_node.out_edges():
        earr.append(e)

    for e in earr:
        gr.remove_edge(e)   
    if remove_node==True:    
       gr.remove_vertex( first_node)



    
def __merging_property(gr, properties_list,caseSensitive=True):

  """Define a merging property for all nodes of a graph, using a concatenation of the values of each property of a list:

  :param gr: a graph
  :param properties_list: a list of node properties
  :param caseSensitive: if True, the value match is case sensitive
  :return: a property
  :rtype: dict 
 
  """


  spropList=list()  
  sep=":"
  gprop = gr.new_vertex_property("string")
  for sprop in  properties_list:
       for prop in gr.vertex_properties.keys():
          if sprop==prop:
                spropList.append(sprop)
  for v in gr.vertices(): 
     gvp=list()
     for sprop in  spropList:
         pv=str(gr.vp[sprop][v])  
         gvp.append(pv)
         fval=sep.join(gvp)
         if caseSensitive==False:
              fval=fval.lower()
     gprop[v]=fval
  return  gprop

 
def merge_graph(gr1,gr2,properties_list,add_void=False,caseSensitive=True):

  """Merge two graphs. all nodes of both graphs, that share the same value of a list of properties are merged:

  :param gr1: first graph
  :param gr2: second graph
  :param properties_list: a list of node properties
  :param add_void:  if True, nodes with void values are merged
  :param caseSensitive: if True, the value match is case sensitive
  :return: the merged graph
  :rtype: graph 
 
  """

    
  gprop1=__merging_property(gr1, properties_list,caseSensitive)
  gprop2=__merging_property(gr2, properties_list,caseSensitive)
  nnodeMap=dict()
  domergeMap=dict()
  sep=";" 
  rprop = gr1.new_vertex_property("int")
 
  for u in gr1.vertices(): 
     
    keyu=gprop1[u]
    rprop[u]=0
    for v in gr2.vertices(): 
        keyv=gprop2[v]
        domerge=False
        if keyu is   None or  keyv is   None or keyu=="":
            if  add_void==True and keyu==keyv:
                domerge=True
        else:

            kvu=keyu.split(sep)
            kvv=keyv.split(sep)
            for euv in kvu:
               for evv in kvv:
                  if  euv==evv:
                      domerge=True
                      break         
        if int(v) not in nnodeMap:
            
            second_node=gr1.add_vertex() 
            nnodeMap[int(v)]=second_node
           
            for prop in gr1.vertex_properties.keys():
                gr1.vp[prop][second_node]=gr2.vp[prop][v]
        else:
            second_node=nnodeMap[int(v)]
            

 
        if domerge==True:
           
            logger.info(utils.node_to_string(gr1, second_node, " , "))
            ki=int(second_node)
            if ki in domergeMap:
                kset=domergeMap[ki]
            else:
                kset=set()
            vu=int(u)
            kset.add(vu)    
            domergeMap[ki]=kset
            rprop[u]=1
             
            
  for v in gr2.vertices():
    
    second_node=nnodeMap[int(v)]
    for e in v.in_edges():
        
         source=nnodeMap[int(e.source())]      
         ee=gr1.edge(source,second_node)
         if ee is None:   
            newEdge=gr1.add_edge(source,second_node)
            properties.copy_edge_properties(gr1, e, newEdge)
                      
    for e in v.out_edges():
        target=nnodeMap[int(e.target())]                     
        ee=gr1.edge(second_node,target)
        if ee is None:   
             newEdge=gr1.add_edge(second_node,target) 
             properties.copy_edge_properties(gr1, e, newEdge)
 
  nmap=dict()
 
  for n in gr1.vertices(): 
 
    nid=int(n)
    nmap[nid]=n
 
            
  for nid in nmap.keys(): 
        second_node=nmap[nid]
    
        if nid in domergeMap.keys():
           
           ulist=list(domergeMap[nid])
           for ix in ulist:
              u=nmap[ix]
       
              merge_nodes(gr1,u,second_node,False)
             
  narr=list()              
  for nid in nmap.keys(): 
        u=nmap[nid]
        if rprop[u] is not None and rprop[u]==1:
           logger.info("  -->>>>"+utils.node_to_string(gr1, u, " , ")) 
           narr.append(u)
  if len(narr)>0:
           gr1.remove_vertex(narr)

 
  return gr1




def merge_node_by_property(gr1,properties_list,add_void=False,caseSensitive=True):


  """Merge all nodes of a graph, that share the same value of a list of properties:

  :param gr: a graph
  :param properties_list: a list of node properties
  :param caseSensitive: if True, the value match is case sensitive
  :return: the modified graph
  :rtype: graph 
 
  """
    
  gprop1=__merging_property(gr1, properties_list,caseSensitive)
  nnodeMap=dict()
  domergeMap=dict()
  sep=";" 
  rprop = gr1.new_vertex_property("int")
 
  for u in gr1.vertices(): 
     
    keyu=gprop1[u]
    rprop[u]=0
    for v in  gr1.vertices(): 
        keyv=gprop1[v]
        nnodeMap[int(v)]=v
        domerge=False
        if keyu is   None or  keyv is   None or keyu=="":
            if  add_void==True and keyu==keyv:
                domerge=True
        else:

            kvu=keyu.split(sep)
            kvv=keyv.split(sep)
            for euv in kvu:
               for evv in kvv:
                  if  euv==evv:
                      domerge=True
                      break         
 
 
        if domerge==True:
            second_node=u
            logger.info(utils.node_to_string(gr1, second_node, " , "))
            ki=int(second_node)
            if ki in domergeMap:
                kset=domergeMap[ki]
            else:
                kset=set()
            vv=int(v)
            if vv!=ki:
               kset.add(vv)    
            
            domergeMap[ki]=kset
            rprop[v]=1

 
  nmap=dict()
    
  for n in gr1.vertices(): 
    nid=int(n)
    nmap[nid]=n     
  # 
  rmm=dict()
  for nid in nmap.keys(): 
        v=nmap[nid]
        if nid in domergeMap.keys():
           ulist=list(domergeMap[nid])
           for ix in ulist: 
              u=nmap[ix]
              logger.info("-v--%s   "%(int(v) )) 
              if int(u)!=int(v):
                 st=set()  
                 st.add(str(ix))
                 st.add(str(nid))  
                 k=",".join(sorted(st))
                 if k not in rmm.keys():
                    rmm[k]=1     
                    logger.info("-v u--%s %s "%(int(v),int(u))) 
                    rprop[u]=2
                    merge_nodes(gr1,u,v,False)
         
  narr=list()              
  for nid in nmap.keys(): 
        u=nmap[nid]
        if rprop[u] is not None and rprop[u]==2:
           logger.info("  -->>>>"+utils.node_to_string(gr1, u, " , ")) 
           narr.append(u)
  if len(narr)>0:
           gr1.remove_vertex(narr)

 
  return gr1    





 
def sub_graph_filter(g, iteration_count, central_node, direction=all, node_limit=None, neighbour_count=None):

    """define a subgraph filter according to parameters:

    :param gr: a graph
    :param iteration_count: number of iterations
    :param central_node: selected node id
    :param direction: edge direction (all,in,out)
    :param node_limit:  maximum node number
    :param neighbour_count:  number of neighbours
    :return: the filter
    :rtype: dict 
 
    """

    vSubFilt=np.zeros(len(list(g.vertices())))
    neighbourhood=[np.int64(central_node)]
    newNeighbours=neighbourhood

    for i in range(1, int(iteration_count)+1):
        newNeighboursTamp=newNeighbours
        newNeighbours=[]

        if (direction is None or str(direction)=="all"):
            for v in newNeighboursTamp:
                for n in g.get_all_neighbours(v):
                    if (n not in neighbourhood):
                        newNeighbours.append(n)
        elif (str(direction)=="in"):
            for v in newNeighboursTamp:
                for n in g.get_in_neighbours(v):
                    if (n not in neighbourhood):
                        newNeighbours.append(n)
        elif (str(direction)=="out"):
            for v in newNeighboursTamp:
                for n in g.get_out_neighbours(v):
                    if (n not in neighbourhood):
                        newNeighbours.append(n)
        else:
            logger.info("\nERROR: DIRECTION UNDEFINED (must be {all, in, out})\n")
            return -1

        if (newNeighbours==[]):
            logger.info("\nBREAK: NO NEW NEIGHBOURS AT ITERATION %s\n" %i)
            break
        if (neighbour_count is not None):#choose randomly a given number (if not none) of neighbours
            newNeighbours=np.random.choice(newNeighbours, int(neighbour_count))

        newNeighbours=np.unique(newNeighbours)
        neighbourhood=np.concatenate((neighbourhood, newNeighbours))
        if (node_limit is not None and len(neighbourhood)>= int(node_limit)):#break if cardinality is over the limit
            logger.info("\nBREAK: CARDINALITY REACHED THE GIVEN LIMIT\n")
            break


    for l in np.int64(neighbourhood):#build filter
        vSubFilt[l]=1
    return vSubFilt



 

def subgraph_by_direction(g, iteration_count, chosen_node_id=None, direction="all", node_limit=None, neighbour_count=None):

    """extract a subgraph  according to parameters:

    :param gr: a graph
    :param iteration_count: number of iterations
    :param chosen_node_id: selected node id
    :param direction: edge direction (all,in,out)
    :param node_limit:  maximum node number
    :param neighbour_count:  number of neighbours
    :return: the subgraph
    :rtype: graph 
 
    """
    if (chosen_node_id is not None):
        central_node=gt.find_vertex(g, g.vp._graphml_vertex_id, chosen_node_id)[0]
 
    else:
        central_node=np.random.choice(g.get_vertices())
     
    logger.info("\nCentral Node Name: "+str(g.vp.name[central_node]))
    logger.info("Central Node Id: "+str(g.vp._graphml_vertex_id[central_node]))
    logger.info("Central Node Degree: "+str(g.get_total_degrees([central_node])))

    vSubFilt=sub_graph_filter(g, iteration_count, central_node, direction, node_limit, neighbour_count)
    subG = gt.GraphView(g, vfilt=vSubFilt)
    subG=gt.Graph(subG, prune=True)
    return subG




def subgraph_by_node(input_graph,output_graph ,nodeid,direction="in",neighbour_count=3):

      """extract a connected component holding a node specified by node id:

      :param input_graph: input graphml file
      :param output_graph: output graphml file
      :param nodeid: selected node id
      :param direction: edge direction (all,in,out)
      :param neighbour_count:  number of neighbours
      :return: the subgraph
      :rtype: graph 
 
      """
      g=graph_explore.load_graphml(input_graph, directed=True)
      g = subgraph_by_direction(g, 2, chosen_node_id=nodeid, direction=direction, neighbour_count=neighbour_count)
      return g





 



