import sys
import logging
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import poisson
from scipy.stats.stats import pearsonr
from scipy.stats import normaltest
from scipy.cluster.hierarchy import linkage, to_tree, is_valid_linkage,  ClusterNode, deque, bisect
import pandas as pd
import collections


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


"""
flat clusters
see https://stackoverflow.com/questions/28687882/cutting-scipy-hierarchical-dendrogram-into-clusters-via-a-threshold-value
assignments = fcluster(linkage(distanceMatrix, method='complete'),4,'distance')

print assignments
       [3 2 2 2 2 2 2 2 2 2 2 2 1 2 1 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]

cluster_output = pandas.DataFrame({'team':df.teamID.tolist() , 'cluster':assignments})


"""

###do dendrogram to test following code

def displayNodeInfo(node,t=1,tag=""):

    s=''.join(str(" ") for i in range(t) )
    if node.is_leaf():
       print(s+"%s is_leaf:%s %s" %(tag, node.id, node.label))
    else:
       print(s+"%s is_node:%s %s %s" %(tag, node.id, node.label, node.dist))
       tt=t+1
       if node.left is not None:
           displayNodeInfo(node.left,tt,"L")
       if node.right is not None:
          displayNodeInfo(node.right,tt,"R")
        

def clustering(cormat,label):
        ni=len(cormat.keys())
        nj=0
        for i in cormat.keys():
           for j in cormat[i].keys():
               nj+=1
           break

        new_symbol_list=[""]
        
        matdist = np.zeros([ni, nj])
        print(matdist)
        for i in cormat.keys():
           for j in cormat[i].keys():
             similarity = cormat[i][j] + 1.   # range 0 to 2
             distance = (-1.0 * (similarity - 2.0)) / 2.0
             matdist[i][j] = distance
             matdist[j][i] = distance      
        print(matdist)
        lk = linkage(matdist, method='average')
        logger.info("-------------------------")
        logger.info(lk)
        logger.info("-------------------------")
        #scipy.cluster.hierarchy.dendrogram(lk)

        #nodelist =bottom_up_cluster_tree(lk,label)
        nodelist = []
        tree = to_tree_labeled(lk,label)
        nodelist.append(tree)
          
        for node in nodelist:
            displayNodeInfo(node)
           
 
          
 

class  ClusterNodeCust(object):
    """
    A tree node class for representing a cluster.
    Leaf nodes correspond to original observations, while non-leaf nodes
    correspond to non-singleton clusters.
    The `to_tree` function converts a matrix returned by the linkage
    function into an easy-to-use tree representation.
    All parameter names are also attributes.
    Parameters
    ----------
    id : int
        The node id.
    left :  ClusterNodeCust instance, optional
        The left child tree node.
    right :  ClusterNodeCust instance, optional
        The right child tree node.
    dist : float, optional
        Distance for this cluster in the linkage matrix.
    count : int, optional
        The number of samples in this cluster.
    See Also
    --------
    to_tree : for converting a linkage matrix ``Z`` into a tree object.
    """

    def __init__(self,label,  id, left=None, right=None, dist=0, count=1):
        if id < 0:
            raise ValueError('The id must be non-negative.')
        if dist < 0:
            raise ValueError('The distance must be non-negative.')
        if (left is None and right is not None) or \
           (left is not None and right is None):
            raise ValueError('Only full or proper binary trees are permitted.'
                             '  This node has one child.')
        if count < 1:
            raise ValueError('A cluster must contain at least one original '
                             'observation.')
        self.label = label # fm +
        self.id = id
        self.left = left
        self.right = right
        self.dist = dist
        if self.left is None:
            self.count = count
        else:
            self.count = left.count + right.count

    def __lt__(self, node):
        if not isinstance(node,  ClusterNodeCust):
            raise ValueError("Can't compare  ClusterNodeCust "
                             "to type {}".format(type(node)))
        return self.dist < node.dist

    def __gt__(self, node):
        if not isinstance(node,  ClusterNodeCust):
            raise ValueError("Can't compare  ClusterNodeCust "
                             "to type {}".format(type(node)))
        return self.dist > node.dist

    def __eq__(self, node):
        if not isinstance(node,  ClusterNodeCust):
            raise ValueError("Can't compare  ClusterNodeCust "
                             "to type {}".format(type(node)))
        return self.dist == node.dist

    def get_id(self):
        """
        The identifier of the target node.
        For ``0 <= i < n``, `i` corresponds to original observation i.
        For ``n <= i < 2n-1``, `i` corresponds to non-singleton cluster formed
        at iteration ``i-n``.
        Returns
        -------
        id : int
            The identifier of the target node.
        """
        return self.id

    def get_count(self):
        """
        The number of leaf nodes (original observations) belonging to
        the cluster node nd. If the target node is a leaf, 1 is
        returned.
        Returns
        -------
        get_count : int
            The number of leaf nodes below the target node.
        """
        return self.count

    def get_left(self):
        """
        Return a reference to the left child tree object.
        Returns
        -------
        left :  ClusterNodeCust
            The left child of the target node.  If the node is a leaf,
            None is returned.
        """
        return self.left

    def get_right(self):
        """
        Return a reference to the right child tree object.
        Returns
        -------
        right :  ClusterNodeCust
            The left child of the target node.  If the node is a leaf,
            None is returned.
        """
        return self.right

    def is_leaf(self):
        """
        Return True if the target node is a leaf.
        Returns
        -------
        leafness : bool
            True if the target node is a leaf node.
        """
        return self.left is None

    def pre_order(self, func=(lambda x: x.id)):
        """
        Perform pre-order traversal without recursive function calls.
        When a leaf node is first encountered, ``func`` is called with
        the leaf node as its argument, and its result is appended to
        the list.
        For example, the statement::
           ids = root.pre_order(lambda x: x.id)
        returns a list of the node ids corresponding to the leaf nodes
        of the tree as they appear from left to right.
        Parameters
        ----------
        func : function
            Applied to each leaf  ClusterNodeCust object in the pre-order traversal.
            Given the ``i``-th leaf node in the pre-order traversal ``n[i]``,
            the result of ``func(n[i])`` is stored in ``L[i]``. If not
            provided, the index of the original observation to which the node
            corresponds is used.
        Returns
        -------
        L : list
            The pre-order traversal.
        """
        # Do a preorder traversal, caching the result. To avoid having to do
        # recursion, we'll store the previous index we've visited in a vector.
        n = self.count

        curNode = [None] * (2 * n)
        lvisited = set()
        rvisited = set()
        curNode[0] = self
        k = 0
        preorder = []
        while k >= 0:
            nd = curNode[k]
            ndid = nd.id
            if nd.is_leaf():
                preorder.append(func(nd))
                k = k - 1
            else:
                if ndid not in lvisited:
                    curNode[k + 1] = nd.left
                    lvisited.add(ndid)
                    k = k + 1
                elif ndid not in rvisited:
                    curNode[k + 1] = nd.right
                    rvisited.add(ndid)
                    k = k + 1
                # If we've visited the left and right of this non-leaf
                # node already, go up in the tree.
                else:
                    k = k - 1

        return preorder



def bottom_up_cluster_tree(Z,ellabel):
    """
    Return clustering nodes in bottom-up order by distance.
    Parameters
    ----------
    Z : scipy.cluster.linkage array
        The linkage matrix.
    Returns
    -------
    nodes : list
        A list of ClusterNode objects.
    """
    q = deque()
    tree = to_tree_labeled(Z,ellabel)
    q.append(tree)
    nodes = []

    while q:
        node = q.popleft()
        if not node.is_leaf():
            bisect.insort_left(nodes, node)
            q.append(node.get_right())
            q.append(node.get_left())
    return nodes


#        clusters = {}
#        for i, el in enumerate(Z):
#          if el[0] <= len(lk):
#            # if it is an original point read it from the centers array
#            idx=int(el[0]) - 1
#            a = label[idx+1]
#          else:
#             # other wise read the cluster that has been created
#             idx=int(el[0])
#             a = clusters[idx]
#          if el[1] <= len(lk):
#            idx=int(el[1]) - 1
#            b = label[idx+1]
#          else:
#            b = clusters[int(el[1])]
#         # the clusters are 1-indexed by scipy
#          clusters[1 + i + len(lk)] = {'children' : [a, b]}



def to_tree_labeled(Z, ellabel, rd=False):
    """
    Converts a hierarchical clustering encoded in the matrix ``Z`` (by
    linkage) into an easy-to-use tree object.
    The reference r to the root  ClusterNodeCust object is returned.
    Each  ClusterNodeCust object has a left, right, dist, id, and count
    attribute. The left and right attributes point to  ClusterNodeCust objects
    that were combined to generate the cluster. If both are None then
    the  ClusterNodeCust object is a leaf node, its count must be 1, and its
    distance is meaningless but set to 0.
    Note: This function is provided for the convenience of the library
    user.  ClusterNodeCusts are not used as input to any of the functions in this
    library.
    Parameters
    ----------
    Z : ndarray
        The linkage matrix in proper form (see the ``linkage``
        function documentation).
    rd : bool, optional
        When False, a reference to the root  ClusterNodeCust object is
        returned.  Otherwise, a tuple (r,d) is returned. ``r`` is a
        reference to the root node while ``d`` is a dictionary
        mapping cluster ids to  ClusterNodeCust references. If a cluster id is
        less than n, then it corresponds to a singleton cluster
        (leaf node). See ``linkage`` for more information on the
        assignment of cluster ids to clusters.
    Returns
    -------
    L : list
        The pre-order traversal.
    """
    Z = np.asarray(Z, order='c')
    is_valid_linkage(Z, throw=True, name='Z')

    # Number of original objects is equal to the number of rows minus 1.
    n = Z.shape[0] + 1

    # Create a list full of None's to store the node objects
    d = [None] * (n * 2 - 1)

    # Create the nodes corresponding to the n original objects.
    for i in range(0, n):
        label=  str(ellabel[i])
        d[i] =  ClusterNodeCust(label, i)

    nd = None

    for i in range(0, n - 1):
        fi = int(Z[i, 0])
        fj = int(Z[i, 1])
        if fi > i + n:
            raise ValueError(('Corrupt matrix Z. Index to derivative cluster '
                              'is used before it is formed. See row %d, '
                              'column 0') % fi)
        if fj > i + n:
            raise ValueError(('Corrupt matrix Z. Index to derivative cluster '
                              'is used before it is formed. See row %d, '
                              'column 1') % fj)
        label="cluster_"+str(i + n)
        nd =  ClusterNodeCust(label, i + n, d[fi], d[fj], Z[i, 2])
        #          ^ id   ^ left ^ right ^ dist
        if Z[i, 3] != nd.count:
            raise ValueError(('Corrupt matrix Z. The count Z[%d,3] is '
                              'incorrect.') % i)
        d[n + i] = nd

    if rd:
        return (nd, d)
    else:
        return nd



