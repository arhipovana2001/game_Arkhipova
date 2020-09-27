import pygame
from random import random
from math import sqrt

SCREEN_SIZE = (1280, 720)


class Vector:
    """class describe vector"""
    def __init__(self, x, y):
        """initialization method"""
        self.x = x
        self.y = y

    def __add__(self, other):
        """return vector addition"""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """return subtraction vectors"""
        return Vector(self.x - other.x, self.y - other.y)

    def multiply(self, k):
        """return multiplying a vector by a number"""
        self.x = self.x * k
        self.y = self.y * k
        return Vector(self.x, self.y)

    def __mul__(self, other):
        """return scalar vector multiplication"""
        if type(other) == 'Vector':
            return Vector(self.x * other.x, self.y * other.y)
        else:
            return self.multiply(other)

    def __len__(self):
        """return vector lenght"""
        result = sqrt(int(self.x) ** 2 + int(self.y) ** 2)
        return int(result)

    def int_pair(self):
        """return a tuple of integer coordinates"""
        return tuple([int(self.x), int(self.y)])


class Line:
    """class describe line"""
    def __init__(self):
        """initialization method"""
        self.all_points = []
        self.all_speed = []

    def add_point(self, point, point_speed):
        """function add point"""
        self.all_points.append(point)
        self.all_speed.append(point_speed)

    def set_points(self):
        """function calculates the coordinates of points"""
        for p in range(len(self.all_points)):
            self.all_points[p].x += self.all_speed[p].x
            self.all_points[p].y += self.all_speed[p].y
            if self.all_points[p].x > SCREEN_SIZE[0] or self.all_points[p].x < 0:
                self.all_speed[p] = Vector(- self.all_speed[p].x, self.all_speed[p].y)
            if self.all_points[p].y > SCREEN_SIZE[1] or self.all_points[p].y < 0:
                self.all_speed[p] = Vector(self.all_speed[p].x, - self.all_speed[p].y)

    def draw_points(self, points, width=3, color=(255, 0, 255)):
        """function draw points"""
        for point in points:
            pygame.draw.circle(gameDisplay, color, point.int_pair(), width)
        self.draw_lines(points, width, color)

    def draw_lines(self, points, width=3, color=(255, 0, 255)):
        """function draw lines"""
        for point_number in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color, (int(points[point_number].x), int(points[point_number].y)),
                             (int(points[point_number + 1].x), int(points[point_number + 1].y)), width)


class Joint(Line):
    """class describe joint"""
    def __init__(self, count):
        """initialization method"""
        super().__init__()
        self.count = count

    def add_point(self, point, point_speed):
        """function add point"""
        super().add_point(point, point_speed)
        self.get_joint()

    def set_points(self):
        """function set points"""
        super().set_points()
        self.get_joint()

    def get_point(self, points, alpha, deg=None):
        """function get point"""
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points):
        """function get points"""
        alpha = 1 / self.count
        result = []
        for i in range(self.count):
            result.append(self.get_point(base_points, i * alpha))
        return result

    def get_joint(self):
        """function get joint"""
        if len(self.all_points) < 3:
            return []
        result = []
        for i in range(-2, len(self.all_points) - 2):
            pnt = []
            pnt.append((self.all_points[i] + self.all_points[i + 1]) * 0.5)
            pnt.append(self.all_points[i + 1])
            pnt.append((self.all_points[i + 1] + self.all_points[i + 2]) * 0.5)
            result.extend(self.get_points(pnt))
        return result

    def draw_lines(self, points, style="line", width=4, color=(255, 255, 255)):
        """function draw lines"""
        if style == "line":
            for point_number in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, (int(points[point_number].x), int(points[point_number].y)),
                                 (int(points[point_number + 1].x), int(points[point_number + 1].y)), width)


def display_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("arial", 30)
    font2 = pygame.font.SysFont("serif", 30)
    data = []
    data.append(["F1", "Помощь"])
    data.append(["R", "Перезапуск"])
    data.append(["P", "Воспроизвести / Пауза"])
    data.append(["Num+", "Добавить точку"])
    data.append(["Num-", "Удалить точку"])
    data.append(["", ""])
    data.append([str(steps), "текущих точек"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for item, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * item))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver")

    steps = 20
    working = True
    points = Line()
    speeds = Joint(steps)
    show_help = False
    pause = False
    color_param = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = Line()
                    speeds = Joint(steps)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.add_point(Vector(event.pos[0], event.pos[1]), Vector(random() * 2, random() * 2))
                #speeds.add_point(Vector(event.pos[0], event.pos[1]), Vector(random() * 2, random() * 2))

        gameDisplay.fill((0, 0, 0))
        color_param = (color_param + 1) % 360
        color.hsla = (color_param, 100, 50, 100)

        points.draw_points(points.all_points)
        #speeds.draw_lines(speeds.get_joint(), 'line', 4)

        if not pause:
            points.set_points()
            #speeds.set_points()
        if show_help:
            display_help()

        pygame.display.flip()
    pygame.display.quit()
    pygame.quit()
    exit(0)
