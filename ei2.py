#TODO: choice for print statements

import pathlib
import sys
import os
import time
import __main__

class loadImports():
    def __init__(self) -> None:
        #get the parent folder __main__ is in
        self.main_name = str(__main__.__file__).split('\\')[-1]
        print(self.main_name)
        self.main_parent = pathlib.Path(__main__.__file__).parent.resolve()
        self.main_parent_name = str(self.main_parent).split('\\')[-1]
        self.main_grandparent = pathlib.Path(self.main_parent).parent.resolve()


'''
==============
loadUncles()
==============

This class loads all files in subfolders of the grandparent folder: f.ex

- grandparent
    - parent
        - main.py
        - module0.py
    - uncle1
        - module1.py
        - module2.py
    - uncle2
        -module3.py

in main.py you can loadUncles(). All modules 0-3 will be importable directly as:
    import modulex
    ...

Module 0 is possible by default python
module 1,2,3 are possible by loadUncles()
'''
class loadUncles(loadImports):
    def __init__(self) -> None:
        #initialise
        super().__init__()
        #get uncle folders of __main__
        self.uncles()
        #append uncles to path for importing
        self.append()

    def uncles(self) -> None:
        uncles = os.listdir(self.main_grandparent)
        self.main_uncles = [f'{self.main_grandparent}\\{folder}' for folder in uncles if folder != self.main_parent_name] #do not include parent

    def append(self) -> None:
        for uncle in self.main_uncles:
            sys.path.append(uncle)


'''
==============
loadSisters()
==============

This class loads all files in subfolders of the parent folder: f.ex

-Parent
    - main.py
    - module0.py
    - child1
        - module1.py
        - module2.py
    - child2
        -module3.py

in main.py you can loadSisters. All modules 0-3 will be importable directly as:
    import modulex
    ...

Module 0 is possible by default python
module 1,2,3 are possible by loadSisters()
'''
class loadSisters(loadImports):
    def __init__(self, project_path=None) -> None:
        #initialise
        super().__init__(project_path=project_path)
        #get sister folders of __main__
        self.sisters()
        #append sisters to path for importing
        self.append()

    def sisters(self) -> None:
        sisters = os.listdir(self.main_parent)
        self.main_sisters = [f'{self.main_grandparent}\\{folder}' for folder in sisters if folder != self.main_name] #do not include __main__

    def append(self) -> None:
        for sister in self.main_sisters:
            sys.path.append(sister)

#if you want to load both uncles and sisters, you can use this simple definition
def loadfamily():
    loadUncles()
    loadSisters()


'''
=================
loadProject(path)
=================
this class will load all files in a specific project folder (which must contain the main file)
f.ex

- project
    - folder 1
        - main.py
        - module0.py
        - folder 2
            - module1.py
            - module2.py
            - folder 2
                - module3.py
    - folder 3
        - module4.py
    - folder 4
        - module5.py
    - module6.py
    - module7.py

loadProject(project) *with project being path to folder*
=> this will load every module in the project folder, module0 - module 7

loadProject(folder 1)
=> this will load every module in folder 1, module0 - module3

loadProject(folder 4)
=> will raise an error, because folder 4 does not contain main.py

every module that is loaded can be imported as normal:
    import modulex
    ...

'''
class loadProject():
    def __init__(self,project_path,ignore_hidden=True) -> None:
        
        #set ignore_level
        self.ignore = ignore_hidden

        #set timer for potential timeout
        self.start_time = time.perf_counter()

        #check if project_path exists
        self.project_path = pathlib.Path(project_path)
        if not pathlib.Path.exists(self.project_path):
            raise ModuleNotFoundError(f"This path does not exist\npath: {self.project_path}")

        #get path of main
        self.main_path = __main__.__file__
        self.main_name = str(__main__.__file__).split("\\")[-1]

        #check if main is inside the project, else raise error
        if str(self.project_path).lower() not in str(self.main_path).lower():
            raise ModuleNotFoundError(f"project folder! does not contain {self.main_name}")

        #get the directory list
        self.dirlist()

        #append directory list to sys_path
        self.append()

    def timeout(self) -> bool:
        return abs(time.perf_counter() - self.start_time) > 3

    def dirlist(self) -> list:
        #basic info 
        self.final_paths = [str(self.project_path)]
        self.working_paths = [f"{self.project_path}\\{name}" for name in os.listdir(self.project_path)]

        #loop to get list of directories
        while True:
            to_del = []
            to_add = []
            #check if working_paths is empty and break if so
            if len(self.working_paths) == 0: break
            #go through working_paths
            for path in self.working_paths:
                name = str(path).split("\\")[-1]
                #check if path is folder
                if not os.path.isdir(path):
                    #if not folder, add to del and continue
                    to_del.append(path)
                    continue
                elif self.ignore and name[0] in ('.', '_'):
                    to_del.append(path)
                    continue
                else:
                    #if folder, add to final_paths and to_del, add children to to_add
                    #add folder to final_paths
                    self.final_paths.append(path)
                    #add to to_del
                    to_del.append(path)
                    #get children
                    try:
                        children = [f"{path}\\{child}" for child in os.listdir(path)]
                        to_add += children
                    except PermissionError: pass
            #delete to_del from working_paths
            for path in to_del:
                self.working_paths.remove(path)
            #add to_add to working_paths
            for path in to_add:
                self.working_paths.append(path)
            #check for timeout and raise error if so
            if self.timeout(): raise TimeoutError("Execution took too long, >3s")
        return self.final_paths

    def append(self) -> None:
        #append paths to sys_path
        try:
            for path in self.final_paths:
                sys.path.append(path)
        except: raise SystemError("Appending to system path failure")


'''
========================
loadTree(parent_folders)

loadTree will load every file under the n'th parent of main
f.ex.

- project
    - module4.py
    - folder1
        - module3.py
        - folder2
            - module2.py
            - folder3 
                - folder4
                    - module1.py
                - main.py
                - module0.py

in main.py, loadTree is used:
loadTree(int)

loadTree(1) => will load everything in parent folder (folder3) => modules 0 - 1 are loaded
loadTree(2) => will load everything in grandparent folder (folder2) => modules 0 - 2 are loaded
loadTree(4) => will load everything in 4th parent folder (project) => modules 0 - 4 are loaded
loadTree(0) => will raise an error
        
again, all loaded modules can be directly imported:
    import modulex
    ...

========================
'''
class loadTree(loadProject):
    def __init__(self, parents:int, ignore_hidden:bool = True) -> None:
        #save is_hidden
        self.is_hidden = ignore_hidden
        #get parents of main
        self.main_path = __main__.__file__
        cur_parent = self.main_path
        
        #error checking for parents argument
        if type(parents) is not int: raise ValueError(f'{parents} is of type: {type(parents)}.\nmust be int')
        if parents < 1: raise ValueError(f'parents argument must be equal to or greater than 1')
        if parents > len(self.main_path.split('\\'))-1: raise ValueError(f'parents argument is too big')

        #get the n'th parent
        newpath = self.main_path
        for _ in range(parents):
            newpath = pathlib.Path(newpath).parent.resolve()

        #initialise the loadProject file with newpath as projectpath
        super().__init__(newpath,self.is_hidden)