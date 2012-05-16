import pyglet
from pyglet.gl import *

import time
from gletools import ShaderProgram, VertexObject, Matrix

window = pyglet.window.Window(width=800, height=600)
rotation = 0.0
import sys
try:
    innerLevel = float(sys.argv[1])
    outerLevel = float(sys.argv[2])
except IndexError:
    innerLevel = 1.0
    outerLevel = 1.0
targetInnerLevel = innerLevel
targetOuterLevel = outerLevel
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

s = 0.3
#s = 0.6
m = 1-s

quadVbo = VertexObject(
    indices = [0, 1, 2, 3,
               4, 5, 6, 7,
               8, 9, 10, 11,
               12, 13, 14, 15,
               16, 17, 18, 19,
               20, 21, 22, 23],
    v4f     = [  
        # 25      
        -m, -m, -1, 1,  
        +m, -m, -1, 1,  
        +m, +m, -1, 1,  
        -m, +m, -1, 1,  
                 
        # 29     
        +1, -m, -m, 1,  
        +1, -m, +m, 1,  
        +1, +m, +m, 1,  
        +1, +m, -m, 1,  
                
        # 33    
        -m, -1, +m, 1,  
        +m, -1, +m, 1,  
        +m, -1, -m, 1,  
        -m, -1, -m, 1,  
               
        # 37   
        -m, +1, -m, 1,  
        +m, +1, -m, 1,  
        +m, +1, +m, 1,  
        -m, +1, +m, 1,  
              
        # 41  
        +m, +m, +1, 1,  
        +m, -m, +1, 1,  
        -m, -m, +1, 1,  
        -m, +m, +1, 1,  
             
        # 45 
        -1, +m, -m, 1,  
        -1, +m, +m, 1,  
        -1, -m, +m, 1,  
        -1, -m, -m, 1,  
    ],
)

rimVbo = VertexObject(
               indices = [24, 34, 33, 25, 53, 52,
                           8, 35, 34,  9, 49, 48,
                          29, 32, 35, 28, 47, 46,
                          17, 33, 32, 16, 42, 41,
                          26, 55, 54, 27, 38, 37,
                          13, 51, 50, 12, 37, 36,
                          31, 45, 44, 30, 36, 39,
                          20, 40, 43, 21, 39, 38,
                          10, 52, 55, 11, 50, 49,
                          18, 41, 40, 19, 54, 53,
                          15, 48, 51, 14, 44, 47,
                          23, 46, 45, 22, 43, 42],
                          


    v4f     = [-1, -1, -1, 1,
        +1, -1, -1, 1,
        +1, +1, -1, 1,
        -1, +1, -1, 1,
        -1, -1, +1, 1,
        -1, +1, +1, 1,
        +1, +1, +1, 1,
        +1, -1, +1, 1,

        # front rims, 8
        -m, -1, -1, 1,    
        +m, -1, -1, 1,    
        +1, -m, -1, 1,    
        +1, +m, -1, 1,    
        +m, +1, -1, 1,    
        -m, +1, -1, 1,    
        -1, +m, -1, 1,    
        -1, -m, -1, 1,    

        # back rims, 16
        -m, -1, +1, 1,    
        +m, -1, +1, 1,    
        +1, -m, +1, 1,    
        +1, +m, +1, 1,    
        +m, +1, +1, 1,    
        -m, +1, +1, 1,    
        -1, +m, +1, 1,    
        -1, -m, +1, 1,    

        # side rims, 24
        +1, -1, -m, 1, # x
        +1, -1, +m, 1, # x
        +1, +1, -m, 1,
        +1, +1, +m, 1,

        -1, -1, -m, 1,
        -1, -1, +m, 1,
        -1, +1, -m, 1,
        -1, +1, +m, 1,

        # 32    
        -m, -1, +m, 1,  
        +m, -1, +m, 1, # x 
        +m, -1, -m, 1, # x
        -m, -1, -m, 1, 
               
        # 36   
        -m, +1, -m, 1,  
        +m, +1, -m, 1,  
        +m, +1, +m, 1,  
        -m, +1, +m, 1,  
              
        # 40  
        +m, +m, +1, 1,  
        +m, -m, +1, 1,  
        -m, -m, +1, 1,  
        -m, +m, +1, 1,  
             
        # 44 
        -1, +m, -m, 1,  
        -1, +m, +m, 1,  
        -1, -m, +m, 1,  
        -1, -m, -m, 1,  

        # 48      
        -m, -m, -1, 1,  
        +m, -m, -1, 1,  
        +m, +m, -1, 1,  
        -m, +m, -1, 1,  
                 
        # 52     
        +1, -m, -m, 1, # x 
        +1, -m, +m, 1, # x
        +1, +m, +m, 1,  
        +1, +m, -m, 1,  
    ],
)

cornerVbo = VertexObject(
               indices = [24, 34,  9, 49, 10, 52,
                          17, 33, 25, 53, 18, 41,
                          29, 32, 16, 42, 23, 46,
                           8, 35, 28, 47, 15, 48,
                          26, 55, 11, 50, 12, 37,
                          13, 51, 14, 44, 30, 36,
                          19, 54, 27, 38, 20, 40,
                          22, 43, 21, 39, 31, 45],
                          


    v4f     = [-1, -1, -1, 1,
        +1, -1, -1, 1,
        +1, +1, -1, 1,
        -1, +1, -1, 1,
        -1, -1, +1, 1,
        -1, +1, +1, 1,
        +1, +1, +1, 1,
        +1, -1, +1, 1,

        # front rims, 8
        -m, -1, -1, 1,    
        +m, -1, -1, 1,    
        +1, -m, -1, 1,    
        +1, +m, -1, 1,    
        +m, +1, -1, 1,    
        -m, +1, -1, 1,    
        -1, +m, -1, 1,    
        -1, -m, -1, 1,    

        # back rims, 16
        -m, -1, +1, 1,    
        +m, -1, +1, 1,    
        +1, -m, +1, 1,    
        +1, +m, +1, 1,    
        +m, +1, +1, 1,    
        -m, +1, +1, 1,    
        -1, +m, +1, 1,    
        -1, -m, +1, 1,    

        # side rims, 24
        +1, -1, -m, 1, # x
        +1, -1, +m, 1, # x
        +1, +1, -m, 1,
        +1, +1, +m, 1,

        -1, -1, -m, 1,
        -1, -1, +m, 1,
        -1, +1, -m, 1,
        -1, +1, +m, 1,

        # 32    
        -m, -1, +m, 1,  
        +m, -1, +m, 1, # x 
        +m, -1, -m, 1, # x
        -m, -1, -m, 1, 
               
        # 36   
        -m, +1, -m, 1,  
        +m, +1, -m, 1,  
        +m, +1, +m, 1,  
        -m, +1, +m, 1,  
              
        # 40  
        +m, +m, +1, 1,  
        +m, -m, +1, 1,  
        -m, -m, +1, 1,  
        -m, +m, +1, 1,  
             
        # 44 
        -1, +m, -m, 1,  
        -1, +m, +m, 1,  
        -1, -m, +m, 1,  
        -1, -m, -m, 1,  

        # 48      
        -m, -m, -1, 1,  
        +m, -m, -1, 1,  
        +m, +m, -1, 1,  
        -m, +m, -1, 1,  
                 
        # 52     
        +1, -m, -m, 1, # x 
        +1, -m, +m, 1, # x
        +1, +m, +m, 1,  
        +1, +m, -m, 1,  
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
    global boxProgram
    global rimProgram
    global cornerProgram
    WriteShaderProgram('/tmp/bevelBoxFlat.shader.tmp',
                       'bevelBoxFlat.shader',
                       {'__SPACING': spacingStr})
    WriteShaderProgram('/tmp/bevelBoxRim.shader.tmp',
                       'bevelBoxRim.shader',
                       {'__SPACING': spacingStr})
    WriteShaderProgram('/tmp/bevelBoxCorner.shader.tmp',
                       'bevelBoxCorner.shader',
                       {'__SPACING': spacingStr})

    boxProgram = ShaderProgram.open('/tmp/bevelBoxFlat.shader.tmp',
        inner_level = 1.0,
        outer_level = 1.0
    )
    rimProgram = ShaderProgram.open('/tmp/bevelBoxRim.shader.tmp',
        inner_level = 1.0,
        outer_level = 1.0
    )
    cornerProgram = ShaderProgram.open('/tmp/bevelBoxCorner.shader.tmp',
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

#    boxProgram.vars.inner_level = innerLevel
#    boxProgram.vars.outer_level = outerLevel
    rimProgram.vars.inner_level = innerLevel
    rimProgram.vars.outer_level = outerLevel
    cornerProgram.vars.inner_level = innerLevel
    cornerProgram.vars.outer_level = outerLevel
    
    levelsLabel.text = "Inner TL: %1.1f     " \
                       "Outer TL: %1.1f" % (innerLevel, outerLevel)

pyglet.clock.schedule(simulate, 0.03)

@window.event
def on_draw():
    glEnable(GL_CULL_FACE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    window.clear()

    boxProgram.vars.modelview = Matrix().translate(0,0,-5).rotatex(-0.175).rotatez(rotation)
    boxProgram.vars.projection = Matrix.perspective(window.width, window.height, 40, 0.1, 100.0)
    rimProgram.vars.modelview = Matrix().translate(0,0,-5).rotatex(-0.175).rotatez(rotation)
    rimProgram.vars.projection = Matrix.perspective(window.width, window.height, 40, 0.1, 100.0)
    cornerProgram.vars.modelview = Matrix().translate(0,0,-5).rotatex(-0.175).rotatez(rotation)
    cornerProgram.vars.projection = Matrix.perspective(window.width, window.height, 40, 0.1, 100.0)

    with boxProgram:
        glPatchParameteri(GL_PATCH_VERTICES, 4);
        quadVbo.draw(GL_PATCHES)

    with rimProgram:
        glPatchParameteri(GL_PATCH_VERTICES, 6);
        rimVbo.draw(GL_PATCHES)

    with cornerProgram:
        glPatchParameteri(GL_PATCH_VERTICES, 6);
        cornerVbo.draw(GL_PATCHES)

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
