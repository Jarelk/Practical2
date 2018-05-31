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

    new_mesh = []
    for x in range(n-1):
        for y in range(n-1):
            (p1x, p1y, p1z) = get_point(x, y)
            (p2x, p2y, p2z) = get_point(x, y+1)
            new_point = ((p1x + p2x) / 2, (p1y + p2y) / 2, (p1z + p2z) / 2)
            new_mesh.append(new_point)
    print("Casteljau:", new_mesh)
    return new_mesh

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
    return 1
    
def DDM_Practical3(context):
    print ("DDM Practical 3")
    n = 10
    length = 10
    s = 3
    
    A = control_mesh(n, length)
    B = De_Casteljau(A, n, s)
    
    # TODO: Calculate the new size of the subdivided surface
    n_B = subdivisions(1, s)
    
    #show_mesh(mesh_from_array(A, n))
    
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