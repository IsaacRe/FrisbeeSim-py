from graphics import *


class Window:

    def __init__(self, title, height, width):
        self.frame = GraphWin(title, height, width)
        self.frame.setBackground('green')
        self.h = height
        self.w = width

    def close(self):
        self.frame.close()

    def add_object(self, size, x, y, color='blue'):
        obj = CircleWrapper(Point(self.w / 2 + x, self.w / 2 + y), size)
        obj.setFill(color)
        obj.draw(self.frame)
        return obj

    def del_objects(self, objs):
        for obj in objs:
            obj.undraw()
        self.frame.update()


class CircleWrapper(Circle):

    def move_to(self, x, y):
        x_current = self.getCenter().x
        y_current = self.getCenter().y
        self.move(x - x_current, y - y_current)