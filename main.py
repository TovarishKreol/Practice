from tkinter import *
from random import randint
global_missile_list = []
global_object_list = []
player = []
window = []

class Object():
    def __init__(self, x, y, HP, speed, size):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.HP = HP
        self.speed = speed
        self.size = size
        global_object_list.append(self)
        self.image_path = "../images/player.gif"
        self.image = PhotoImage(file=self.image_path)
        self.image_ref = window[0].create_image(self.x, self.y, image=self.image)
        
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
        self.image.coords(self.x, self.y)
            
    def target(self, x, y):
        self.target_x = x
        self.target_y = y
        
    def shoot(self, x, y):
        shot = Missile(self.x, self.y)
        Missile.target(x, y)
        
    def update(self):     
        if HP <= 0:
            self.destroy()
            exit
        self.move() 
            
    def destroy(self):
        global_object_list.remove(self)
        window[0].delete(self.image_ref)
        del self        

    def collision_correction(self, last_x, last_y):
        for concrete_object in global_object_list:
            if abs(concrete_object.x - self.x) < concrete_object.size + self.size\
            and abs(concrete_object.y - self.y) < concrete_object.size + self.size:
                self.x == last_x
                self.y == last_y



class Missile(Object):
    def __init__(self, x, y, HP, speed, size):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.HP = HP
        self.speed = speed
        global_missile_list.append(self)
        self.image_path = "../images/missile.gif"
        self.image = PhotoImage(file=self.image_path)
        window[0].create_image(self.x, self.y, image=self.image)
        self.image_ref = window[0].create_image(self.x, self.y, image=self.image)
        
    def move(self):
        last_x = self.x
        last_y = self.y
        if self.target_x * 200 < self.x:
            self.x -= speed * x / y
        elif self.target_x  * 200 > self.x:
            self.x += speed * x / y
        if self.target_y * 200 < self.y:
            self.y -= speed * x / y
        elif self.target_y * 200 > self.y:
            self.y += speed * x / y
        self.collision_correction(last_x, last_y)
    
    def collision_correction(self, last_x, last_y):
        for concrete_object in global_object_list:
            if abs(concrete_object.x - self.x) < concrete_object.size + self.size\
            and abs(concrete_object.y - self.y) < concrete_object.size + self.size:
                concrete_object.HP -=1
                self.destroy()
                exit
                
    def update(self):
        self.HP -= 1
        if HP <= 0:
            self.destroy()
            exit
        self.move()
        
class Enemy(Object):
    def __init__(self, x, y, HP, speed, size, e_range):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.HP = HP
        self.speed = speed
        self.size = size
        global_object_list.append(self)
        self.range = e_range
        self.image_path = "../images/enemy.gif"
        self.image = PhotoImage(file=self.image_path)
        window[0].create_image(self.x, self.y, image=self.image)
        self.image_ref = window[0].create_image(self.x, self.y, image=self.image)
        

        
    def update(self):
        if HP <= 0:
            self.destroy()
            exit
        if (player[0].x - self.x) < e_range and (player[0].y - self.y) < e_range:
            self.shoot(player[0].x, player[0].y)
        self.move()


class Decoration(Object):
    def __init__(self, x, y, HP, size):
        self.x = x
        self.y = y
        self.HP = HP
        self.size = size
        global_object_list.append(self)
        self.image_path = "../images/decor{}.gif".format(randint(1,5))
        self.image = PhotoImage(file=self.image_path)
        window[0].create_image(self.x, self.y, image=self.image)
        self.image_ref = window[0].create_image(self.x, self.y, image=self.image)
        
def main():
    
    root = Tk()
    canvas = Canvas(root, width=600, height=480)
    window.append(canvas)
    canvas.pack()
    gamer = Object(randint(0, 600), randint(0, 480), 10, 2, 1.5)
    player.append(gamer)
    gamer.destroy()
    root.mainloop()
    
if __name__ == "__main__":
        main()


