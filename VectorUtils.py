import glm
from glm import *

def D2V(Degrees: 'float|int'):
    return glm.vec2(float(glm.cos(glm.radians(Degrees))), float(glm.sin(glm.radians(Degrees))))


def angleB2V(a: glm.vec2, b: glm.vec2):
    try:
        return glm.degrees(glm.acos(glm.dot(a, b) / (glm.length(a) * glm.length(b))))
    except ZeroDivisionError:
        return 0


def vec2str(vec: 'glm.vec1|glm.vec2|glm.vec3|glm.vec4') -> str:
    if isinstance(vec, glm.vec4): return f'Vector4({vec.x}, {vec.y}, {vec.z}, {vec.w})'
    if isinstance(vec, glm.vec3): return f'Vector3({vec.x}, {vec.y}, {vec.z})'
    if isinstance(vec, glm.vec2): return f'Vector2({vec.x}, {vec.y})'
    if isinstance(vec, glm.vec1): return f'Vector1({vec.x})'
