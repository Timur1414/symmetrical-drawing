from math import sqrt, acos, pi, cos, sin
import pygame
from constants import size, width, height, center, BLACK, WHITE


class Game:
    def __init__(self):
        self.end = False
        self.screen = pygame.display.set_mode(size)
        self.drawing_flag = False
        self.points = []
        self.symmetrical_points = []
        self.radius_of_circumscribed_circle = sqrt((width // 2) ** 2 + (height // 2) ** 2)
        self.count_lines = 2
        self.lines = []
        self.lines_enable = True

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.drawing_flag = True
                elif event.button == 2:
                    self.lines_enable = not self.lines_enable
                elif event.button == 3:
                    self.points = []
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.drawing_flag = False
            elif event.type == pygame.MOUSEMOTION:
                if self.drawing_flag:
                    x = event.pos[0] - center[0]
                    y = event.pos[1] - center[1]
                    self.points.append([y, x])
                    self.points.append([-y, x])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                    self.count_lines = min(10, self.count_lines + 2)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    self.count_lines = max(2, self.count_lines - 2)

    def process_logic(self):
        self.symmetrical_points = []
        for point in self.points:
            radius = sqrt(point[0] ** 2 + point[1] ** 2)
            corner = acos(point[0] / radius)
            for _ in range(self.count_lines):
                corner += 2 * pi / self.count_lines
                x = radius * cos(corner)
                y = radius * sin(corner)
                self.symmetrical_points.append([x, y])
        self.lines = []
        corner = 0
        for i in range(self.count_lines):
            start = [0, 0]
            start[0] = self.radius_of_circumscribed_circle * cos(corner) + center[0]
            start[1] = self.radius_of_circumscribed_circle * sin(corner) + center[1]
            end = [0, 0]
            end[0] = self.radius_of_circumscribed_circle * cos(corner + pi) + center[0]
            end[1] = self.radius_of_circumscribed_circle * sin(corner + pi) + center[1]
            self.lines.append([start, end])
            corner += pi / self.count_lines

    def process_draw(self):
        self.screen.fill(BLACK)
        if self.lines_enable:
            for line in self.lines:
                pygame.draw.line(self.screen, WHITE, line[0], line[1])
        for point in self.symmetrical_points:
            x = point[0] + center[0]
            y = point[1] + center[1]
            pygame.draw.circle(self.screen, WHITE, [y, x], 2)
        pygame.display.flip()

    def main_loop(self):
        while not self.end:
            self.process_events()
            self.process_logic()
            self.process_draw()
            pygame.time.wait(5)

    def exit(self):
        self.end = True
