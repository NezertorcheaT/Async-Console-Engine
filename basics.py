from __future__ import annotations

import importlib
import random
from typing import final

import VectorUtils
import all_subclasses
import logger
import objects
from UI import *
from colors import BaceColor
from config import *
from draw_matrix import DrawMatrix
from logger import *

MAP: Map = None
UP = "up"
DOWN = "down"
RIGHT = "right"


class Component:
    """Standard Component"""

    def __init__(self, gameobject: Object):
        self.gameobject: Object = gameobject

    def fixed_upd(self):
        ...

    def upd(self):
        ...

    def late_upd(self):
        ...

    def start(self):
        ...

    def awake(self):
        ...

    def __str__(self):
        return "{0}({1}null)".format(self.__class__.__name__, "".join(
            [
                f"{i}: {str(self.__dict__[i]) if not isinstance(self.__dict__[i], (VectorUtils.vec1, VectorUtils.vec2, VectorUtils.vec3, VectorUtils.vec4)) else VectorUtils.vec2str(self.__dict__[i])}; "
                if i != 'gameobject' and i != 'parent' and i != 'nears'
                else ''
                for i in self.__dict__]))


class Object:
    """Object representation"""
    name = ''
    tag = ""
    __components = []
    isInstantiated = False

    def __init__(self, name: str, map: Map, parent: Transform = None):
        self.name = name
        self.MAP = map
        self.tag = ''
        self.layer = 0
        self.enabled = True
        self.isInstantiated = False
        self.__components = TypedList(type_of=Component, data=[])
        self.AddComponent(Transform)
        self.transform: Transform = self.GetAllComponents()[0]
        if parent is None:
            self.transform.parent = self.transform
        else:
            self.transform.parent = parent

    def __str__(self):
        return f"Obj(name:{self.name}, tag:{self.tag}, layer:{self.layer})"

    @final
    def upd(self):
        self.transform.upd()

        for i in self.GetAllComponents():
            i.upd()

    @final
    def fixed_upd(self):
        for i in self.GetAllComponents():
            i.fixed_upd()

    @final
    def late_upd(self):
        for i in self.GetAllComponents():
            i.late_upd()

    @final
    def start(self):
        for i in self.GetAllComponents():
            i.start()

    @final
    def awake(self):
        for i in self.GetAllComponents():
            i.awake()

    @final
    def AddComponent(self, comp: Component):
        a = comp(self)
        self.__components.append(a)
        return a

    @final
    def GetComponentByID(self, i) -> Component:
        return self.__components[i]

    @final
    def AddCreatedComponent(self, comp):
        self.__components.append(comp)

    @final
    def AddComponents(self, comps: list):
        for i in comps:
            self.__components.append(i(self))

    @final
    def GetAllComponents(self) -> list[Component]:
        return self.__components

    @final
    def GetAllComponentsOfType(self, typ: Component) -> list[Component]:
        if configs["USE RECURSION"]:
            return self.__gacotRec(typ)
        else:
            l = []
            for i in self.__components:
                if isinstance(i, typ):
                    l.append(i)
            return l

    @final
    def GetAllComponentsOfTypes(self, typs: []) -> list[Component]:
        if configs["USE RECURSION"]:
            return self.__gacotsRec(typs)
        else:
            l = []
            for i in self.__components:
                if isinstance(i, tuple(typs)):
                    l.append(i)
            return l

    def __gacotsRec(self, typs, l=[], i=0):
        if i >= len(self.__components):
            return l
        if isinstance(self.__components[i], typs):
            return self.__gacotRec(typs, l=l + [self.__components[i]], i=i + 1)
        return self.__gacotRec(typs, l=l, i=i + 1)

    @final
    def Find(self, name: str) -> Object:
        MAP.ObjList.getObjByName(name)

    @final
    def FindWithComponent(self, comp: Component) -> Object:
        if configs["USE RECURSION"]:
            return self.__fwcRec(comp)
        else:
            for i in MAP.ObjList.getObjs():
                if i.GetComponent(comp):
                    return i

    def __fwcRec(self, comp, i=0):
        if i >= len(MAP.ObjList.getObjs()):
            return None
        if MAP.ObjList.getObjs()[i].GetComponent(comp):
            return MAP.ObjList.getObjs()[i]
        return self.__gcRec(comp, i + 1)

    @final
    def FindAllWithComponent(self, comp: Component) -> list[Object]:
        if configs["USE RECURSION"]:
            return self.__fawcRec(comp)
        else:
            l = []
            for i in MAP.ObjList.getObjs():
                if i.GetComponent(comp):
                    l.append(i)
            return l

    def __fawcRec(self, comp: Component, l=[], i=0):
        if i >= len(MAP.ObjList.getObjs()):
            return l
        if MAP.ObjList.getObjs()[i].GetComponent(comp):
            return self.__fawcRec(comp, l=l + [MAP.ObjList.getObjs()[i]], i=i + 1)
        return self.__fawcRec(comp, l=l, i=i + 1)

    @final
    def FindByTag(self, tag: str) -> Object:
        if configs["USE RECURSION"]:
            return self.__fbtRec(tag)
        else:
            for i in MAP.ObjList.getObjs():
                if i.tag == tag:
                    return i

    def __fbtRec(self, tag, i=0):
        if i >= len(MAP.ObjList.getObjs()):
            return None
        if MAP.ObjList.getObjs()[i].tag == tag:
            return MAP.ObjList.getObjs()[i]
        return self.__fbtRec(tag, i + 1)

    @final
    def FindAllByTag(self, tag: str) -> list[Object]:
        if configs["USE RECURSION"]:
            return self.__fabtRec(tag)
        else:
            l = []
            for i in MAP.ObjList.getObjs():
                if i.tag == tag:
                    l.append(i)
            return l

    def __fabtRec(self, tag: str, l=[], i=0):
        if i >= len(MAP.ObjList.getObjs()):
            return l
        if MAP.ObjList.getObjs()[i].tag == tag:
            return self.__fabtRec(tag, l=l + [MAP.ObjList.getObjs()[i]], i=i + 1)
        return self.__fabtRec(tag, l=l, i=i + 1)

    def __gacotRec(self, typ, l=[], i=0):
        if i >= len(self.__components):
            return l
        if isinstance(self.__components[i], typ):
            return self.__gacotRec(typ, l=l + [self.__components[i]], i=i + 1)
        return self.__gacotRec(typ, l=l, i=i + 1)

    @final
    def GetComponent(self, typ: Component) -> Component:
        if configs["USE RECURSION"]:
            return self.__gcRec(typ)
        else:
            for i in self.__components:
                if isinstance(i, typ):
                    return i
            return None

    def __gcRec(self, typ, i=0):
        if i >= len(self.__components):
            return None
        if isinstance(self.__components[i], typ):
            return self.__components[i]
        return self.__gcRec(typ, i + 1)

    @final
    def RemoveComponent(self, typ: Component):
        if configs["USE RECURSION"]:
            return self.__rcRec(typ)
        else:
            for i in self.__components:
                if isinstance(i, typ):
                    self.__components.remove(i)
                    return

    @final
    def RemoveComponentCreated(self, typ: Component):
        if configs["USE RECURSION"]:
            return self.__rcRecC(typ)
        else:
            for i in self.__components:
                if i == typ:
                    self.__components.remove(i)
                    return

    def __rcRec(self, typ: Component, i=0):
        if i >= len(self.__components):
            return
        if isinstance(self.__components[i], typ):
            self.__components.pop(i)
            return
        return self.__gcRec(typ, i + 1)

    def __rcRecC(self, typ: Component, i=0):
        if i >= len(self.__components):
            return
        if self.__components[i] == typ:
            self.__components.pop(i)
            return
        return self.__gcRecC(typ, i + 1)

    @final
    def PopComponent(self, i: int):
        self.__components.pop(i)

    @final
    def __check(self, n):
        if type(n) in (int, float, VectorUtils.vec3):
            return n
        else:
            return None


class Behavior(Component):
    """Custom script behavior representation"""
    startPos: VectorUtils.vec3 = VectorUtils.vec3()

    def __init__(self, gameobject: Object):
        super().__init__(gameobject)
        self.transform = self.gameobject.transform

    @final
    def start(self):
        self.Start()

    @final
    def awake(self):
        self.Awake()

    def Update(self):
        ...

    def FixedUpdate(self):
        ...

    def LateUpdate(self):
        ...

    def Start(self):
        ...

    def Awake(self):
        ...

    @final
    def fixed_upd(self):
        self.FixedUpdate()

    @final
    def upd(self):
        self.Update()

    @final
    def late_upd(self):
        self.LateUpdate()

    def OnCollide(self, collision: Collision):
        ...

    def StayCollide(self, collision: Collision):
        ...

    @staticmethod
    def Instantiate(MAP: Map, Pos: VectorUtils.vec2 = VectorUtils.vec2(), comps=(), tag='') -> Object:
        b = Object(f"obj_({str(len(MAP.ObjList.getObjs()))})", MAP)
        b.tag = tag
        b.transform.local_position = Pos
        b.isInstantiated = True
        b.AddComponents(comps)

        MAP.ObjList.addObj(b)

        b.awake()
        b.start()
        return b

    @staticmethod
    def Destroy(o: Object = None):
        if o is not None:
            MAP.ObjList.removeObj(o)
        else:
            return


class Transform(Component):
    """Transformation representation"""

    def __init__(self, gameobject: Object, parent=None):
        super().__init__(gameobject)
        self.local_position: VectorUtils.vec2 = VectorUtils.vec2(0, 0)
        self.parent: Transform = parent
        self.position: VectorUtils.vec2 = self.__getPosition()
        self.nears: list[Transform] = []

    def upd(self):
        super().upd()
        n = self.findAllObjsAtRad(self.position, 3)
        for i in n:
            if i is None or not isinstance(i, Object) or i == self.gameobject:
                continue
            self.nears += [i.transform]
        self.position = self.__getPosition()

    def __getPosition(self) -> VectorUtils.vec2:
        if self.parent is not None and self.parent != self:
            p = self.__getParents(parents=[self.parent])
            g: VectorUtils.vec2 = self.local_position
            for i in p:
                g = g + i.local_position
            return g
        else:
            return self.local_position

    def __getParents(self, par=None, parents: list[Transform] = None) -> list[Transform]:
        if parents is None:
            parents = []
        if par is not None:
            if par.parent is not None:
                return self.__getParents(par=par.parent, parents=parents + [par])
            else:
                return parents + [par]
        else:
            return parents

    def moveDir(self, Dir: VectorUtils.vec2):
        self.setLocalPosition(self.local_position + Dir)

    def setLocalPosition(self, V: VectorUtils.vec2):
        self.local_position = V

    @staticmethod
    def findAllObjsAtRad(V: VectorUtils.vec2, rad: float) -> list[Object]:
        g = dict(zip([(i if (ds := VectorUtils.distance(V, i.transform.position)) <= rad else 'None') for i in
                      MAP.ObjList.getObjs()], [(ds if ds <= rad else 'None') for _ in MAP.ObjList.getObjs()]))
        if g.get('None', False): g.pop('None')
        return list(dict(sorted(g.items(), key=lambda item: item[1])).keys())

    @staticmethod
    def findNearObjByRad(V: VectorUtils.vec2, rad: float) -> Object:
        return dict(zip(range(len((g := Transform.findAllObjsAtRad(V, rad)))), g)).get(0, None)


class Camera(Component):
    """Camera representation"""

    def __init__(self, gameobject: Object):
        super().__init__(gameobject)
        self.draw_layers: TypedList[int] = TypedList(type_of=int, data=[0])
        self.offset = VectorUtils.vec2(configs["WIDTH"] / 2, configs["HEIGHT"] / 2)


class Drawer(Component):
    """Representation of renderer in world"""

    # symb = ' '

    def __init__(self, gameobject: Object):
        super().__init__(gameobject)
        self.symb = ""
        self.color = ""

    def upd(self):
        if self.symb != "":
            self.drawSymb(self.gameobject.MAP.matrix, self.symb, self.color, self.gameobject.transform.position,
                          self.gameobject.layer)

    @final
    def drawSymb(self, a: DrawMatrix, symb: str, color: str, pos: VectorUtils.vec2, layer=0):
        cam_obj = self.gameobject.FindByTag("MainCamera")
        pos = VectorUtils.vec2(pos.x, -pos.y)
        if cam_obj is None:
            cam_obj = self.gameobject.FindWithComponent(Camera)
        if cam_obj is None:
            return
        cam_comp: Camera = cam_obj.GetComponent(Camera)
        cam_pos = cam_obj.transform.position

        if configs.get("LOG DRAW CALLS", False): logger.Logger.log(
            f' symb= "{symb}"; color= {color}; pos= {VectorUtils.vec2str(pos)}; layer= {layer}; cam_comp= {cam_comp}',
            logger.Logger.DrawCall)

        if 0.0 <= pos.y - cam_pos.y + cam_comp.offset.y < configs['HEIGHT'] and \
                0.0 <= pos.x - cam_pos.x + cam_comp.offset.x < configs['WIDTH'] and \
                symb != "nl" and \
                layer in cam_comp.draw_layers:
            a[int(VectorUtils.clamp(pos.y - cam_pos.y + cam_comp.offset.y, 0.0, configs['HEIGHT'] - 1.0)),
              int(VectorUtils.clamp(pos.x - cam_pos.x + cam_comp.offset.x, 0.0, configs['WIDTH'] - 1.0))] = BaceColor(
                color)() + symb

    @final
    def drawSymbImage(self, a: DrawMatrix, img: SymbolImage, pos: VectorUtils.vec2, layer=0, flip_h=False,
                      flip_v=False):
        for i in range(len(img.get()) - 1, -1, -1) if flip_h else range(len(img.get())):
            for j in range(len(img.get()[i])) if flip_v else range(len(img.get()[i]) - 1, -1, -1):
                self.drawSymb(a, img.get()[i][j], '',
                              pos + VectorUtils.vec2(-j if flip_h else j, i if flip_v else -i),
                              layer=layer)

    @final
    def drawLine(self, a: DrawMatrix, symb: str, color: str, pos1: VectorUtils.vec2, pos2: VectorUtils.vec2, layer=0):
        # UI.printStrAtPos(Vector3.angleB2V((pos1 - pos2).norm, Vector3(1)), 0, 50)
        # p = VectorUtils.angleB2V(pos1 - pos2, VectorUtils.vec2(1, 1))
        for i in range(int(0 if pos1.x > pos2.x else pos1.x - pos2.x),
                       int(pos1.x - pos2.x if pos1.x > pos2.x else 0)):
            self.drawSymb(a, symb[i % len(symb)], color,
                          VectorUtils.vec2(i, (pos1.y - pos2.y) / (pos1.x - pos2.x) * (i - pos2.x)),
                          layer=layer)
        for i in range(int(0 if pos1.y > pos2.y else pos1.y - pos2.y),
                       int(pos1.y - pos2.y if pos1.y > pos2.y else 0)):
            self.drawSymb(a, symb[i % len(symb)], color,
                          VectorUtils.vec2((pos1.x - pos2.x) / (pos1.y - pos2.y) * (i - pos2.y), i),
                          layer=layer)

    @final
    def clearSymb(self, a: DrawMatrix, pos: VectorUtils.vec2):
        self.drawSymb(a, ' ', '', pos)

    @final
    def clearAll(self, a: DrawMatrix):
        a.matrix = DrawMatrix().matrix
        # for i in a.leny:
        #    for j in a.lenx:
        #        self.clearSymb(VectorUtils.vec3(i, j))


class Collision:
    def __init__(self, ):
        self.normal = VectorUtils.vec2(0, 0)
        self.collider: Collider = None
        self.length = 1

    def __str__(self):
        return f"Collision()"


class Collider(Component):
    """Standard Collider"""

    def __init__(self, gameobject):
        super().__init__(gameobject)
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0

    def _stay_collide(self, selfCollision: Collision, otherCollision: Collision):
        for beh in otherCollision.collider.gameobject.GetAllComponentsOfType(Behavior):
            beh.StayCollide(selfCollision)
        for beh in selfCollision.collider.gameobject.GetAllComponentsOfType(Behavior):
            beh.StayCollide(otherCollision)

        for rb in otherCollision.collider.gameobject.GetAllComponentsOfType(RigidBody):
            rb.velocity += selfCollision.normal / selfCollision.length
        for rb in selfCollision.collider.gameobject.GetAllComponentsOfType(RigidBody):
            rb.velocity += otherCollision.normal / otherCollision.length

    def _on_collide(self, selfCollision: Collision, otherCollision: Collision):
        for beh in otherCollision.collider.gameobject.GetAllComponentsOfType(Behavior):
            beh.OnCollide(selfCollision)
        for beh in selfCollision.collider.gameobject.GetAllComponentsOfType(Behavior):
            beh.OnCollide(otherCollision)


class BoxCollider(Collider):
    """Collider like rectangle"""

    def __init__(self, gameobject):
        super().__init__(gameobject)
        self.width = 1
        self.height = 1
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0

    def fixed_upd(self):
        self.left = self.gameobject.transform.position.x - self.width / 2
        self.right = self.gameobject.transform.position.x + self.width / 2
        self.top = self.gameobject.transform.position.y + self.height / 2
        self.bottom = self.gameobject.transform.position.y - self.height / 2

        for near in self.gameobject.FindAllWithComponent(Collider):
            if near == self.gameobject: continue
            for collider in near.GetAllComponentsOfType(Collider):
                if collider.left < self.right and \
                        collider.right > self.left and \
                        collider.bottom < self.top and \
                        collider.top > self.bottom:

                    norm = VectorUtils.vec2(0, 0)
                    if collider.top < self.top and collider.bottom > self.bottom:
                        norm.x = -1 if collider.gameobject.transform.position.x > self.gameobject.transform.position.x else 1
                    if collider.left > self.left and collider.right < self.right:
                        norm.y = -1 if collider.gameobject.transform.position.y > self.gameobject.transform.position.y else 1
                    if norm == VectorUtils.vec2(0, 0):
                        norm = -VectorUtils.normalize(
                            collider.gameobject.transform.position - self.gameobject.transform.position)
                    if norm == VectorUtils.vec2(0, 0):
                        norm = VectorUtils.normalize(
                            VectorUtils.vec2(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)))
                    logger.Logger.log(VectorUtils.vec2str(norm))

                    coll = Collision()
                    coll.normal = norm
                    coll.collider = collider

                    self_coll = Collision()
                    self_coll.normal = -norm
                    self_coll.collider = self

                    self._stay_collide(self_coll, coll)
                    # return


class RigidBody(Component):
    """Representation of physics"""

    def __init__(self, gameobject: Object):
        super().__init__(gameobject)
        self.velocity = VectorUtils.vec2(0, 0)
        self.drag = 0.1

    def fixed_upd(self):
        # self.velocity += VectorUtils.vec2(0,self.gravity)
        if self.velocity != VectorUtils.vec2(0, 0):
            self.gameobject.transform.moveDir(self.velocity * self.drag)
            self.velocity -= self.velocity * self.drag


for module in os.listdir(os.path.dirname(__file__) + "\\Scripts"):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    # __import__("Scripts." + module[:-3], locals(), globals())
    importlib.import_module("Scripts." + module[:-3])
del module


def all_components():
    return all_subclasses.all_subclasses(Component)


def getcls(n: str):
    for jj in all_components():
        logger.Logger.log(jj.__name__)
        if jj.__name__ == n:
            return jj


logger.Logger.log(str([i.__name__ for i in all_components()]) + ' ass')


class Map:
    def __init__(self, map_name: str):
        if map_name in objMaps:
            self.ObjList = objects.GlobalObjectList()
            self.ui = UI()
            self.matrix = DrawMatrix()

            mape = objMaps[map_name]

            for im in mape:
                bb = Object(im, self)
                bb.transform.local_position = VectorUtils.vec2(float(mape[im]["startPos"].get('x', 0)),
                                                               float(mape[im]["startPos"].get('y', 0)))
                bb.enabled = mape[im].get("enabled", False)
                bb.tag = mape[im].get("tag", '')
                bb.layer = mape[im].get("layer", 0)
                for j in mape[im]["components"]:

                    bbc = getcls(j)(bb)
                    for jji in mape[im]["components"][j]:
                        if isinstance(bbc.__getattribute__(jji), VectorUtils.vec3):
                            bbc.__setattr__(jji,
                                            VectorUtils.vec3(float(mape[im]["components"][j][jji].get('x', 0)),
                                                             float(mape[im]["components"][j][jji].get('y', 0)),
                                                             float(mape[im]["components"][j][jji].get('z', 0))))
                            continue
                        if isinstance(bbc.__getattribute__(jji), VectorUtils.vec2):
                            bbc.__setattr__(jji,
                                            VectorUtils.vec2(float(mape[im]["components"][j][jji].get('x', 0)),
                                                             float(mape[im]["components"][j][jji].get('y', 0))))
                            continue
                        if isinstance(bbc.__getattribute__(jji), TypedList):
                            bbc.__setattr__(jji, TypedList(from_dict=mape[im]["components"][j][jji]))
                            continue
                        bbc.__setattr__(jji, mape[im]["components"][j][jji])
                    bb.AddCreatedComponent(bbc)
                self.ObjList.addObj(bb)
                del bb

            for im in mape:
                if mape[im].get("parent", '') != '':
                    self.ObjList.getObjByName(im).transform.parent = self.ObjList.getObjByName(
                        mape[im]["parent"]).transform
