import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import compileShader, compileProgram

# Data for object 1 (triangle)
triangle_vertices = np.array([
    # Positions        # Colors
    0.0,  0.5, 0.0,   1.0, 0.0, 0.0,  # Top (red)
   -0.5, -0.5, 0.0,   0.0, 1.0, 0.0,  # Bottom left (green)
    0.5, -0.5, 0.0,   0.0, 0.0, 1.0   # Bottom right (blue)
], dtype=np.float32)

triangle_indices = np.array([0, 1, 2], dtype=np.uint32)

# Data for object 2 (rectangle)
rectangle_vertices = np.array([
    # Positions        # Colors
    -0.5,  0.5, 0.0,   1.0, 1.0, 0.0,  # Top left (yellow)
     0.5,  0.5, 0.0,   1.0, 0.0, 1.0,  # Top right (magenta)
     0.5, -0.5, 0.0,   0.0, 1.0, 1.0,  # Bottom right (cyan)
    -0.5, -0.5, 0.0,   1.0, 1.0, 1.0   # Bottom left (white)
], dtype=np.float32)

rectangle_indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

# VAO, VBO, EBO for the triangle
triangle_vao = glGenVertexArrays(1)
triangle_vbo = glGenBuffers(1)
triangle_ebo = glGenBuffers(1)

glBindVertexArray(triangle_vao)

glBindBuffer(GL_ARRAY_BUFFER, triangle_vbo)
glBufferData(GL_ARRAY_BUFFER, triangle_vertices.nbytes, triangle_vertices, GL_STATIC_DRAW)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, triangle_ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, triangle_indices.nbytes, triangle_indices, GL_STATIC_DRAW)

# Define vertex attributes (position: location 0, color: location 1)
stride = 6 * triangle_vertices.itemsize
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * triangle_vertices.itemsize))
glEnableVertexAttribArray(1)

glBindVertexArray(0)  # Unbind VAO

# VAO, VBO, EBO for the rectangle
rectangle_vao = glGenVertexArrays(1)
rectangle_vbo = glGenBuffers(1)
rectangle_ebo = glGenBuffers(1)

glBindVertexArray(rectangle_vao)

glBindBuffer(GL_ARRAY_BUFFER, rectangle_vbo)
glBufferData(GL_ARRAY_BUFFER, rectangle_vertices.nbytes, rectangle_vertices, GL_STATIC_DRAW)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, rectangle_ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, rectangle_indices.nbytes, rectangle_indices, GL_STATIC_DRAW)

# Define vertex attributes (position: location 0, color: location 1)
stride = 6 * rectangle_vertices.itemsize
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * rectangle_vertices.itemsize))
glEnableVertexAttribArray(1)

glBindVertexArray(0)  # Unbind VAO

# Render loop
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw the triangle
    glBindVertexArray(triangle_vao)
    glDrawElements(GL_TRIANGLES, len(triangle_indices), GL_UNSIGNED_INT, None)

    # Draw the rectangle
    glBindVertexArray(rectangle_vao)
    glDrawElements(GL_TRIANGLES, len(rectangle_indices), GL_UNSIGNED_INT, None)

    glutSwapBuffers()

# Initialize GLUT
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Multiple Objects with VAO, VBO, EBO")
glutDisplayFunc(display)

# Set background color
glClearColor(0.2, 0.3, 0.3, 1.0)

glutMainLoop()
