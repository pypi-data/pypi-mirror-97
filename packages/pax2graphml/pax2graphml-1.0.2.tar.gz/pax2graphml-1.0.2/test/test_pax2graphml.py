import logging
import os,sys
import json
import pax2graphml  as p2g


def main():
    #logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.basicConfig( level=logging.INFO)
    logging.info('Started')
    logging.info("resource_path:"+p2g.utils.resource_path())
    logging.info("data_path:"+p2g.utils.data_path())
    logging.info("GDIR:"+p2g.paxutils.gdir())
    biopax_file_1="test-data/ppara_neig_1.owl"
    graphml_file="test-data/ppara_neig_1.graphml"

    biopax_file_2="test-data/G6P_neig_1.owl"
    biopax_file_all="test-data/merged.owl"

    p2g.pax_import.biopax_to_reaction_graph(biopax_file_1,graphml_file)
    sys.exit()
    g=p2g.utils.loadGraph(graphml_file, directed=True)
    logging.info('-1-')
    nodes=p2g.node_list(g)
    for n in nodes:
             print("-n-"+str(n))    

    edges=p2g.edge_list(g)
    for n in edges:
             print("-e-"+str(n))    

    stat=p2g.graph_explore.compute_graph_metrics(g)

    logging.info(stat)

    logging.info('-2-')

    p2g.merge([ biopax_file_1 ,biopax_file_2 ] , biopax_file_all)  

    logging.info('start iter')
    sys.exit()

if __name__ == '__main__':
    main()


"""

#two BIOPAX data source files can be merged:

p2g.merge([ "biopax1 .owl" , "biopax2 .owl" ] , "merged.owl")


# then a SPAIM following can be produced:
p2g. convertSpaim("merged.owl" , "spaim . graphml")
# then topological metrics computes : \ newline

m=p2g.compute_graph_metrics("spaim. graphml")


#and an efficient graph traversal is performed : \ newline

iter=p2g.depthFirstNodeIterator("spaim . graphml")

#[...]
# we draw the graph
g=p2g. defineGraphModel("spaim . graphml")
p2g.draw(g, "graph .png"


"""
