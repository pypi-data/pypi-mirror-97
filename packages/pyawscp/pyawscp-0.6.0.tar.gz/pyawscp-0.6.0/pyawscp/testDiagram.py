from diagrams import Diagram, Edge, Node, Cluster
from diagrams.custom import Custom
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.network import VPC
from diagrams.aws.network import PublicSubnet
from diagrams.aws.network import PrivateSubnet


shapes         = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"]
num_shapes     = len(shapes)
shapes_per_row = 5
num_of_rows    = int(num_shapes / shapes_per_row) + (num_shapes % shapes_per_row > 0)

with Diagram("Diagram", show=False) as test2:
    with Cluster("vpc"):
        with Cluster("subnet"):
            for row in range(num_of_rows)[::-1]:
                items_in_row = shapes_per_row - (row+1) * shapes_per_row // num_shapes
                shapes_i = row * shapes_per_row
                node_list = ['EC2(\'' + shapes[shapes_i+item_num] + '\') - Edge(penwidth="0.0")'
                    for item_num in range(items_in_row)[:-1]
                ] + ['EC2(\'' + shapes[shapes_i+items_in_row-1] + '\')']

                node_row = "-".join(node_list)
                eval(node_row)

test2

