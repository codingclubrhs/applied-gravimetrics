class Planet:
    def __init__(self, x, y, m, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.m = m
        self.locked = False
        self.vlock = False
    def passTime(self, time, d2x, d2y):
        if not self.vlock:
            self.dx += d2x*time
            self.dy += d2y*time
        if not self.locked:
            self.x += self.dx*time
            self.y += self.dy*time
    def __str__(self):
        return "Planet: [X=" + str(self.x) + ", Y=" + str(self.y) + ", M=" + str(self.m) + ", DX=" + str(self.dx) + ", DY=" + str(self.dy) + "]"