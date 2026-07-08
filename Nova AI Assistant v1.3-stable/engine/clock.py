import time


class Clock:

    def __init__(self, target_fps=120):

        self.target_fps = target_fps

        self.last_time = time.perf_counter()

        self.delta = 0


    def update(self):

        current = time.perf_counter()

        self.delta = current - self.last_time

        self.last_time = current


    def get_delta(self):

        return self.delta