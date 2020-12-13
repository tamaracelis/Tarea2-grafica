import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import csv

import transformations as tr
import basic_shapes as bs
import easy_shaders as es
import lighting_shaders as ls
import scene_graph2 as sg

class Barra:
    def __init__(self):
        gpu_barra = es.toGPUShape(bs.createColorCube(0.7, 0.4, 0))
            
        self.model = gpu_barra
        self.dibujo=True
        self.real=True
        self.posx=0
        self.posy=0
        self.posz=0
        
    def Draw(self, color_pipeline, projection, view):
        if self.dibujo:
            self.transform = tr.matmul([tr.scale(2, 2, 0.3), tr.translate(self.posx, self.posy, self.posz)])
            glUseProgram(color_pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(color_pipeline.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
            glUniformMatrix4fv(glGetUniformLocation(color_pipeline.shaderProgram, 'view'), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(color_pipeline.shaderProgram, 'model'), 1, GL_TRUE, self.transform)
            
            color_pipeline.drawShape(self.model)
            
    def move1(self):
        self.posx=1.2
        self.posy=-1.7
        
    def move2(self):
        self.posx=-1.2
        self.posy=-0.8
        
    def move3(self):
        self.posx=1.2
        self.posy=0
    
    def move4(self):
        self.posx=-1.2
        self.posy=0.8
    
    def move5(self):
        self.posx=1.2
        self.posy=1.7
        
    def moveUp(self,z):
        self.posz=z
        
class CreateBarras():
    def __init__(self):
        self.barras=[]
    
    def create(self,estructura):
        with open(estructura) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            altura = 0.3
            for row in csv_reader:   
                for i in range(9):
                    if row[0][i]=="1":
                        b=Barra()
                        b.moveUp(altura*7)
                        if i==0:
                            b.move1()
                        elif i==2:
                            b.move2()
                        elif i==4:
                            b.move3()
                        elif i==6:
                            b.move4()
                        elif i==8:
                            b.move5()
                        self.barras.append(b)
                    if row[0][i]=="x":
                        b=Barra()
                        b.moveUp(altura*7)
                        b.real=False
                        if i==0:
                            b.move1()
                        elif i==2:
                            b.move2()
                        elif i==4:
                            b.move3()
                        elif i==6:
                            b.move4()
                        elif i==8:
                            b.move5()
                        self.barras.append(b)
                altura += 1
    def draw(self, pipeline, projection, view):
        for k in self.barras:
            k.Draw(pipeline, projection, view)

class Fondo():
    def __init__(self):
        self.models=[]
        self.transform=[]
        
        fondo1=bs.createTextureCube('fondo.jpg')
        gpufondo1 = es.toGPUShape(fondo1, GL_REPEAT, GL_NEAREST)
        self.models.append(gpufondo1)
        self.transform.append(tr.matmul([tr.uniformScale(24), tr.translate(-1, 0, 0.4)]))
        
        fondo2=bs.createTextureCube('fondo.jpg')
        gpufondo2 = es.toGPUShape(fondo2, GL_REPEAT, GL_NEAREST)
        self.models.append(gpufondo1)
        self.transform.append(tr.matmul([tr.uniformScale(24), tr.translate(0, -1, 0.4)]))
        
        fondo3=bs.createTextureCube('fondo.jpg')
        gpufondo3 = es.toGPUShape(fondo3, GL_REPEAT, GL_NEAREST)
        self.models.append(gpufondo1)
        self.transform.append(tr.matmul([tr.uniformScale(24), tr.translate(0, 1, 0.4)]))
        
        fondo4=bs.createTextureCube('fondo.jpg')
        gpufondo4 = es.toGPUShape(fondo4, GL_REPEAT, GL_NEAREST)
        self.models.append(gpufondo1)
        self.transform.append(tr.matmul([tr.uniformScale(24), tr.translate(1, 0, 0.4)]))
        
    def Draw(self, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)
        for i in range (len(self.models)):
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform[i])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            pipeline.drawShape(self.models[i])
        
    
# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True


# We will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    global controller
    if key == glfw.KEY_ESCAPE:
        sys.exit()


def readFaceVertex(faceDescription):

    aux = faceDescription.split('/')

    assert len(aux[0]), "Vertex index has not been defined."

    faceVertex = [int(aux[0]), None, None]

    assert len(aux) == 3, "Only faces where its vertices require 3 indices are defined."

    if len(aux[1]) != 0:
        faceVertex[1] = int(aux[1])

    if len(aux[2]) != 0:
        faceVertex[2] = int(aux[2])

    return faceVertex



def readOBJ(filename, color):

    vertices = []
    normals = []
    textCoords= []
    faces = []

    with open(filename, 'r') as file:
        for line in file.readlines():
            aux = line.strip().split(' ')
            
            if aux[0] == 'v':
                vertices += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'vn':
                normals += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'vt':
                assert len(aux[1:]) == 2, "Texture coordinates with different than 2 dimensions are not supported"
                textCoords += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'f':
                N = len(aux)                
                faces += [[readFaceVertex(faceVertex) for faceVertex in aux[1:4]]]
                for i in range(3, N-1):
                    faces += [[readFaceVertex(faceVertex) for faceVertex in [aux[i], aux[i+1], aux[1]]]]

        vertexData = []
        indices = []
        index = 0

        # Per previous construction, each face is a triangle
        for face in faces:

            # Checking each of the triangle vertices
            for i in range(0,3):
                vertex = vertices[face[i][0]-1]
                normal = normals[face[i][2]-1]

                vertexData += [
                    vertex[0], vertex[1], vertex[2],
                    color[0], color[1], color[2],
                    normal[0], normal[1], normal[2]
                ]

            # Connecting the 3 vertices to create a triangle
            indices += [index, index + 1, index + 2]
            index += 3        

        return bs.Shape(vertexData, indices)


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 700
    height = 700

    window = glfw.create_window(width, height, "Amy Jump", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Defining shader programs
    pipeline = ls.SimpleGouraudShaderProgram()
    texture_pipeline = es.SimpleTextureModelViewProjectionShaderProgram()
    color_pipeline = es.SimpleModelViewProjectionShaderProgram()


    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAmy = es.toGPUShape(shape = readOBJ('amy.obj', (0.9,0.6,0.2)))
    
    fondo=Fondo()
        
    #Piso
    piso = bs.createTextureCube('piso.jpg')
    gpupiso = es.toGPUShape(piso, GL_REPEAT, GL_LINEAR)
    piso_transform = tr.matmul([tr.uniformScale(24), tr.translate(0, 0, -0.53)])
    
    barras=CreateBarras()
    barras.create('estructura.csv')
    
  #  b=Barra()
   # b.moveUp(1)
    
    t0 = glfw.get_time()

    posX=0
    posY=0
    posZ=0.5
    grav=True
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1
    
        view = tr.lookAt(
            np.array([12, -3,8+(posZ-0.5)]),
            np.array([posX*0.4,posY*0.4,posZ]),
            np.array([0,0,1])
        )

        if (glfw.get_key(window, glfw.KEY_B) == glfw.PRESS):
             view = tr.lookAt(
                 np.array([0,1,17.5+(posZ)]),
                 np.array([0,0,0]),
                 np.array([0,0,1]))
        if (glfw.get_key(window, glfw.KEY_N) == glfw.PRESS):
             view = tr.lookAt(
                 np.array([9,9,7+posZ]),
                 np.array([posX,posY,posZ]),
                 np.array([0,0,1]))
        if (glfw.get_key(window, glfw.KEY_M) == glfw.PRESS):
             view = tr.lookAt(
                 np.array([0,10,-0.5+posZ]),
                 np.array([posX,posY,posZ]),
                 np.array([0,0,1]))
    
        # Setting up the projection transform
        projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        fondo.Draw(texture_pipeline, projection, view)
        glUseProgram(texture_pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "model"), 1, GL_TRUE, piso_transform)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        texture_pipeline.drawShape(gpupiso)
        
               
        
        # Drawing shapes
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.5, 0.5, 0.5)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 0, 3, 3)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), 0, 0, 7)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 10)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.01)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.1)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)
        
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE,tr.matmul([         
                tr.translate(posX, posY, posZ),
                tr.rotationZ(np.pi),
                tr.rotationX(np.pi/2),
                tr.uniformScale(0.4)]))
        pipeline.drawShape(gpuAmy)
        b=barras.barras
      #  if posZ>0.6 and grav==True:
       #     posZ-=3*dt
        for i in range(len(b)):
            if posX<=2*b[i].posx+1 and posX>=2*b[i].posx-1 and posY<=2*b[i].posy+1 and posY>=2*b[i].posy-1 and posZ<=b[i].posz*0.3+1.5 and posZ>=b[i].posz*0.3+1.25:
                grav=False
            else:
                grav=True
        if (glfw.get_key(window, glfw.KEY_A) == glfw.PRESS):
            if posX>-6:
                posX-=5*dt
        if (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS):
            if posX<6:
                posX+=5*dt
        if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS):
            if posY<6:
                posY+=5*dt
        if (glfw.get_key(window, glfw.KEY_S) == glfw.PRESS):
            if posY>-6:
                posY-=5*dt
        if (glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS):
            posZ+=6*dt
            
        print ("amy x"+"   z"+str(posZ))
        print (str(b[0].posz))
       # print ("bra x"+str(b.posx)+"   y"+str(b.posy)+"   z"+str(b.posz))
       # b.Draw(color_pipeline, projection, view)
        barras.draw(color_pipeline,projection, view)
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)
        

    glfw.terminate()
