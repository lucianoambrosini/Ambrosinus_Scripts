#THE COMET IS BACK! Happy New Year 2021 - by Luciano Ambrosini

import rhinoscriptsyntax as rs
import random as rnd

#create an empty list
ptList = []


##-----INPUT-----##

#input values for imax and jmax and x and y spacing values
imax = rs.GetInteger("input number in x direction",10)
jmax = rs.GetInteger("input number in y direction",10)
dx = rs.GetReal("input number for x spacing direction",5)
dy = rs.GetReal("input number for y spacing direction",5)


#ASK ABOUT DISPLAYING DOT TEXT E CHECK IF THE ANSWER IS CORRECT

#SET MESSAGE AND OPTIONS
#for dotText
strPrompt1 = "would you like to print dotText?"
strOptions1 = ["yes","no"]
strPromptErr1="Please write 'yes' or 'no'"

#for shifting Pts
strPrompt2 = "would you like to shift Points location?"


#ASK FOR INPUT/QUESTION ABOU DOT TEXT
showDot=rs.GetString(strPrompt1,"no",strOptions1)

#assign check-flag
if (showDot == "yes" or showDot == "no"):
    checkDot=1
else:
    checkDot=0
    
#check loop for dotText
while checkDot!=1:
    showDot=rs.GetString(strPromptErr1,"no",strOptions1)
    if (showDot != "yes" or showDot !="no"):
        checkDot=0
    elif showDot==None:
        showDot="no"
        checkDot=1
    else:
        checkDot=1


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

#SELECT ATTRACTOR CURVE
attrCrv=rs.GetObject("pick an attractor curve",rs.filter.curve)


##-----TRANSFORMATION-----##

#set shifting Pts random values
rndSpts=1
rndEpts=5
rndSTpts=1


#nested incremental loop to generate a matrix-points
for i in range(imax):
    for j in range(jmax):
        if shiftPts=="yes":
            x = i*dx + (rnd.randrange(rndSpts,rndEpts,rndSTpts,int))
            y = j*dy + (rnd.randrange(rndSpts,rndEpts,rndSTpts,int))
            z = 0
        else:           #case: no-shifted Pts
            x = i*dx 
            y = j*dy
            z = 0
            
        #draw Pts in Rhino.Space
        #rs.AddPoint(x,y,z)
        
        #print dot texts
        if showDot=="yes":
            rs.AddTextDot((x,y,z), (x,y,z)) 
            
        #save point values in a list
        ptList.append((x,y,z))


#RETRIEVE MIN-DISTANCE BETWEEN Matrix Pts[i] AND THE ATTRACTOR CURVE
#divide attractor curve in N parts
Ndiv=imax*jmax

#create an array of Pts on attrCrv
PtsOnCrv=rs.DivideCurve(attrCrv,Ndiv)
PtsCrv=rs.AddPoints(PtsOnCrv)
rs.HideObject(PtsCrv)

DistFrmCrv=[]       #array of pts on attrCrv
MinDistFrmCrv=[]    #array of min-ditance values

for i in range(len(ptList)):
    for k in range(Ndiv+1):
        DistFrmCrv.append(rs.Distance(ptList[i], PtsOnCrv[k]))

#retrieve min-distance value between matrix points and attractor curve
    DistFrmCrv.sort()
    MinDistFrmCrv.append(DistFrmCrv[0])
    #print(MinDistFrmCrv[i])
    DistFrmCrv*=0

#retrieve min and max of MinDistFrmCrv useful for remapping values
minDist=min(MinDistFrmCrv)
maxDist=max(MinDistFrmCrv)
#print(minDist)
#print(maxDist)


#draw a circle with scaled-radius
ratio=dx/dy
sclF=6 

Circles=[]      #array of drew circles

if dx<=dy:
    Rmax=dx*0.55
    Rmin=dy*0.3
else:
    Rmax=dy*0.55
    Rmin=dx*0.3
    
for i in range(len(ptList)):
    #remap min distance
    rmpR=((Rmax-Rmin)/(maxDist-minDist))*MinDistFrmCrv[i]
    radius=rmpR*sclF
    #create circle using distance value as radius
    Circles.append(rs.AddCircle(ptList[i], radius))


#Set Stars parameters
maxStars=imax*jmax-1        #max number of stars
nLines=12                   #stars resolution
dfltN=int(maxStars/2)       #suitable n stars value
rndList = []
Lines=[]
nl=int(nLines/3)            #number of lines to scale


#ask for how many stars you want
nStars = rs.GetInteger("How many stars you want?",dfltN)
if nStars>maxStars:
    nStars=maxStars

for i in range(nStars):
    n = rnd.randint(0,maxStars)
    rndList.append(n)
#print(rndList)

#draw a star (inner circle-lines) from center (matrix points) to some points on circle
for i in range(nStars):
    rndID=rndList[i]
    cPts=rs.DivideCurve((Circles[rndID]),nLines)
    crcPts=rs.AddPoints(cPts)
    rs.HideObject(crcPts)      #not hide to perform better final-7visualization
    
    #draw lines
    for j in range(nLines):
        XsclStar = round((rnd.uniform(0.25,0.8)),2) #stars scale factors
        YsclStar = round((rnd.uniform(0.25,0.8)),2)
        if j%2:
            Lines.append(rs.AddLine(ptList[rndID],crcPts[j]))
        else:
            lin=rs.AddLine(ptList[rndID],crcPts[j])
            Lines.append(rs.ScaleObject(lin,ptList[rndID],(XsclStar,YsclStar,1),False))
        
    #hide the circle of the star
    rs.HideObject(Circles[rndID])


#message box
msg=rs.MessageBox("the Comet is coming!", 0 | 32)

if msg==1:
    #POPULATE ATTRACTOR CURVE WITH SCALED CIRCLES
    
    #create an array of Pts on attrCrv
    PtsOnCrv=rs.DivideCurve(attrCrv,Ndiv)
    PtsCrv=rs.AddPoints(PtsOnCrv)
    rs.HideObject(PtsCrv)
    
    #create circle (the comet)
    for i in range(Ndiv):
        radius=Rmax
        circle=rs.AddCircle(PtsCrv[i], radius)
        sF=(1/Ndiv)*0.5+(1/Ndiv)*i
        DefCirc=rs.ScaleObject(circle,PtsCrv[i],(sF,sF,1),False)
    
#Final message box
rs.MessageBox("Happy New Year 2021!", 0 | 32)
