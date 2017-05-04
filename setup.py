import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["json", "sets", "os", "pickle", "random", "sys", "nltk"]}

setup(  name = "zork",
        version = "0.1",
        keywords = "zork",
        license = "Python Software Foundation License",
        maintainer = "Siddharth Sahay",
        maintainer_email = "sahaysid@gmail.com",
        description = "Zork, the classic text based game, with a customisable map",
        options = {"build_exe": build_exe_options},
        executables = [Executable("zork.py")])

