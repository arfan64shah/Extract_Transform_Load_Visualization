from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph

#create a diagram for all the tables
graph = create_schema_graph(metadata=MetaData('sqlite:///hr'),
                            show_datatypes=False,
                            show_indexes=False,
                            rankdir='LR',
                            concentrate=False 
                            )
graph.write_png('ER.png')