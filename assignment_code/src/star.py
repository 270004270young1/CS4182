from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, time
import ImportObject
from path import get_resource_path

class star:
    obj = 0
    displayList = 0
    
    posX = 0.0
    posY = 0.0
    posZ = 0.0

    sizeX = 5.0
    sizeY = 5.0
    sizeZ = 5.0

    rotation = 0.0
    
    def __init__(self, x, y, z):
        self.obj = ImportObject.ImportedObject(get_resource_path("objects/star"))
        self.posX = x
        self.posZ = z
        self.posY = y
        
    def makeDisplayLists(self):
        self.obj.loadOBJ()

        self.displayList = glGenLists(1)
        glNewList(self.displayList, GL_COMPILE)
        self.obj.drawObject()
        glEndList()
    
    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.posX,self.posY,self.posZ)
        #glRotatef(self.rotation,0.0,1.0,0.0)
        glScalef(self.sizeX,self.sizeY,self.sizeZ)

        glCallList(self.displayList)
        glPopMatrix()
