import sqlite3
import networkx as nx
import matplotlib.pyplot as plt

# Connect to the database
conn = sqlite3.connect("hr")
cursor = conn.cursor()

# Query the schema to get a list of tables and their columns
cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

# Create a graph representation of the tables and their relationships
G = nx.Graph()
for table_name, sql in tables:
    G.add_node(table_name)
    for column in sql.split(","):
        if "FOREIGN KEY" in column:
            # Extract the table and column names from the foreign key constraint
            _, fk_table, fk_column, _, _, pk_table, pk_column = column.split()
            # Add an edge between the two tables
            G.add_edge(fk_table, pk_table)

# Visualize the graph using Matplotlib
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_size=16, node_size=1000)
plt.show()
