#Импорт библиотек
from tkinter import *
from random import randint
from random import seed
from time import time
#Глобальные листы с объектами и счетчиками
global_missile_list = []
global_object_list = []
player = []
window = []
temp = [0, 0]
#Базовый класс, используется напрямую игроком.
#Также от него унаследованы остальные объекты в игре
class Object():
    #Инициализация, создание спрайта
    def __init__(self, x, y, HP, speed, size):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.HP = HP
        self.speed = speed
        self.size = size
        self.image_path = "images/player.gif"
        self.image = PhotoImage(file=self.image_path)
        self.image_ref = window[0].create_image(self.x, self.y, image=self.image)
        
    #Двинуть объект к цели, также вызвать коррецию столкновений и подвинуть спрайт
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
    #Нацелить объект        
    def target(self, x, y):
        self.target_x = x
        self.target_y = y
    #Выстрелить по координатам, создать самонаводяющуюся ракету, нацелить ее    
    def shoot(self, x, y):
        if self in player:
            shot = Missile(self.x, self.y, 40, 3, 3)
        else:
            shot = Missile(self.x, self.y, 20, 3, 4)
        shot.target(x, y)
    #Обновить статус объекта    
    def update(self):     
        if self.HP <= 0:
            self.destroy()
            exit
        self.move() 
    #Уничтожить объект удалив его из листа, к которому он принадлежит.
    #Также удаляет из окна его картинку
    def destroy(self):
        window[0].delete(self.image_ref)
        if self in global_object_list:
            global_object_list.remove(self)
        if self in player:
            player.remove(self)
        if self in global_missile_list:
            global_missile_list.remove(self)
    #Коррекция столконовений, через откат к предыдущему состоянию
    def collision_correction(self, last_x, last_y):
        for concrete_object in global_object_list:
            if abs(concrete_object.x - self.x) < concrete_object.size + self.size\
            and abs(concrete_object.y - self.y) < concrete_object.size + self.size:
                self.x == last_x
                self.y == last_y


#Класс самонаводящейся ракеты, комментариев особых не будет.
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
        self.image_path = "images/missile.gif"
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
        if self.HP < 15:
            self.collision_correction(last_x, last_y)
        window[0].coords(self.image_ref, self.x, self.y)

    #Если происходит столкновение - уничтожается и вычитает один HP из объекта
    #с которым было столкновение
    def collision_correction(self, last_x, last_y):
        for concrete_object in player:
            if abs(concrete_object.x - self.x) < concrete_object.size + self.size\
            and abs(concrete_object.y - self.y) < concrete_object.size + self.size:
                concrete_object.HP -=1
                self.destroy()
                exit
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
        
#Класс врага        
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
        self.image_path = "images/enemy.gif"
        self.image = PhotoImage(file=self.image_path)
        self.image_ref = window[0].create_image(self.x, self.y, image=self.image)

    #Если в его радиусе видимости игрок - начинает стрелять    
    def update(self):
        if self.HP <= 0:
            self.destroy()
            exit
        if len(player) != 0:
            if (player[0].x - self.x) < self.range and (player[0].y - self.y) < self.range:
                self.shoot(player[0].x, player[0].y)
        self.move()

#Просто декорация, не может двигаться
class Decoration(Object):
    def __init__(self, x, y, HP, size):
        self.x = x
        self.y = y
        self.HP = HP
        self.size = size
        global_object_list.append(self)
        self.image_path = "images/decor{}.gif".format(randint(1,5))
        self.image = PhotoImage(file=self.image_path)
        window[0].create_image(self.x, self.y, image=self.image)
        self.image_ref = window[0].create_image(self.x, self.y, image=self.image)
        
    def move(self):
        pass
#Инициализация, создание игрока, врагов и декораций
def init():
    gamer = Object(randint(0, 600), randint(0, 480), 40, 2, 3)
    player.append(gamer)
    for x in range(randint(5, 10)):
        enemy = Enemy(randint(0, 600), randint(0, 480), 2, 1, 3, 50)
    for x in range(randint(5, 10)):
        temp[0] += 1
        decor = Decoration(randint(0, 600), randint(0, 480), 2, 3)
#Очищение ссылок на объекты
def clear():
    del global_object_list[:]
    del global_missile_list[:]
    del player[:]
    del window[:]
#Нацелить игрока по клику мышки
def target_player(event):
    player[0].target(event.x, event.y)
#Нацелить игрока на цель и выстрелить
def shoot_player(event):
    player[0].shoot(event.x, event.y)
#Основная функция цикла, в которой всё обновляется    
def main_loop(temp):
    seed(time())
    player[0].update()
    for x in global_object_list:
        if temp[1] == 5:
            x.target(randint(0, 600), randint(0, 480))
        x.update()
    for x in global_missile_list:
        x.update()
        
        
#Начало, создание root'a - Tk приложения, canvas окна.
#Объявление двух событий и прикрепление их к функциям
#Главный цикл игры + проверка на разницу во времени, для верной временной разниц
#между кадрами. Проверка на победу или поражение
def main():
    root = Tk()
    canvas = Canvas(root, width=600, height=480)
    window.append(canvas)
    canvas.pack()
    init()
    canvas.bind("<Button-1>", target_player)
    canvas.bind("<Button-3>", shoot_player)
    start_time = time()
    temp[1] = 0
    while True:
        next_time = time()
        try:
            root.update()
        except:
            break
        if next_time - start_time > 0.05:
            temp[1] += 1
            start_time = next_time
            main_loop(temp)
            if temp[1] == 5:
                temp[1] = 0
        if len(player) == 0:
            print("GAME OVER, YOU LOST")
            root.destroy()
            break
        elif len(global_object_list) == temp[0]:
            print("WIN")
            root.destroy()
            break
    #PURGE THE UNCLEAN
    clear()
#Откуда есть пошло начало программы    
if __name__ == "__main__":
        main()

