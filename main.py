from tkinter import *
from random import randint
from time import time
global_missile_list = []
global_object_list = []
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
        
    def move(self):
        last_x = self.x
        last_y = self.y
        if self.target_x < self.x:
            self.x -= self.speed
        elif self.target_x > self.x:
            self.x += self.speed
        if self.target_y < self.y:
            self.y -= self.speed
        elif self.target_y > self.y:
            self.y += self.speed
        self.collision_correction(last_x, last_y)
        window[0].coords(self.image_ref, self.x, self.y)
            
    def target(self, x, y):
        self.target_x = x
        self.target_y = y
        
    def shoot(self, x, y):
        shot = Missile(self.x, self.y, 20, 3, 3)
        shot.target(x, y)
        
    def update(self):     
        if self.HP <= 0:
            self.destroy()
            exit
        self.move() 
            
    def destroy(self):
        window[0].delete(self.image_ref)
        if self in global_object_list:
            global_object_list.remove(self)        

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
        self.size = size
        global_missile_list.append(self)
        self.image_path = "../images/missile.gif"
        self.image = PhotoImage(file=self.image_path)
        window[0].create_image(self.x, self.y, image=self.image)
        self.image_ref = window[0].create_image(self.x, self.y, image=self.image)
        
    def move(self):
        last_x = self.x
        last_y = self.y
        if self.target_x < self.x:
            self.x -= self.speed
        elif self.target_x > self.x:
            self.x += self.speed
        if self.target_y < self.y:
            self.y -= self.speed
        elif self.target_y > self.y:
            self.y += self.speed
        if self.HP < 15:
            self.collision_correction(last_x, last_y)
        window[0].coords(self.image_ref, self.x, self.y)

        
    def collision_correction(self, last_x, last_y):
        for concrete_object in global_object_list:
            if abs(concrete_object.x - self.x) < concrete_object.size + self.size\
            and abs(concrete_object.y - self.y) < concrete_object.size + self.size:
                concrete_object.HP -=1
                self.destroy()
                exit
                
    def update(self):
        self.HP -= 1
        if self.HP <= 0:
            self.destroy()
            exit
        self.move()
        
    def destroy(self):
        window[0].delete(self.image_ref)
        if self in global_missile_list:
            global_missile_list.remove(self)
        
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
        if self.HP <= 0:
            self.destroy()
            exit
        if (global_object_list[0].x - self.x) < self.range and (global_object_list[0].y - self.y) < self.range:
            self.shoot(global_object_list[0].x, global_object_list[0].y)
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
        
    def move(self):
        pass

def init():
    gamer = Object(randint(0, 600), randint(0, 480), 15, 2, 3)
    global_object_list.append(gamer)
    for x in range(5, 15):
        enemy = Enemy(randint(0, 600), randint(0, 480), 2, 1, 3, 50)
        global_object_list.append(enemy)
    for x in range(5, 15):
        decor = Decoration(randint(0, 600), randint(0, 480), 2, 3)
        global_object_list.append(decor)

def clear():
    del global_object_list[:]
    del global_missile_list[:]
    del window[:]

def target_player(event):
    global_object_list[0].target(event.x, event.y)

def shoot_player(event):
    global_object_list[0].shoot(event.x, event.y)
    
def main_loop():
        global_object_list[0].update()
        for x in global_object_list[1:]:
            x.update()
        for x in global_missile_list:
            x.update()
        
        
    
def main():
    root = Tk()
    canvas = Canvas(root, width=600, height=480)
    window.append(canvas)
    canvas.pack()
    init()
    canvas.bind("<Button-1>", target_player)
    canvas.bind("<Button-3>", shoot_player)
    start_time = time()
    while True:
        next_time = time()
        root.update()
        if next_time - start_time > 0.05:
            start_time = next_time
            main_loop()
    clear()
    
if __name__ == "__main__":
        main()


