# EasyImports
## About

EasyImports is a python package that allows users to easily access and import files from sister folders:\
**f.ex:**
```
- Project
    - Folder 1
        -main.py
    - Folder 2
        -userpackage1.py
        -other_stuff.py
    - My Folder 
        -important_package.py
```

if you would try to import anything in *main.py* that isn't in *Folder 1* you'll get an error.\
**F.ex:**

*in main.py*
```
import userpackage1
from Folder 2 import other_stuff.py
import My Folder.important_package.py
```

=> Each of these will raise a *ModuleNotFoundError*\
With EasyImports this can be fixed.

## Installing

To install EasyImports:
```
pip install EasyImports
```

## Loading Imports

Inside *main.py*, type the following code:
```
from EasyImports import easyimports
easyimports.loadImports()
```

Now, you can just import the files *userpackage1.py*, *other_stuff.py* and *important_package.py* like you would normally:
```
#import EasyImports and load sister files
from EasyImports import easyimports
easyimports.loadImports()

#import files
import userpackage1
import other_stuff
import important_package

#alternatively, you can also do
import userpackage1, other_stuff, important_package
```

## Pylance error

Sometimes, Pylance can raise a warning: *Import "package" could not be resolved*\
this isn't problematic, as the program will still run without issues, but it may be visually annoying\
you can fix this by ignoring the Pylance error:

```
#import EasyImports and load sister files
from EasyImports import easyimports
easyimports.loadImports()

#import files and ignore warning 
import userpackage1 #type: ignore
```
