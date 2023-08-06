from diagrams import Cluster, Edge, Node, Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.network import VPC
from diagrams.aws.network import PublicSubnet
from diagrams.aws.network import PrivateSubnet
from pyawscp.Utils import Utils, Style
from pyawscp.PyEc2Cp import PyEc2CP
from pyawscp.PyS3Cp import PyS3CP
from pyawscp.Config import Config

class DiagramMgnt:

    def __init__(self, config):
        self.config = config
        """ with Diagram("listEc2", show=False):
             for idx_row, row in enumerate(self.content):
                 for idx_col, val in enumerate(row):
                     ELB(val) """
    
    def diagramVpcEc2(self):
        self.config.commandArguments = "sort9,vpc,subnet"
        pyEc2Cp = PyEc2CP(self.config)
        report, content = pyEc2Cp.listEc2()
        if content:
            EC2_INST_COL       = 1
            EC2_NAME_COL       = 2
            EC2_TYPE_COL       = 3
            EC2_LAUNCHTIME_COL = 4
            EC2_PRIVATEIP_COL  = 5
            EC2_PUBLICIP_COL   = 6
            EC2_STATE_COL      = 7
            VPC_COL            = 8
            SUBNET_COL         = 9

            data = {}
            for idx_row, row in enumerate(content):
                for idx_col, col in enumerate(row):
                    if idx_col == VPC_COL:
                       vpc = row[VPC_COL]
                data[vpc] = {}
            
            for idx_row, row in enumerate(content):
                for idx_col, col in enumerate(row):
                    if idx_col == VPC_COL:
                       vpc = row[VPC_COL]
                    if idx_col == SUBNET_COL:
                       subnet = row[SUBNET_COL]   
                data[vpc][subnet] = {}
            
            for idx_row, row in enumerate(content):
                for idx_col, col in enumerate(row):
                    if idx_col == VPC_COL:
                       vpc = row[VPC_COL]
                    if idx_col == SUBNET_COL:
                       subnet = row[SUBNET_COL]   
                    if idx_col == EC2_INST_COL:
                       instanceId = row[EC2_INST_COL]
                    if idx_col == EC2_NAME_COL:
                       name = row[EC2_NAME_COL]
                    if idx_col == EC2_TYPE_COL:
                       type = row[EC2_TYPE_COL]
                    if idx_col == EC2_PRIVATEIP_COL:
                       privateIp = row[EC2_PRIVATEIP_COL]
                    if idx_col == EC2_PUBLICIP_COL:
                       publicIp = row[EC2_PUBLICIP_COL]
                    if idx_col == EC2_STATE_COL:
                       state = row[EC2_STATE_COL]

                data[vpc][subnet][instanceId] = {
                    "Name": name,"Type": type, "PrivateIp": privateIp, "PublicIp": publicIp, "State": state
                }

            
            with Diagram("ListEc2", show=False, direction="TB") as builtDiagram:
                for vpc in data:
                    with Cluster(vpc):
                        for subnet in data[vpc]:
                            with Cluster(subnet):

                                ec2s = []
                                for ec2 in data[vpc][subnet]:
                                    ec2s.append(ec2)

                                cols       = 4
                                numberEc2s = len(ec2s)
                                rows       =  numberEc2s // cols
                                if (numberEc2s / cols) > (numberEc2s // cols):
                                   rows += 1
                                
                                index = 0
                                for row in range(rows):
                                    for col in range(cols):
                                        index += 1
                                        if index < len(ec2s):
                                            
                                           EC2(ec2s[index-1])
                                           
                                    
                                
                                

            
            #  with Diagram("ListEc2", show=False, direction="TB") as builtDiagram:
            #     for vpc in data:
            #         with Cluster(vpc):

            #             for subnet in data[vpc]:
            #                 with Cluster(subnet):

            #                     ec2s = []
            #                     for ec2 in data[vpc][subnet]:
            #                         ec2s.append(ec2)

            #                     print(vpc)
            #                     print(subnet)
            #                     print(ec2s)   
            #                     print("-------------------------")

            #                     shapes         = ec2s
            #                     num_shapes     = len(shapes)
            #                     shapes_per_row = 3
            #                     num_of_rows    = int(num_shapes / shapes_per_row) + (num_shapes % shapes_per_row > 0)

            #                     for row in range(num_of_rows)[::-1]:
            #                         items_in_row = shapes_per_row - (row+1) * shapes_per_row // num_shapes
            #                         shapes_i = row * shapes_per_row
            #                         node_list = ['EC2(\'' + shapes[shapes_i+item_num] + '\') - Edge(penwidth="0.0")'
            #                              for item_num in range(items_in_row)[:-1]
            #                         ] + ['EC2(\'' + shapes[shapes_i+items_in_row-1] + '\')']

            #                         print(node_list)

            #                         node_row = "-".join(node_list)
            #                         eval(node_row)
                                

# ['EC2(\'i-00b634c2643283086\') - Edge(penwidth="0.0")', "EC2('i-0996ac119c6ee0895')"]
# ['EC2(\'i-0becc277226e2053d\') - Edge(penwidth="0.0")', 'EC2(\'i-07ba3f05755dc725d\') - Edge(penwidth="0.0")', "EC2('i-0c7724d072ba3a1b4')"]
# ['EC2(\'i-0194df0d6a568fb7d\') - Edge(penwidth="0.0")', 'EC2(\'i-0fe280bce8efcda6d\') - Edge(penwidth="0.0")', "EC2('i-044aeb4b11e8901c5')"]
# ['EC2(\'i-04afcb7171c79b2d5\') - Edge(penwidth="0.0")', 'EC2(\'i-0ec5dce0be7aabdc7\') - Edge(penwidth="0.0")', "EC2('i-0ae56529c226e4c62')"]

                                   
            # builtDiagram

            # with Diagram("ListEc2", show=False, direction="TB"):
            #     for vpc in data:
            #         with Cluster(vpc):
            #             for subnet in data[vpc]:
            #                 with Cluster(subnet):
            #                     for ec2 in data[vpc][subnet]:
            #                         EC2(ec2) 
        else:
            print("No Content to Diagram!")
    
        


