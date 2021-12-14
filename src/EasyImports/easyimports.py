import pathlib
import sys
import os
import __main__

class loadImports():
    def __init__(self) -> None:
        #get the parent folder __main__ is in
        self.main_parent = pathlib.Path(__main__.__file__).parent.resolve()
        self.main_parent_name = str(self.main_parent).split('\\')[-1]
        #get the grandparent folder of __main__ location
        self.grandparent()
        #get uncle folders of __main__ (all folders under grandparent)
        self.uncles()
        #append all uncles to path
        self.append()

    def grandparent(self) -> None:
        self.main_grandparent = pathlib.Path(self.main_parent).parent.resolve()

    def uncles(self) -> None:
        uncles = (os.listdir(self.main_grandparent))
        self.main_uncles = [f'{self.main_grandparent}\\{folder}' for folder in uncles if folder != self.main_parent_name] #do not include parent

    def append(self) -> None:
        for uncle in self.main_uncles:
            sys.path.append(uncle)