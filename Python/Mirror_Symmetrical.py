"""
Mirror objs by simmetrical axes
by LUCIANO AMBROSINI (2023)
www.lucianoaambrosini.it
"""

import rhinoscriptsyntax as rs
import ctypes

#This script
script_name= "\"Mirror_Symmetrical\""
vers= "v0.0.2"
credit= "Luciano Ambrosini"

#Message in the Rhino cmdline
message = "\nScriptMessage: Running the {} {} by {}\n".format(script_name, vers, credit)
print(message)

try:
    #Initial condition
    rs.UnselectAllObjects() #unselect all objs
    
    #Select objects to mirror
    objects_to_mirror = rs.GetObjects("Select objects to mirror")
    
    if objects_to_mirror==None:
      print(script_name + " terminated!")    
      ctypes.windll.user32.MessageBoxW(0, script_name + " terminated!","ERROR MESSAGE", 64+262144)
      
    else:
        #Transformation
        rs.UnselectAllObjects() #unselect all objs
        rs.SelectObjects(objects_to_mirror) #select only objs mirror to
        
        #Generate Bbox and centroid elements
        rs.Command("!_BoundingBox CoordinateSystem=World  Cumulative=Yes  Output=Curves _Enter")
        rs.UnselectAllObjects() #unselect all objs
        rs.Command("!_SelLast")
        bbox=rs.GetObjects(preselect=True)
        
        centroid=rs.CurveAreaCentroid(bbox[0])[0]
        StartPt = centroid
    
        #Remove useless objcts
        rs.UnselectAllObjects() #unselect all objs
        for crv in bbox:
            rs.SelectObjects([crv])
            
        objs_todelete=rs.GetObjects(preselect=True)
        rs.DeleteObjects(objs_todelete)
        
        #Ask the user to specify the axis of symmetry (X, Y, or Z)
        axis = rs.GetString("Select the symmetry axis (X, Y, or Z):", "Y")
        
        if axis is None:
        #User canceled the input dialog, so exit the script
            print("Input canceled. Script terminated.")
            ctypes.windll.user32.MessageBoxW(0, script_name + " terminated!","ERROR MESSAGE", 64+262144)

        else:
        
            if axis not in ["X", "Y", "Z","x", "y", "z"]:
                print("Invalid input. You must select one of 'X', 'Y', or 'Z'.")
            else:
        
                #Define the mirroring transformation
                k=2 #dist-increment between StartPt and EndPt
                
                if axis == "X" or axis == "x":
                    EndPt=rs.CreatePoint(StartPt[0]*k,StartPt[1],StartPt[2])
                
                elif axis == "Y" or axis == "y":
                    EndPt=rs.CreatePoint(StartPt[0],StartPt[1]*k,StartPt[2])
                
                elif axis == "Z" or axis == "z":
                    EndPt=rs.CreatePoint(StartPt[0],StartPt[1],StartPt[2]*k)
                
                rs.UnselectAllObjects() #unselect all objs
                rs.SelectObjects(objects_to_mirror) #select only objs mirror to
                MirrorBetween=rs.Command("!_Mirror Copy=No " + str(StartPt)+" "+str(EndPt))
    
                #Process message
                print("Objects mirrored successfully along the {} axis.".format(axis))                
            
except Exception as e:
    
    #Remove useless objcts
    rs.Command("_SelLast")
    objs_todelete=rs.GetObjects(preselect=True)
    rs.DeleteObjects(objs_todelete)
    
    #Process message
    print("Script failed to run: {}".format(e))
    ctypes.windll.user32.MessageBoxW(0, script_name + " Script failed to run!\n{}".format(e), "ERROR MESSAGE", 64 + 262144)

