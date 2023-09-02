from typed_list import TypedList


class SymbolImage:
    def __init__(self, dirr: "list | TypedList", name: str = ""):
        self.dirr: list = dirr if isinstance(dirr, list) else dirr.returnAsList()
        self.name: str = name

    def get(self):
        return self.dirr


class SymbolImageAnimation:
    def __clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)

    def __init__(self, anim: list, loop=True,
                 start_now=True, start_frame=0, speed: float = 1):
        self.__anim: list = anim if isinstance(anim, list) else anim.returnAsList()
        self.frame = start_frame
        self.speed = speed
        self.__protect()
        self.__start = False
        self.loop = loop
        self.start() if start_now else self.stop()

    def __protect(self, do=False):
        if do:
            raise ValueError(f"Type of symbol image are not \"Symbols.{SymbolImage.__name__}\"")
        self.frame = max(self.frame, 0)
        self.speed = max(self.speed, 0.001)
        raiseanims = []
        for i in range(len(self.__anim)):
            if not isinstance(self.__anim[i], SymbolImage):
                raiseanims.append(i)
        if len(raiseanims) == 1:
            raise ValueError(
                f"Type of symbol image at position \"{raiseanims[0]}\" are not \"Symbols.{SymbolImage.__name__}\"")
        if len(raiseanims) != 0:
            raise ValueError(
                f"Type of symbol images at positions \"{raiseanims}\" are not \"Symbols.{SymbolImage.__name__}\"")

    def update(self):
        if round(self.frame) == 0 and not self.loop:
            self.frame = len(self.__anim) - 1
            self.stop()
        if self.__start:
            self.__protect()
            if self.frame < len(self.__anim) - 1:
                self.frame += self.speed
            else:
                self.frame = 0

    def start(self):
        self.__protect()
        self.__start = True

    def stop(self):
        self.__protect()
        self.__start = False

    def append(self, im: SymbolImage):
        if isinstance(im, SymbolImage):
            self.__anim.append(im)
        else:
            self.__protect(True)
        self.__protect()

    def get(self):
        return self.__anim[round(self.frame)]


class Border:
    """Representation of border like Symbols.SymbolImage"""

    def __init__(self):
        self.name = 'base'
        self.width = 5
        self.height = 5
        self.border_r = '│'
        self.border_l = '│'
        self.border_u = '─'
        self.border_d = '─'
        self.border_angle_rd = '┘'
        self.border_angle_dl = '└'
        self.border_angle_lu = '┌'
        self.border_angle_ur = '┐'

    def get(self):
        f = []
        f.append([])
        f[0].append(self.border_angle_lu)
        for j in range(self.width):
            f[0].append(self.border_u)
        f[0].append(self.border_angle_ur)
        for i in range(1, self.height):
            f.append([])
            f[i].append(self.border_l)
            for j in range(self.width):
                f[i].append(" ")
            f[i].append(self.border_r)
        f.append([])
        f[self.height].append(self.border_angle_dl)
        for j in range(self.width):
            f[self.height].append(self.border_d)
        f[self.height].append(self.border_angle_rd)
        return SymbolImage(f, name=self.name)

    def get_Arr(self):
        return [self.border_r, self.border_l, self.border_u, self.border_d, self.border_angle_rd, self.border_angle_dl,
                self.border_angle_lu, self.border_angle_ur]
