# from __future__ import absolute_import
from matplotlib import path 
import numpy as np
from Constant import get_eps,get_sig_figures

### Computation on 3D Lines and Polygons
'''
    All vertices need numpy.array(N,3)
'''
# Vectors

def Repmat(M,m,n):          # matlab alternative to broadcasting of Python
    return np.tile(M,(m,n)) 

def Array(x):
    return np.array(x)

def MatShape(v):
    ret = v.shape
    n = len(v)
    if len(ret) == 1:
        ret = (1,n)
    return ret
    
def Cross(u,v):
    return np.cross(u,v)

def Dot(u,v):
    return np.dot(u,v)

def Inv(Matrix):
    return np.linalg.inv(Matrix)

def Det(Matrix):
    return np.linalg.det(Matrix)

# Fast Version
def Length(v):
    return np.sqrt(v.dot(v))

def UnitVector(v): 
    return v/Length(v)   

def Mask(v,bSelected):
    """
    It returns an array made of elements selected ( bSelected == True ).
    """
    P = np.array(v)
    return P[bSelected]

#判断矩阵，list，值等是否相同（在误差允许范围内），若相同，返回True
def Equal(a,b):
    return np.all(Round(a)==Round(b))

def Round(x):
    return np.round(x, get_sig_figures())

def ScalarEqual(a,b):
    return Round(abs(a-b))<=get_eps()

def ScalarZero(x):
    return ScalarEqual(x,get_eps())

# Vertices 
def Vertices(x):
    return Array(x)

#计算直线与直线的交点，输入为两个直线上的一点和直线的斜率，，支持三维空间下的 计算，输出为
##                                                              1.直线相交输出点Array（P)
##                                                              2.直线平行输出None
##                                                              3.直线重合输出‘Line’
##                                                              4.直线相异输出None
# 3D Lines
def LineXLine(P1,L1,P2,L2):
    ##向量单位化
    L1  = UnitVector(np.array(L1))
    L2  = UnitVector(np.array(L2)) 
    C, D = Array(P1), Array(P2)
    CD = D - C
    e,f  = Array(L1), Array(L2)
    X = Cross(f,CD)
    Y = Cross(f,e)
    ##判断向量是否为0
    if(np.linalg.norm(X) <= get_eps() and np.linalg.norm(Y)  <= get_eps()):
        return 'Line'
    else:
        if((np.linalg.norm(Y)) <= get_eps() ):
            return None
        else  :
            Z = Dot(X,Y)
            sign = 1 if Z>0 else -1
            M = C + sign * Length(X)/Length(Y) * e
            if PointInLine(M,P1,L1)==False or PointInLine(M,P2,L2)==False:
                return None
            else:
                return M

##判断点是否在直线上，支持三维计算，输入为点，直线上的一点，直线的斜率，输出为Ture和False
def PointInLine(P0,P,L):
    V0 = Array(P0)
    V  = Array(P)
    L1 = UnitVector( V0 - V)                ##UnitVector为之前定义的函数，用于向量单位化
    Lx = UnitVector(Array(L))
    if Equal(L1, Lx) or Equal(L1, (-1)*Lx):
        return True
    else:
        return False



##判断点是否在线段上，支持三维计算，输入为点，线段的两个端点，输出为Ture或False
def PointInSegment(P,P1,P2):
    pos = np.vstack((P1, P2))
    pos = np.array([np.min(pos[ :, :], axis=0),
                    np.max(pos[ :, :], axis=0)])
    return np.all(P>=pos[0,:]) & np.all(P<=pos[1,:])


# 3D Polygons
'''
   交点:
   计算从 P0 出发的直线（L）与多边形（Polygon）相交

        （1）直线与平面的交点；
        （2）确定交点是否落在多边形区域内（包括边界上）。

           P0      : the starting point ,
                    P0 =np.array((x0,y0,z0))
           L       : 
                the slope of line
                    L = np.array((dx,dy,dz))
           Polygon : 
                vertices of the polygon
                    = np.array(
                                [x1 y1 z1],
                                [x2 y2 z2],
                                ...
                                [xm ym zm])
'''
##判断线段和多边形的交点，输入线段的两个端点P1，P2和多边形，输出交点（暂未使用）
def SegmentXPolygon(P1,P2,polygon):
    L  = UnitVector(np.array(P2) - np.array(P1))
    P0 = P1

    Point = LineXPolygon(P0,L,polygon)

    if Point is None :
        return None
    else :
       if PointInSegment(Point,P1,P2):
           return Point
       else :
           return None

##计算直线和线段的交点，只支持二维下的计算，输入直线上的一点和直线的斜率，线段端点的x，y值，输出：
##                                                              1.相交于一点输出点Array（P)
##                                                              2.无交点输出None
##                                                              3.直线与线段重合输出‘Line’
def LineXSegment2D(P0,L,x1,y1,x2,y2):
    P1,L1,P2=(x1,y1),(x1-x2,y1-y2),(x2,y2)
    L1  = UnitVector(np.array(L1))
    if np.linalg.norm(L1) <= get_eps():
        return None
    else:
        P=LineXLine(P0,L,P1,L1)             ##点坐标的计算是用直线相交的函数进行计算
        if P is None:
            return None
        elif P == 'Line':
            return P
        else:
            if PointInSegment(P,P1,P2):     ##所以需要判断点是否在线段上
                return P
            else:
                return None

##计算直线和多边形的交点，（多边形不能是凹多边形）只支持二维下的计算，输入直线上的一点和直线的斜率，多边形的矩阵，输出为2个值：
##                                                              1.相交于一点输出点Array（P1)，None
##                                                              2.无交点输出None，None
##                                                              3.直线与多边形有两个交点输出‘Array（P1)，Array（P2)
def LineXPolygon2D(P0,L,Polygon):
    L=UnitVector(L) 
    n = len(Polygon)
    IS = 0
    P1=None
    P2=None
    for i in range(n):
        x1,y1 = Polygon[i]
        x2,y2 = Polygon[(i+1)%n]
        P = LineXSegment2D(P0,L,x1,y1,x2,y2)  ##通过计算线与多边形每一条边的交点计算它与多边形的交点
        if P is None :
            pass
        elif P == 'Line':                       ##直线与线段重合
            P1,P2=(x1,y1),(x2,y2)
            return P1,P2
        else:
            if P1 is None:
                P1=P
            elif np.linalg.norm(P-P1) <= get_eps():
                pass  
            else:
                P2=P
                return P1,P2

       
    if P1 is None :
        return None,None
    else:
        return P1,None

####计算直线和多边形的交点，（多边形不能是凹多边形）三维下的计算，输入直线上的一点和直线的斜率，多边形的矩阵，输出为1个值：
##                                                              1.相交于一点输出点Array（P1)
##                                                              2.无交点输出None，None
##                                                              3.直线与多边形有两个交点输出‘Line’，同时会输出一段文字提示
def LineXPolygon(P0,L,Polygon):
    n = PolygonNormal(Polygon)          # [dx,dy,dz] 
    R0 = np.array(Polygon[0,:])          # [x,y,z]
    Point = LineXPlane(P0,L,R0,n)          #用直线和面的交点函数求交点

    if Point is None:
        return None
    if Point == 'Line':                #如果直线在平面内，就线用转换矩阵转到二维，再用二维下的公式
        PL=P0+L
        P03D,Polygon3D,U,R0=D3ToD2(P0,Polygon)                      ##从三维矩阵变成二维
        PL3D,Polygon3D,U,R0=D3ToD2(PL,Polygon)
        Polygon2D = Polygon3D[:,0:2]
        L3D=P03D-PL3D
        P02D=P03D[0:2]
        L2D= L3D[0:2]
        P1,P2=LineXPolygon2D(P02D,L2D,Polygon2D)
        if P1 is None and P2 is None:
            return None
        elif P2 is None:
            P1=D2toD3Point(P1,U,R0)
            return P1
        else:
            P1=D2toD3Point(P1,U,R0)
            P2=D2toD3Point(P2,U,R0)
            print('相交的图形是一个线段，端点分别为',np.around(P1, decimals=3, out=None),np.around(P2, decimals=3, out=None))
            return 'Line'
    if PointInPolygon(Point,Polygon) :
        return Point
    else :
        return None

#####计算直线和平面的交点，（多边形不能是凹多边形）三维下的计算，输入直线上的一点和直线的斜率，平面上的一点和平面的法向量，输出：
##                                                              1.相交于一点输出点Array（P1)
##                                                              2.无交点输出None
##                                                              3.直线与在平面上输出‘Line’
def LineXPlane(P0,L,R0,n):
    L = UnitVector(L) 
    n_dot_L = Dot(n,L)
    dP = R0 - P0                         # [dx,dy,dz]

    if ScalarZero(n_dot_L):
        if ScalarZero(Dot(dP,dP)) or ScalarZero(Dot(dP,n)):
            return 'Line'
        else:
            return None

    x  = Dot(n,dP)/n_dot_L
    P  = P0 + x*L                         # [x,y,z]
    return P


##三维坐标转为二维坐标，输入要转换的点和多边形，返回的点为（0，0，0）是三维点，vertices3D是三维坐标，U是变换矩阵，R0是基准点（一般不直接使用）
def D3ToD2(Point,Polygon):
    U  = GetU(Polygon)
    R  = Array(Polygon)
    R0 = Array(Polygon[0,:])
    P  = Array(Point)
    r = U@(R - R0).T  #@表示矩阵乘法
    p = U@(P - R0).T
    xy=p.T
    vertices3D = r.T
    vertices2D = r.T[:,0:2]
    return xy,vertices3D,U,R0
##二维坐标转为三维坐标，输入要转换的多边形，U是变换矩阵，R0是基准点，返回vertices3D是三维坐标，（一般不直接使用）
def D2toD3Polygon(Polygon,U,R0):
    r=Polygon.T
    U=np.mat(U)
    U=U.I
    R=(U@r).T+R0
    return R
##二维坐标转为三维坐标，输入要转换的点，U是变换矩阵，R0是基准点，返回vertices3D是三维坐标，（一般不直接使用）
def D2toD3Point(Point,U,R0):
    Point3D=np.array([[Point[0]],[Point[1]],[0]])
    p=Point3D
    U=np.mat(U)
    U=U.I
    R=(U@p).T+R0
    return R

##判断点是否在多边形内部，输入点和多边形，仅适用于单个点的情况。返回True或False
def PointInPolygon(Point,Polygon):
    p,vertices3D,U,R0=D3ToD2(Point,Polygon)
    z=p[2]
    vertices2D = vertices3D[:,0:2]
    if ScalarZero(z) :                  ##若变换之后z坐标不为0说明点没有落在平面上
        xy = p[0:2]   # first two columns 
        return PointInPolygon2D(xy[0], xy[1], vertices2D)
    else :
        return False

##判断点是否在多边形内部，输入点和多边形，适用于单个点或多个点的情况。返回True或False
def PointsInPolygon(Points,Polygon):
    Points = np.array(Points)
    ##多维数组转成1
    j=0
    if Points.ndim ==1:
        return PointInPolygon(Points,Polygon)
    elif Points.ndim ==3:
        j=1
        dimen = Points.shape
        a=dimen[0]
        b=dimen[1]
        Points = Points.reshape(int(a*b),3)
    U  = GetU(Polygon)
    R  = Array(Polygon)
    R0 = Array(Polygon[0,:])
    Ps = Array(Points)
    r = U@(R - R0).T
    p = U@(Ps - R0).T
    n = len(p[0])                   ##判断点的z坐标是否为0，不为0说明不在面上
    ret = np.array(list(False for i in range(n)))
    for i in range(n):
        if ScalarZero(p[2,i]):
            ret[i] = True

    xy = (p[0:2]).T   # first two columns 
    vertices2D = r.T[:,0:2]
    if j==1:
        ret = ret.reshape(a,b)
        xy=xy.reshape(a,b,2)
    ret=ret*PointsInPolygon2D(xy, vertices2D)
    return ret
##多点在多边形的关系判断方法2
def PointsInPolygon0(Points,Polygon):
    Points = np.array(Points)
    ret=[]
    if Points.ndim ==2:
        for i,point in enumerate(Points):
            ret.append(PointInPolygon(point,Polygon))
        ret=np.array(ret)
        return ret
    elif Points.ndim ==3:
        for i,points in enumerate(Points):
            for j,point in enumerate(points):
                ret.append(PointInPolygon(point,Polygon))
        ret=np.array(ret)
        ret = ret.reshape(i+1,j+1)
        return ret
    else:
        return None

##多点在多边形的关系判断方法3
def PointsInPolygon1(Points,Polygon):
    Points = np.array(Points)
    if Points.ndim ==2:
        n=len(Points)
        ret = np.array(list(False for i in range(n)))
        for i,point in enumerate(Points):
            ret[i]=(PointInPolygon(point,Polygon))
        return ret
    elif Points.ndim ==3:
        n=len(Points)
        m=len(Points[0])
        ret = np.array(list(False for i in range(n*m)))
        ret = ret.reshape(n,m)
        for i,points in enumerate(Points):
            for j,point in enumerate(points):
                ret[i,j]=(PointInPolygon(point,Polygon))
        return ret
    else:
        return None


##判断点是否在多边形内部，输入点和多边形，适用于单个点或多个点的情况。仅适用于二维。返回True或False
def PointsInPolygon2D(Points,Polygon,Method='Custom'):
    from functools import reduce
    from operator import mul

    Vertices = Points
    if type(Points) is not np.array:
        Vertices = Array(Points)

    # one Point
    # 1) input as np.array([7,8]), shape =(2,)
    if len(Vertices.shape) == 1 :
        x0 = Vertices[0]
        y0 = Vertices[1]
        ##print(x0,y0,Polygon)
        ret = PointInPolygon2D(x0,y0,Polygon) 
        return ret

    # 2) input as np.array([(7,8)]), shape = (1,2)
    elif (len(Vertices.shape) == 2 and Vertices.shape[0] == 1) : 
        x0 = Vertices[0][0]
        y0 = Vertices[0][1]
        ret = PointInPolygon2D(x0,y0,Polygon)
        return ret

    # Many Points
    shape = np.shape(Vertices)    #  0,...,n-1
    matrix_shape = shape[0:-1]  #  0,...,n-2, excluding shape[-1]
    n = reduce(mul, matrix_shape, 1)   #  how many points
    Points_array = Vertices.reshape(n,shape[-1])  # 1D array of (x,y,z).

    key_str = Method.lower()
    
    if key_str == 'custom':
        ret = _PointsInPolygon2D_Custom(Points_array,Polygon)
    elif key_str == 'matplotlib':
        ret = _PointsInPolygon2D_Matplotlib(Points_array, Polygon)

    return ret.reshape(matrix_shape)
##上述函数的分支之一
def _PointsInPolygon2D_Custom(Points,Polygon):

    n = len(Points)
    ret = np.array(list(False for i in range(n)))
    for i in range(n):
        x0,y0  = Points[i]
        ret[i] = PointInPolygon2D(x0,y0,Polygon)   
    return ret
##上述函数的分支之二
def _PointsInPolygon2D_Matplotlib(Points,Polygon):
    row = len(Polygon)   # row = N, Polygon = N x 2   
    
    # Inside
    edge = path.Path([(Polygon[i,0],Polygon[i,1]) for i in range(row)])
    ret  = edge.contains_points(Points)    
    
    # print(ret)
    # On edge
    if not all(ret) :        
        n = len(Points)
        for i in range(0,row):
            j = (i+1)%row 
            x1,y1 = Polygon[i]
            x2,y2 = Polygon[j]
            dy = y2-y1
            dx = x2-x1
           
            for k in range(n):
                if ret[k] :
                    continue          
                
                x0,y0 = Points[k]
                if not ScalarZero(dy):
                    if min(y1,y2) <= y0 and y0 <= max(y1,y2) :                        
                        x = x1 + (y0-y1)*dx/dy   # any slant line, including vertical line
                        if ScalarEqual(x,x0) :
                            ret[k] = True
                            
                elif not ScalarZero(dx):    # horizontal line
                    if min(x1,x2) <= x0 and x0 <= max(x1,x2) :
                        if ScalarEqual(y1,y0):
                            ret[k] = True
                                     
    # inside + on Edge
    return ret
##判断点是否在多边形内部，输入点和多边形，仅适用于单个点的情况。仅适用于二维。返回True或False
def PointInPolygon2D(x0,y0,Polygon):
    """
       return value :
         True,  (XO,YO) IS LOCATED BOTH IN Polygon and ON EDGE
         False, (XO,YO) FAILS TO DO SO
    """
    if type(x0) is np.ndarray or type(y0) is np.ndarray :
        raise ValueError(f"PointInPolygon2D(x0,y0,Polygon)\n"
            "x0,y0 need be scalar value, but be given array.")

    n = len(Polygon)
    IS = 0
    for i in range(n):
        x1,y1 = Polygon[i]
        x2,y2 = Polygon[(i+1)%n]
        I = PointInSegment2D(x0,y0,x1,y1,x2,y2)
        # print(f" {loc[I]} of line = ({x1},{y1}) - ({x2},{y2})  ")
        if I == 1 :    
            IS += 1    #  x0 < x_predicted
        elif I == 2 :  # on edge
            return True
        
    ret = IS%2
    if ret == 1 :
        return True
    else:
        return False

#从点处向x轴正方向做直线，判断点的位置。服务于用于判断点是否在二维多边形内的函数，意义不大，一般不直接使用 输入为点的横纵坐标，线段两个端点的横纵坐标。
    #规定射线经过的点属于射线上的一侧
    """
    从点处向x轴正方向做射线，判断点的位置
        INTERSECTION ?
            ret=O  NO  ( no crossover point )  直线和所给线段没有交点
            ret=1  Have  ( have a crossover point,  )直线和所给线段有交点
            ret=2  YES ( ON EDGE )  点刚好在线段上
    """
    # ymin < y0 < ymax 
def PointInSegment2Dold(x0,y0,x1,y1,x2,y2):
    if ScalarEqual(max(y1,y2),y0) or ScalarEqual(min(y1,y2),y0) or ((max(y1,y2)>y0) & ( y0>min(y1,y2))):   ##    if (max(y1,y2)>=y0) & ( y0>=min(y1,y2)) :    #规定射线经过的点属于射线上的一侧
        if not ScalarEqual(y1 , y2) :   # y1 != y2 :
            if not ScalarEqual(x1, x2) : # x1 != x2 :
                x=x1+(y0-y1)*(x2-x1)/(y2-y1)   # predicted point
                if  ScalarEqual(x0, x) :  # x0 == x :
                    return 2
                
                if x0 < x :
                    if ScalarEqual(min(y1,y2) , y0):
                        return 0
                    else:
                        return 1            
                return 0
            
            else:        # vertical line
                if ScalarEqual(x0,x1) :
                    return 2
                
                elif x0 < x1 :
                    if ScalarEqual(min(y1,y2) , y0):
                        return 0
                    else:
                        return 1            

                else :               # x0 > x1 :
                    return 0
               
        else:  # horizontal line
            if not ScalarEqual(y0 , y1) :
                return 0

            elif ScalarEqual(x1,x0) or ScalarEqual(x0,x2) or max(x1,x2)>x0 and x0>min(x1,x2) :  #  y1 == y0
                return 2
    else:
        return 0

def PointInSegment2D(x0,y0,x1,y1,x2,y2):
    if ScalarEqual(max(y1,y2),y0) or ((max(y1,y2)>y0) & ( y0>min(y1,y2))):   ##    if (max(y1,y2)>=y0) & ( y0>=min(y1,y2)) :    #规定射线经过的点属于射线上的一侧
        if not ScalarEqual(y1 , y2) :   # y1 != y2 :
            x=x1+(y0-y1)*(x2-x1)/(y2-y1)   # predicted point
            if  ScalarEqual(x0, x) :  # x0 == x :
                return 2
            if x0 < x :
                return 1 
            return 0
               
        else:  # horizontal line
            if ScalarEqual(x1,x0) or ScalarEqual(x0,x2) or max(x1,x2)>x0 and x0>min(x1,x2) :  #  y1 == y0
                return 2
            return 0
    elif ScalarEqual(min(y1,y2) , y0):
        if ScalarEqual(min(y1,y2) , y1):
            if ScalarEqual(x1,x0):
                return 2
            else:
                return 0
        else:
            if ScalarEqual(x2,x0):
                return 2
            else:
                return 0
    else:
        return 0

##得到一个垂直于多边形的向量，输入为多边形Polygon 输出为垂直于多边形的单位向量
def PolygonNormal(v):
    """
       get a vector normal to the polygon 
       parameter : v
                     np.array(M,3)
    """
    #
    #   C = A x B 
    #
    A = v[1,:] - v[0,:]
    B = v[2,:] - v[1,:]
    C = Cross(A,B)
    
    return UnitVector(C)

##用于得到多边形从三维到二维对应的转换矩阵
def GetU(polygon):
    """
        Get transform matrix of a polyogn
            U = GetU(polygon)
        Parameter :
            polygon : vertices of np.array(M,3)
    """
    v = polygon 

    a = v[1,:] - v[0,:]
    b = v[2,:] - v[1,:]
    c = Cross(a,b)

    # show("a",a)
    # show("b",b)
    # show("c",c)

    #   unitary vectors 
    i = UnitVector(a)
    k = UnitVector(c)
    j = Cross(k,i)

    # show("i",i)
    # show("j",j)
    # show("k",k)

    U = np.vstack((i,j,k))

    # show('U',U)

    return U


# element-wise view factor
##用于角系数的计算（暂未应用）
def fij(P1, P2, n1, n2, A2 ):
    '''
    P1,P2 : centers of two elements, np.array([x,y,z])
    n1,n2 : unit vectors of the two elements, np.array([x,y,z])
    A2 : the area.of receiving element
    '''
    dP = P1 - P2
    S  = np.sqrt(dP.dot(dP))
    
    V12 = P2 - P1
    V21 = P1 - P2
    d1 = V12.dot(n1)
    d2 = V21.dot(n2)
    
    f12 = d1*d2*A2/( np.pi* S*S*S*S)
    
    return f12


"""
    Rapid Creation of 3D Polygons
      - Shape Functions
         (1) Input a 2D Polygon in yz Plane 
         (2) Move it to a 3D position
"""
def add_col(n, dtype=int):
    """
    It adds a column of length n
    return a column of array.
    """
    return np.reshape(np.arange(n, dtype = dtype), (n, 1))

from math import *
# 1) To create a dictionary list that holds all arguments 
#      for shapes just inputed.
__shapeInputDicts = []

def  shapeInputDict(each_shape_input):
    __shapeInputDicts.append(each_shape_input)
    return each_shape_input

@shapeInputDict
def dict_rectangle(*args):
    return {"shape":"rectangle","W":args[0],"H":args[1]}

@shapeInputDict
def dict_triangle(*args):
    return {"shape":"triangle","W" : args[0], "H" : args[1], "A" : args[2]}

@shapeInputDict
def dict_rectangleWithHole(*args):
    return {
            "shape":"rectangleWithHole",
            "W" : args[0],
            "H" : args[1], 
            "A" : args[2],
            "B" : args[3],
            "C" : args[4],
            "D" : args[5]}

@shapeInputDict
def dict_fourSided(*args):
    return {
            "shape":"fourSided","W" : args[0],
            "H" : args[1], 
            "A" : args[2],
            "B" : args[3],
            "C" : args[4]}

@shapeInputDict
def dict_fiveSided(*args):
    return {
            "shape":"fiveSided","W" : args[0],"W" : args[0],
            "H" : args[1], 
            "A" : args[2],
            "B" : args[3],
            "C" : args[4],
            "D" : args[5]}

@shapeInputDict
def dict_regularPolygon(*args):
    return {
            "n": args[0], 
            "R": args[1],
            "Center": args[2]
            }

@shapeInputDict
def dict_polygon(*args):
    # return np.array(list(map(lambda x:x,args)))
    return  np.array(list(map(lambda x:x,args[0])))


#2) to create vertices (0,y,z) for each shape
__shapeFunctions = []

def  shapeFunction(each_shape_func):
    __shapeFunctions.append(each_shape_func)
    return each_shape_func

@shapeFunction
def rectangle(*args):
    dict_rectangle(*args)
    W = args[0]
    H = args[1]
    return np.array([(0,0,0),(0,W,0),(0,W,H),(0,0,H)])

@shapeFunction
def triangle(*args):
    dict_triangle(*args)
    W = args[0]
    H = args[1] 
    A = args[2]
    return np.array([(0,0,0),(0,W,0),(0,A,H)])

@shapeFunction
def rectangleWithHole(*args):
    dict_rectangleWithHole(*args)

    W = args[0]
    H = args[1] 
    A = args[2]
    B = args[3]
    C = args[4]
    D = args[5]

    if A>0 and B>0 and (A+C)<W and (B+D)<H :
        ret = np.array([(0,0,0),(0,W,0),(0,W,H),(0,A,H),(0,A,D+B),(0,A+C,B+D),(0,A+C,B),(0,A,B),(0,A,H),(0,0,H)])

    elif A == 0.0 :
        if B == 0.0 and C < W and D < H :
            ret = np.array([(0,C,0),(0,W,0),(0,W,H),(0,0,H),(0,0,D),(0,C,D)])

        if B != 0.0 and C < W and (B+D) < H :
            ret = rectangle(W=W-C,H=H) + (0,C,0)

        if B != 0.0 and C < W and (B+D) >= H :
            ret = np.array([(0,0,0),(0,W,0),(0,W,H),(0,C,H),(0,C,B),(0,0,B)])


    elif A != 0.0 :
        if B == 0.0 and (A+C) < W and D < H :
            ret = np.array([(0,0,0),(0,A,0),(0,A,D),(0,A+C,D),(0,A+C,0),(0,W,0),(0,W,H),(0,0,H)])
                
        if B != 0.0 and (A+C) < W and (B+D) >= H :
            ret = np.array([(0,0,0),(0,W,0),(0,W,H),(0,A+C,H),(0,A+C,B),(0,A,B),(0,A,H),(0,0,H)])

        if B == 0.0 and (A+C) >= W and D < H :
            ret = np.array([(0,0,0),(0,A,0),(0,A,D),(0,A+C,D),(0,W,H),(0,0,H)])

        if B != 0.0 and (A+C) >= W and (B+D) < H :
            ret = np.array([(0,0,0),(0,W,0),(0,W,B),(0,A,B),(0,A,B+D),(0,W,B+D),(0,W,H),(0,0,H)])

        if B != 0.0 and (A+C) >= W and (B+D) >= H :
            ret = np.array([(0,0,0),(0,W,0),(0,W,B),(0,A,B),(0,A,H),(0,0,H)])

    else :
        raise ValueError(f"Incorrect inputs : W={W}, H={H}, A={A}, B={B}, C={C}, D={D}")

    return ret 

@shapeFunction
def fourSided(*args):
    dict_fourSided(*args)
    W = args[0]
    H = args[1] 
    A = args[2]
    B = args[3]
    C = args[4]
    return np.array([(0,0,0),(0,W,0),(0,A+C,H),(0,A,B)])

@shapeFunction
def fiveSided(*args):
    dict_fiveSided(*args)
    W = args[0]
    H = args[1] 
    A = args[2]
    B = args[3]
    C = args[4]
    D = args[5]
    return np.array([(0,0,0),(0,W,0),(0,W+C,D),(0,A+B,H),(0,A,H)])

@shapeFunction
def regularPolygon(*args):
    if len(args) < 3 :
        raise ValueError("arguments are : n , R, Center ")
        return
    dict_regularPolygon(*args)

    n     = args[0]
    R     = args[1] 
    Center= args[2]

    if n < 3 :
        return

    theta = pi/n
    s = R * sin(theta)
    a = R * cos(theta)

    theta = 2*pi/n
    vertices = []
    for i in range(n):
        angle = i * theta
        x = 0.0
        y = R * cos(angle)
        z = R * sin(angle)
        vertices.append((x,y,z))

    return np.array(vertices)  #,s,a

@shapeFunction
def polygon(*args):
    value = args[0]
    if isinstance(value,list):
        vertices = np.array(value)
    elif isinstance(value,np.ndarray) :
        vertices = value
    else :
        raise ValueError('CoreUtils.polygon needs a list/np.array for vertices')

    dict_polygon(*args)

    if vertices.shape[1] == 2:
    # from Utilities import add_col
        vertices = np.hstack((add_col(vertices.shape[0])*0, vertices))

    # return np.array(list(map(lambda x:x,args)))
    return np.array(vertices)
    

# create a namelist of these function
__shapeNames = [func.__name__ for func in __shapeFunctions ]

def createShape(shapeName,*args):
    name = [x.lower() for x in __shapeNames]
    i = name.index(shapeName.lower())
    __shapeInputDicts[i](*args)
    return __shapeFunctions[i](*args)

def shapes():
    for each in __shapeNames:
        print(each)

def getShapeInputDict(shapeName,*args):
    name = [x.lower() for x in __shapeNames]
    i = name.index(shapeName.lower())
    return __shapeInputDicts[i](*args)

# For a 2D shape created at the initial position,
# one can move it to a desired position by a matrix below
def tranMatrix(alpha, beta):
    al = radians(alpha)
    be = radians(beta)
    X = [cos(be)*cos(al), -sin(al), -sin(be)*cos(al)]
    Y = [cos(be)*sin(al),  cos(al), -sin(be)*sin(al)]
    Z = [sin(be), 0, cos(be)]
    return np.vstack([X,Y,Z])

# move from the intial position to a desired position
def move(shape = rectangle(1.0,1.0), reference = (0.0,0.0,0.0), to = (0.0,0.0,0.0), by = (30.0,0.0)):
    (alpha, beta) = by
    # Comment them out for fast run
    # if (type(shape) is list) or type(shape) is tuple:
    #     vertices = np.array(shape)
    # elif type(shape) is np.ndarray :
    #     vertices = shape
    # else :
    #     raise ValueError('move() needs a list/np.array for a polygon')

    vertices = shape
    if vertices.shape[1] == 2:
        vertices = np.hstack((add_col(vertices.shape[0])*0, vertices))
    
    facet = vertices.transpose() 

    R1 = np.array(reference).reshape(-1,1) 
    R2 = np.array(to).reshape(-1,1)
    dR = R2 - R1

    U = tranMatrix(alpha,beta)
    facet_new = U.dot(facet) + dR

    return facet_new.transpose()

#
#  Demo how to use them
#
def test_PointsInPolygon2D():
    P = [(7,8),(6.5,7.7),(10,5),(10,11),(7,13),(6,-1),(5,5),(10,10),(10,5),(5,10)]
    vertices = [(5,5),(5,10),(10,10),(10,5)]

    Points = np.array(P)
    polygon = np.array(vertices)
    ret = PointsInPolygon2D(Points, polygon)
    print(ret)
    print(Points[ret])

def test_PointsInPath2D():
    P = [(7,8),(6.5,7.7),(10,5),(10,11),(7,13),(6,-1),(5,5),(10,10),(10,5),(5,10)]
    vertices = [(5,5),(5,10),(10,10),(10,5)]
    Points = np.array(P)
    polygon = np.array(vertices)
    ret = PointsInPolygon2D(P, polygon, Method = 'Matplotlib')
    print(ret)
    print(Points[ret])

def main():
    test_PointsInPolygon2D()
    test_PointsInPath2D()

if __name__ == '__main__':
    main()
