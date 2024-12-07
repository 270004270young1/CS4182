from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import ImportObject
from path import get_resource_path

class male:
    obj = 0
    displayList = 0
    
    posX = 0.0
    posY = 0.0
    posZ = 0.0

    sizeX = 1.0
    sizeY = 1.0
    sizeZ = 1.0

    rotation = 0.0  # Rotation angle around the Y-axis
    
    def __init__(self, x, z):
        self.obj = ImportObject.ImportedObject(get_resource_path("objects/Male"))
        self.posX = x
        self.posZ = z
        self.posY = 0.0  # Assuming the human stands on the ground level

        # Set the rotation so the human faces the road
        # Assuming the road is along the positive Z-axis at x = 0
        self.rotation = -90

    def calculateRotationAngle(self):
        # Calculate the angle to rotate so the human faces the road
        # Assuming the road is at x = 0
        dx = -self.posX  # Difference in X from human to road center
        dz = 0  # Road is along Z-axis, so Z difference is zero

        # If dx is zero, set rotation to 0 or 180 degrees depending on position
        if dx == 0:
            return 0.0 if self.posX >= 0 else 180.0

        # Calculate angle in radians
        angle_radians = math.atan2(dz, dx)
        # Convert to degrees and adjust
        angle_degrees = math.degrees(angle_radians)
        # Adjust angle since OpenGL rotates counter-clockwise
        return angle_degrees

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
        glRotatef(self.rotation, 0.0, 1.0, 0.0)  # Rotate around Y-axis
        glScalef(self.sizeX, self.sizeY, self.sizeZ)

        glCallList(self.displayList)
        glPopMatrix()
