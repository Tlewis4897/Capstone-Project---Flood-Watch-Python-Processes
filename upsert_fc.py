import arcpy
from utils import zip_hosted_layer

##Create temp FC
def create_temp_fc(config):
    # Set local variables
    out_folder_path = r"C:\Capstone_Project\Scripts"
    out_name = "Capstone.gdb"

    # Execute CreateFileGDB
    arcpy.CreateFileGDB_management(out_folder_path, out_name)
    for i in config["sde"]["sde_fc"]:
        name = i.split('/')[-1]
        name = name.split('.')[-1]
        arcpy.FeatureClassToFeatureClass_conversion(i, 
                                            "C:\Capstone_Project\Scripts\Capstone.gdb", 
                                            name)
    zip_hosted_layer(r'C:\Capstone_Project\Scripts\Capstone.gdb', 'Capstone_FC')
