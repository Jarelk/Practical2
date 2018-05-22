# File created on: 2018-05-08 15:24:47.263919
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
import sys
import math
from numpy.polynomial.polynomial import polyvander3d
from mathutils import Vector
from numpy import empty as new_Matrix
from numpy import matrix as Matrix
from math import sqrt

# You can perform the marching cubes algorithm by first constructing an instance of the marching cubes class:
#
# mc = My_Marching_Cubes()
#
# and then calling the calculate function for this class:
#
# mc.calculate(origin_x, origin_y, origin_z, x_size, y_size, z_size, cube_size)
#
# Where:
# - (origin_x, origin_y, origin_z) is the bottom left coordinate of the area meshed by marching cubes
# - (x_size, y_size, z_size) is the number of cubes in each direction
# - cube_size is the length of the edge of a single cube
#
class My_Marching_Cubes(ddm.Marching_Cubes):
    # You may place extra members and functions here
    
    def __init__(self, points, normals, epsilon, radius, wendland_constant, degree):
        super().__init__()
        
        # Build a dictionary for getting the normals
        self.point_normal = {}
        for i in range(len(points)):
            self.point_normal[ (points[i][0], points[i][1], points[i][2]) ] = normals[i]
        
        # Do NOT modify these parameter values within this class
        self.epsilon = epsilon
        self.radius = radius
        self.degree = degree
        self.wendland_constant = wendland_constant
        
        
        self.grid = ddm.Grid(points)        
    
    # Returns the normals belonging to a given (sub)set of points
    def normals_for_points(self, points):
        result = []
        for point in points:
            result.append(self.point_normal[(point[0], point[1], point[2])])
        return result

    # Queries the grid for all points around q within radius
    def query_points(self, q, radius):
        result = []
        for point in self.grid.query(q, radius):
            result.append(Vector(point))
        return result
    
    # This function returns the result of estimated function f(q) which is essentially the entire estimation plus the calculation of its result, note that the estimated polynomial is different for every q = (x, y, z)
    def sample(self, x, y, z):
        
        q = Vector([x, y, z])
        
        # TODO: make sure that your radial query always contains enough points to a) ensure that the MLS is well defined, b) you always know if you are on the inside or outside of the object.
        query = self.query_points( q, self.radius)
        normals = self.normals_for_points(query)
        
        constraints = constraint_points(query, normals, self.epsilon, self.radius)
        c = MatrixC(q, constraints, self.degree)
        
        return distance(Vector([0, 0, 0]), Vector([x, y, z])) - 1
        
        
# This function is called when the DDM Practical 2 operator is selected in Blender.
def DDM_Practical2(context):

    # TODO: modify this function so it performs reconstruction on the active point cloud
    print("MLS")
    points = get_vertices(context)
    normals = get_normals(context)
    epsilon = get_epsilon(points)
    radius = get_radius(points)
    wendland_constant = 0.1
    degree = get_degree()
    
    mc = My_Marching_Cubes(points, normals, epsilon, radius, wendland_constant, degree)
    
    triangles = mc.calculate(-1, -1, -1, 20, 20, 20, 0.1)
    
    show_mesh(triangles)

    
#########################################################################
# You may place extra variables and functions here to keep your code tidy
#########################################################################


# Returns the points of the first object
def get_vertices(context):
    result = []
    for vertex in context.active_object.data.vertices:
        result.append( Vector(vertex.co) )

    return result

# Returns the normals of the first object
def get_normals(context):
    if ('surface_normals' not in context.active_object):
        print("\n\n##################\n\nWARNING:\n\nThis object does not contain any imported surface normals! Please use one of the example point clouds provided with the assignment.\n\n##################\n\n")
        return []

    result = []

    for normal in context.active_object['surface_normals']:
        result.append( Vector( [normal[0], normal[1], normal[2] ] ) )

    return result

# Returns an query radius for the given point set
def get_radius(points):
    (b, t) = bounding_box(points)
    return 0.1 

# Returns the epsilon for the given point set
def get_epsilon(points):
    (b, t) = bounding_box(points)
    return 0.01 * distance(b, t)
    
# Returns the degree 'k' used in this reconstruction
def get_degree():
    return 2
    
# Returns the minimum and the maximum corner of a point set
def bounding_box(points):
    
    bottom = Vector([0, 0, 0])
    top = Vector([0, 0, 0])
    for p in points:
        for i in [0, 1, 2]:
            if p[i] < bottom[i]:
                bottom[i] = p[i]
            if p[i] > bottom[i]:
                top[i] = p[i]
            
    return (bottom, top)
    
# The vector containing the values for '{c_m}'
def constraint_points(points, normals, epsilon, radius):
    
    column = []
    for i in range(len(points)):
        p = points[i]
        n = normals[i]
        
        column.append(p)
        column.append(p + epsilon * n)
        column.append(p - epsilon * n)
    
    return column

# The vector 'd'
def constraint_values(points, normals, epsilon, radius):
    
    d = []
    for p in points:
        d.append (0)
        d.append ( epsilon)
        d.append (-epsilon)
    
    return d
    
# The vector (NOT matrix) 'W'
def weights(q, constraints, wendland_constant):
    
    w = []
    for c in constraints:
        d = distance(q, c)
        w_c = Wendland(d, wendland_constant)
    
    return w

# The vector that contains the numerical values of each term of the polynomial, this is NOT vector 'a'
def indeterminate(q, degree):
    return polyvander3d(q[0], q[1], q[2], [degree, degree, degree] )[0]

# For a given list of coefficients a, use this to find the actual value for 'f(p)'
def polynomial(p, a, degree):
    
    # TODO: Implement
    
    return 0
    
# Returns 'C'
# NOTE: There is no need for this function to be passed the parameters 'wendland_constant', 'epsilon' and 'radius', you can structure the assignment in such a way this is not necessary.
def MatrixC(q, constraints, degree):    
    
    # TODO: Implement
    
    return new_Matrix([1, 1])
    
# Returns the Wendland weight for a given distance with shape/range parameter wendland_constant
def Wendland(distance, wendland_constant):
    
    r_over_h = distance / wendland_constant
    
    a1 = (1 - r_over_h)
    a2 = a1 * a1
    a4 = a2 * a2
    
    b = 4 * r_over_h + 1
    
    return a4 * b

# Returns the distance between vector 'a' and 'b'
def distance(a, b):
    return (b - a).length

# Builds a mesh using a list of triangles
# This function is the same as from the previous practical
def show_mesh(triangles):
    
    me = bpy.data.meshes.new("Mesh")
    ob = bpy.data.objects.new("mesh", me)
    bpy.context.scene.objects.link(ob)
    
    edges = []
    faces = []
    verts = []
    i = 0
    for triangle in triangles:
        for j in range(0, 3):
            verts.append(triangle[j])
        faces.append( (i, i+1, i+2) )  
        i += 3
 
    # Create mesh from given verts, edges, faces. Either edges or
    # faces should be [], or you ask for problems
    me.from_pydata(verts, edges, faces)
    return
