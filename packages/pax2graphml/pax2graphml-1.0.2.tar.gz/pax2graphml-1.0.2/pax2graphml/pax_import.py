"""This module contains function to manipulate BIOPAX and GRAPHML files."""


__license__ = "MIT"
__docformat__ = 'reStructuredText'


import os, sys
import logging
import os.path


import json
from pprint import pprint
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import graph_tool.all as gt
import pandas as pd
import traceback
 
 
from pax2graphml import utils
from pax2graphml import properties
from pax2graphml import graph_explore

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
 
def biopax_to_reaction_graph(biopax_file,graphml_file,blackList=None):

    """Generate a reaction graph with binary interactions as a GRAPHML file from a BIOPAX file. Tte BIOPAX file is filtered, keeping only the regulation part (metabolism and genes). The process use PAXTOOLS, need a lot of memory and can be slow for big BIOPAX files:

    :param biopax_file: input BIOPAX file
    :param graphml_file: output GRAPHML reaction file
    :return: void
    :rtype: None
  
    """ 

    cls="dyliss.biopax.app.Pax2GraphML"

    if blackList is not None:
       blackListOpt=" -b %s" %(blackList)
    else:
       blackListOpt=""

    cmd="%s %s -cp %s %s -i '%s' -o '%s' -t '%s' %s" %(utils.__jvm(),utils.__jvmopt(),utils.__jarpath(),cls,biopax_file,graphml_file,utils.__template(), blackListOpt)
    logger.info("command : %s" %(cmd))
    return utils.__runCmd(cmd)





 

def biopax_merge(biopax_list,output_file="output.owl"):
    """Merge multiple BIOPAX (RDSF/XML) files. The process use PAXTOOLS, need a lot of memory and can be slow for big BIOPAX files:

    :param biopax_list: a list of  input BIOPAX files to be merged
    :param output_file: output BIOPAX file
    :return: void
    :rtype: None
  
    """     
    cls="dyliss.biopax.app.Pax2Merge"
    biopax_filestr=",".join(biopax_list)


    cmd="%s %s -cp %s %s -i '%s' -o '%s'" %(utils.__jvm(),utils.__jvmopt(),utils.__jarpath(),cls,biopax_filestr,output_file)
    logger.info("command : %s" %(cmd))
    return utils.__runCmd(cmd)

 

def biopax_filter(biopax_file,datasources,output_file="output.owl"):
    """Remove Datasources  from a BIOPAX file. The process use PAXTOOLS, need a lot of memory and can be slow for big BIOPAX files:

    :param biopax_file: input BIOPAX files 
    :param datasources: list of datasources to exclude 
    :param output_file: output BIOPAX file
    :return: void
    :rtype: None
  
    """       
    cls="dyliss.biopax.app.BioPaxFilter"
    filterd=":".join(datasources)
    cmd="%s %s -cp %s %s  %s %s %s" %(utils.__jvm(),utils.__jvmopt(),utils.__jarpath(),cls,biopax_file,filterd,output_file)
    logger.info("command : %s" %(cmd))
    return utils.__runCmd(cmd)





def name_alias(biopax_file,output_file="entities_aliases.json",opt="--uri-ids"):
    """#generate a json file with annottaions extracted from a BIOPAX file. The process use PAXTOOLS :

    :param biopax_file: input BIOPAX files 
    :param output_file: output json file
    :param opt: output generation options
    :return: void
    :rtype: None
  
    """   
    cls="dyliss.biopax.app.P2GAliasProcessor"  
    cmd="%s %s -cp %s %s NAME_ALIAS '%s' '%s' %s" %(utils.__jvm(),utils.__jvmopt(),utils.__jarpath(),cls,biopax_file,output_file,opt)
    logger.info("command : %s" %(cmd))
    return utils.__runCmd(cmd)


 
def annotation_dict(alias_file):
  """Create a dictionary from an annotation json file:

  :param alias_file: annotation json file
  :return: annotation dictionary
  :rtype: dict
  
  """     
  
  alias=dict()
  dkey="any"
  with open(alias_file) as jsf:
    ar = json.load(jsf)
    jsf.close()
    for t in ar:
      if t['uri'] is not None: 
        uri=t['uri']
        if t['datasource'] is not None:
            ds=t['datasource']
        else:
            ds=[dkey]
        for px in ds:
           k=px.lower() +"@"+uri
           alias[k]=t
  return alias

def join_annotation(g,alias_file,annot_field, dest_field,default_val, property_type="string"):
  
 
   """Populate a new node property with values extracted from an annotation json file:

   :param properties_file: json annotation file    
   :param annot_field: field in json data dictionary to be processed
   :param dest_field: new property name
   :param default_val: property default value for None
   :param property_type: new property type
   :return: annotation dictionary
   :rtype: dict
  
   """ 
   mapd=annotation_dict(alias_file)
  
   docreate=True
   for p in   g.vertex_properties.keys() :
    if p != None:
       if p ==dest_field:    
            docreate=False
   if docreate:
      g.vp[dest_field]=g.new_vertex_property(property_type);
    
   uri =  g.vertex_properties["uri"]  
   provider =  g.vertex_properties["provider"]
   nprop =  g.vertex_properties[dest_field]

   
   for n in g.vertices():
       pv=provider[n] 
       ur=uri[n] 
       if pv is  None :
          pv="any"
            
       k=str(pv).lower()+"@"+ur
 
       if k in mapd:
          tupl=mapd[k]
 

          if annot_field in tupl : 
             nprop[n]=tupl[annot_field]
          else:
            if default_val is not None:
             nprop[n]=default_val
       else:
         if default_val is not None:
            nprop[n]=default_val




############################influence graph
 

#CREATING INFLUENCE GRAPH
##INITIATE QUANTITY NODES
def __initiateQuantityNode(g):
    g.vp.influenceType = g.new_vertex_property("string")
    for v in g.vertices():
        if (g.vp.entityType[v] == "reaction"):
            g.vp.influenceType[v]="reaction"

        elif (g.vp.entityType[v] == "chemical" ):
            g.vp.influenceType[v]="availability"
            qNode=g.add_vertex()
            #Copie des informations
            properties.copy_node_properties(g, v, qNode)
            g.vp.influenceType[qNode]="quantity"
            g.vp._graphml_vertex_id[qNode]=g.vp._graphml_vertex_id[v]+"Q"
            g.vp.color[qNode]="peru"


        else:
            g.vp.influenceType[v]="undef"
    return g


#LINK EDGES
def __linkEdges(g, displayProgress=False):
    reaction= gt.find_vertex(g, g.vp.influenceType, "reaction")
    count=0
    g.ep.effect=g.new_edge_property("string")
    for r in reaction:

        if (displayProgress):
            logger.info(str(count)+" / "+str(len(reaction))+" edges")
            count+=1

        source=[]
        target=[]
        catalysisBool=False
        for e in r.all_edges():#get all the (source, target) pairs and test if reaction is moderated or not
            source.append(int(e.source()))
            target.append(int(e.target()))
            if (g.ep.spaim[e] in 'aim'):
                catalysisBool=True #True if the reaction is moderated

        substrate=[]
        for s, t in zip(source, target):
            e=g.edge(s,t)

            ##LINK PRODUCT
            if (g.ep.spaim[e]=='p'):
                 g.ep.effect[e]='1'


                 try:
                        logger.info("LINK PRODUCT")
                        vid=g.vp._graphml_vertex_id
                        vidsrc=g.vp._graphml_vertex_id[e.target()]
                        rl= gt.find_vertex(g, vid, vidsrc+"Q" )
                       
                        if len(rl)>0:
                            rr=rl[0]    
                            sEdge = g.add_edge(r,rr )
                            g.ep.effect[sEdge]='1'
                            g.ep.color[sEdge]='red'
                        else:
                             ed=utils.edge_description(g,e)
                             logger.info("==>ERROR:LINK PRODUCT, no ref vertex found   %s "%(ed))
                                
                 except:
                        logger.error("\nERROR IN ADDING EDGE(LINK PRODUCT) %s\n" %(traceback.format_exc() ) )
                        return -1


            ##LINK ACTIVATOR, INHIBITOR, MODULATOR
            if (g.ep.spaim[e] in 'aim'):

                try:
                        logger.info("LINK ACTIVATOR, INHIBITOR, MODULATOR")
                        vid=g.vp._graphml_vertex_id
                        vidsrc=g.vp._graphml_vertex_id[e.source()]
                        rl= gt.find_vertex(g, vid, vidsrc+"Q" )
                       
                        if len(rl)>0:
                            rr=rl[0]    
                            #ed=utils.edge_description(g,e)
                            #print("==>OK:LINK SUBSTRATE,  ref vertex found   %s "%(ed))
                            sEdge = g.add_edge(r,rr )
 

                            if (g.ep.spaim[e]=='a'):#activator
                               g.ep.effect[sEdge]='1'
                            if (g.ep.spaim[e]=='i'):#inhibitor
                               g.ep.effect[sEdge]='-1'
                            if (g.ep.spaim[e]=='m'):#modulator
                               g.ep.effect[sEdge]='0'
                            g.ep.color[sEdge]=g.ep.color[e]
                            g.remove_edge(e)

                        else:
                             ed=utils.edge_description(g,e)
                             logger.error("==>ERROR:LINK ACTIVATOR, INHIBITOR, MODULATOR, no ref vertex found   %s "%(ed))
                                
                except:
                        logger.error("\nERROR IN ADDING EDGE(LINK ACTIVATOR, INHIBITOR, MODULATOR) %s\n" %(traceback.format_exc() ) )
                        return -1

####



            ##LINK SUBSTRATE
            if (g.ep.spaim[e] in 's'):
                g.ep.effect[e]='1'
                if (catalysisBool):#ie if the reaction is moderated
                    try:
                        logger.info("LINK SUBSTRATE")
                        vid=g.vp._graphml_vertex_id
                        vidsrc=g.vp._graphml_vertex_id[e.source()]
                        rl= gt.find_vertex(g, vid, vidsrc+"Q" )
                       
                        if len(rl)>0:
                            rr=rl[0]    
                            #ed=utils.edge_description(g,e)
                            #print("==>OK:LINK SUBSTRATE,  ref vertex found   %s "%(ed))
                            sEdge = g.add_edge(r,rr )
                            g.ep.effect[sEdge]='-1'
                            g.ep.color[sEdge]='blue'
                        else:
                             ed=utils.edge_description(g,e)
                             logger.info("==>ERROR:LINK SUBSTRATE, no ref vertex found   %s "%(ed))
                                
                    except:
                        logger.error("\nERROR IN ADDING EDGE(LINK SUBSTRATE) %s\n" %(traceback.format_exc() ) )
                        return -1


                else:
                    substrate.append(e.source())

        ##LINK SUBSTRATE (MODERATED REACTION)
        for sub in range(len(substrate)):#for each reaction that is not moderated, link by a down-regulation substrates' availabilities to other substrates' quantities
            substrateTamp=list(np.copy(substrate))
            substrateTamp.pop(sub)
            for v in substrateTamp:
                try:
                    logger.info("LINK SUBSTRATE (MODERATED REACTION)")
                    vid=g.vp._graphml_vertex_id
                    vidsrc=g.vp._graphml_vertex_id[v]  
                    rl= gt.find_vertex(g, vid, vidsrc+"Q" )
                                          
                    if len(rl)>0:
                            rr=rl[0]    
                            #sEdge = g.add_edge(r,rr )
                            sEdge = g.edge(substrate[sub], rr, add_missing=True )
                            g.ep.effect[sEdge]='-1'
                            g.ep.color[sEdge]='skyblue'
                    else:
                             ed=utils.edge_description(g,e)

                             sbiopaxType=g.vp.biopaxType[e.source()]
                             tbiopaxType=g.vp.biopaxType[e.target()]   
                             if sbiopaxType=="DnaRegion" and tbiopaxType=="ComplexAssembly":
                                msg="WARNING:LINK SUBSTRATE(MODERATED REACTION),unmanaged case for quantity %s -> %s" %(sbiopaxType, tbiopaxType )                               
                             else:
                                msg="ERROR:LINK SUBSTRATE(MODERATED REACTION), no ref vertex found"

                             logger.info("==>%s  %s "%(msg,ed))

 
                except:
                    logger.error("\nERROR IN ADDING EDGE(LINK SUBSTRATE (MODERATED REACTION) %s\n" %(traceback.format_exc() ) )
                    return -1

    g=gt.Graph(g, prune=True)
    return g



def reaction_to_influence_graph(reaction_graph):

    """generate an influence graph from a checked reaction graph:

    :param reaction_graph: checked reaction graph   
    :return: influence graph
    :rtype: graph object
  
    """ 

    infG=reaction_graph.copy()
    __initiateQuantityNode(infG)
    __linkEdges(infG)
    return infG


def prepare_spaim(input_graph,output_graph,output_image,checkInvertP=True):

    """generate an checked reaction graph from a raw reaction graph:

    :param input_graph: input graphml file containing the raw reaction graph
    :param output_graph: output graphml file containing the checked reaction graph
    :return: void
    :rtype: None
  
    """ 
    g=graph_explore.load_graphml(input_graph)
    g=__setEntityType(g)
    #for v in g.vertices():
    #    print(g.vp.name[v].lower())
    anormalConnections=__checkConnections(g)
    anormalNodes=np.reshape(anormalConnections, -1)
    #ADHOC INCLUSION
    logger.info("\nAdhoc Inclusion Attempt...")
    for v in anormalNodes:
        undefAnormalButReaction=['TRANSCRIPTION', 'INHIBITION', 'PHYSICAL_STIMULATION', 'CATALYSIS', 'MODULATION', 'STATE_TRANSITION']
        g.vp.biopaxType[v]='UNDEF_CHEMICAL_ENTITY'
        g.vp.entityType[v]="chemical"
        #print("hey")
        for bpType in undefAnormalButReaction:
            #print(g.vp.name[v].lower())
            nm=g.vp.name[v].upper()
            if (bpType in nm):

                logger.info("-fix abnormal reaction   %s " %(nm))

                g.vp.biopaxType[v]=bpType
                g.vp.entityType[v]="reaction"

    if checkInvertP==True:
       #INVERT PRODUCT EDGES
       logger.info("\ncheck if need to invert product edges...")
       source=[]
       target=[]
       try:
         g.ep.color=g.new_edge_property("string")
       except: 
         logger.error("\nedge color already exists")

         
       for e in g.edges():
        if (g.ep.spaim[e]=='p' and g.vp.entityType[e.source()]!="reaction"  and g.vp.entityType[e.target()]=="reaction" ):
            ed=utils.edge_description(g,e)
            logger.info("-inversion from %s -%s-> %s --[ %s ]--" %(e.source(),g.ep.spaim[e],e.target(), ed ))
            source.append(int(e.source()))
            target.append(int(e.target()))
       for s, t in zip(source, target):
            e=g.edge(s,t)
            newEdge=g.add_edge(t, s)
            g.ep.color[newEdge]=g.ep.color[e]
            g.ep.interaction[newEdge]=g.ep.interaction[e]
            g.ep.spaim[newEdge]=g.ep.spaim[e]
            g.remove_edge(e)


    g=gt.Graph(g, prune=True)
    __undefNodesAndEdges(g)
    graph_explore.color_nodes(g)
    graph_explore.color_edges(g)
 
    if output_graph is not None:
       graph_explore.save_graphml(g, output_graph)
    if output_image is not None:
       graph_explore.save_image(g, output_image)



def influence_subgraph(input_graph,output_graph,output_image,min_node,max_node):
   """Generate an influence graph as a graphml file from a checked reaction graphml file. The graph is generated from one connected component:
 
   :param input_graph: input graphml file containing the raw reaction graph
   :param output_graph: output graphml file containing the checked reaction graph
   :param output_image: output png file for graph visualization
   :param min_node: minimum node count of tne connected component
   :param max_node: maximum node count of tne connected component
   :return: void
   :rtype: None
  
   """  
   g=graph_explore.load_graphml(input_graph, directed=True)
   g=utils.cc_by_node_count(g,min_node,max_node)
   if g is not None:
      g = reaction_to_influence_graph(g)
      graph_explore.__saveOrPlot(g, output_graph, output_image)
      return g
   else:
      return None




def influence_graph(input_graph,output_graph,output_image):
  """
  generate an influence graph as a graphml file from a checked reaction graphml file
 
  :param input_graph: input graphml file containing the raw reaction graph
  :param output_graph: output graphml file containing the checked reaction graph
  :return: void
  :rtype: None
  
  """ 

  g=graph_explore.load_graphml(input_graph, directed=True)
  g = reaction_to_influence_graph(g)
  graph_explore.__saveOrPlot(g, output_graph, output_image)





 




def __setEntityType(g):
    """
    set the entity type node property {REACTION, CHEMICAL} 
    """
    g.vp.entityType = g.new_vertex_property("string")
    for v in g.vertices():
        if (g.vp.biopaxType[v] in ('undef','ComplexAssembly','Catalysis','BiochemicalReaction','Control','Interaction', 'TRANSCRIPTION', 'INHIBITION', 'PHYSICAL_STIMULATION', 'CATALYSIS', 'MODULATION', 'STATE_TRANSITION')):
            g.vp.entityType[v]="reaction"
        elif (g.vp.biopaxType[v] in ('Complex', 'Dna', 'PhysicalEntity', 'Protein', 'Rna', 'SmallMolecule','UNDEF_CHEMICAL_ENTITY')):
            g.vp.entityType[v]="chemical"
        else:
            g.vp.entityType[v]="undef"
    return g



def __undefNodesAndEdges(g):

    """
    return   undef enity type nodes and undef spaim type edges
    """
    undefTypeNodes=[]
    undefTypeEdges=[]
    for v in g.vertices():
        if (g.vp.entityType[v]=='undef'):
            undefTypeNodes.append(v)
    for e in g.edges():
        if (g.ep.spaim[e]=='undef'):
            undefTypeEdges.append((int(e.source()), int(e.target())))

    logger.info("\nnumber of undef entityType nodes: "+str(len(undefTypeNodes)))
    logger.info("number of undef spaim edges: "+str(len(undefTypeEdges)))
    return (undefTypeNodes, undefTypeEdges)


#CHECK IF A REACTION IS LINKED TO A REACTION OR A CHEMICAL IS LINKED TO A CHEMICAL OR A UNDEF IS LINKED TO A UNDEF
def __checkConnections(g):
    """ 
    Connections validation function. Check if a reaction is linked to a reaction or a chemical is linked to a chemical or an undef is linked to an undef
    """
    anormalConnections=[]
    try :
        g.vp.entityType[0]
    except:
        logger.error("\nERROR: ENTITY TYPE PROPERTY NOT FOUND\n")
        return -1
    for e in g.edges():
        if (g.vp.entityType[e.source()]==g.vp.entityType[e.target()]):
            anormalConnections.append((int(e.source()), int(e.target())))

    logger.info("\nnumber of anormal connections: "+str(len(anormalConnections)))
    return anormalConnections












