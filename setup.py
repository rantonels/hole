from distutils.core import setup
import py2exe

setup(
    console=["hole"],
    options = {
        "py2exe":{
            "dist_dir":"",
            "unbuffered":True,
            "excludes":["curses"],
            "optimize":0,
            "bundle_files":1
        }
    }
    )

