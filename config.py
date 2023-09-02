import json
from os import listdir
from os.path import abspath, dirname, isfile, join

from symbols import SymbolImage

configs = {}
with open(dirname(abspath(__file__))+'\\config.json') as json_file:
    configs = json.load(json_file)

objMaps = {}
for i in [f for f in listdir(dirname(abspath(__file__)) + "\\Maps\\") if
          isfile(join(dirname(abspath(__file__)) + "\\Maps\\", f))]:
    with open(f"{dirname(abspath(__file__))}\\Maps\\{i}") as json_file:
        objMaps.update(json.load(json_file))
del i
images = {}
for i in [f for f in listdir(dirname(abspath(__file__)) + "\\TextImages\\") if
          isfile(join(dirname(abspath(__file__)) + "\\TextImages\\", f))]:
    with open(f"{dirname(abspath(__file__))}\\TextImages\\{i}") as json_file:
        jl = json.load(json_file)
        for j in jl:
            images.update({j: SymbolImage(name=j, dirr=jl.get(j))})
del i,j
