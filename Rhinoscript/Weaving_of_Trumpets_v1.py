#WEAVING OF TRUMPETS by Luciano Ambrosini
import rhinoscriptsyntax as rs
import random as rnd


##---MY FUNCTIONS DEFINITION---#

def SetGrid():
    
    #create an empty list/dict
    ptList = []
    ptDict = {}
    
    ##-----INPUT-----##
    
    #input values for imax and jmax and x and y spacing values
    imax = rs.GetInteger("input number in x direction",10)
    jmax = rs.GetInteger("input number in y direction",2)
    kmax = rs.GetInteger("input number in k direction",10)
    dx = rs.GetReal("input number for x spacing direction",5)
    dy = rs.GetReal("input number for y spacing direction",5)
    dz = rs.GetReal("input number for z spacing direction",5)
    
    
    #ASK ABOUT DISPLAYING DOT TEXT E CHECK IF THE ANSWER IS CORRECT
    
    #SET MESSAGE AND OPTIONS
    #for dotText
    strPrompt1 = "would you like to print dotText?"
    strOptions1 = ["yes","no"]
    strPromptErr1="Please write 'yes' or 'no'"
    
    #for shifting Pts
    strPrompt2 = "would you like to shift Points location?"
    
    #proportionally space the points
    strPrompt3 = "would you like to proportionally space the points?"
    
    
    #ASK FOR INPUT/QUESTION ABOUT TEXT DOT
    showDot=rs.GetString(strPrompt1,"no",strOptions1)
    
    #assign check-flag
    if (showDot == "yes" or showDot == "no"):
        checkDot=1
    else:
        checkDot=0
        
    #check loop for Text dot
    while checkDot!=1:
        showDot=rs.GetString(strPromptErr1,"no",strOptions1)
        if (showDot != "yes" or showDot !="no"):
            checkDot=0
        elif showDot==None:
            showDot="no"
            checkDot=1
        else:
            checkDot=1
    
    
    #ASK THE FOR PROPORTIONAL SPACING
    propPts=rs.GetString(strPrompt3,"no",strOptions1)
    
    #assign check-flag
    if (propPts == "yes" or propPts == "no"):
        checkProp=1
    else:
        checkProp=0
        
    #check loop for spacing proportionally Pts
    while checkProp!=1:
        propPts=rs.GetString(strPromptErr1,"no",strOptions1)
        if (propPts != "yes" or propPts !="no"):
            checkProp=0
        elif propPts==None:
            propPts="no"
            checkProp=1
        else:
            checkProp=1
    
    
    #ASK THE FOR SHIFTING PTS
    shiftPts=rs.GetString(strPrompt2,"no",strOptions1)
    
    #assign check-flag
    if (shiftPts == "yes" or shiftPts == "no"):
        checkShift=1
    else:
        checkShift=0
        
    #check loop for shifting Pts
    while checkShift!=1:
        shiftPts=rs.GetString(strPromptErr1,"no",strOptions1)
        if (shiftPts != "yes" or shiftPts !="no"):
            checkShift=0
        elif shiftPts==None:
            shiftPts="no"
            checkPts=1
        else:
            checkShift=1
    #return (checkDot,checkProp,checkPts)


    ##-----GENERATE GRID-----##
    
    #set shifting Pts random values
    rndSpts=1
    rndEpts=5
    rndSTpts=1
    
    
    #nested incremental loop to generate a matrix-points
    for i in range(imax):
        for j in range(jmax):
            for k in range(kmax):
                
                if shiftPts=="yes" and propPts=="yes":
                    x = (i+i*i)*dx + i*(rnd.randrange(rndSpts,rndEpts,rndSTpts,int))
                    y = (j+j*j)*dy + i*(rnd.randrange(rndSpts,rndEpts,rndSTpts,int))
                    z = (k+k*k)*dz + i*(rnd.randrange(rndSpts,rndEpts,rndSTpts,int))
                elif shiftPts=="yes" and propPts=="no":
                    x = i*dx + (rnd.randrange(rndSpts,rndEpts,rndSTpts,int))
                    y = j*dy + (rnd.randrange(rndSpts,rndEpts,rndSTpts,int))
                    z = k*dz + (rnd.randrange(rndSpts,rndEpts,rndSTpts,int))
                elif shiftPts=="no" and propPts=="yes":
                    x = (i+i*i)*dx
                    y = (j+j*j)*dy
                    z = (k+k*k)*dz
                else:           #case: no-shifted and no prop Pts
                    x = i*dx 
                    y = j*dy
                    z = k*dz
                    
                #draw Pts in Rhino.Space
                #rs.AddPoint(x,y,z)
                
                #print dot texts
                if showDot=="yes":
                    rs.AddTextDot((x,y,z), (x,y,z)) 
                    
                #save point values in a dictionary using (i,j) as a key
                ptDict[(i,j,k)] = (x,y,z)
    return(ptDict,imax,jmax,kmax,propPts)

def numberPoints(points):
    for i in range(len(points)):
        #rs.AddPoint(points[i])
        rs.AddTextDot(i, points[i])

def RndID(gridPts):
    #find max dim of a list of points (points from srf control points list)
    dim=len(gridPts)-1
    id=rnd.randint(0,dim)
    return(id)

def RndRAD(max):
    #random radius
    rad=round(rnd.uniform(0.5,max/3),2)
    return (rad)

def PtFrame(origin,ptDict,loc):
    #generate frame of my cube-module by origin and loc (loc:front,back,left,right,bottom,up)
    if loc=='front'or loc=='back':
        xaxis=(1,0,0)
        yaxis=(0,0,1)
    elif loc=='left' or loc=='right':
        xaxis=(0,1,0)
        yaxis=(0,0,1)
    elif loc=='bott' or loc=='up':
        xaxis=(1,0,0)
        yaxis=(0,1,0)
    Frm=rs.PlaneFromFrame(origin,xaxis,yaxis)
    return(Frm)



def wallType01(ptDict,IMAX,JMAX,KMAX,propGrid):
    
    #scale factor
    sclF=0.5
    
    #Mid circle radius
    midRad=0.5
    
    
    for i in range(IMAX):
        for j in range(JMAX):
            for k in range(KMAX):
                if i > 0 and j > 0 and k > 0:
                    
                    #cube-module centroid
                    Crossline=rs.AddCurve((ptDict[(i-1,j-1,k-1)],ptDict[(i,j,k)]))
                    centroid=rs.AddPoint(rs.CurveMidPoint(Crossline))
                    rs.DeleteObject(Crossline)
                    
                    
                    #FRONT FACE
                    #find Front Face centroid
                    FFline=rs.AddCurve((ptDict[(i-1,j-1,k-1)],ptDict[(i,j-1,k)]))
                    centFace=rs.AddPoint(rs.CurveMidPoint(FFline))
                    rs.DeleteObject(FFline)
                    #create construction surface to find grid of points
                    srf = rs.AddSrfPt((ptDict[(i-1,j-1,k)], ptDict[(i,j-1,k)], 
                    ptDict[(i,j-1,k-1)], ptDict[(i-1,j-1,k-1)]))
                    #scale srf
                    rs.ScaleObject(srf,centFace,(sclF,sclF,sclF),False)
                    #rebuild surface to create 4 x 4 grid (9 quadrants)
                    rs.RebuildSurface(srf, (3,3), (4,4))
                    #extract points from grid
                    FFpts = rs.SurfacePoints(srf)
                    #call function to reveal order of points
                    #numberPoints(FFpts)
                    #delete construction surface
                    rs.DeleteObject(srf)
                    rs.DeleteObject(centFace)
                    
                    
                    #BACK FACE
                    #find Back Face centroid
                    BFline=rs.AddCurve((ptDict[(i-1,j,k-1)],ptDict[(i,j,k-1)]))
                    centFace=rs.AddPoint(rs.CurveMidPoint(BFline))
                    rs.DeleteObject(BFline)
                    #create construction surface to find grid of points
                    srf = rs.AddSrfPt((ptDict[(i-1,j,k-1)], ptDict[(i,j,k-1)], 
                    ptDict[(i,j,k)], ptDict[(i-1,j,k)]))
                    #scale srf
                    rs.ScaleObject(srf,centFace,(sclF,sclF,sclF),False)
                    #rebuild surface to create 4 x 4 grid (9 quadrants)
                    rs.RebuildSurface(srf, (3,3), (4,4))
                    #extract points from grid
                    BFpts = rs.SurfacePoints(srf)
                    #delete construction surface
                    rs.DeleteObject(srf)
                    rs.DeleteObject(centFace)
                    
                    
                    #LEFT FACE
                    #find Left Face centroid
                    LFline=rs.AddCurve((ptDict[(i-1,j,k-1)],ptDict[(i-1,j-1,k)]))
                    centFace=rs.AddPoint(rs.CurveMidPoint(LFline))
                    rs.DeleteObject(LFline)
                    #create construction surface to find grid of points
                    srf = rs.AddSrfPt((ptDict[(i-1,j,k-1)], ptDict[(i-1,j-1,k-1)], 
                    ptDict[(i-1,j-1,k)], ptDict[(i-1,j,k)]))
                    #scale srf
                    rs.ScaleObject(srf,centFace,(sclF,sclF,sclF),False)
                    #rebuild surface to create 4 x 4 grid (9 quadrants)
                    rs.RebuildSurface(srf, (3,3), (4,4))
                    #extract points from grid
                    LFpts = rs.SurfacePoints(srf)
                    #call function to reveal order of points
                    #numberPoints(LFpts)
                    #delete construction surface
                    rs.DeleteObject(srf)
                    rs.DeleteObject(centFace)
                    
                    
                    #RIGHT FACE
                    #find Right Face centroid
                    RFline=rs.AddCurve((ptDict[(i,j-1,k-1)],ptDict[(i,j,k)]))
                    centFace=rs.AddPoint(rs.CurveMidPoint(RFline))
                    rs.DeleteObject(RFline)
                    #create construction surface to find grid of points
                    srf = rs.AddSrfPt((ptDict[(i,j-1,k-1)], ptDict[(i,j,k-1)], 
                    ptDict[(i,j,k)], ptDict[(i,j-1,k)]))
                    #scale srf
                    rs.ScaleObject(srf,centFace,(sclF,sclF,sclF),False)
                    #rebuild surface to create 4 x 4 grid (9 quadrants)
                    rs.RebuildSurface(srf, (3,3), (4,4))
                    #extract points from grid
                    RFpts = rs.SurfacePoints(srf)
                    #delete construction surface
                    rs.DeleteObject(srf)
                    rs.DeleteObject(centFace)
                    
                    
                    #BOTTOM FACE
                    #find Bottom Face centroid
                    BbFline=rs.AddCurve((ptDict[(i-1,j-1,k-1)],ptDict[(i,j,k-1)]))
                    centFace=rs.AddPoint(rs.CurveMidPoint(BbFline))
                    rs.DeleteObject(BbFline)
                    #create construction surface to find grid of points
                    srf = rs.AddSrfPt((ptDict[(i-1,j-1,k-1)], ptDict[(i-1,j,k-1)], 
                    ptDict[(i,j,k-1)], ptDict[(i,j-1,k-1)]))
                    #scale srf
                    rs.ScaleObject(srf,centFace,(sclF,sclF,sclF),False)
                    #rebuild surface to create 4 x 4 grid (9 quadrants)
                    rs.RebuildSurface(srf, (3,3), (4,4))
                    #extract points from grid
                    BbFpts = rs.SurfacePoints(srf)
                    #call function to reveal order of points
                    #numberPoints(BbFpts)
                    #delete construction surface
                    rs.DeleteObject(srf)
                    rs.DeleteObject(centFace)
                    
                    
                    #UPPER FACE
                    #find Bottom Face centroid
                    UpFline=rs.AddCurve((ptDict[(i-1,j-1,k)],ptDict[(i,j,k)]))
                    centFace=rs.AddPoint(rs.CurveMidPoint(UpFline))
                    rs.DeleteObject(UpFline)
                    #create construction surface to find grid of points
                    srf = rs.AddSrfPt((ptDict[(i-1,j-1,k)], ptDict[(i-1,j,k)], 
                    ptDict[(i,j,k)], ptDict[(i,j-1,k)]))
                    #scale srf
                    rs.ScaleObject(srf,centFace,(sclF,sclF,sclF),False)
                    #rebuild surface to create 4 x 4 grid (9 quadrants)
                    rs.RebuildSurface(srf, (3,3), (4,4))
                    #extract points from grid
                    UpFpts = rs.SurfacePoints(srf)
                    #delete construction surface
                    rs.DeleteObject(srf)
                    rs.DeleteObject(centFace)
                    
                    
                    ###CREATE CIRCLES###
                    
                    #DRAW FRONT-FACE AND BACK-FACE CIRCLES
                    #random point from srf control points
                    id=RndID(FFpts)                    
                    #Draw a circle in Front/Back planes
                    Fframe=PtFrame(FFpts[id],ptDict,'front')
                    radius=RndRAD(5)
                    FCircle=rs.AddCircle(Fframe,radius)                    
                    #random point from srf control points
                    id=RndID(BFpts)   
                    Bframe=PtFrame(BFpts[id],ptDict,'back')
                    radius=RndRAD(5)
                    BCircle=rs.AddCircle(Bframe,radius)                    
                    #Middle circle
                    C1frame=PtFrame(centroid,ptDict,'front')
                    MCircle1=rs.AddCircle(C1frame,midRad)
                    
                    
                    #DRAW LEFT-FACE AND RIGHT-FACE CIRCLES
                    #random point from srf control points
                    id=RndID(LFpts)                    
                    #Draw a circle in Front/Back planes
                    Lframe=PtFrame(LFpts[id],ptDict,'left')
                    radius=RndRAD(5)
                    LCircle=rs.AddCircle(Lframe,radius)                    
                    #random point from srf control points
                    id=RndID(RFpts)   
                    Rframe=PtFrame(RFpts[id],ptDict,'right')
                    radius=RndRAD(5)
                    RCircle=rs.AddCircle(Rframe,radius)                    
                    #Middle circle
                    C2frame=PtFrame(centroid,ptDict,'left')
                    MCircle2=rs.AddCircle(C2frame,midRad)
                    
                    
                    #DRAW BOTTOM-FACE AND UPPER-FACE CIRCLES
                    #random point from srf control points
                    id=RndID(BbFpts)                    
                    #Draw a circle in Front/Back planes
                    Bbframe=PtFrame(BbFpts[id],ptDict,'bott')
                    radius=RndRAD(5)
                    BbCircle=rs.AddCircle(Bbframe,radius)                    
                    #random point from srf control points
                    id=RndID(UpFpts)   
                    Upframe=PtFrame(UpFpts[id],ptDict,'up')
                    radius=RndRAD(5)
                    UpCircle=rs.AddCircle(Upframe,radius)                    
                    #Middle circle
                    C3frame=PtFrame(centroid,ptDict,'bott')
                    MCircle3=rs.AddCircle(C3frame,midRad)
                    
                    
                    ###CREATE SURFACES###
                    
                    #Loft from Front to Back
                    loft1=rs.AddLoftSrf((FCircle,MCircle1,BCircle))
                    #rs.ObjectColor(loft1, (255/IMAX*i, 255-(255/JMAX)*j,255/KMAX*k))
                    
                    #loft from left to Right
                    loft2=rs.AddLoftSrf((LCircle,MCircle2,RCircle))                    
                    #rs.ObjectColor(loft2, (255/IMAX*i, 255-(255/JMAX)*j,255/KMAX*k))
                    
                    #loft from bottom to up
                    loft3=rs.AddLoftSrf((BbCircle,MCircle3,UpCircle)) 
                    
                    #Draw sphere
                    if propGrid=='yes':
                        sphere=rs.AddSphere(centroid,1.2*i)
                    else:
                        sphere=rs.AddSphere(centroid,1.2)
                        
                    rs.ObjectColor(sphere, (255/IMAX*i, 255-(255/JMAX)*j,255/KMAX*k))

                    Obj=loft1+loft2+loft3
                    rs.ObjectColor(Obj, (255/IMAX*i, 255-(255/JMAX)*j,255/KMAX*k))
    return()


##---MAIN RUN---#

def main():
    #call function
    rs.EnableRedraw(False)
    
    Pts3D,IMAX,JMAX,KMAX,propGrid=SetGrid()
    wallType01(Pts3D,IMAX,JMAX,KMAX,propGrid)
    
    rs.EnableRedraw(True)

#call main() function to start program
main()
