import logging

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import graph_tool.all as gt
import pandas as pd
import argparse


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def hyperbolicTangent(n):
    return np.tanh(x)

def sigmoid(x, derivative=False):
    sigm = 1 / (1 + np.exp(-x))
    if derivative:
        return sigm * (1 - sigm)
    return sigm
 
#https://fr.wikipedia.org/wiki/Sigmo%C3%AFde_(math%C3%A9matiques)




def sigmoidTransform(x):
    x=np.double(x)
    zr=np.double(0)
    if x < zr:
          r=sigmoid(-x)
          return -r
    else:    
          r=sigmoid(x)
          return r
