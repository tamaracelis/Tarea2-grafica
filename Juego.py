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

#Clase de la cracion de barras 
class Barra:
    def __init__(self):
        
        #crea una barra
        gpu_barra = es.toGPUShape(bs.createColorCube(0.7, 0.4, 0))
            
        self.model = gpu_barra
        self.dibujo=True
        self.real=True
        self.posx=0
        self.posy=0
        self.posz=0
        
    #Dibuja una barra
    def Draw(self, color_pipeline, projection, view):
        if self.dibujo:
            self.transform = tr.matmul([tr.scale(2, 2, 0.3), tr.translate(self.posx, self.posy, self.posz)])
            glUseProgram(color_pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(color_pipeline.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
            glUniformMatrix4fv(glGetUniformLocation(color_pipeline.shaderProgram, 'view'), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(color_pipeline.shaderProgram, 'model'), 1, GL_TRUE, self.transform)
            
            color_pipeline.drawShape(self.model)
    #Traslada las barras    
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
 
#clase que crea las barras del archivo csv       
class CreateBarras():
    def __init__(self):
        self.barras=[]
        self.altura=0.5
    
    def create(self,estructura):
        with open(estructura) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            #se lee el archivo
            for row in csv_reader:   
                for i in range(9):
                    if row[0][i]=="1":
                        b=Barra()
                        b.moveUp(self.altura*7)
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
                        b.moveUp(self.altura*7)
                        b.real=False #indica que una barra es falsa y si la toca el mono esta desaparece 
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
                #aumenta la altura para las proximas barras
                self.altura += 1
    #dibuja todas las barras
    def draw(self, pipeline, projection, view):
        for k in self.barras:
            k.Draw(pipeline, projection, view)

#Crea los fondos 
class Fondo():
    def __init__(self):
        self.models=[]
        self.transform=[]
        
        #crea el "manto de un cubo 
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
    
    #dibuja todo los objetos creados en fondo
    def Draw(self, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)
        for i in range (len(self.models)):
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform[i])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            pipeline.drawShape(self.models[i])

#pone fondos azules a los costados simulando el cielo         
class FondoAzul():
    def __init__(self,count,fondo):
        
        fondoa1=bs.createTextureCube('azul.jpg')
        gpufondoa1 = es.toGPUShape(fondoa1, GL_REPEAT, GL_NEAREST)
        fondo.models.append(gpufondoa1)
        fondo.transform.append(tr.matmul([tr.uniformScale(24), tr.translate(-1, 0, 0.4+count)]))
        
        fondoa2=bs.createTextureCube('azul.jpg')
        gpufondoa2 = es.toGPUShape(fondoa2, GL_REPEAT, GL_NEAREST)
        fondo.models.append(gpufondoa2)
        fondo.transform.append(tr.matmul([tr.uniformScale(24), tr.translate(0, -1, 0.4+count)]))
        
        fondoa3=bs.createTextureCube('azul.jpg')
        gpufondoa3 = es.toGPUShape(fondoa3, GL_REPEAT, GL_NEAREST)
        fondo.models.append(gpufondoa3)
        fondo.transform.append(tr.matmul([tr.uniformScale(24), tr.translate(0, 1, 0.4+count)]))
        
        fondoa4=bs.createTextureCube('azul.jpg')
        gpufondoa4 = es.toGPUShape(fondoa4, GL_REPEAT, GL_NEAREST)
        fondo.models.append(gpufondoa4)
        fondo.transform.append(tr.matmul([tr.uniformScale(24), tr.translate(1, 0, 0.4+count)]))
        

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

#crea las flechas 
class Flecha():
    def __init__(self, posX, posY, posZ):
        gpuarrow = es.toGPUShape(shape = readOBJ('Arrow.obj', (0,0,0)))
        self.model=gpuarrow
        self.posx=posX*0.2-4
        self.posy=-posY*0.2
        self.posz=posZ*0.2
    #dibuja las flechas 
    def draw(self, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE,tr.matmul([  
                tr.rotationZ(-np.pi/2),
                tr.uniformScale(4),
                tr.translate(self.posy, self.posx, self.posz)]))
        pipeline.drawShape(self.model)
    #mueve las flechas 
    def update(self,dt):
        self.posx+=dt
             
     
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

def Amy_jump(estructura):
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
        tex_pipeline=es.SimpleTextureTransformShaderProgram()


        # Telling OpenGL to use our shader program
        glUseProgram(pipeline.shaderProgram)

        # Setting up the clear screen color
        glClearColor(0.85, 0.85, 0.85, 1.0)

        # As we work in 3D, we need to check which part is in front,
        # and which one is at the back
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Creamos los objetos 
        # Amy 
        gpuAmy = es.toGPUShape(shape = readOBJ('amy.obj', (1,0,0.5)))
        
        # Anillo (trofeo)
        gpuAnillo = es.toGPUShape(shape = readOBJ('ring.obj', (0.9,0.9,0)))
        
        # Fondo
        fondo=Fondo()
            
        #Piso
        piso = bs.createTextureCube('piso.jpg')
        gpupiso = es.toGPUShape(piso, GL_REPEAT, GL_LINEAR)
        piso_transform = tr.matmul([tr.uniformScale(24), tr.translate(0, 0, -0.53)])
    
        # Pantalla de inicio 
        amyi = es.toGPUShape(bs.createTextureQuad("amy2.png", 1, 1), GL_REPEAT, GL_LINEAR)
    
        # Pantala de perdida 
        eggman = es.toGPUShape(bs.createTextureQuad("eggman.png", 1, 1), GL_REPEAT, GL_LINEAR)
    
        # Pantalla de ganador 
        amyf = es.toGPUShape(bs.createTextureQuad("am.png", 1, 1), GL_REPEAT, GL_LINEAR)
    
        # Barras
        barras=CreateBarras()
        barras.create(estructura)
    
        #Revisamos el tiempo
        t0 = glfw.get_time()
        
        # Posiciones de Amy
        posX=0
        posY=0
        posZ=0.5
        
        #Cuenta los fondo que ya se crearon
        count=1
    
        # Indica hasta que altura se debe llegar al saltar 
        alt=0
        
        # Dice si se puede saltar o no 
        salto=True
        
        #Indica cuando se "pierde" por saltar mal 
        perder=False
    
        #Indica cuando se pierde por una flecha
        perder2=False
        
        # Dice si se debe mandar una flecha de ataque 
        arrow=True
        
        #Se crea la flecha con las posiciones hacia Amy
        flechas=Flecha(posX, posY,posZ)
        
        #Tamaño inicial de la imagen de partida, de perdida y de ganador
        ag=2
        eg=0
        af=0
    
        # rotaciones de Amy
        rotz=np.pi
        rotx=np.pi/2
        roty=0
        
        #Indica si ya estuvo en una barra 
        bt=False
        
        #Rotaciones y posiciones del aro 
        ra=0
        x=0
        y=0
        #Indica si gana o pierde 
        ganar=False
        
        while not glfw.window_should_close(window):
        # Using GLFW to check for input events
            glfw.poll_events()
            

            # Getting the time difference from the previous iteration
            t1 = glfw.get_time()
            dt = t1 - t0
            t0 = t1
        
            #Se define la vista "fija" del juego 
            view = tr.lookAt(
                np.array([12,-5,8+(posZ-0.5)]),
                np.array([posX*0.4,posY*0.4,posZ]),
                np.array([0,0,1])
                )
        
            #Cambia la vista mientras se mantengan apretadas las teclas 
            
            if (glfw.get_key(window, glfw.KEY_B) == glfw.PRESS):
                view = tr.lookAt(
                    np.array([0,1,17.5+(posZ)]),
                    np.array([0,0,0]),
                    np.array([0,0,1]))
            if (glfw.get_key(window, glfw.KEY_N) == glfw.PRESS):
                view = tr.lookAt(
                    np.array([-12,-5,7.5+posZ]),
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

            #Dibujamos el fondo 
            fondo.Draw(texture_pipeline, projection, view)
        
            # Revisamos si se debe crear otro fondo
            if posZ>13*count:
                fondoazul=FondoAzul(count, fondo)
                count+=1
        
            #Dibujamos el piso           
            glUseProgram(texture_pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "model"), 1, GL_TRUE, piso_transform)
            glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            texture_pipeline.drawShape(gpupiso)
        
            # Luz 
            glUseProgram(pipeline.shaderProgram)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)
            
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.3, 0.3, 0.3)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.2, 0.2, 0.2)
            
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 0, 0, posZ+5)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), 0, 0, posZ+5)
            glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 1000)
            glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.01)
            glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.1)
            glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)
                
            #Dibujamos a Amy
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE,tr.matmul([         
                    tr.translate(posX, posY, posZ),
                    tr.rotationZ(rotz),
                    tr.rotationX(rotx),
                    tr.rotationY(roty),
                    tr.uniformScale(0.4)]))
            pipeline.drawShape(gpuAmy)
        
            #Dibujamos el anillo a la altura de la ultima barra
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE,tr.matmul([         
                    tr.translate(x, y, barras.altura*2),
                    tr.rotationZ(ra),
                    tr.uniformScale(0.5)]))
            pipeline.drawShape(gpuAnillo)
        
            # Dibujamos la pantalla inicial
            glUseProgram(tex_pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(tex_pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
                tr.translate(0, 0, 0),
                tr.uniformScale(ag)]))
            tex_pipeline.drawShape(amyi)
        
            # Dibujamos la pantalla de perdida 
            glUniformMatrix4fv(glGetUniformLocation(tex_pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
                tr.translate(0, 0, 0),
                tr.uniformScale(eg)]))
            tex_pipeline.drawShape(eggman)
        
            # Dibujamos la pantalla de ganador  
            glUniformMatrix4fv(glGetUniformLocation(tex_pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
                tr.translate(0, 0, 0),
                tr.uniformScale(af)]))
            tex_pipeline.drawShape(amyf)
        
            # Hace una copia de la lista de barras 
            b=barras.barras
        
            #Indica que hay gravedad por lo cual amy va a caer mientras no este en una plataforma 
            grav=True
        
            #Cambia el angulo de de rotación del aro 
            ra-=2*dt
        
            #Revisa que la posición de las barras calza con Amy 
            for i in range(len(b)):
                if posX<=2*b[i].posx+1 and posX>=2*b[i].posx-1 and posY<=2*b[i].posy+1 and posY>=2*b[i].posy-1 and posZ<=b[i].posz*0.3+1.4 and posZ>=b[i].posz*0.3+1.25:
                    if b[i].real==False: #Revisa si la barra es real, de serlo no la dibuja y no apaga la gravedad 
                        b[i].dibujo=False
                    else:
                        grav=False #si no, apaga la gravedad 
                        bt=True #indica que ya se subio una barra 
                    
            # Implementa la gravedad 
            if posZ>0.6 and grav==True:
                posZ-=3*dt
            
            #Mueve a Amy dependiendo de la tecla que se precione 
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
            #Implementa los saltos 
            if (glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS):
                #si se puede saltar
                if salto==True: 
                    salto=False #se bloquea otro salto
                    alt=2+posZ #calcula hasta donde debe llegar 
                #si no pierde y no llega al limite de altura
                if alt>=posZ and perder==False: 
                    posZ+=5*dt #salta 
                #Si esta en una barra y aún no pierde 
                if grav==False and perder2==False:
                    salto=True #Puede volver a saltar 
                    perder=False #aún no pierde 
                #Inidica que perdio 
                if alt<posZ+0.01:
                    perder=True
            # Si es que se puede hacer una flecha 
            if arrow==True:
                ti=t1 #Revisamos el tiempo actual 
                arrow=False #decimos que no se pueden hacer mas flechas
                flechas=Flecha(posX,posY,posZ) #se indica las posicones de la flecha 
            # Si ya pasa un tiempo especifico
            if ti+3<t1:
                arrow=True # se puede hacer otra flecha 
            #Revisamos que una flecha toca a Amy
            if flechas.posx<=posX+0.1 and flechas.posx>=posX-0.1 and flechas.posy<=-posY*0.2+0.1 and flechas.posy>=-posY*0.2-0.1 and flechas.posz<=posZ*0.2+0.1 and flechas.posz>=posZ*0.2-0.1:
                perder2=True #Pierde
            #Mueve las flechas a partir de un tiempo en especifico 
            if t1>8:
                flechas.update(4*dt)
                flechas.draw(pipeline, projection, view) 
            #Hace el movimiento de la imagen inicial 
            if t1<8: 
                if ag>0:
                    ag-=dt    
            #Si pierde genera la imagen de game over y Amy empieza a rotar 
            if ((posZ>=0.5 and posZ<=0.6 and grav and bt) or perder2 or (salto==False and posZ>=0.5 and posZ<=0.6) )and ganar==False:
                if eg<2:
                    eg+=0.8*dt
                rotx-=2*dt
                rotz-=2*dt
            #Indica cuando gana 
            if barras.altura*2-posZ<=0.5 and barras.altura*2-posZ>=0 and grav==False:
                ganar=True
            #Mueve el aro a Amy 
                if x<1.7*posX:
                    x+=5*dt
                elif x>=1.7*posX:
                    x-=5*dt   
                if y<1*posY:
                    y+=5*dt
                elif y>=1*posY:
                    y-=5*dt
                #Hace el movimiento de la imagen de ganador 
                if af<2:
                    af+=0.8*dt
                
            #Dibuja las barras 
            barras.draw(color_pipeline,projection, view)
        
            # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
            glfw.swap_buffers(window)
        

        glfw.terminate()