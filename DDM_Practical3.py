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
    
    size = subdivisions(n, s)
    print(size)
    sizelist = [x * 1/size for x in range(0, size + 1)]
    print("Length:" + str(len(sizelist)))
    print(sizelist)

    new_mesh = []
    for v in range(len(sizelist)):
        for u in range(len(sizelist)):
            point_u_v = (0, 0, 0)
            for i in range(n):
                Bernstein_iu = (math.factorial(n) / (math.factorial(i) * math.factorial(n - i))) * math.pow(sizelist[u],i) * math.pow((1 - sizelist[u]), (n - i))
                for j in range(n):
                    Bernstein_jv = (math.factorial(n) / (math.factorial(j) * math.factorial(n - j))) * math.pow(sizelist[v],j) * math.pow((1 - sizelist[v]), (n - j))
                    point_u_v = tuple([tup + Bernstein_iu * Bernstein_jv * tup for tup in get_point(i,j)])
            new_mesh.append(point_u_v)
            print(point_u_v)
    print("Length of new_mesh: " + str(len(new_mesh)))
    print(sizelist)
    return new_mesh

#This here is my previous method which sucks
"""     for y in range(n):
        points = A[n * y:n * y + n].copy()
        new_mesh.append(points[0])
        for i in range((n - 1) * (s + 1) - 1):
            u = (i + 1) / ((n-1) * (s+1) - 1)
            u_points = points.copy()
            while len(u_points) > 1:
                for j in range(len(u_points) - 1):
                    u_points[j] = u_points[j] + u * (u_points[j+1] - u_points[j])
                u_points.pop()
            new_mesh.append(u_points[0])
        new_mesh.append(points.pop())
    
    for x in range((n - 1 ) * (s + 1) + 1):
        points = []
        for p in range(n):
            points.append(x + p * ((n - 1 ) * (s + 1) + 1))
        for i in range((n - 1) * (s + 1) - 1):
            u = (i + 1) / ((n-1) * (s+1) - 1)
            u_points = points.copy()
            while len(u_points) > 1:
                for j in range(len(u_points) - 1):
                    u_points[j] = u_points[j] + u * (u_points[j+1] - u_points[j])
                u_points.pop()
            if (i+1) % (s+1) == 0:

            new_mesh.insert(u_points[0])
        new_mesh.append(points.pop())
         """

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
    return False
    
def subdivisions(n, s):
    return (n - 1) * (s + 1) + 1
    
def DDM_Practical3(context):
    print ("DDM Practical 3")
    n = 10
    length = 10
    s = 3
    
    A = control_mesh(n, length)

    show_mesh(mesh_from_array(A, n))
    B = De_Casteljau(A, n, s)
    
    n_B = subdivisions(n, s) + 1
    
    
    show_mesh(mesh_from_array(B, n_B))
    
    p1 = (1,2,3)
    p2 = (3,4,5)
    
    print(line_intersect(A, n, p1, p2, 0.01))
    
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