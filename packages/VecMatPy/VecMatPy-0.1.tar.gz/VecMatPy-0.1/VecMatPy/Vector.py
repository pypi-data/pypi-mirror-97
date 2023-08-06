import math
class Vector2D():
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def sum(self, vec2):
        self.x += vec2.x
        self.y += vec2.y

    def subtract(self, vec2):
        self.x -= vec2.x
        self.y -= vec2.y

    def scale(self, scalar):
        self.x *= scalar
        self.y *= scalar

    def setVector(self,x,y):
        self.x = x
        self.y = y

    def getMagnitude(self):
        ax = self.x * self.x
        bx = self.y * self.y
        d = ax + bx
        return math.sqrt(d)

    def negate(self):
        self.x *= -1
        self.y *= -1

    def normalise(self):
        m = self.getMagnitude()
        if m > 0:
            self.x /= m
            self.y /= m

    def dot(self,vec2):
        vx = self.x * vec2.X
        vy = self.y * vec2.y
        return vx + vy

    def dist(self, vec2):
        d = (self.x - vec2.x) * (self.x - vec2.x)
        e = (self.y - vec2.y) * (self.y - vec2.y)
        f = d + e
        return math.sqrt(f)

    def div(self, div):
        self.x /= div
        self.y /= div 

    def setMagnitude(self, len):
        self.normalise()
        self.scale(len)

    def limitMag(self, max):
        mSq = self.getMagnitude() * self.getMagnitude()
        if mSq > (max * max):
            self.setMagnitude(max)

    def copy(self):
        return self

    def getAngle(self, vec1):
        vx = self.x - vec1.x
        vy = self.y - vec1.y
        return math.degrees(math.atan2(vx, vy))
    
    def __str__(self):
        return str("X: " + str(self.x) + ", " "Y: " + str(self.y) + ", Mag: " + str(self.getMagnitude()))

class Vector3D():
    def __init__(self,x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z

    def sum(self, vec2):
        self.x += vec2.x
        self.y += vec2.y
        self.z += vec2.z

    def subtract(self, vec2):
        self.x -= vec2.x
        self.y -= vec2.y
        self.z -= vec2.z

    def scale(self, scalar):
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar

    def setVector(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def getMagnitude(self):
        ax = self.x * self.x
        bx = self.y * self.y
        cx = self.z * self.z
        d = ax + bx + cx
        return math.sqrt(d)

    def negate(self):
        self.x *= -1
        self.y *= -1
        self.z *= -1

    def normalise(self):
        m = self.getMagnitude()
        if m > 0:
            self.x /= m
            self.y /= m
            self.z /= m

    def dot(self,vec2):
        vx = self.x * vec2.X
        vy = self.y * vec2.y
        vz = self.z * vec2.z
        return vx + vy + vz

    def dist(self, vec2):
        d = (self.x - vec2.x) * (self.x - vec2.x)
        e = (self.y - vec2.y) * (self.y - vec2.y)
        f = (self.z - vec2.z) * (self.z - vec2.z)
        g = d + e + f
        return math.sqrt(g)

    def div(self, div):
        self.x /= div
        self.y /= div
        self.z /= div

    def setMagnitude(self, len):
        self.normalise()
        self.scale(len)

    def limitMag(self, max):
        mSq = self.getMagnitude() * self.getMagnitude()
        if mSq > (max * max):
            self.setMagnitude(max)

    def copy(self):
        return self

    def getAngle(self, vec1):
        vx = self.x - vec1.x
        vy = self.y - vec1.y
        vz = self.z - vec1.z
        numerator = vx + vy + vz
        denominator = math.sqrt((self.x * self.x + (self.y * self.y) + (self.z * self.z)) * math.sqrt((vec1.x * vec1.x) + (vec1.y * vec1.y) + (vec1.z * vec1.z)))
        return math.degrees(math.atan2(vx, vy))

    def __str__(self):
        return str("x: " + str(self.x) + ", y: " + str(self.y) + ", z: " + str(self.z) + ", Mag: " + str(self.getMagnitude()))

