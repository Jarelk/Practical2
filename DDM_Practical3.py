# File created on: 2018-05-08 15:24:47.264919
#
# IMPORTANT:
# ----------
# - Before making a new Practical always make sure you have the latest version of the addon!
# - Delete the old versions of the files in your user folder for practicals you want to update (make a copy of your work!).
# - For the assignment description and to download the addon, see the course website at: http://www.cs.uu.nl/docs/vakken/ddm/
# - Mail any bugs and inconsistencies you see to: uuinfoddm@gmail.com
# - Do not modify any of the signatures provided.
# - You may add as many functions to the assignment as you see fit but try to avoid global variables.

import ddm
import bpy
import numpy
import math
import mathutils

# To view the printed output toggle the system console in "Window -> Toggle System Console"

# A(rray) = z-values for xy-pairs; format: [(x1y1, x1y2, x1y3, ...), (x2y1, x2y2, x2y3, ...), ...]

def mesh_from_array(A, n):
    def get_point(ax, ay):
        return A[ax + ay * n]

    quads = []
    for x in range(n - 1):
        for y in range(n - 1):
            point1 = get_point(x, y)
            point2 = get_point(x + 1, y)
            point3 = get_point(x + 1, y + 1)
            point4 = get_point(x, y + 1)
            quads.append( (point4, point3, point2, point1) )
            
    
    return quads
        
    
def De_Casteljau(A, n, s):
    def get_point(ax, ay):
        return A[ax + ay * n]

    new_mesh = [0 for i in range(n * ((n-1) * (s + 1) + 1))]
    #print(len(new_mesh))
    for x in range(n):
        points = []
        for p in range(n):
            points.append(get_point(x, p))
        #print("Points for iteration " + str(x))
        #print(points)
        new_mesh[x] = points[0]
        for i in range((n - 1) * (s + 1) - 1):
            u = (i + 1) / ((n-1) * (s+1) - 1)
            u_points = list(points)
            #print(u_points)
            while len(u_points) > 1:
                for j in range(len(u_points) - 1):
                    u_points[j] = (u_points[j][0] + u * (u_points[j+1][0] - u_points[j][0]), u_points[j][1] + u * (u_points[j+1][1] - u_points[j][1]), u_points[j][2] + u * (u_points[j+1][2] - u_points[j][2]))
                u_points.pop()
            #print("Replacing point at index " + str((i + 1) * n + x))
            #print("Replacing with " + str(u_points[0]))
            new_mesh[(i + 1) * n + x] = u_points[0]
        #print("Replacing point at index " + str((n-1) * (s+1) * n + x))
        #print("Replacing with " + str(u_points[len(u_points) - 1]))
        new_mesh[(n-1) * (s+1) * n + x] = points.pop()
    
    #print(new_mesh)
    new_range = int(len(new_mesh) / n)
    new_mesh2 = []

    for y in range(new_range):
        points = new_mesh[n * y:n * y + n].copy()
        new_mesh2.append(points[0])
        for i in range((n - 1) * (s + 1) - 1):
            u = (i + 1) / ((n-1) * (s+1) - 1)
            u_points = points.copy()
            while len(u_points) > 1:
                for j in range(len(u_points) - 1):
                    u_points[j] = (u_points[j][0] + u * (u_points[j+1][0] - u_points[j][0]), u_points[j][1] + u * (u_points[j+1][1] - u_points[j][1]), u_points[j][2] + u * (u_points[j+1][2] - u_points[j][2]))
                u_points.pop()
            new_mesh2.append(u_points[0])
        new_mesh2.append(points.pop())

    return new_mesh2
        

def control_mesh(n, length):
    array = []
    unit = length / (n-1)
    maxPoint = (length, length)
    for x in range(n):
        for y in range(n):
            z = 0
            if x != 0 and x != n - 1 and y != 0 and y != n - 1:
                x2 = x - n / 2
                y2 = y - n / 2
                z = (x2 * x2 * y2 * y2) / (n * n) + 0.2
            point = (x * unit, y * unit, z * length * 0.1)
            array.append(point)
    return array
    
def line_intersect(A, n, p1, p2, e):
    p1x = p1[0] + 10 * (p1[0] - p2[0])
    p1y = p1[1] + 10 * (p1[1] - p2[1])
    p1z = p1[2] + 10 * (p1[2] - p2[2])
    p2x = p2[0] + 10 * (p2[0] - p1[0])
    p2y = p2[1] + 10 * (p2[1] - p1[1])
    p2z = p2[2] + 10 * (p2[2] - p1[2])
    p1 = (p1x, p1y, p1z)
    p2 = (p2x, p2y, p2z)
    def distanceSQR(po1, po2):
        (x1, y1, z1) = po1
        (x2, y2, z2) = po2
        return (x1 * x2 + y1 * y2 + z1 * z2)
    def get_point(ax, ay):
        return A[ax + ay * n]
        return (a1 * b1 + a3 * b3)
    def intersect(pA, pn, pe, minX, maxX, minY, maxY):
        for x in range(minX, maxX):
            for y in range(minY, maxY):
                (a, b) = (get_point(x, y), get_point(x + 1, y))
                a2 = (a[1], a[2])
                b2 = (b[1], b[2])
                p12 = (p1[1], p1[2])
                p22 = (p2[1], p2[2])
                intPoint = mathutils.geometry.intersect_line_line_2d(a2, b2, p12, p22)
                # check intersection and bounding box
                if intPoint != None:
                    # intersection at this y-curve, so check corresponding x-curve
                    for xx in range(minX, maxX):
                        (a, b) = (get_point(xx, y), get_point(xx, y + 1))
                        a2 = (a[0], a[2])
                        b2 = (b[0], b[2])
                        p12 = (p1[0], p1[2])
                        p22 = (p2[0], p2[2])
                        intPoint2 = mathutils.geometry.intersect_line_line_2d(a2, b2, p12, p22)
                        if intPoint2 != None:
                            # intersection
                            iPoint = (intPoint2[0], intPoint[0], intPoint[1])
                            print ("intersect at ca.", iPoint, intPoint2[1])
                            return iPoint
        return None
    
    length = get_point(n - 1, n - 1)[0]
    minX = 0
    maxX = n - 1
    minY = 0
    maxY = n - 1
    for i in range(10):
        iPoint = intersect(A, n, e, minX, maxX, minY, maxY)
        print("e", length / n)
        if iPoint != None:
           # currE = min(distanceSQR(iPoint, 
            if length / n * 0.5 < e:
                # precise enough
                return True
            # might intersect, so subdiv and try again
            A = De_Casteljau(A, n, 1)
            old_n = n
            n = subdivisions(n, 1)
            
            minX = math.floor(iPoint[0] / old_n * n) - 3
            maxX = math.floor(iPoint[0] / old_n * n) + 4
            minY = math.floor(iPoint[1] / old_n * n) - 3
            maxY = math.floor(iPoint[1] / old_n * n) + 4
        else:
            #guaranteed no intersection, so return False
            return False
    # give up, and return false
    return False
    
def subdivisions(n, s):
    return (n - 1) * (s + 1) + 1
    
def DDM_Practical3(context):
    print ("DDM Practical 3")
    n = 10
    length = 9
    s = 1
    
    A = control_mesh(n, length)

    #show_mesh(mesh_from_array(A, n))
    B = De_Casteljau(A, n, s)
    
    n_B = subdivisions(n, s)
    #print("n_B size: " + str(n_B))
    
    show_mesh(mesh_from_array(B, n_B))
    
    p1 = (1, 2, 2)
    p2 = (1, 2, 0)
    
    print("lineIntersect:", line_intersect(B, n_B, p1, p2, 0.1))
    
# Builds a mesh using a list of triangles
# This function is the same as the previous practical
def show_mesh(triangles):
    
    me = bpy.data.meshes.new("Mesh")
    ob = bpy.data.objects.new("mesh", me)
    bpy.context.scene.objects.link(ob)
    
    edges = []
    faces = []
    verts = []
    
    for quad in triangles:
        verts_indices = [0, 0, 0, 0]
        for j in range(4):
            if quad[j] not in verts:
                verts_indices[j] = len(verts)
                verts.append(quad[j])
            else:
                verts_indices[j] = verts.index(quad[j])
        faces.append( tuple(verts_indices) )
    
    #for triangle in triangles:
    #    for j in range(0, 3):
    #        verts.append(triangle[j])
    #    faces.append( (i, i+1, i+2) )  
    #    i += 3
 
    # Create mesh from given verts, edges, faces. Either edges or
    # faces should be [], or you ask for problems
    me.from_pydata(verts, edges, faces)
    return