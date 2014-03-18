from tkinter import *
global_missile_list = []
global_object_list = []

class Object():
    def __init__(self, x, y, HP, speed):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.HP = HP
        self.speed = speed
        global_object_list.append(self)
        
    def move(self, speed):
        last_x = self.x
        last_y = self.y
        if self.target_x < self.x:
            self.x -= speed
        elif self.target_x > self.x:
            self.x += speed
        if self.target_y < self.y:
            self.y -= speed
        elif self.target_y > self.y:
            self.y += speed
        self.collision_correction(last_x, last_y)
            
    def target(self, x, y):
        self.target_x = x
        self.target_y = y
        
    def shoot(self, x, y):
        shot = Missile(self.x, self.y)
        Missile.target(x, y)
        
    def update(self):
        self.move()                
        if HP <= 0:
            self.destroy()
            exit
            
    def destroy(self):
        global_object_list.remove(self)
        del self        

    def collision_correction(self, last_x, last_y):
        for concrete_object in global_object_list:
            if concrete_object.x == self.x and concrete_object.y == self.y:
                self.x == last_x
                self.y == last_y

class Missile(Object):
    def __init__(self, x, y, HP, speed):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.HP = HP
        self.speed = speed
        global_missile_list.append(self)

    def collision_correction(self, last_x, last_y):
        for concrete_object in global_object_list:
            if concrete_object.x == self.x and concrete_object.y == self.y:
                concrete_object.HP -=1
                self.destroy()
                exit
                
    def update(self):
        self.move()
        self.HP -= 1
        if HP <= 0:
            self.destroy()
            exit
        self.move()
        












def main():
    gamer = Object(10, 10, 10, 1)
    gamer.destroy()
    root = Tk()
    canvas = Canvas(root, width=300, height=200)
    canvas.pack()
    #root.mainloop() 
if __name__ == "__main__":
    main()

