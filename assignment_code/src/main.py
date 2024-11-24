#!/usr/bin/env python
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, time, random, csv, datetime
import ImportObject
import PIL.Image as Image
import jeep, cone
from star import star
from diamond import diamond

# Light type identifiers
AMBIENT = 0
POINT = 1
DIRECTIONAL = 2
SPOTLIGHT = 3

currentLightType = AMBIENT  # Default light type

isFullScreen = False
windowWidth = 600
windowHeight = 600
isResizing = False  # Track if the user is resizing the window
resizeStartX = 0    # Initial X position when resizing starts
resizeStartY = 0    # Initial Y position when resizing starts

windowSize = 600
helpWindow = False
helpWin = 0
mainWin = 0
centered = True

beginTime = 0
countTime = 0
score = 0
finalScore = 0
canStart = False
overReason = ""

# For wheel spinning
tickTime = 0

# Creating objects
objectArray = []
jeep1Obj = jeep.jeep('p')
jeep2Obj = jeep.jeep('g')
jeep3Obj = jeep.jeep('r')

allJeeps = [jeep1Obj, jeep2Obj, jeep3Obj]
jeepNum = 0
jeepObj = allJeeps[jeepNum]
# personObj = person.person(10.0,10.0)

# Concerned with camera
eyeX = 0.0
eyeY = 2.0
eyeZ = 10.0
midDown = False
topView = False
behindView = False

# Concerned with panning
nowX = 0.0
nowY = 0.0
jeepPastZ = 0
ribbonZ = 40.0
speed = 1.0

angle = 0.0
radius = 10.0
phi = 0.0
rotation = 0.0

# Concerned with scene development
land = 20
gameEnlarge = 10

# Concerned with obstacles (cones) & rewards (stars)
coneAmount = 15
starAmount = 5 #val = -10 pts
diamondAmount = 1 #val = deducts entire by 1/2
# diamondObj = diamond.diamond(random.randint(-land, land), random.randint(10.0, land*gameEnlarge))
usedDiamond = False

allcones = []
allstars = []
obstacleCoord = []
rewardCoord = []
ckSense = 5.0

# Concerned with lighting
applyLighting = True  # Set to True to enable lighting

fov = 30.0
attenuation = 1.0

# Updated light position to be consistent across modes
light0_Position = [0.0, 10.0, 10.0, 1.0]
light0_Intensity = [1.0, 1.0, 1.0, 1.0]

matAmbient = [0.2, 0.2, 0.2, 1.0]
matDiffuse = [0.8, 0.8, 0.8, 1.0]
matSpecular = [0.5, 0.5, 0.5, 1.0]
matShininess = 50.0

# Variables for star movement
starSpeed = 0.02  # Speed at which the star moves
starAngle = 0.0   # Angle for circular movement


# Variables for the animation
animationTime = 0
animationDuration = 8000  # Duration in milliseconds
animationStartTime = None
animationRunning = True

def introAnimation():
    global animationTime, animationStartTime, animationRunning

    if animationStartTime is None:
        animationStartTime = glutGet(GLUT_ELAPSED_TIME)

    currentTime = glutGet(GLUT_ELAPSED_TIME)
    animationTime = currentTime - animationStartTime

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Calculate animation progress
    progress = animationTime / animationDuration

    # Animate camera movement
    cameraX = 20 * math.sin(progress * 2 * math.pi)
    cameraY = 5 + 5 * math.sin(progress * 2 * math.pi)
    cameraZ = 20 * math.cos(progress * 2 * math.pi)

    gluLookAt(cameraX, cameraY, cameraZ, 0, 0, 0, 0, 1, 0)

    # Draw scene elements
    for obj in objectArray:
        obj.draw()
    for cone_obj in allcones:
        cone_obj.draw()
    for star_obj in allstars:
        star_obj.posX = 10 * math.cos(progress * 4 * math.pi)
        star_obj.posZ = 10 * math.sin(progress * 4 * math.pi)
        star_obj.draw()

    # Display advertisement text
    glColor3f(1.0, 1.0, 0.0)
    text3d("Welcome to Jeep Adventure!", -5, 10, 0)
    text3d("An Exciting Journey Awaits.", -5, 8, 0)

    glutSwapBuffers()

    # Check if the animation duration is over
    if animationTime >= animationDuration:
        animationRunning = False
        # Reset camera position
        setView()
        # Switch to the main display and idle functions
        glutDisplayFunc(display)
        glutIdleFunc(idle)
        glutPostRedisplay()
    else:
        glutPostRedisplay()



# --------------------------------------developing scene---------------
class Scene:
    axisColor = (0.5, 0.5, 0.5, 0.5)
    axisLength = 50   # Extends to positive and negative on all axes
    landColor = (.47, .53, .6, 0.5)  # Light Slate Grey
    landLength = land  # Extends to positive and negative on x and y axis
    landW = 1.0
    landH = 0.0
    cont = gameEnlarge

    def draw(self):
        self.drawAxis()
        self.drawLand()

    def drawAxis(self):
        glColor4f(self.axisColor[0], self.axisColor[1], self.axisColor[2], self.axisColor[3])
        glBegin(GL_LINES)
        glVertex(-self.axisLength, 0, 0)
        glVertex(self.axisLength, 0, 0)
        glVertex(0, -self.axisLength, 0)
        glVertex(0, self.axisLength, 0)
        glVertex(0, 0, -self.axisLength)
        glVertex(0, 0, self.axisLength)
        glEnd()

    def drawLand(self):
        glEnable(GL_TEXTURE_2D)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glBindTexture(GL_TEXTURE_2D, roadTextureID)

        glBegin(GL_POLYGON)

        glTexCoord2f(self.landH, self.landH)
        glVertex3f(self.landLength, 0, self.cont * self.landLength)

        glTexCoord2f(self.landH, self.landW)
        glVertex3f(self.landLength, 0, -self.landLength)

        glTexCoord2f(self.landW, self.landW)
        glVertex3f(-self.landLength, 0, -self.landLength)

        glTexCoord2f(self.landW, self.landH)
        glVertex3f(-self.landLength, 0, self.cont * self.landLength)
        glEnd()

        glDisable(GL_TEXTURE_2D)

# --------------------------------------populating scene----------------
def staticObjects():
    global objectArray
    objectArray.append(Scene())
    print('append')

def display():
    global jeepObj, canStart, score, beginTime, countTime, midDown, speed, jeepPastZ
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Set the view
    if not midDown:
        setObjView()
    else:
        setView()

    # Configure the lighting
    if applyLighting:
        configureLight()
        # drawLightMarker(light0_Position)
        


    # Render the scene
    beginTime = 6 - score
    countTime = score - 6
    if score <= 5:
        canStart = False
        glColor3f(1.0, 0.0, 1.0)
        text3d("Begins in: " + str(beginTime), jeepObj.posX, jeepObj.posY + 3.0, jeepObj.posZ)
    elif score == 6:
        canStart = True
        glColor(1.0, 0.0, 1.0)
        text3d("GO!", jeepObj.posX, jeepObj.posY + 3.0, jeepObj.posZ)
    else:
        canStart = True
        glColor3f(0.0, 1.0, 1.0)
        text3d("Scoring: " + str(countTime), jeepObj.posX, jeepObj.posY + 3.0, jeepObj.posZ)

    if jeepObj.posZ >= ribbonZ and jeepPastZ < ribbonZ and jeepObj.posX >= -20.0 and jeepObj.posX <= 20.0:
        speed = 2.0
        glutTimerFunc(2 * 1000, removeAcceleration, 0)

    jeepPastZ = jeepObj.posZ
    for obj in objectArray:
        obj.draw()
    for cone in allcones:
        cone.draw()
    for star in allstars:
        star.draw()

    # if (usedDiamond == False):
    #     diamondObj.draw()
    
    jeepObj.draw()
    jeepObj.drawW1()
    jeepObj.drawW2()
    jeepObj.drawLight()
    drawAcceleratingRibbon()

    drawTextTopLeft("Press f to toggle full screen")

    glutSwapBuffers()

def drawAcceleratingRibbon():
    global ribbonZ
    glPushMatrix()
    glTranslatef(0, 0, ribbonZ)
    glColor3f(0.3, 0.7, 0.9)
    glRectf(-20, -0.5, 20, 0.5)
    glPopMatrix()

def removeAcceleration(val):
    global speed
    print("remove acceleration")
    speed = 1.0

def idle():
    global tickTime, prevTime, score, starAngle
    jeepObj.rotateWheel(-0.1 * tickTime)
    
    # Update the star's position
    moveStars()
    
    glutPostRedisplay()

    curTime = glutGet(GLUT_ELAPSED_TIME)
    tickTime = curTime - prevTime
    prevTime = curTime
    score = curTime / 1000

def moveStars():
    """Move the star(s) automatically."""
    global starAngle
    radius = 14.0  # Radius of the circular path
    starAngle += starSpeed  # Update the angle

    # Loop through all stars and update their positions
    for star_obj in allstars:
        star_obj.posX = radius * math.cos(starAngle)
        star_obj.posZ = radius * math.sin(starAngle)
        # React to the environment by changing color
        reactToEnvironment(star_obj)

def reactToEnvironment(star_obj):
    """Make the star react to the environment (e.g., light)."""
    if currentLightType == AMBIENT:
        # Dimmer color in ambient light
        star_obj.color = (0.5, 0.5, 0.0)  # Dark yellow
    else:
        # Brighter color in other light modes
        star_obj.color = (1.0, 1.0, 0.0)  # Bright yellow


def drawLightMarker(position):
    """
    Draws a small marker (sphere) at the light's position.
    :param position: A list or tuple representing the light position [x, y, z, w].
    """
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    glColor3f(1.0, 1.0, 0.0)  # Yellow color for the marker
    glutSolidSphere(0.2, 20, 20)  # Draw a small sphere
    glPopMatrix()


def configureLight():
    global currentLightType, light0_Position

    glEnable(GL_LIGHTING)  # Enable lighting
    glEnable(GL_LIGHT0)    # Use light source 0
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)


    resetLightProperties()  # Reset light properties

    if currentLightType == AMBIENT:
        # Ambient light properties
        ambient_intensity = [0.5, 0.5, 0.5, 1.0]  # Moderate intensity
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient_intensity)
        # drawLightMarker(light0_Position)
        # Disable other components
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])

        # Enable color tracking for ambient material properties
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])  # Disable diffuse
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])  # Disable specular
    else:
        # Reset global ambient light to default (black)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.0, 0.0, 0.0, 1.0])

        if currentLightType == POINT:
            # Point light properties
            position = light0_Position.copy()
            position[3] = 1.0  # w = 1.0 for positional light
            glLightfv(GL_LIGHT0, GL_POSITION, position)
            glLightfv(GL_LIGHT0, GL_DIFFUSE, light0_Intensity)
            glLightfv(GL_LIGHT0, GL_SPECULAR, light0_Intensity)
        elif currentLightType == DIRECTIONAL:
            # Directional light properties
            # Light coming from the top (negative Y-axis)
            direction = [0.0, 0.0, -1.0, 0.0]  # Direction vector for light
            glLightfv(GL_LIGHT0, GL_POSITION, direction)
            glLightfv(GL_LIGHT0, GL_DIFFUSE, light0_Intensity)
            glLightfv(GL_LIGHT0, GL_SPECULAR, light0_Intensity)
            # Disable ambient component for the light source
            glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
        elif currentLightType == SPOTLIGHT:
            # Set the light position above the scene
            position = [0.0, 10.0, 10.0, 1.0]
            glLightfv(GL_LIGHT0, GL_POSITION, position)
            
            # # Configure the spotlight
            glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 60.0) # Adjust cutoff angle for narrower spotlight
            glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 2.0)      # Higher exponent for more focused light
            
            # # Set the spotlight direction to point downwards
            spotlight_direction = [0.0, -1.0, 0.0]

            glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, spotlight_direction)
            
            # # Set light intensities
            glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
            glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
            
            # Set attenuation factors
            glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
            glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.1)
            glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.01)  # Slight quadratic attenuation for realistic falloff


        # Set material properties
        setMaterialProperties()


def resetLightProperties():
    """Reset all light properties to avoid interference between modes."""
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 180.0)  # Disable spotlight
    glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 0.0)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0.0, 0.0, -1.0])  # Default spot direction
    # Reset global ambient light
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
    glDisable(GL_COLOR_MATERIAL)  # Disable color material tracking

def setMaterialProperties():
    """Set material properties based on the current lighting mode."""
    if currentLightType == AMBIENT:
        # For ambient light, color tracking is enabled
        pass  # No need to set material properties here
    else:
        # For other lights, set ambient, diffuse, and specular
        glDisable(GL_COLOR_MATERIAL)  # Disable color tracking
        glMaterialfv(GL_FRONT, GL_AMBIENT, matAmbient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, matDiffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, matSpecular)
        glMaterialf(GL_FRONT, GL_SHININESS, matShininess)

def lightMenu(option):
    global currentLightType
    currentLightType = option
    glutPostRedisplay()  # Redraw the scene

def createMenu():
    menu = glutCreateMenu(lightMenu)  # Create the menu and link it to lightMenu()
    glutAddMenuEntry("Ambient Light", AMBIENT)
    glutAddMenuEntry("Point Light", POINT)
    glutAddMenuEntry("Directional Light", DIRECTIONAL)
    glutAddMenuEntry("Spotlight", SPOTLIGHT)
    glutAttachMenu(GLUT_RIGHT_BUTTON)  # Attach menu to the right mouse button

# ---------------------------------setting camera----------------------------
def setView():
    global eyeX, eyeY, eyeZ, jeepObj
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.1, 100)
    if topView:
        gluLookAt(0, 10, land * gameEnlarge / 2, 0, jeepObj.posY, land * gameEnlarge / 2, 0, 1, 0)
    elif behindView:
        gluLookAt(jeepObj.posX, jeepObj.posY + 1.0, jeepObj.posZ - 2.0, jeepObj.posX, jeepObj.posY, jeepObj.posZ, 0, 1, 0)
    else:
        gluLookAt(eyeX, eyeY, eyeZ, jeepObj.posX, jeepObj.posY, jeepObj.posZ, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    glutPostRedisplay()

def setObjView():
    global eyeX, eyeY, eyeZ, jeepObj
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.1, 100)

    eyeX = jeepObj.posX + 10 * math.sin(-rotation)
    eyeY = jeepObj.posY + 10.0
    eyeZ = jeepObj.posZ - 10.0 * math.cos(rotation)

    gluLookAt(eyeX, eyeY, eyeZ, jeepObj.posX, jeepObj.posY, jeepObj.posZ, 0, 1, 0)

    glMatrixMode(GL_MODELVIEW)
    glutPostRedisplay()

# -------------------------------------------user inputs------------------
def mouseHandle(button, state, x, y):
    global midDown
    if button == GLUT_MIDDLE_BUTTON and state == GLUT_DOWN:
        midDown = True
        print('pushed')
    else:
        midDown = False

def motionHandle(x, y):
    global nowX, nowY, angle, eyeX, eyeY, eyeZ, phi, jeepObj
    if midDown:
        pastX = nowX
        pastY = nowY
        nowX = x
        nowY = y
        if nowX - pastX > 0:
            angle -= 0.25
        elif nowX - pastX < 0:
            angle += 0.25
        eyeX = jeepObj.posX + radius * math.sin(angle)
        eyeZ = jeepObj.posZ + radius * math.cos(angle)
    if midDown:
        setView()
    else:
        setObjView()

def specialKeys(keypress, mX, mY):
    global rotation, speed
    div = glutGet(GLUT_WINDOW_WIDTH) / 3
    rot = 0.0
    if mX < div:
        rot = 1.0
    elif mX > div * 2:
        rot = -1.0
    if keypress == GLUT_KEY_UP:
        rotation += rot * 0.0175
        jeepObj.move(False, speed)
        jeepObj.move(True, rot)

    if keypress == GLUT_KEY_DOWN:
        rotation += rot * 0.0175
        jeepObj.move(False, -speed / 2)
        jeepObj.move(True, rot)

def myKeyboard(key, mX, mY):
    global isFullScreen, windowWidth, windowHeight, helpWindow, helpWin

    if key == b'f':  # Toggle full-screen mode
        print("f key pressed")
        isFullScreen = not isFullScreen
        if isFullScreen:
            # Enter full-screen mode
            glutFullScreen()
        else:
            # Exit full-screen mode
            print("Exiting full-screen mode")
            glutReshapeWindow(windowWidth, windowHeight)
            glutPositionWindow(100, 100)  # Reset the window's position to the center

    elif key == b"h":  # Toggle Help Window
        print("h key pressed")
        winNum = glutGetWindow()
        if not helpWindow:
            helpWindow = True
            glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
            glutInitWindowSize(500, 300)
            glutInitWindowPosition(600, 0)
            helpWin = glutCreateWindow(b"Help Guide")
            glutDisplayFunc(showHelp)
            glutKeyboardFunc(myKeyboard)
        elif helpWindow and winNum != 1:
            helpWindow = False
            glutHideWindow()

def drawTextTopLeft(message):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, windowWidth, 0, windowHeight)  # Set coordinate system to window size

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1.0, 1.0, 1.0)  # White color for text
    glRasterPos2i(10, windowHeight - 20)  # Position 10px from the left, 20px below the top

    for char in message:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# -------------------------------------------------tools----------------------
def drawTextBitmap(string, x, y):  # For writing text to display
    glRasterPos2f(x, y)
    for char in string:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def text3d(string, x, y, z):
    glRasterPos3f(x, y, z)
    for char in string:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def dist(pt1, pt2):
    a = pt1[0]
    b = pt1[1]
    x = pt2[0]
    y = pt2[1]
    return math.sqrt((a - x) ** 2 + (b - y) ** 2)

# --------------------------------------------making game more complex--------
def addCone(x, z):
    allcones.append(cone.cone(x, z))
    obstacleCoord.append((x, z))

def addStar(x, y, z):
    new_star = star(x, y, z)
    allstars.append(new_star)
    new_star.makeDisplayLists()

def collisionCheck():
    global overReason, score, usedDiamond, countTime
    for obstacle in obstacleCoord:
        if dist((jeepObj.posX, jeepObj.posZ), obstacle) <= ckSense:
            overReason = "You hit an obstacle!"
            gameOver()
    if (jeepObj.posX >= land or jeepObj.posX <= -land):
        overReason = "You ran off the road!"
        gameOver()

    if (jeepObj.posZ >= land * gameEnlarge):
        gameSuccess()

# ----------------------------------multiplayer dev (using tracker)-----------
def recordGame():
    with open('results.csv', 'wt') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print(st)
        spamwriter.writerow([st] + [finalScore])

# -------------------------------------developing additional windows/options----
def gameOver():
    global finalScore
    print("Game completed!")
    finalScore = score - 6
    glutHideWindow()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(200, 200)
    glutInitWindowPosition(600, 100)
    overWin = glutCreateWindow("Game Over!")
    glutDisplayFunc(overScreen)
    glutMainLoop()

def gameSuccess():
    global finalScore
    print("Game success!")
    finalScore = score - 6
    glutHideWindow()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(200, 200)
    glutInitWindowPosition(600, 100)
    overWin = glutCreateWindow("Complete!")
    glutDisplayFunc(winScreen)
    glutMainLoop()

def winScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.0, 1.0, 0.0)
    drawTextBitmap("Completed Trial!", -0.6, 0.85)
    glColor3f(0.0, 1.0, 0.0)
    drawTextBitmap("Your score is: ", -1.0, 0.0)
    glColor3f(1.0, 1.0, 1.0)
    drawTextBitmap(str(finalScore), -1.0, -0.15)
    glutSwapBuffers()

def overScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 0.0, 1.0)
    drawTextBitmap("Incomplete Trial", -0.6, 0.85)
    glColor3f(0.0, 1.0, 0.0)
    drawTextBitmap("Because you...", -1.0, 0.5)
    glColor3f(1.0, 1.0, 1.0)
    drawTextBitmap(overReason, -1.0, 0.35)
    glColor3f(0.0, 1.0, 0.0)
    drawTextBitmap("Your score stopped at: ", -1.0, 0.0)
    glColor3f(1.0, 1.0, 1.0)
    drawTextBitmap(str(finalScore), -1.0, -0.15)
    glutSwapBuffers()

def showHelp():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0)
    drawTextBitmap("Help Guide", -0.2, 0.85)
    glColor3f(0.0, 0.0, 1.0)
    drawTextBitmap("Describe your control strategy.", -1.0, 0.7)
    glutSwapBuffers()

# ----------------------------------------------texture development-----------
def loadTexture(imageName):
    texturedImage = Image.open(imageName)
    try:
        imgX = texturedImage.size[0]
        imgY = texturedImage.size[1]
        img = texturedImage.tobytes("raw", "RGBX", 0, -1)
    except Exception:
        print("Error:")
        print("Switching to RGBA mode.")
        imgX = texturedImage.size[0]
        imgY = texturedImage.size[1]
        img = texturedImage.tobytes("raw", "RGB", 0, -1)

    tempID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tempID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, imgX, imgY, 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
    return tempID

def loadSceneTextures():
    global roadTextureID
    roadTextureID = loadTexture("./img/road2.png")

# -----------------------------------------------lighting work--------------
def initializeLight():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    
    glClearColor(0.1, 0.1, 0.1, 0.0)

# ~~~~~~~~~~~~~~~~~~~~~~~~~the finale!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    glutInit()

    global prevTime, mainWin
    prevTime = glutGet(GLUT_ELAPSED_TIME)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(windowSize, windowSize)

    glutInitWindowPosition(0, 0)
    mainWin = glutCreateWindow(b'CS4182')
    # glutDisplayFunc(display)
    # glutIdleFunc(idle)  # Wheel turn

    # Set the initial display function to the animation
    glutDisplayFunc(introAnimation)
    glutIdleFunc(introAnimation)  # Run animation in idle

    setView()
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)

    glutMouseFunc(mouseHandle)
    glutMotionFunc(motionHandle)
    glutSpecialFunc(specialKeys)
    glutKeyboardFunc(myKeyboard)

    # Create the lighting menu
    createMenu()

    loadSceneTextures()

    jeep1Obj.makeDisplayLists()
    jeep2Obj.makeDisplayLists()
    jeep3Obj.makeDisplayLists()

    for i in range(coneAmount):  # Create cones randomly for obstacles
        addCone(random.randint(-land, land), random.randint(10.0, land * gameEnlarge))

    # things to do
    # add stars
    addStar(10,5,10)

    for cone in allcones:
        cone.makeDisplayLists()

    # Note: The star's display list is created in addStar()

    staticObjects()
    if applyLighting:
        initializeLight()
    glutMainLoop()

if __name__ == "__main__":
    main()
