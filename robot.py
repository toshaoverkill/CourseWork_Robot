import pygame
import os
import math
import random


class Robot:
    DEFAULT_RADIUS = 10
    DEFAULT_OUTLINE_COLOR = (205, 133, 63)
    DEFAULT_INSIDE_COLOR = (255, 222, 173)
    MOVE_SPEED = 3

    def __init__(self, center, hexagon):
        self.center = center
        self.target = None  # Целевая точка, к которой робот движется
        self.radius = Robot.DEFAULT_RADIUS
        self.outline_color = Robot.DEFAULT_OUTLINE_COLOR
        self.inside_color = Robot.DEFAULT_INSIDE_COLOR

    def draw(self, screen):
        pygame.draw.circle(screen, self.outline_color, self.center, self.radius)
        pygame.draw.circle(screen, self.inside_color, self.center, self.radius - 1)

    def set_target(self, target):
        self.target = target

    def update(self):
        if self.target:
            # Рассчитываем вектор направления к целевой точке
            direction = pygame.math.Vector2(self.target[0] - self.center[0], self.target[1] - self.center[1])

            # Нормализуем вектор направления, чтобы получить единичный вектор
            direction.normalize_ip()

            # Умножаем направление на скорость перемещения
            movement = direction * Robot.MOVE_SPEED

            # Обновляем положение робота
            self.center = (self.center[0] + movement.x, self.center[1] + movement.y)

