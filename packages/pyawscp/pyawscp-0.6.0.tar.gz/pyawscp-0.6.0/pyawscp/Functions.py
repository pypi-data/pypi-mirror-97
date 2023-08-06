#from pyawscp.Utils import Style
from .Utils import Style

class Functions:

    ROLE_LOGOFF                  = "roleLogoff"
    ROLE_INFO                    = "roleInfo"
    SUBNET_IS_PUBLIC             = "subnetIsPublic"
    LIST_SUBNETS_VPC             = "listSubnetsVpc"
    LIST_VPC                     = "listVpc"
    LIST_SG                      = "listSgs"
    LIST_TARGET_GROUPS           = "listTargetGroups"
    FIND_ELBS_EC2                = "findElbsEc2"
    LIST_EC2                     = "listEc2"
    LIST_ROUTE_TABLES            = "listRt"
    LIST_NACLS                   = "listNacls"
    LIST_BUCKETS_S3              = "listBucketsS3"
    LIST_OBJECTS_BUCKETS_S3      = "listObjectsBucketS3"
    LIST_UPLOADS_S3              = "listUploadsS3"
    ABORT_UPLOADS_S3             = "abortUploadsS3"
    TRANSFER_TO_S3               = "transferToS3"
    SHOW_TARGET_S3               = "showTargetsS3"
    SHOW_TARGET_UPLOADS_S3       = "showTargetUploadsS3"
    SHOW_TARGET_UPLOAD_PARTS_S3  = "showTargetUploadPartsS3"
    REMOVE_TARGET_HISTORY_S3     = "removeTargetHistoryS3"
    NSLOOKUP_EC2_R53             = "nslookupEc2R53"
    AWS_NAVIGATOR                = "navigator"
    DRAW_NETWORKING              = "drawNetworking"
    S3_PRESIGNED_URL             = "s3PreSignedURL"
   
    excelFileDescription         = "Generate an Excel file from the result (saved at your home folder ~/)"
    verboseDescription           = "Show information in JSON format."
    saveDescription              = "Save the results to a JSON file."
    highLightDescription         = "Hightlight content using \"| {VALUE}\""
    filterDescription            = "Filter content using \"| grep {VALUE}\""

    ROLE_SESSION = "Session Role"
    NETWORKING   = "Networking"
    EC2          = "EC2"
    S3           = "S3"
    GENERAL      = "General"
    
    GROUPS = [NETWORKING, EC2, S3, GENERAL]

    FUNCTIONS = {
        SUBNET_IS_PUBLIC:{
            "group": NETWORKING,
            "name": "Subnet is Public",
            "description": "Check if the subnet is public looking for Route Tables with route 0.0.0.0/0 containing Internet Gateways (igw-*)",
            "arguments": [
                {"name": "{SUBNET_ID}","mandatory": True, "description": "Id of the Subnet","biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "subnetIsPublic " + Style.BLUE + "subnet-074a9ad8389a90bb8" + Style.RESET}
            ]
        },
        LIST_SUBNETS_VPC:{
            "group": NETWORKING,
            "name": "List Subnets VPC",
            "description": "List all Subnets of a VPC",
            "arguments": [
                {"name": "{VPC_ID}",           "mandatory": True,  "description": "Id of the VPC","biggerLabel": 20},
                {"name": "ispublic",           "mandatory": False, "description": "Add a column info showing if the subnet is Public","biggerLabel": 20},
                {"name": "sort{Column Number}","mandatory": False, "description": "Column number to sort the table result","biggerLabel": 20},
                {"name": "desc",               "mandatory": False, "description": "Do a desceding sort","biggerLabel": 20},
                {"name": "tags",               "mandatory": False, "description": "Tags to filter the resource (will be added to the Environment Tags set)","biggerLabel": 20},
                {"name": "showtags",           "mandatory": False, "description": "Add a column with all Tags of the Subnet.","biggerLabel": 20},
                {"name": "excel",              "mandatory": False, "description": excelFileDescription,"biggerLabel": 20},
                {"name": "verbose",            "mandatory": False, "description": verboseDescription,"biggerLabel": 20},
                {"name": "save",               "mandatory": False, "description": saveDescription,"biggerLabel": 20},
                {"name": "| {VALUE}",          "mandatory": False, "description": highLightDescription,"biggerLabel": 20},
                {"name": "| grep {VALUE}",     "mandatory": False, "description": filterDescription,"biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "listSubnetsVpc " + Style.BLUE + "vpc-050a1a1dccd178b9a" + Style.RESET},
                {"command":Style.GREEN + "listSubnetsVpc " + Style.BLUE + "vpc-050a1a1dccd178b9a,tags:Environment=production#Project=xpto" + Style.RESET},
                {"command":Style.GREEN + "listSubnetsVpc " + Style.BLUE + "vpc-050a1a1dccd178b9a,ispublic" + Style.RESET},
                {"command":Style.GREEN + "listSubnetsVpc " + Style.BLUE + "vpc-050a1a1dccd178b9a,sort3,desc" + Style.RESET},
                {"command":Style.GREEN + "listSubnetsVpc " + Style.BLUE + "vpc-050a1a1dccd178b9a,tag:Environment=production,sort3" + Style.RESET},
                {"command":Style.GREEN + "listSubnetsVpc " + Style.BLUE + "vpc-050a1a1dccd178b9a,ispublic" + Style.RESET},
                {"command":Style.GREEN + "listSubnetsVpc " + Style.BLUE + "vpc-050a1a1dccd178b9a,save" + Style.RESET}
            ]
        },
        LIST_VPC:{
            "group": NETWORKING,
            "name": "List VPCs",
            "description": "List all VPCs (and its subnets)",
            "arguments": [
                {"name": "subnets",            "mandatory": False, "description": "List all the subnets of the VPCs, grouping by VPC Id. Notice: the grouping will be disabled when sort/desc is requested.","biggerLabel": 20},
                {"name": "ispublic",           "mandatory": False, "description": "To use in conjunction with subnets, adding a column saying if the Subnet is public.","biggerLabel": 20},
                {"name": "drawio",             "mandatory": False, "description": "Generates a CSV file Diagram with only the VPCs to be imported into DrawIo / app.diagrams.net ( Go to: Arrange -> Insert -> Advanced -> CSV). The CSV will be at you user's home folder","biggerLabel": 20},
                {"name": "sort{Column Number}","mandatory": False, "description": "Column number to sort the table result","biggerLabel": 20},
                {"name": "desc",               "mandatory": False, "description": "Do a desceding sort","biggerLabel": 20},
                {"name": "tags",               "mandatory": False, "description": "Tags to filter the resource (will be added to the Environment Tags set)","biggerLabel": 20},
                {"name": "showtags",           "mandatory": False, "description": "Add a column with all Tags of the VPC.","biggerLabel": 20},
                {"name": "excel",              "mandatory": False, "description": excelFileDescription,"biggerLabel": 20},
                {"name": "verbose",            "mandatory": False, "description": verboseDescription,"biggerLabel": 20},
                {"name": "save",               "mandatory": False, "description": saveDescription,"biggerLabel": 20},
                {"name": "| {VALUE}",          "mandatory": False, "description": highLightDescription,"biggerLabel": 20},
                {"name": "| grep {VALUE}",     "mandatory": False, "description": filterDescription,"biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "listVpc " + Style.RESET},
                {"command":Style.GREEN + "listVpc " + Style.BLUE + "tags:Environment=production#Project=xpto" + Style.RESET},
                {"command":Style.GREEN + "listVpc " + Style.BLUE + "subnets" + Style.RESET},
                {"command":Style.GREEN + "listVpc " + Style.BLUE + "subnets,ispublic" + Style.RESET},
                {"command":Style.GREEN + "listVpc " + Style.BLUE + "subnets,ispublic,showtags" + Style.RESET},
                {"command":Style.GREEN + "listVpc " + Style.BLUE + "sort1" + Style.RESET},
                {"command":Style.GREEN + "listVpc " + Style.BLUE + "sort3,desc" + Style.RESET}
            ]
        },
        LIST_SG:{
            "group": NETWORKING,
            "name": "List Security Groups",
            "description": "List all Security Groups",
            "arguments": [
                {"name": "list-associated",    "mandatory": False, "description": "List the ENIs of all the Resources(ELB,R53,RDS,EC2) associated with this Security Group.","biggerLabel": 20},
                {"name": "list-permissions",   "mandatory": False, "description": "List the Inbound and Outbound rules","biggerLabel": 20},
                {"name": "sort{Column Number}","mandatory": False, "description": "Column number to sort the table result","biggerLabel": 20},
                {"name": "desc",               "mandatory": False, "description": "Do a desceding sort","biggerLabel": 20},
                {"name": "tags",               "mandatory": False, "description": "Tags to filter the resource (will be added to the Environment Tags set)","biggerLabel": 20},
                {"name": "showtags",           "mandatory": False, "description": "Add a column with all Tags of the VPC.","biggerLabel": 20},
                {"name": "excel",              "mandatory": False, "description": excelFileDescription,"biggerLabel": 20},
                {"name": "verbose",            "mandatory": False, "description": verboseDescription,"biggerLabel": 20},
                {"name": "save",               "mandatory": False, "description": saveDescription,"biggerLabel": 20},
                {"name": "| {VALUE}",          "mandatory": False, "description": highLightDescription,"biggerLabel": 20},
                {"name": "| grep {VALUE}",     "mandatory": False, "description": filterDescription,"biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "listSg " + Style.RESET},
                {"command":Style.GREEN + "listSg " + Style.BLUE + "list-associated" + Style.RESET},
                {"command":Style.GREEN + "listSg " + Style.BLUE + "list-associated,list-permissions" + Style.RESET},
                {"command":Style.GREEN + "listSg " + Style.BLUE + "list-permissions" + Style.RESET},
                {"command":Style.GREEN + "listSg " + Style.BLUE + "sort1" + Style.RESET},
                {"command":Style.GREEN + "listSg " + Style.BLUE + "sort3,desc" + Style.RESET}
            ]
        },
        LIST_ROUTE_TABLES:{
            "group": NETWORKING,
            "name": "List Route Tables",
            "description": "List all Route Tables",
            "arguments": [
                {"name": "show-routes",        "mandatory": False, "description": "Add a column with all Routes register for this Route Table","biggerLabel": 20},
                {"name": "drawio",             "mandatory": False, "description": "Generates a CSV file Diagram to be imported into DrawIo / app.diagrams.net ( Go to: Arrange -> Insert -> Advanced -> CSV). The CSV will be at you user's home folder","biggerLabel": 20},
                {"name": "sort{Column Number}","mandatory": False, "description": "Column number to sort the table result","biggerLabel": 20},
                {"name": "desc",               "mandatory": False, "description": "Do a desceding sort","biggerLabel": 20},
                {"name": "tags",               "mandatory": False, "description": "Tags to filter the resource (will be added to the Environment Tags set)","biggerLabel": 20},
                {"name": "showtags",           "mandatory": False, "description": "Add a column with all Tags of the VPC.","biggerLabel": 20},
                {"name": "excel",              "mandatory": False, "description": excelFileDescription,"biggerLabel": 20},
                {"name": "verbose",            "mandatory": False, "description": verboseDescription,"biggerLabel": 20},
                {"name": "save",               "mandatory": False, "description": saveDescription,"biggerLabel": 20},
                {"name": "| {VALUE}",          "mandatory": False, "description": highLightDescription,"biggerLabel": 20},
                {"name": "| grep {VALUE}",     "mandatory": False, "description": filterDescription,"biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "listRt " + Style.RESET},
                {"command":Style.GREEN + "listRt " + Style.BLUE + "show-routes" + Style.RESET},
                {"command":Style.GREEN + "listRt " + Style.BLUE + "show-routes,drawio" + Style.RESET},
                {"command":Style.GREEN + "listRt " + Style.BLUE + "showtags" + Style.RESET},
                {"command":Style.GREEN + "listRt " + Style.BLUE + "sort1" + Style.RESET},
                {"command":Style.GREEN + "listRt " + Style.BLUE + "sort3,desc" + Style.RESET}
            ]
        },
        LIST_NACLS:{
            "group": NETWORKING,
            "name": "List Network Access Control List",
            "description": "List all Network Access Control List",
            "arguments": [
                {"name": "show-entries",       "mandatory": False, "description": "Add a column with all Entries register for this NACL","biggerLabel": 20},
                {"name": "drawio",             "mandatory": False, "description": "Generates a CSV file Diagram to be imported into DrawIo / app.diagrams.net ( Go to: Arrange -> Insert -> Advanced -> CSV). The CSV will be at you user's home folder","biggerLabel": 20},
                {"name": "sort{Column Number}","mandatory": False, "description": "Column number to sort the table result","biggerLabel": 20},
                {"name": "desc",               "mandatory": False, "description": "Do a desceding sort","biggerLabel": 20},
                {"name": "tags",               "mandatory": False, "description": "Tags to filter the resource (will be added to the Environment Tags set)","biggerLabel": 20},
                {"name": "showtags",           "mandatory": False, "description": "Add a column with all Tags of the VPC.","biggerLabel": 20},
                {"name": "excel",              "mandatory": False, "description": excelFileDescription,"biggerLabel": 20},
                {"name": "verbose",            "mandatory": False, "description": verboseDescription,"biggerLabel": 20},
                {"name": "save",               "mandatory": False, "description": saveDescription,"biggerLabel": 20},
                {"name": "| {VALUE}",          "mandatory": False, "description": highLightDescription,"biggerLabel": 20},
                {"name": "| grep {VALUE}",     "mandatory": False, "description": filterDescription,"biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "listNacls " + Style.RESET},
                {"command":Style.GREEN + "listNacls " + Style.BLUE + "show-routes" + Style.RESET},
                {"command":Style.GREEN + "listNacls " + Style.BLUE + "showtags" + Style.RESET},
                {"command":Style.GREEN + "listNacls " + Style.BLUE + "sort1" + Style.RESET},
                {"command":Style.GREEN + "listNacls " + Style.BLUE + "sort3,desc" + Style.RESET}
            ]
        },
        LIST_TARGET_GROUPS:{
            "group": NETWORKING,
            "name": "List Target Groups",
            "description": "List all the Target Groups",
            "arguments": [
                {"name": "Target Groups ARN",  "mandatory": False, "description": "List only the requested Target Groups, to pass more than one use \";\" to separate them. This argument is exclusive with Load Balancer option, it will overwrite it if both were chosen.","biggerLabel": 20},
                {"name": "Load Balancer ARN",  "mandatory": False, "description": "List all the Target Groups associated with the requested Load Balancer.","biggerLabel": 20},
                {"name": "health",             "mandatory": False, "description": "Add the columns of Health Check. Notice! This might exceed the horizontal width of the Terminal Window.","biggerLabel": 20},
                {"name": "tgarn",              "mandatory": False, "description": "Show the Target Groups ARN, otherwise will show only the name.","biggerLabel": 20},
                {"name": "elbarn",             "mandatory": False, "description": "Add a column with the complete ELB ARN, other just the name will be presented.","biggerLabel": 20},
                {"name": "sort{Column Number}","mandatory": False, "description": "Column number to sort the table result","biggerLabel": 20},
                {"name": "desc",               "mandatory": False, "description": "Do a desceding sort","biggerLabel": 20},
                {"name": "excel",              "mandatory": False, "description": excelFileDescription,"biggerLabel": 20},
                {"name": "verbose",            "mandatory": False, "description": verboseDescription,"biggerLabel": 20},
                {"name": "save",               "mandatory": False, "description": saveDescription,"biggerLabel": 20},
                {"name": "| {VALUE}",          "mandatory": False, "description": highLightDescription,"biggerLabel": 20},
                {"name": "| grep {VALUE}",     "mandatory": False, "description": filterDescription,"biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "listTargetGroups " + Style.RESET},
                {"command":Style.GREEN + "listTargetGroups " + Style.BLUE + " arn:aws:elb:xxx:123456:loadbalancer/app/LB-Gandalf" + Style.RESET},
                {"command":Style.GREEN + "listTargetGroups " + Style.BLUE + " arn:aws:elb:xxx:123456:targetgroup/app/TG-Frodo" + Style.RESET},
                {"command":Style.GREEN + "listTargetGroups " + Style.BLUE + " arn:aws:elb:xxx:123456:targetgroup/app/TG-Frodo;\n                                 arn:aws:elb:xxx:123456:targetgroup/app/TG-Sam" + Style.RESET},
                {"command":Style.GREEN + "listTargetGroups " + Style.BLUE + " arn:aws:elb:xxx:123456:loadbalancer/app/LB-Gandal,\n                                 health" + Style.RESET},
                {"command":Style.GREEN + "listTargetGroups " + Style.BLUE + " arn:aws:elb:xxx:123456:loadbalancer/app/LB-Gandal,\n                                 health,sort1" + Style.RESET},
                {"command":Style.GREEN + "listTargetGroups " + Style.BLUE + " sort3,desc" + Style.RESET},
                {"command":Style.GREEN + "listTargetGroups " + Style.BLUE + " | production" + Style.RESET}
            ]
        },
        FIND_ELBS_EC2:{
            "group": NETWORKING,
            "name": "Find ELBs targeting/pointing to a specific EC2 Instance",
            "description": "Find Load Balancers and Target Groups pointing to a specific EC2 Instance",
            "arguments": [
                {"name": "EC2 Instance Id",    "mandatory": True,  "description": "EC2 Instance Id that the Load Balancers are pointing to.","biggerLabel": 20},
                {"name": "elbarn",             "mandatory": False, "description": "Shoe the Load Balance ARN, otherwise will show the name.","biggerLabel": 20},
                {"name": "tgarn",              "mandatory": False, "description": "Show the Target Groups ARN, otherwise will show the name.","biggerLabel": 20},
                {"name": "sort{Column Number}","mandatory": False, "description": "Column number to sort the table result","biggerLabel": 20},
                {"name": "desc",               "mandatory": False, "description": "Do a desceding sort","biggerLabel": 20},
                {"name": "excel",              "mandatory": False, "description": excelFileDescription,"biggerLabel": 20},
                {"name": "verbose",            "mandatory": False, "description": verboseDescription,"biggerLabel": 20},
                {"name": "save",               "mandatory": False, "description": saveDescription,"biggerLabel": 20},
                {"name": "| {VALUE}",          "mandatory": False, "description": highLightDescription,"biggerLabel": 20},
                {"name": "| grep {VALUE}",     "mandatory": False, "description": filterDescription,"biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "findElbsEc2 " + Style.RESET},
                {"command":Style.GREEN + "findElbsEc2 " + Style.BLUE + " i-0361f6405c08923b6" + Style.RESET},
                {"command":Style.GREEN + "findElbsEc2 " + Style.BLUE + " i-0361f6405c08923b6,elbarn" + Style.RESET},
                {"command":Style.GREEN + "findElbsEc2 " + Style.BLUE + " i-0361f6405c08923b6,sort3,desc" + Style.RESET}
            ]
        },
        NSLOOKUP_EC2_R53:{
            "group": NETWORKING,
            "name": "Describe route from a DNS Domain to EC2 Instances",
            "description": "From a DNS domain, since Route 53, it will query and describe the route path all the day down to an EC2 Instance/IP",
            "arguments": [
                {"name": "{DNS}",              "mandatory": True,  "description": "DNS to describe the path","biggerLabel": 20},
                {"name": "thin",               "mandatory": False, "description": "Present less information, a summary form","biggerLabel": 20},
                {"name": "graph",              "mandatory": False, "description": "Generates a graph and opens in a browser","biggerLabel": 20},
                {"name": "verbose",            "mandatory": False, "description": verboseDescription,"biggerLabel": 20},
                {"name": "save",               "mandatory": False, "description": saveDescription,"biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "nslookupEc2R53 " + Style.BLUE + " prd.jenkins.mycompany.com" + Style.RESET},
                {"command":Style.GREEN + "nslookupEc2R53 " + Style.BLUE + " prd.jenkins.mycompany.com,thin" + Style.RESET},
                {"command":Style.GREEN + "nslookupEc2R53 " + Style.BLUE + " prd.jenkins.mycompany.com,thin,save" + Style.RESET},
                {"command":Style.GREEN + "nslookupEc2R53 " + Style.BLUE + " prd.jenkins.mycompany.com,save,verbose" + Style.RESET}
            ]
        },
        LIST_EC2:{
            "group": EC2,
            "name": "List EC2 Instances",
            "description": "List EC2s Instances",
            "arguments": [
                {"name": "{INSTANCE ID}",      "mandatory": False, "description": "Filter with theInstance Id  requested, otherwise all will be listed","biggerLabel": 20},
                {"name": "{PRIVATE IP}",       "mandatory": False, "description": "Filter with the Private IP requested, otherwise all will be listed","biggerLabel": 20},
                {"name": "{VPC ID}",           "mandatory": False, "description": "Filter with the VPC Id requested, otherwise all will be listed","biggerLabel": 20},
                {"name": "{SUBNET ID}",        "mandatory": False, "description": "Filter with the Subnet Id requested, otherwise all will be listed","biggerLabel": 20},

                {"name": "sg",                 "mandatory": False, "description": "Add a column with the Security Groups associated to the EC2 Instance","biggerLabel": 20},
                {"name": "vpc",                "mandatory": False, "description": "Add a column with the VPC Id where the EC2 Instance is located","biggerLabel": 20},
                {"name": "subnet",             "mandatory": False, "description": "Add a column with the Subnet Id where the EC2 Instance is located","biggerLabel": 20},
                {"name": "image",              "mandatory": False, "description": "Add a column with the Image Id of the EC2 Instance","biggerLabel": 20},
                {"name": "cpu",                "mandatory": False, "description": "Add a column with the information of EC2 Instance CPU Options","biggerLabel": 20},
                {"name": "noname",             "mandatory": False, "description": "Remove the column name information of EC2 Instance","biggerLabel": 20},

                {"name": "sort{Column Number}","mandatory": False, "description": "Column number to sort the table result","biggerLabel": 20},
                {"name": "desc",               "mandatory": False, "description": "Do a desceding sort","biggerLabel": 20},
                {"name": "tags",               "mandatory": False, "description": "Tags to filter the resource (will be added to the Environment Tags set)","biggerLabel": 20},
                {"name": "showtags",           "mandatory": False, "description": "Add a column with all Tags of the VPC.","biggerLabel": 20},
                {"name": "excel",              "mandatory": False, "description": excelFileDescription,"biggerLabel": 20},
                {"name": "verbose",            "mandatory": False, "description": verboseDescription,"biggerLabel": 20},
                {"name": "save",               "mandatory": False, "description": saveDescription,"biggerLabel": 20},
                {"name": "| {VALUE}",          "mandatory": False, "description": highLightDescription,"biggerLabel": 20},
                {"name": "| grep {VALUE}",     "mandatory": False, "description": filterDescription,"biggerLabel": 20}

            ],
            "examples-interactive": [
                {"command":Style.GREEN + "listEc2 " + Style.RESET},
                {"command":Style.GREEN + "listEc2 " + Style.BLUE + "i-0902ce6ab97baa8e7" + Style.RESET},
                {"command":Style.GREEN + "listEc2 " + Style.BLUE + "i-0bbb04a9cd37a4675,showtags" + Style.RESET},
                {"command":Style.GREEN + "listEc2 " + Style.BLUE + "10.115.201.1" + Style.RESET},
                {"command":Style.GREEN + "listEc2 " + Style.BLUE + "172.168.239.33,showtags" + Style.RESET},
                {"command":Style.GREEN + "listEc2 " + Style.BLUE + "tags:Environment=production#Project=xpto" + Style.RESET},
                {"command":Style.GREEN + "listEc2 " + Style.BLUE + "showtags" + Style.RESET},
                {"command":Style.GREEN + "listEc2 " + Style.BLUE + "sort1" + Style.RESET},
                {"command":Style.GREEN + "listEc2 " + Style.BLUE + "sort3,desc" + Style.RESET}
            ]
        },
        LIST_UPLOADS_S3:{
            "group": S3,
            "name": "List Uploads that did not finished yet",
            "description": "List Uploads that did not finished yet, known as MultiPart Uploads",
            "arguments": [
                {"name": "{BUCKET}",           "mandatory": True,  "description": "Name of the bucket","biggerLabel": 20},
                {"name": "excel",              "mandatory": False, "description": excelFileDescription,"biggerLabel": 20},
                {"name": "verbose",            "mandatory": False, "description": verboseDescription,"biggerLabel": 20},
                {"name": "save",               "mandatory": False, "description": saveDescription,"biggerLabel": 20},
                {"name": "| {VALUE}",          "mandatory": False, "description": highLightDescription,"biggerLabel": 20},
                {"name": "| grep {VALUE}",     "mandatory": False, "description": filterDescription,"biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "listUploadsS3 " + Style.BLUE + " bucketName" + Style.RESET},
                {"command":Style.GREEN + "listUploadsS3 " + Style.BLUE + " bucketName/key1/" + Style.RESET},
                {"command":Style.GREEN + "listUploadsS3 " + Style.BLUE + " bucketName/key1/key2/" + Style.RESET},
                
            ]
        },
        ABORT_UPLOADS_S3:{
            "group": S3,
            "name": "Abort Uploads that did not finished yet",
            "description": "Abort Uploads that did not finished yet, known as MultiPart Uploads",
            "arguments": [
                {"name": "{BUCKET}",           "mandatory": True,  "description": "Name of the bucket","biggerLabel": 20},
                {"name": "verbose",            "mandatory": False, "description": verboseDescription,"biggerLabel": 20},
                {"name": "save",               "mandatory": False, "description": saveDescription,"biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "abortUploadsS3 " + Style.BLUE + " bucketName" + Style.RESET}
            ]
        },
        TRANSFER_TO_S3:{
            "group": S3,
            "name": "Upload files/folder to a Bucket S3",
            "description": "Upload files/folder to a Bucket S3 using the MultiPart Uploads (can be resumed in case drop in the middle of the process)",
            "arguments": [
                {"name": "{BUCKET}",           "mandatory": True, "description": "Name of the bucket to receive the content","biggerLabel": 20},
                {"name": "{FILE|FOLDER}",      "mandatory": True, "description": "The file or folder to be uploaded","biggerLabel": 20},
                {"name": "recursive",          "mandatory": False,"description": "In case a folder, the copy will be recursive (all subfolders)","biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "transferToS3 " + Style.BLUE + " bucketName,c:\\MyFiles\\logs-armagedon.tar.gz" + Style.RESET},
                {"command":Style.GREEN + "transferToS3 " + Style.BLUE + " bucketName,c:\\MyFiles" + Style.RESET},
                {"command":Style.GREEN + "transferToS3 " + Style.BLUE + " bucketName,c:\\MyFiles,recursive" + Style.RESET},
                {"command":Style.GREEN + "transferToS3 " + Style.BLUE + " iron-maiden,~/Downloads/repo-com.tar.gz" + Style.RESET},
                {"command":Style.GREEN + "transferToS3 " + Style.BLUE + " iron-maiden,/home/ualter/Downloads/repo-com.tar.gz" + Style.RESET},
                {"command":Style.GREEN + "transferToS3 " + Style.BLUE + " iron-maiden,/home/ualter/Downloads,recursive" + Style.RESET}
            ]
        },
        SHOW_TARGET_S3:{
            "group": S3,
            "name": "Show all the targets used for Uploads (files, folders) to S3",
            "description": "Show all history of files/folders (Targets) you have used to upload to S3",
            "arguments": [
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "showTargetsS3 " + Style.RESET}
            ]
        },
        SHOW_TARGET_UPLOADS_S3:{
            "group": S3,
            "name": "Show all uploads history of a target",
            "description": "List all uploads performed to a specific target (files/folder)",
            "arguments": [
                {"name": "{TARGET}",           "mandatory": True, "description": "Name of the target (File or Folder)","biggerLabel": 20},
                {"name": "showAll",            "mandatory": False,"description": "Verbose, list all the columns available","biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "showTargetUploadsS3 " + Style.BLUE + "d:\\Downloads\\repository.zip" + Style.RESET},
                {"command":Style.GREEN + "showTargetUploadsS3 " + Style.BLUE + "d:\\Downloads\\repository.zip,showAll" + Style.RESET},
                {"command":Style.GREEN + "showTargetUploadsS3 " + Style.BLUE + "d:\\MyFiles\\" + Style.RESET}
            ]
        },
        SHOW_TARGET_UPLOAD_PARTS_S3:{
            "group": S3,
            "name": "Show all parts of a Multipart Upload",
            "description": "List all parts of a performed Multipart Upload",
            "arguments": [
                {"name": "{TARGET}",           "mandatory": True, "description": "Name of the target (File or Folder)","biggerLabel": 20},
                {"name": "key",                "mandatory": True,"description": "Name of the file/key","biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "showTargetUploadPartsS3 " + Style.BLUE + "d:\\Downloads\\repository.zip,repository.zip" + Style.RESET},
                {"command":Style.GREEN + "showTargetUploadPartsS3 " + Style.BLUE + "d:\\Downloads\\,myFile.tar.gz" + Style.RESET}
            ]
        },
        REMOVE_TARGET_HISTORY_S3:{
            "group": S3,
            "name": "Delete the history of a target upload",
            "description": "Delete all the data of a target (File/folder) upload",
            "arguments": [
                {"name": "{TARGET}",           "mandatory": True, "description": "Name of the target (File or Folder)","biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "removeTargetHistoryS3 " + Style.BLUE + "d:\\Downloads\\repository.zip" + Style.RESET},
                {"command":Style.GREEN + "removeTargetHistoryS3 " + Style.BLUE + "d:\\Downloads\\" + Style.RESET}
            ]
        },
        LIST_BUCKETS_S3:{
            "group": S3,
            "name": "List all buckets",
            "description": "List all buckets",
            "arguments": [
                {"name": "csv",                "mandatory": False, "description": "Create a csv file with the results","biggerLabel": 20},
                {"name": "sort{Column Number}","mandatory": False, "description": "Column number to sort the table result","biggerLabel": 20},
                {"name": "desc",               "mandatory": False, "description": "Do a desceding sort","biggerLabel": 20},
                {"name": "excel",              "mandatory": False, "description": excelFileDescription,"biggerLabel": 20},
                {"name": "verbose",            "mandatory": False, "description": verboseDescription,"biggerLabel": 20},
                {"name": "save",               "mandatory": False, "description": saveDescription,"biggerLabel": 20},
                {"name": "| {VALUE}",          "mandatory": False, "description": highLightDescription,"biggerLabel": 20},
                {"name": "| grep {VALUE}",     "mandatory": False, "description": filterDescription,"biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "listBuckets " + Style.RESET},
                {"command":Style.GREEN + "listBuckets " + Style.BLUE + " sort3,desc" + Style.RESET}
            ]
        },
        LIST_OBJECTS_BUCKETS_S3:{
            "group": S3,
            "name": "List objects in a bucket",
            "description": "List objects in a bucket",
            "arguments": [
                {"name": "{BUCKET}",           "mandatory": True, "description": "Name of the bucket","biggerLabel": 20},
                {"name": "{BUCKET}/{PREFIX}",  "mandatory": False, "description": "Specify a prefix, works like a \"folder\" inside S3 Buckets. If finish with a / will list it" ,"biggerLabel": 20},
                {"name": "csv",                "mandatory": False, "description": "Create a csv file with the results","biggerLabel": 20},
                {"name": "excel",              "mandatory": False, "description": excelFileDescription,"biggerLabel": 20},
                {"name": "verbose",            "mandatory": False, "description": verboseDescription,"biggerLabel": 20},
                {"name": "save",               "mandatory": False, "description": saveDescription,"biggerLabel": 20},
                {"name": "sort{Column Number}","mandatory": False, "description": "Column number to sort the table result","biggerLabel": 20},
                {"name": "desc",               "mandatory": False, "description": "Do a desceding sort","biggerLabel": 20},
                {"name": "tags",               "mandatory": False, "description": "Tags to filter the resource (will be added to the Environment Tags set)","biggerLabel": 20},
                {"name": "showtags",           "mandatory": False, "description": "Add a column with all Tags of the VPC.","biggerLabel": 20},
                {"name": "| {VALUE}",          "mandatory": False, "description": highLightDescription,"biggerLabel": 20},
                {"name": "| grep {VALUE}",     "mandatory": False, "description": filterDescription,"biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "listObjectsBucketS3 " + Style.BLUE + " bucket_root" + Style.RESET},
                {"command":Style.GREEN + "listObjectsBucketS3 " + Style.BLUE + " bucket_root/folder1/" + Style.RESET},
                {"command":Style.GREEN + "listObjectsBucketS3 " + Style.BLUE + " bucket_root/folder1/folder2/" + Style.RESET},
                {"command":Style.GREEN + "listObjectsBucketS3 " + Style.BLUE + " production/logs/2019" + Style.RESET}
            ]
        },
        S3_PRESIGNED_URL:{
            "group": S3,
            "name": "Create a PreSigned URL",
            "description": "Create a PreSigned URL for an S3 Object",
            "arguments": [
                {"name": "{BUCKET}",           "mandatory": True, "description": "Name of the bucket","biggerLabel": 20},
                {"name": "{OBJECT}",           "mandatory": True, "description": "Name of the Object" ,"biggerLabel": 20},
                {"name": "verbose",            "mandatory": False, "description": "Get and show the object's content" ,"biggerLabel": 20},
                {"name": "{NUMBER}",           "mandatory": False, "description": "Expiration in seconds (min: 15 minutes, max: 7 days), default is 3600 secs (1h), if not informed" ,"biggerLabel": 20},
            ], 
            "examples-interactive": [
                {"command":Style.GREEN + "s3PreSignedURL " + Style.RESET},
                {"command":Style.GREEN + "s3PreSignedURL " + Style.BLUE + " my-bucket-name,my-object-name" + Style.RESET},
                {"command":Style.GREEN + "s3PreSignedURL " + Style.BLUE + " my-bucket-name,my-object-name,verbose" + Style.RESET},
                {"command":Style.GREEN + "s3PreSignedURL " + Style.BLUE + " my-bucket-name,my-object-name,verbose,900" + Style.RESET},
                {"command":Style.GREEN + "s3PreSignedURL " + Style.BLUE + " my-bucket-name,my-object-name,verbose,86400" + Style.RESET},
            ]
        },
        ROLE_LOGOFF:{
            "group": ROLE_SESSION,
            "name": "Logoff and Remove a Temporary Session Role",
            "description": "If you have a Assume Role and a Temporary Session set, this will remove this session before it expires",
            "arguments": [
                #{"name": "{SUBNET_ID}","mandatory": True, "description": "Id of the Subnet","biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "roleLogoff " + Style.RESET}
            ]
        },
         ROLE_INFO:{
            "group": ROLE_SESSION,
            "name": "Show info of a current Temporary Session Role",
            "description": "If you have an valid current Session using the Assume Role (for MFA or accessing another account), this will show some information",
            "arguments": [
                #{"name": "{SUBNET_ID}","mandatory": True, "description": "Id of the Subnet","biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "roleInfo " + Style.RESET}
            ]
        },
        AWS_NAVIGATOR:{
            "group": GENERAL,
            "name": "Navigate interactively through Network information of the current AWS Account",
            "description": "Using a browser as user interface, allows to interate with Network information of the current AWS Account",
            "arguments": [
                {"name": "verbose",            "mandatory": False, "description": verboseDescription,"biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "navigator " + Style.RESET},
                {"command":Style.GREEN + "navigator " + Style.BLUE + " verbose" + Style.RESET}
            ]
        },
        DRAW_NETWORKING: {
            "group": GENERAL,
            "name": "Generate a AWS VPC Networking Diagram (Beta version)",
            "description": "Generate a traditional AWS VPC Networking diagram (VPCs, Subnets, CIDRBlocks, RTs, NACLs, etc.) to use in DrawIo CVS Import. The CSV file to be imported will be created at your home folder ~/, besides copied to your Clipboard as well (At app.diagrams.net, go to Menu: Arrange -> Insert -> Advanced ->  CSV...)",
            "arguments": [
                {"name": "routetables",        "mandatory": False, "description": "Add Route Tables into the Graph","biggerLabel": 20},
                {"name": "nacls",              "mandatory": False, "description": "Add Network Access Control list into the Graph","biggerLabel": 20},
                {"name": "tgws",               "mandatory": False, "description": "Add Transit Gateway into the Graph","biggerLabel": 20},
                {"name": "rttgws",             "mandatory": False, "description": "Add Transit Gateway Route Tables into the Graph","biggerLabel": 20},
                {"name": "all",                "mandatory": False, "description": "Add all you've got into the Graph, everything above!","biggerLabel": 20}
            ],
            "examples-interactive": [
                {"command":Style.GREEN + "drawNetworking " + Style.RESET},
                {"command":Style.GREEN + "drawNetworking " + Style.BLUE + "routetables" + Style.RESET},
                {"command":Style.GREEN + "drawNetworking " + Style.BLUE + "addRouteTables,nacls,tgws" + Style.RESET},
                {"command":Style.GREEN + "drawNetworking " + Style.BLUE + "all" + Style.RESET}
            ]
        }
    }

    def formatDescr(text, margin, width):
        MARGIN    = margin
        WIDTH     = width
        formatted = text
        line      = ""

        if len(formatted) > WIDTH:
           formatted = ""
           for word in text.split(" "):
               if len(line + word + " ") <= (WIDTH):
                  line += word + " "
               else:
                  finalLine  = Functions.fillLineSpacesUntil(line,WIDTH)
                  #finalLine  = line
                  formatted += finalLine + "\n" + "".ljust(MARGIN," ") 
                  line = word + " " 
        
        return formatted + line

    def fillLineSpacesUntil(line, width):
        finalLine = line
        posSpace  = 0
        #while True:
        #   if (len(finalLine) + 1)  < width:
        #      spaceIndex = finalLine.find(' ',posSpace)
        #      finalLine  = finalLine[:spaceIndex] + " " + finalLine[spaceIndex:]
        #      posSpace   = spaceIndex + 2
        #   else:
        #      break   
        while (len(finalLine) + 1)  < width:
            spaceIndex = finalLine.find(' ',posSpace)
            finalLine  = finalLine[:spaceIndex] + " " + finalLine[spaceIndex:]
            posSpace   = spaceIndex + 2
           
        return finalLine      

    def showFunctions():
        print (" ")
        LABEL_LENGTH_FUNCTION_NAME = 17
        SIZE_SEPARATOR             = 95
        output  = "-".ljust(SIZE_SEPARATOR,"-") + "\n"           
        output += "   🔧   " + Style.CYAN + "A W S    F U N C T I O N S" + Style.RESET + "" + "\n"
        output += "-".ljust(SIZE_SEPARATOR,"-") + "\n"    
        for key in Functions.FUNCTIONS:
            function     = Functions.FUNCTIONS[key]
            functionName = key
            functionDescr = "  👉 " + Style.GREEN + functionName + Style.RESET + (" ".ljust(LABEL_LENGTH_FUNCTION_NAME - len(functionName) + 2,"-")) + \
                                  "> "+ Functions.formatDescr(function["description"], 26, 59) + "\n"
            output += functionDescr
            output += Style.MAGENTA + "          Arguments: " + Style.RESET + "\n"
            for args in function["arguments"]:
                output += Style.BLUE + "               " + args["name"] + " ".ljust(args["biggerLabel"] - len(args["name"])," ") + Style.MAGENTA 
                output += ("[Required]" if args["mandatory"] == True else "[Optional]")
                output += Style.RESET + "....: " + Style.RESET + Functions.formatDescr(args["description"],51,45) + "\n"

            output += "          " + Style.MAGENTA + "Examples:" + Style.RESET + "\n"
            for exs in function["examples-interactive"]:
                output += "               " + exs["command"] + "\n"
            output += "-".ljust(SIZE_SEPARATOR,"-") + "\n"
        print(output)

    def showFunctionsSummary():
        print (" ")
        LABEL_LENGTH_FUNCTION_NAME = 23
        SIZE_SEPARATOR             = 95
        output  = "-".ljust(SIZE_SEPARATOR,"-") + "\n"           
        output += "   🔧   " + Style.CYAN + "A W S    F U N C T I O N S" + Style.RESET + "" + "\n"
        output += "-".ljust(SIZE_SEPARATOR,"-") + "\n"    
        for key in Functions.FUNCTIONS:
            function     = Functions.FUNCTIONS[key]
            functionName = key
            functionDescr = "  👉 " + Style.GREEN + functionName + Style.RESET + (" ".ljust(LABEL_LENGTH_FUNCTION_NAME - len(functionName) + 2,"-")) + \
                                  "> "+ Functions.formatDescr(function["description"], 32, 59) + "\n"
            output += functionDescr
        print(output)         


Functions.formatDescr         = staticmethod(Functions.formatDescr)
Functions.fillLineSpacesUntil = staticmethod(Functions.fillLineSpacesUntil)
Functions.showFunctions       = staticmethod(Functions.showFunctions)