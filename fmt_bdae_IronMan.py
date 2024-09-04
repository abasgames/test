#by Durik256
#original max Script https://forum.xentax.com/viewtopic.php?f=16&t=11248#p92899
from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Iron Man", ".bdae")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadModel(handle, noepyLoadModel)
    return 1

def noepyCheckType(data):
    if data[:4] != b'BRES':
        return 0
    return 1
    
def noepyLoadModel(data, mdlList):
    bs = NoeBitStream(data)
    bs.seek(16)
    
    num = bs.readInt()
    bs.seek(44)
    for x in range(num):
    	print(bs.readInt())
    bs.seek(0x10)
    LongCount = bs.readInt()
    bs.seek(0x8,1)
    MatOffset = bs.readInt()
    bs.seek(0x130)
    MakePos=bs.getOffset()
    check1= bs.readInt()
    check2= bs.readInt()
    if (check2-check1)>1000:
        bs.seek(MakePos)
    for x in range(1):
        VertOff = bs.readInt()
        FaceOff = bs.readInt()
        UnkOff = bs.readInt()
        BonesOff = bs.readInt()

    bs.seek(MakePos)
    if (check2-check1)<1000: 
        bs.seek(0x8,1)
    MakePos2=bs.getOffset()
    check2= bs.readInt()
    check3= bs.readInt()
    if (check3-check2)>1000:
        bs.seek(MakePos2)
    for x in range(1):
        VertOff = bs.readInt()
        FaceOff = bs.readInt()
        UnkOff = bs.readInt()
        BonesOff = bs.readInt()
        
    bs.seek(MakePos2)
    if (check3-check2)<1000: 
        bs.seek(0x8,1)
    VertOff = bs.readInt()
    FaceOff = bs.readInt()
    UnkOff = bs.readInt()
    BonesOff = bs.readInt()
    print("Last Read @ ",bs.getOffset())
    
    print('>>>>>>>>>>>>>>>>>>>>',VertOff, FaceOff)
    bs.seek(BonesOff)
    Unk1 = bs.readInt()
    BoneCount = bs.readInt()
    bs.seek(0x20,1)
    WeightType = bs.readInt()
    BNArr = []
    BoneNamesArray = []
        
    for a in range(BoneCount):
        getPos = bs.getOffset() + 64
        bs.seek(getPos)
        print(bs.getOffset())
        
    for a in range(BoneCount):
        BoneNameOff = bs.readInt()
        Pos=bs.getOffset()
        bs.seek(BoneNameOff)
        BoneName=searchString(bs)
        bs.seek(Pos)
        BoneNamesArray.append(BoneName)
        
    WeightsOff=bs.getOffset()

    bs.seek(BonesOff)
    Unk1 = bs.readInt()
    BoneCount = bs.readInt()
    bs.seek(0x20,1)
    WeightType = bs.readInt()
    
    for a in range(BoneCount):
        tfm = NoeMat44.fromBytes(bs.readBytes(64)).inverse().toMat43()*100
                
        newBone = NoeBone(a, BoneNamesArray[a], tfm)
        BNArr.append(newBone)
    
    bs.seek(VertOff)
    MeshNameOff= bs.readInt()
    bs.seek(MeshNameOff)
    MeshName=searchString(bs)

    bs.seek(VertOff)
    print("Mesh Off @ ",bs.getOffset())	
    MeshNameOff= bs.readInt()
    bs.seek(0xC,1)
    vertexcount = bs.readInt()
    bs.seek(0x28,1)
    SecOffStart=bs.getOffset()
    SecOff=bs.readInt()
    bs.seek(0x24,1)
    VertSize=bs.readInt()
    bs.seek(SecOffStart+SecOff)
    
    Vert_array=[]
    Face_array=[]
    UV_array=[]	
    Weight_array=[]
    Normal_array=[]
    print("Vert Section @ ",bs.getOffset())	
    if VertSize==52:	
        for x in range(vertexcount):
            getPos = bs.getOffset() + 48	
            vx = bs.readFloat()
            vy = bs.readFloat()
            vz = bs.readFloat()
            n1 = bs.readFloat()
            n2 = bs.readFloat()
            n3 = bs.readFloat()		

            bs.seek(getPos)
            tu = (bs.readShort())/65534.00
            tv = (bs.readShort()*-1)/65534.00
                
                
            Vert_array.append(NoeVec3([vx,vy,vz])*100)
            Normal_array.append(NoeVec3([n1,n2,n3]))
            UV_array.append(NoeVec3([tu,tv,0]))
    
    if VertSize==56:	
        for x in range(vertexcount):
            getPos = bs.getOffset() + 52	
            vx = bs.readFloat()
            vy = bs.readFloat()
            vz = bs.readFloat()
            n1 = bs.readFloat()
            n2 = bs.readFloat()
            n3 = bs.readFloat()
                
            bs.seek(getPos)
            tu = (bs.readShort())/65534.00
            tv = (bs.readShort()*-1)/65534.00	
                
                
            Vert_array.append(NoeVec3([vx,vy,vz]))#*100
            Normal_array.append(NoeVec3([n1,n2,n3]))
            UV_array.append(NoeVec3([tu,tv,0]))
    
    bs.seek(FaceOff)
    bs.seek(0x20,1)
    UnkCount = bs.readInt()
    facecount = bs.readInt()
    bs.seek(0xC,1)
    print("Face Section @ ", bs.getOffset())
    for x in range(facecount//3):
        fa=bs.readShort()
        fb=bs.readShort()
        fc=bs.readShort()
        Face_array +=[fa,fb,fc]
    
    bs.seek(WeightsOff)
    print("Weights Section @ ", bs.getOffset())
    if WeightType==4: 	
        for x in range(vertexcount):
            bone1 = bs.readUByte()
            bone2 = bs.readUByte()
            bone3 = bs.readUByte()
            bone4 = bs.readUByte()
            weight1 = bs.readFloat()
            weight2 = bs.readFloat()
            weight3 = bs.readFloat()
            weight4 = bs.readFloat()
            boneids, weights = [], []
            maxweight = 0
            
            if(weight1 != 0):
                maxweight = maxweight + weight1
            if(weight2 != 0):
                maxweight = maxweight + weight2
            if(weight3 != 0):
                maxweight = maxweight + weight3
            if(weight4 != 0):
                maxweight = maxweight + weight4

            if(maxweight != 0):
                if(weight1 != 0):
                    w1 = weight1
                    boneids.append(bone1)
                    weights.append(w1)
                
                if(weight2 != 0):
                    w2 = weight2
                    boneids.append(bone2)
                    weights.append(w2)

                if(weight3 != 0):
                    w3 = weight3
                    boneids.append(bone3)
                    weights.append(w3)

                if(weight4 != 0):
                    w4 = weight4
                    boneids.append(bone4)
                    weights.append(w4)
        
            Weight_array.append(NoeVertWeight(boneids, weights))
    
    if WeightType==3:
        for x in range(vertexcount):
            bone1 = bs.readUByte()
            bone2 = bs.readUByte()
            bone3 = bs.readUByte()
            bone4 = bs.readUByte()
            weight1 = bs.readFloat()
            weight2 = bs.readFloat()
            weight3 = bs.readFloat()
            boneids, weights = [], []
            maxweight = 0
                
            if(weight1 != 0):
                maxweight = maxweight + weight1
            if(weight2 != 0):
                maxweight = maxweight + weight2
            if(weight3 != 0):
                maxweight = maxweight + weight3

            if(maxweight != 0):
                if(weight1 != 0):
                    w1 = weight1
                    boneids.append(bone1)
                    weights.append(w1/255)
                
                if(weight2 != 0):
                    w2 = weight2
                    boneids.append(bone2)
                    weights.append(w2)
                
                if(weight3 != 0):
                    w3 = weight3
                    boneids.append(bone3)
                    weights.append(w3)
            
            Weight_array.append(NoeVertWeight(boneids, weights))
    
    if WeightType==2:
        for x in range(vertexcount):
            bone1 = bs.readUByte()
            bone2 = bs.readUByte()
            bone3 = bs.readUByte()
            bone4 = bs.readUByte()
            weight1 = bs.readFloat()
            weight2 = bs.readFloat()
            boneids, weights = [], []
            maxweight = 0
                
            if(weight1 != 0):
                maxweight = maxweight + weight1
            if(weight2 != 0):
                maxweight = maxweight + weight2

            if(maxweight != 0):
                if(weight1 != 0):
                    w1 = weight1
                    boneids.append(bone1)
                    weights.append(w1)
                
                if(weight2 != 0):
                    w2 = weight2
                    boneids.append(bone2)
                    weights.append(w2)  

            Weight_array.append(NoeVertWeight(boneids, weights))
    
    msh = NoeMesh(Face_array, Vert_array, MeshName)
    msh.setUVs(UV_array)
    msh.name=MeshName
    msh.setWeights(Weight_array)
    
    mdl = NoeModel([msh])
    mdl.setBones(BNArr)
    mdlList.append(mdl)
    rapi.setPreviewOption("setAngOfs", "0 -90 0")
    return 1
    
def searchString(bs):
    bytes = []
    byte = None
    while byte != 0:
        byte = bs.readUByte()
        bytes.append(byte)
    return noeAsciiFromBytes(bytes)