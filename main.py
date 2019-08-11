import os

class usuarios():
    def __init__ (self,nombre):
        self.sig=None
        self.ant=None
        self.nombre=nombre
class cc_usuario():
    def __init__(self):
        self.primero=None
        self.ultimo=None
        self.tam=0
    def agregar(self,name):
        nuevo=usuarios(name)
        if self.primero is None:
            self.primero=nuevo
            self.ultimo=nuevo
            self.primero.sig=self.ultimo
            self.ultimo.ant=self.primero
            self.tam += 1

        else:
            nuevo.ant=self.ultimo
            nuevo.sig=self.primero
            self.ultimo.sig=nuevo
            self.primero.ant=nuevo
            self.ultimo=nuevo
            self.tam+=1
            
            
                
               





#guenas

def main():
    #el main
    print("hola")

main()
