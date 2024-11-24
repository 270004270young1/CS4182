from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import ImportObject

class street_lamp:
    obj = 0
    displayList = 0
    
    posX = 0.0
    posY = 0.0
    posZ = 0.0

    sizeX = 1
    sizeY = 0.7
    sizeZ = 1

    rotation = 0.0  # Rotation angle around the Y-axis
    
    def __init__(self, x, z):
        self.obj = ImportObject.ImportedObject("./objects/LAMP_OBJ")
        self.posX = x
        self.posZ = z
        self.posY = 0  # Assuming the human stands on the ground level

        # Set the rotation so the human faces the road
        # Assuming the road is along the positive Z-axis at x = 0
        # self.rotation = 0


    def makeDisplayLists(self):
        self.obj.loadOBJ()

        self.displayList = glGenLists(1)
        glNewList(self.displayList, GL_COMPILE)
        self.obj.drawObject()
        glEndList()
    
    def draw(self):
        glPushMatrix()
        
        # Apply transformations in the correct order:
        # 1. Translate to position
        # 2. Rotate to face the road
        # 3. Scale to desired size

        glTranslatef(self.posX, self.posY, self.posZ)
        # glRotatef(self.rotation, 0.0, 1.0, 0.0)  # Rotate around Y-axis
        glScalef(self.sizeX, self.sizeY, self.sizeZ)

        glCallList(self.displayList)
        glPopMatrix()
