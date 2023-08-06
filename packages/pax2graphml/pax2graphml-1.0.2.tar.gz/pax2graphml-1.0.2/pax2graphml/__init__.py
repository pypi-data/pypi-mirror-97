import os
import sys
import logging

__version__='1.0.2'

## disable stdout and stderr during import if silent=True
silent=False

SKEY="P2G_IMPORT_SILENT"
if SKEY in os.environ.keys():
   sv=os.environ[SKEY]
   if sv.lower() in ['true', '1', 't', 'y', 'yes'] :
      silent=True


logging.getLogger(__name__).addHandler(logging.NullHandler())    

def get_loggers():
    """
    Get all the logger for the current package
    """
    loggers = []
    #print("__name__:%s" %(__name__))
    for logger in logging.Logger.manager.loggerDict.values():
        if not isinstance(logger, logging.Logger):
            continue

        if logger.name.startswith(__name__):
            #print("  logger.name:%s" %(logger.name))
            loggers.append(logger)
    return loggers


def enable_logs(level=logging.DEBUG):
    """
    Configure loggers to print on stdout/stderr
    """
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(name)s :: %(levelname)s :: %(message)s'))
    for logger in get_loggers():
        logger.removeHandler(handler)
        logger.addHandler(handler)
        logger.setLevel(level)
        logger.propagate = False



def verbose():
    enable_logs(logging.DEBUG)


def disable_logs():
    """
    Configure loggers not to print anywhere
    """
    handler = logging.NullHandler()
    for logger in get_loggers():
        #print("    removeHandler:%s" %(logger.name))
        #logger.removeHandler(handler)
        logger.handlers = []
        logger.addHandler(handler)
        
        logger.propagate = False




def importPkBase():
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            import numpy as np
            import graph_tool.all as gt
            import pandas as pd
            import argparse

            import pax2graphml.utils
            import pax2graphml.math
            import pax2graphml.clust
            import pax2graphml.pax_import
            import pax2graphml.graph_explore
            import pax2graphml.properties
            import pax2graphml.extract

def importPk():
  

            import pax2graphml.utils
            import pax2graphml.math
            import pax2graphml.clust
            import pax2graphml.pax_import
            import pax2graphml.graph_explore
            import pax2graphml.properties
            import pax2graphml.extract


if silent==True:
            prevOutFd = os.dup(1)
            prevInFd = os.dup(0)
            prevErrFd = os.dup(2)
            #Redirect standard in, out, and error
            si = open(os.devnull,"r")
            se = open(os.devnull,"a+")
            so = open(os.devnull,"a+")


            os.dup2(si.fileno(), 0)
            os.dup2(so.fileno(), 1)
            os.dup2(se.fileno(), 2)

            #print("silent")
            importPkBase()
            #Restore standard in, out, and error
            os.dup2(prevOutFd, 1)
            os.close(prevOutFd)
            os.dup2(prevInFd, 0)
            os.close(prevInFd)
            os.dup2(prevErrFd,2)
            os.close(prevErrFd)
            #print("not silent")

            importPk()
           
else:
     importPkBase()
     importPk()

       






def convertSpaim( biopax_file , graphml_file ):
    return convert(biopax_file, graphml_file)
#alias  
def convert( biopax_file , graphml_file ):
    return pax_import.biopax_to_reaction_graph(biopax_file,graphml_file)


def merge(infiles,outfile):
     return pax_import.biopax_merge(infiles,outfile)
    


def  node_list( g ):
    lst=utils.node_list(g)
 
    return lst

def  edge_list( g ):
    lst=utils.edge_list(g)
 
    return lst

 
def compute_graph_metrics( g ):
    return graph_explore.compute_graph_metrics(g)


def  defineGraphModel( graphml_file ):
    return graph_explore.load_graphml(graphml_file)

def load( graphml_file ):
    return defineGraphModel(graphml_file)



def drawGraph(g,ouputfile="g.png"):
     graph_explore.saveOrPlot(g, None, ouputfile)

def save(g,ouputfile="g.graphml"):
     graph_explore.saveOrPlot(g, ouputfile,None)


           


