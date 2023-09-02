import VectorUtils
import keyboard

from basics import *


class Player(Behavior):
    speed = 0.5
    coll = None
    fr = False
    f = VectorUtils.vec2()

    def Start(self):
        self.rr: Drawer = self.gameobject.GetComponent(Drawer)
        self.rb: RigidBody = self.gameobject.GetComponent(RigidBody)
        self.gameobject.MAP.ui.add("", True)
        self.coll: Collider = self.gameobject.GetComponent(Collider)
        # self.gameobject.GetComponent(Drawer).color = "Blue"

    def Update(self):
        self.transform.moveDir(self.f)

        self.f = VectorUtils.vec2(0, 0)
        if keyboard.is_pressed("w"):
            self.f = self.f + VectorUtils.vec2(0, self.speed)
        if keyboard.is_pressed("a"):
            self.f = self.f + VectorUtils.vec2(-self.speed, 0)
        if keyboard.is_pressed("s"):
            self.f = self.f + VectorUtils.vec2(0, -self.speed)
        if keyboard.is_pressed("d"):
            self.f = self.f + VectorUtils.vec2(self.speed, 0)
        self.rr.symb = "5"

    def StayCollide(self, collision: Collision):
        self.rr.symb = "6"

    def LateUpdate(self):
        # self.rr.drawLine(self.gameobject.MAP.matrix, 'э', '', self.transform.position, VectorUtils.vec2(0, 0))
        # self.rr.drawSymbImage(self.gameobject.MAP.matrix, config.images.get('table'), self.transform.position)
        self.gameobject.MAP.ui.changeSpace(0, f'pos = {self.transform.position}', True)
        self.gameobject.MAP.ui.changeSpace(1, f'pos = {self.rb.velocity}', True)

    # UI.printImageAtPos("table", self.transform.position.x, self.transform.position.y)
