from settings import pygame


class Timer:
    def __init__(self, duration, repeated=False, callback=None) -> None:
        self.repeated = repeated
        self.callback = callback
        self.duration = duration

        self.start_time = 0
        self.active = False

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration and self.activate:
            if self.callback and self.start_time != 0:
                self.callback()

            # reset timer
            self.deactivate()

            # repeat the timer
            if self.repeated:
                self.activate()
