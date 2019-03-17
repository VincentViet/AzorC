import click, os
from pathlib import Path
from examples import custom_style_1
from PyInquirer import prompt

QUESTIONS = [
    {
        'type': 'input',
        'name': 'project_name',
        'message': 'What is your project\'s name?',
    },
    {
        'type': 'input',
        'name': 'desc',
        'message': 'Description?',
    },
    {
        'type': 'list',
        'name': 'project_type',
        'message': 'Which project type do you want to generate?',
        'choices': ['C Library', 'C++ Library', 'C Executable', 'C++ Executable'],
        'default': 0
    },
    {
        'type': 'list',
        'name': 'language_standard',
        'message': 'Language standard?',
        'choices': ['C90', 'C99', 'C11'],
        'default': 0,
        'when': lambda answer: answer['project_type'] == 'C Library' or answer['project_type'] == 'C Executable'
    },
    {
        'type': 'list',
        'name': 'language_standard',
        'message': 'Language standard?',
        'choices': ['C++98', 'C++11', 'C++14', 'C++17'],
        'default': 0,
        'when': lambda answer: answer['project_type'] == 'C++ Library' or answer['project_type'] == 'C++ Executable'
    },
    {
        'type': 'list',
        'name': 'library_type',
        'message': 'Library type?',
        'choices': ['STATIC', 'SHARED'],
        'default': 0,
        'when': lambda answer: answer['project_type'] == 'C Library' or answer['project_type'] == 'C++ Library'
    },
]

C_IGNORE = """
# Prerequisites
*.d

# Object files
*.o
*.ko
*.obj
*.elf

# Linker output
*.ilk
*.map
*.exp

# Precompiled Headers
*.gch
*.pch

# Libraries
*.lib
*.a
*.la
*.lo

# Shared objects (inc. Windows DLLs)
*.dll
*.so
*.so.*
*.dylib

# Executables
*.exe
*.out
*.app
*.i*86
*.x86_64
*.hex

# Debug files
*.dSYM/
*.su
*.idb
*.pdb

# Kernel Module Compile Results
*.mod*
*.cmd
.tmp_versions/
modules.order
Module.symvers
Mkfile.old
dkms.conf
"""

CPP_IGNORE = """
# Prerequisites
*.d

# Compiled Object files
*.slo
*.lo
*.o
*.obj

# Precompiled Headers
*.gch
*.pch

# Compiled Dynamic libraries
*.so
*.dylib
*.dll

# Fortran module files
*.mod
*.smod

# Compiled Static libraries
*.lai
*.la
*.a
*.lib

# Executables
*.exe
*.out
*.app
"""

C_MAIN = """
#include <stdio.h>

int main(int argc, char** argv)
{{
    printf("hello, {0}");
    return 0;
}}"""

CPP_MAIN = """
#include <cstdio>

int main(int argc, char** argv)
{{
    printf("hello, {0}");
    return 0;
}}"""

C_MAKE_LIBRARY = """
cmake_minimum_required(VERSION 3.0)
project({0})

set(CMAKE_C_STANDARD {1})
set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY bin)

include_directories("include")

file(GLOB_RECURSE C_HEADER "${{PROJECT_SOURCE_DIR}}" "src/*.h" )
file(GLOB_RECURSE C_SRC "${{PROJECT_SOURCE_DIR}}" "src/*.c" )
file(GLOB_RECURSE LIB "${{PROJECT_SOURCE_DIR}}" "lib/*.a" )

add_library({0} {2} ${{C_HEADER}} ${{C_SRC}})
target_link_libraries({0} ${{LIB}})
"""

C_MAKE_EXECUTABLE = """
cmake_minimum_required(VERSION 3.0)
project({0})

set(CMAKE_C_STANDARD {1})
set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY bin)

include_directories("include")

file(GLOB_RECURSE C_HEADER "${{PROJECT_SOURCE_DIR}}" "src/*.h" )
file(GLOB_RECURSE C_SRC "${{PROJECT_SOURCE_DIR}}" "src/*.c" )
file(GLOB_RECURSE LIB "${{PROJECT_SOURCE_DIR}}" "lib/*.a" )

add_executable({0} ${{C_HEADER}} ${{C_SRC}})
target_link_libraries({0} ${{LIB}})
"""

CPP_MAKE_LIBRARY = """
cmake_minimum_required(VERSION 3.0)
project({0})

set(CMAKE_C_STANDARD {1})
set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY bin)

include_directories("include")

file(GLOB_RECURSE C_HEADER "${{PROJECT_SOURCE_DIR}}" "src/*.h" )
file(GLOB_RECURSE C_SRC "${{PROJECT_SOURCE_DIR}}" "src/*.c" )
file(GLOB_RECURSE CPP_HEADER "${{PROJECT_SOURCE_DIR}}" "src/*.hpp" )
file(GLOB_RECURSE CPP_SRC "${{PROJECT_SOURCE_DIR}}" "src/*.cc" )
file(GLOB_RECURSE LIB "${{PROJECT_SOURCE_DIR}}" "lib/*.a" )

add_library({0} {2} ${{C_HEADER}} ${{C_SRC}} ${{CPP_HEADER}} ${{CPP_SRC}})
target_link_libraries({0} ${{LIB}})
"""

CPP_MAKE_EXECUTABLE = """
cmake_minimum_required(VERSION 3.0)
project({0})

set(CMAKE_C_STANDARD {1})
set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY bin)

include_directories("include")

file(GLOB_RECURSE C_HEADER "${{PROJECT_SOURCE_DIR}}" "src/*.h" )
file(GLOB_RECURSE C_SRC "${{PROJECT_SOURCE_DIR}}" "src/*.c" )
file(GLOB_RECURSE CPP_HEADER "${{PROJECT_SOURCE_DIR}}" "src/*.hpp" )
file(GLOB_RECURSE CPP_SRC "${{PROJECT_SOURCE_DIR}}" "src/*.cc" )
file(GLOB_RECURSE LIB "${{PROJECT_SOURCE_DIR}}" "lib/*.a" )

add_executable({0} ${{C_HEADER}} ${{C_SRC}} ${{CPP_HEADER}} ${{CPP_SRC}})
target_link_libraries({0} ${{LIB}})
"""


def generate_c_library(name: str, standard: str, proj_type: str):
    if standard == 'C90':
        standard = '90'
    elif standard == 'C99':
        standard = '99'
    else:
        standard = '11'

    ignore = open(".gitignore", "w+")
    ignore.write(C_IGNORE)
    ignore.close()

    main = open("src/main.c", "w+")
    main.write(C_MAIN.format(name))
    main.close()

    cmake = open("CMakeLists.txt", "w+")
    cmake.write(C_MAKE_LIBRARY.format(name, standard, proj_type))
    cmake.close()


def generate_c_executable(name: str, standard: str):
    if standard == 'C90':
        standard = '90'
    elif standard == 'C99':
        standard = '99'
    else:
        standard = '11'

    ignore = open(".gitignore", "w+")
    ignore.write(C_IGNORE)
    ignore.close()

    main = open("src/main.c", "w+")
    main.write(C_MAIN.format(name))
    main.close()

    cmake = open("CMakeLists.txt", "w+")
    cmake.write(C_MAKE_EXECUTABLE.format(name, standard))
    cmake.close()


def generate_cpp_library(name: str, standard: str, proj_type: str):

    if standard == 'C++98':
        standard = '98'
    elif standard == 'C++11':
        standard = '11'
    elif standard == 'C++14':
        standard = '14'
    else:
        standard = '17'

    ignore = open(".gitignore", "w+")
    ignore.write(CPP_IGNORE)
    ignore.close()

    main = open("src/main.cc", "w+")
    main.write(CPP_MAIN.format(name))
    main.close()

    cmake = open("CMakeLists.txt", "w+")
    cmake.write(CPP_MAKE_LIBRARY.format(name, standard, proj_type))
    cmake.close()


def generate_cpp_executable(name: str, standard: str):
    if standard == 'C++98':
        standard = '98'
    elif standard == 'C++11':
        standard = '11'
    elif standard == 'C++14':
        standard = '14'
    else:
        standard = '17'

    ignore = open(".gitignore", "w+")
    ignore.write(CPP_IGNORE)
    ignore.close()

    main = open("src/main.cc", "w+")
    main.write(CPP_MAIN.format(name))
    main.close()

    cmake = open("CMakeLists.txt", "w+")
    cmake.write(CPP_MAKE_EXECUTABLE.format(name, standard))
    cmake.close()


@click.command()
def init():
    """Generate C/C++ project"""
    global root
    answers = prompt(QUESTIONS, style=custom_style_1)

    try:
        root = Path(os.getcwd(), answers['project_name'])
        os.mkdir(root)
        path = Path(root, 'include')
        os.mkdir(path)
        path = Path(root, 'lib')
        os.mkdir(path)
        path = Path(root, 'src')
        os.mkdir(path)

        os.chdir(root)

        readme = open("README.md", "w+")
        readme.write(
"""# %s
---------------
%s
""" % (answers['project_name'], answers['desc']))
        readme.close()

        if answers['project_type'] == 'C Library':
            generate_c_library(answers['project_name'], answers['language_standard'], answers['library_type'])
        elif answers['project_type'] == 'C Executable':
            generate_c_executable(answers['project_name'], answers['language_standard'])
        elif answers['project_type'] == 'C++ Library':
            generate_cpp_library(answers['project_name'], answers['language_standard'], answers['library_type'])
        else:
            generate_cpp_executable(answers['project_name'], answers['language_standard'])

        os.system('git init')
        os.system('git add .')
        os.system('git commit -m \"Create {0} project\"'.format(answers['project_name']))

    except OSError:
        print("[Creation of the directory %s failed]" % root)
        print(OSError.__str__)
    else:
        print("[Successfully created %s]" % root)
        print("[Successfully created %s]" % Path(root, 'include'))
        print("[Successfully created %s]" % Path(root, 'lib'))
        print("[Successfully created %s]" % Path(root, 'src'))
        print("[Successfully created %s]" % Path(root, 'README.md'))
        print("[Successfully created %s]" % Path(root, '.gitignore'))
        print("[Successfully created %s]" % Path(root, 'CMakeLists.txt'))
        print("[Successfully created %s]" % Path(root, 'src/main'))
