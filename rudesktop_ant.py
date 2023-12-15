"""
Здравствуйте, меня зовут Куликов Петр и это мое решение задачи о муравье.
Уточню, что в зависимости от представления координат сетки, рисунок может изменяться.
В данном случае y - значение по горизонтали слева направо, а x - по вертикали сверху вниз.
Кроме того, если по условию, муравей, попадая на поле, сразу меняет его цвет и поворачивается, получается один рисунок.
Если он не поворачивается на первой клетке и не меняет её цвет, итоговый рисунок будет другой.
Я посчитал, что при попадании на поле, он должен сразу же поменять цвет и повернуться.
Итоговое количество черных клеток: 3684

P.S. проверил пошагово, он красит в черный стартовую клетку, идет вправо,вниз,влево,вверх,влево и тд
"""

import numpy as np  # для логики
import cv2  # для изображения


class ant():
    def __init__(self, x, y, facing, grid):  # инициализация муравья
        self.x = x  # координаты позиции муравья
        self.y = y  # координаты позиции муравья
        self.facing = facing  # направление муравья: 0 - вверх, 1 - вправо, 2 -вниз, 3 - влево
        self.grid = grid  # сетка

    def ant_rotate(self, cell, facing):  # направление муравья
        if not cell:  # поскольку массив нулей, использую отрицание для понятности
            self.facing = (facing + 1) % 4  # поворот по часовой стрелке
        else:
            self.facing = (facing - 1) % 4  # поворот против часовой стрелке
        return facing


    def ant_move_forward(self):  # движение муравья
        match self.facing:
            case 0:  # в зависимости от положения "головы" муравья, он передвигается, поворачивается и перекрашивает клетку
                self.x -= 1
                self.ant_rotate(self.grid[self.x,self.y], self.facing)
                self.grid[self.x,self.y] = abs(self.grid[self.x,self.y] - 1)
            case 1:
                self.y += 1
                self.ant_rotate(self.grid[self.x,self.y], self.facing)
                self.grid[self.x,self.y] = abs(self.grid[self.x,self.y] - 1)
            case 2:
                self.x += 1
                self.ant_rotate(self.grid[self.x,self.y], self.facing)
                self.grid[self.x,self.y] = abs(self.grid[self.x,self.y] - 1)
            case 3:
                self.y -= 1
                self.ant_rotate(self.grid[self.x,self.y], self.facing)
                self.grid[self.x,self.y] = abs(self.grid[self.x,self.y] - 1)

    def ant_start(self):  # метод для "запуска" муравья, который шагает, пока не дойдет до края
        while 0 <= self.x < self.grid.shape[0]-1 and 0 <= self.y < self.grid.shape[1]-1:
            self.ant_move_forward()
            #ant_showpath()  # пошаговая отрисовка для проверки
        print(np.sum(self.grid))  # подсчет пикселей
        self.ant_showpath()  # вызов отрисовки

    def ant_showpath(self):  # отрисовка пути
        img = np.array(self.grid*255 ,dtype=np.uint8)  # наверняка это можно оптимизировать и использовать np.bool_,
                                                       # но я не сообразил как. все значения умножаются на 255
        ret, bw_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)  # бинаризация изображения по порогу 127
        bw_img = cv2.bitwise_not(bw_img)  # инвертирование цветов
        cv2.imwrite("bw.png", bw_img, [cv2.IMWRITE_PNG_BILEVEL, 1])  # сохранение изображения с глубиной цвета 1бит
        cv2.imshow("Binary", bw_img)  # демонстрация изображения
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def test_start():
    new_grid = np.zeros((1024, 1024), dtype=bool)  # стартовые параметры сетки
    new_ant = ant(512, 512, 0, new_grid)  # позиция и направление муравья
    new_ant.ant_start()  # запуск муравья

test_start()