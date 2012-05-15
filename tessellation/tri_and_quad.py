import pyglet
from pyglet.gl import *

import time
from gletools import ShaderProgram, VertexObject, Matrix

window = pyglet.window.Window(width=1100, height=500)
rotation = 0.0
innerLevel = 1.0
outerLevel = 1.0
targetInnerLevel = 1.0
targetOuterLevel = 1.0
#spacing = 0
spacingStr = 'equal_spacing'

import math
import pyglet.font
from pyglet.font import load as load_font
font = load_font('', 12, bold=True)
levelsLabel = pyglet.font.Text(font, 'Press the arrow keys.', color=(1,0,0,.5),x=10,y=10)
auxLabel = pyglet.font.Text(font, 'asdf', color=(1,0,0,.5),x=10,y=30)
helpLabel = pyglet.font.Text(font,
                             'Q,W,E: Change Spacing     '
                             'Arrows: Change Tess Levels',
                             color=(1,0,0,.5),x=10,y=window.height-20)
allLabels = [levelsLabel, auxLabel, helpLabel]

def WriteShaderProgram(destPath, templatePath, replacements):
    with open(templatePath) as templateFile:
        with open(destPath, 'w') as destFile:
            for line in templateFile:
                for key, value in replacements.iteritems():
                    line = line.replace(key, value)
                destFile.write(line)

h = math.sqrt(3)/2
triVbo = VertexObject(
    indices = [0, 1, 2],
    v4f     = [
         0, 4.0/3*h, 0, 1,
        -1, -2.0/3*h, 0, 1,
        +1, -2.0/3*h, 0, 1,
    ],
)

quadVbo = VertexObject(
    indices = [0, 1, 2, 3],
    v4f     = [
        +1, +1, 0, 1,
        +1, -1, 0, 1,
        -1, -1, 0, 1,
        -1, +1, 0, 1,
    ],
)

class FadingValue:
    def __init__(self, value, speed):
        self.value = value
        self.target = value
        self.speed = speed

    def step(self):
        self.value += (self.target - self.value) * self.speed


noiseStrength = FadingValue(1, 0.3)


def WriteAllPrograms():
    global trisProgram
    global quadsProgram
    WriteShaderProgram('/tmp/tris.shader.tmp',
                       'tris.shader',
                       {'__SPACING': spacingStr})
    WriteShaderProgram('/tmp/quads.shader.tmp',
                       'quads.shader',
                       {'__SPACING': spacingStr})

    trisProgram = ShaderProgram.open('/tmp/tris.shader.tmp',
        inner_level = 1.0,
        outer_level = 1.0
    )
    quadsProgram = ShaderProgram.open('/tmp/quads.shader.tmp',
        inner_level = 1.0,
        outer_level = 1.0
    )
    auxLabel.text = 'Spacing: %s' % spacingStr

WriteAllPrograms()


def simulate(delta, _):
    global rotation
    global innerLevel
    global outerLevel

    rotation += 0.1 * delta

    if spacingStr == 'equal_spacing':
        innerLevel = targetInnerLevel
        outerLevel = targetOuterLevel
    else:
        innerLevel += (targetInnerLevel - innerLevel)*0.3
        outerLevel += (targetOuterLevel - outerLevel)*0.3

    noiseStrength.step()

    trisProgram.vars.inner_level = innerLevel
    trisProgram.vars.outer_level = outerLevel
    trisProgram.vars.dispStrength = noiseStrength.value
    trisProgram.vars.timestamp = time.time() % 10000.0
    quadsProgram.vars.inner_level = innerLevel
    quadsProgram.vars.outer_level = outerLevel
    
    levelsLabel.text = "Inner TL: %1.1f     " \
                       "Outer TL: %1.1f" % (innerLevel, outerLevel)

pyglet.clock.schedule(simulate, 0.03)

@window.event
def on_draw():
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    window.clear()

    spacing = 2
    trisProgram.vars.modelview = Matrix().translate(-spacing,0,-5).rotatex(-0.175).rotatez(rotation)
    trisProgram.vars.projection = Matrix.perspective(window.width, window.height, 40, 0.1, 100.0)

    quadsProgram.vars.modelview = Matrix().translate(spacing,0,-5).rotatex(-0.175).rotatez(rotation)
    quadsProgram.vars.projection = Matrix.perspective(window.width, window.height, 40, 0.1, 100.0)

    with trisProgram:
        glPatchParameteri(GL_PATCH_VERTICES, 3);
        triVbo.draw(GL_PATCHES)

    with quadsProgram:
        glPatchParameteri(GL_PATCH_VERTICES, 4);
        quadVbo.draw(GL_PATCHES)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    for label in allLabels:
        label.draw()

@window.event
def on_key_press(symbol, modifiers):
    global targetInnerLevel
    global targetOuterLevel 
    global spacingStr
    global auxLabel
    global noiseStrength

    key_right = 0xff53 # right
    key_left = 0xff51 # left
    key_up = 0xff52 # up
    key_down = 0xff54 # down

    increment = 1 if spacingStr == 'equal_spacing' else 2

    spacingChanged = False
    innerChanged = False
    outerChanged = False
    if symbol==key_right:
        targetInnerLevel+=increment
        innerChanged = True
    elif symbol==key_left:
        targetInnerLevel-=increment
        innerChanged = True
    elif symbol==key_up:
        targetOuterLevel+=increment
        outerChanged = True
    elif symbol==key_down:
        targetOuterLevel-=increment
        outerChanged = True
    elif symbol==ord('q'):
        spacingStr = 'fractional_even_spacing'
        spacingChanged = True
    elif symbol==ord('w'):
        spacingStr = 'fractional_odd_spacing'
        spacingChanged = True
    elif symbol==ord('e'):
        spacingStr = 'equal_spacing'
        spacingChanged = True
    elif symbol==ord('n'):
        noiseStrength.target = 1-noiseStrength.target
        

    if spacingChanged:
        WriteAllPrograms()

    if innerChanged or spacingChanged:
        if spacingStr == 'fractional_even_spacing':
            targetInnerLevel = max(round(targetInnerLevel/2)*2,2.0)
        elif spacingStr == 'fractional_odd_spacing':
            targetInnerLevel = max(round(targetInnerLevel/2)*2-1,1.0)
        elif spacingStr == 'equal_spacing':
            targetInnerLevel = max(targetInnerLevel, 1.0)

    if outerChanged or spacingChanged:
        if spacingStr == 'fractional_even_spacing':
            targetOuterLevel = max(round(targetOuterLevel/2)*2,2.0)
        elif spacingStr == 'fractional_odd_spacing':
            targetOuterLevel = max(round(targetOuterLevel/2)*2-1,1.0)
        elif spacingStr == 'equal_spacing':
            targetOuterLevel = max(targetOuterLevel, 1.0)

if __name__ == '__main__':
    pyglet.app.run()
