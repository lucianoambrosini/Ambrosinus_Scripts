"""
Mirror objects by using a Between points axes
by LUCIANO AMBROSINI (2023)
www.lucianoaambrosini.it
"""

import rhinoscriptsyntax as rs
import ctypes

#This script
script_name= "\"Mirror_Between\""
vers= "v0.0.1"
credit= "Luciano Ambrosini"

#Message in the Rhino cmdline
message = "\nScriptMessage: Running the {} {} by {}\n".format(script_name, vers, credit)
print(message)

objs = rs.GetObjects("Select objects to mirror")

if objs==None:
  print(script_name + " Script failed to run")
  ctypes.windll.user32.MessageBoxW(0, script_name + " Script failed to run!","ERROR MESSAGE", 64+262144)
  
else:
    #Give the two between axes points
    p1 = rs.GetPoint("Start point of the Mirror between axes")
    p2 = rs.GetPoint("End point of the Mirror between axes")
    
    #Mid point
    mid = rs.PointDivide(rs.PointAdd(p1, p2), 2)
    
    rs.UnselectAllObjects() #unselect all objs
    rs.SelectObjects(objs) #select only objs mirror to
    
    MirrorBetween=rs.Command("_Mirror " + str(mid))