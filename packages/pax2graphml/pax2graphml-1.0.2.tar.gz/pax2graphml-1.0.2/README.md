# PAX2GraphML 

## Features

PAX2GraphML is   dedicated to design biological reaction graph analysis softwares.

The package PAX2GraphML  allows to efficiently  manipulate   BioPAX data sources transformed as GRAPHML files.

It is expecially design  around the SPAIM reaction model (Substrate, Product, Activator, Inhibitor, Modulator). Among other things, it allows to  analyze the graphs, to extract sub-components and to build an influence graph.
Input graphs are in .graphml format, assumed under the SPAIM model.




##### Documentation


The package relies mainly on the python graph_tool module to extract, manipulate and save these graphs: https://graph-tool.skewed.de/static/doc/quickstart.html. 

Java is as well necessary for some sub-modules, like for BIOPAX export features.

the full documentation is available at  [https://fjrmoreews.github.io/pax2graphml/](https://fjrmoreews.github.io/pax2graphml/)

##### Installation

We provide a easy to use docker installation and a Debian/Ubuntu installation tutorial and a jupyter lab notebook with live examples.
 

The docker container provides the necessary environment to run the package (mainly, installation of python3 and graph_tool java and paxtools).

See   [https://gitlab.inria.fr/fmoreews/pax2graphml](https://gitlab.inria.fr/fmoreews/pax2graphml) for full installation instructions.



### Source repository

The sources are available at  [https://gitlab.inria.fr/fmoreews/pax2graphml](https://gitlab.inria.fr/fmoreews/pax2graphml)


