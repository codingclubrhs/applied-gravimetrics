class Planet:
    def __init__(self, x, y, m, dx=0, dy=0, locked = False, vlock=False):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.m = m
        self.locked = locked
        self.vlock = vlock
        self.radius = 1
    def passTime(self, time, d2x, d2y):
        if not (self.vlock or self.locked):
            self.dx += d2x*time
            self.dy += d2y*time
            # self.dx *= 0.999
            # self.dy *= 0.999
        if not self.locked:
            self.x += self.dx*time
            self.y += self.dy*time
    def __str__(self):
        return "Planet: [X=" + str(self.x) + ", Y=" + str(self.y) + ", M=" + str(self.m) + ", DX=" + str(self.dx) + ", DY=" + str(self.dy) + "]"