import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileShader, compileProgram
from jeep import jeep   

# Shader sources
vertex_shader_src = open("./src/vertex.glsl").read()
fragment_shader_src = open("./src/fragment.glsl").read()

shader_program = None
jeepObj = jeep("r")

jeepVert = []
jeepNorm = []

# Cube vertices (position + normal)
vertices = np.array([
    # Positions          Normals
    -0.7, -0.7, -0.7,    0.0,  0.0, -1.0,
     0.7, -0.7, -0.7,    0.0,  0.0, -1.0,
     0.7,  0.7, -0.7,    0.0,  0.0, -1.0,
    -0.7,  0.7, -0.7,    0.0,  0.0, -1.0,
    # Additional vertices for other faces...
], dtype=np.float32)

indices = np.array([
    0, 1, 2, 2, 3, 0,  # Front face
    # Additional indices for other faces...
], dtype=np.uint32)



vertices2 = np.array([
    # Positions          Normals
    -0.5, -0.5, -0.7,    0.0,  0.0, -1.0,
    0.7, -0.7, -0.7,    0.0,  0.0, -1.0,
    0.5, 1.0, -0.7,    0.0,  0.0, -1.0
    # Additional vertices for other faces...
], dtype=np.float32)

indices2 = np.array([
    0,1,2  # Front face
    # Additional indices for other faces...
], dtype=np.uint32)
VAO = None
VBO = None
EBO = None
VAO2 = None
VBO2 = None
EBO2 = None

def init():
    global shader_program, VAO, VBO, EBO, VBO2, EBO2, VAO2

    # Compile shaders
    shader_program = compileProgram(
        compileShader(vertex_shader_src, GL_VERTEX_SHADER),
        compileShader(fragment_shader_src, GL_FRAGMENT_SHADER)
    )

    # Generate VAO and VBO
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)
    
    
    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    
    # Vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Vertex normals
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * vertices.itemsize, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    VAO2 = glGenVertexArrays(1)
    VBO2 = glGenBuffers(1)
    EBO2 = glGenBuffers(1)
    glBindVertexArray(VAO2)

    glBindBuffer(GL_ARRAY_BUFFER, VBO2)
    glBufferData(GL_ARRAY_BUFFER, vertices2.nbytes, vertices2, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO2)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices2.nbytes, indices2, GL_STATIC_DRAW)

    # Vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * vertices2.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Vertex normals
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * vertices2.itemsize, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    glBindVertexArray(0)

    glEnable(GL_DEPTH_TEST)

def display():
    global jeepObj
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(shader_program)

    # Set uniforms
    model_loc = glGetUniformLocation(shader_program, "model")
    view_loc = glGetUniformLocation(shader_program, "view")
    proj_loc = glGetUniformLocation(shader_program, "projection")
    light_pos_loc = glGetUniformLocation(shader_program, "lightPos")
    view_pos_loc = glGetUniformLocation(shader_program, "viewPos")
    light_color_loc = glGetUniformLocation(shader_program, "lightColor")
    object_color_loc = glGetUniformLocation(shader_program, "objectColor")

    model = np.identity(4, dtype=np.float32)
    view = np.identity(4, dtype=np.float32)
    projection = np.identity(4, dtype=np.float32)
    light_pos = np.array([0.0, 1.0, 1.5], dtype=np.float32)
    view_pos = np.array([0.0, 5.0, 10.0], dtype=np.float32)
    light_color = np.array([1.0, 1.0, 1.0], dtype=np.float32)
    object_color = np.array([1.0, 0.5, 0.3], dtype=np.float32)

    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniform3fv(light_pos_loc, 1, light_pos)
    glUniform3fv(view_pos_loc, 1, view_pos)
    glUniform3fv(light_color_loc, 1, light_color)
    glUniform3fv(object_color_loc, 1, object_color)

    # Render cube
    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

    # glBindVertexArray(VAO2)

    # glDrawElements(GL_TRIANGLES, len(indices2), GL_UNSIGNED_INT, None)
    
    # glDrawElements(GL_TRIANGLES, len(indices2), GL_UNSIGNED_INT, None)
    # glDrawElements(GL_TRIANGLES, len(indices2), GL_UNSIGNED_INT, None)
    # glDrawArrays(GL_TRIANGLES,0,1)

    # jeepObj.posZ = 20.0
    # jeepObj.posX = 20.0
    # jeepObj.posY = 20.0
    
    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    # gluPerspective(90, 1, 0.1, 100)
    # gluLookAt(0,5,10, jeepObj.posX,jeepObj.posY,jeepObj.posZ,0,1,0)
    # glMatrixMode(GL_MODELVIEW)
    # glutPostRedisplay()
    # jeepObj.draw()
    # jeepObj.drawW1()
    # jeepObj.drawW2()
    # jeepObj.drawLight()

    


    glutSwapBuffers()

def setupJeep():
    global jeepObj,jeepVert, jeepNorm
    for face in jeepObj.obj.faces:
            ## Check if a material
            if face[0] == -1:
               self.setModelColor(face[1])
            else:
               
               ## drawing normal, then texture, then vertice coords.  
               for f in face:
                   norm = []
                   vert = []
                   if f[2] != -1:
                       norm.append(jeepObj.obj.norms[f[2]][0])
                       norm.append(jeepObj.obj.norms[f[2]][1])
                       norm.append(jeepObj.obj.norms[f[2]][2])
              
                   vert.append(jeepObj.obj.verts[f[0]][0])
                   vert.append(jeepObj.obj.verts[f[0]][1])
                   vert.append(jeepObj.obj.verts[f[0]][2])

def main():
    global jeepObj
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Phong Shading with Normal Interpolation")
    jeepObj.makeDisplayLists()

    # setupJeep()

    glutDisplayFunc(display)

    init()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.1, 100)
    gluLookAt(0,5,10, jeepObj.posX,jeepObj.posY,jeepObj.posZ,0,1,0)
    glMatrixMode(GL_MODELVIEW)
    glutPostRedisplay()
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    # glEnable(GL_LIGHTING)
    # glEnable(GL_LIGHT0)
    # glEnable(GL_DEPTH_TEST)
    # glEnable(GL_NORMALIZE)
    
    glClearColor(0.1, 0.1, 0.1, 0.0)
    glutMainLoop()

if __name__ == "__main__":
    main()
