import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Light modes
AMBIENT, POINT, DIRECTIONAL, SPOTLIGHT = range(4)
current_light_mode = AMBIENT

# Light properties
ambient_light = [0.2, 0.2, 0.2, 1.0]
diffuse_light = [1.0, 1.0, 1.0, 1.0]
specular_light = [1.0, 1.0, 1.0, 1.0]

# Common light position (top-center)
position = [0.0, 5.0, 5.0, 1.0]  # Light source at (0, 5, 5)
direction = [0.0, -1.0, -1.0]   # Direction pointing downward-left

def resetLightProperties():
    """Reset all light properties to avoid interference between modes."""
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 180.0)  # Disable spotlight
    glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 0.0)

def setAmbientLight():
    """Set up ambient lighting."""
    resetLightProperties()
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])  # No diffuse component
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0]) # No specular component
    glLightfv(GL_LIGHT0, GL_POSITION, position)  # Position is irrelevant for ambient light

def setPointLight():
    """Set up point lighting."""
    resetLightProperties()
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])   # No ambient component
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)
    position[3] = 1.0  # w = 1.0 for positional light
    glLightfv(GL_LIGHT0, GL_POSITION, position)

def setDirectionalLight():
    """Set up directional lighting."""
    resetLightProperties()
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])   # No ambient component
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)
    position[3] = 0.0  # w = 0.0 for directional light
    glLightfv(GL_LIGHT0, GL_POSITION, position)

def setSpotlight():
    """Set up spotlight lighting."""
    resetLightProperties()
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])   # No ambient component
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)
    position[3] = 1.0  # w = 1.0 for positional light
    glLightfv(GL_LIGHT0, GL_POSITION, position)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, direction)  # Align direction with position
    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 30.0)  # Spotlight cone angle
    glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 2.0)  # Spotlight intensity

def setLightingMode():
    """Set the current lighting mode."""
    glDisable(GL_LIGHT0)  # Disable current light to reset settings
    if current_light_mode == AMBIENT:
        setAmbientLight()
    elif current_light_mode == POINT:
        setPointLight()
    elif current_light_mode == DIRECTIONAL:
        setDirectionalLight()
    elif current_light_mode == SPOTLIGHT:
        setSpotlight()
    glutPostRedisplay()

def createMenu():
    """Create a popup menu to switch lighting modes."""
    menu = glutCreateMenu(menuHandler)
    glutAddMenuEntry("Ambient Light (1)", AMBIENT)
    glutAddMenuEntry("Point Light (2)", POINT)
    glutAddMenuEntry("Directional Light (3)", DIRECTIONAL)
    glutAddMenuEntry("Spotlight (4)", SPOTLIGHT)
    glutAttachMenu(GLUT_RIGHT_BUTTON)

def menuHandler(option):
    """Handle menu selections."""
    global current_light_mode
    current_light_mode = option
    setLightingMode()
    printMode()

def keyboard(key, x, y):
    """Handle keyboard input to switch lighting modes."""
    global current_light_mode
    key = key.decode('utf-8')  # For Python 3 compatibility
    if key == '1':
        current_light_mode = AMBIENT
    elif key == '2':
        current_light_mode = POINT
    elif key == '3':
        current_light_mode = DIRECTIONAL
    elif key == '4':
        current_light_mode = SPOTLIGHT
    else:
        return  # Ignore other keys
    setLightingMode()
    printMode()

def printMode():
    """Print the current lighting mode."""
    modes = {
        AMBIENT: "Ambient Light",
        POINT: "Point Light",
        DIRECTIONAL: "Directional Light",
        SPOTLIGHT: "Spotlight"
    }
    print(f"Current Lighting Mode: {modes[current_light_mode]}")

def display():
    """Render the scene."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # Set the camera position and orientation
    gluLookAt(0.0, 0.0, 8.0,   # Eye position
              0.0, 0.0, 0.0,   # Look-at point
              0.0, 1.0, 0.0)   # Up direction
    # Rotate the object for better visualization
    glRotatef(25, 1.0, 1.0, 0.0)
    # Render a teapot
    glColor3f(0.8, 0.5, 0.2)
    glutSolidTeapot(1.5)
    glutSwapBuffers()

def init():
    """Initialize OpenGL settings."""
    glClearColor(0.1, 0.1, 0.1, 1.0)  # Background color
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    setAmbientLight()  # Set default lighting mode

def reshape(width, height):
    """Handle window resizing."""
    glViewport(0, 0, width, height)
    aspect_ratio = width / float(height) if height != 0 else width
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, aspect_ratio, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    """Main function to set up the OpenGL context and start the event loop."""
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"OpenGL Lighting Modes")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    createMenu()
    print("Press 1 for Ambient Light")
    print("Press 2 for Point Light")
    print("Press 3 for Directional Light")
    print("Press 4 for Spotlight")
    glutMainLoop()

if __name__ == "__main__":
    main()
