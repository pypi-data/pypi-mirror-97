import os
import os.path
import shutil
from pyrustic.manager import constant
from pyrustic.jasonix import Jasonix
from pyrustic.gurl import Gurl
import pyrustic


def check_project_state(target):
    """ Target is the path to the project
    Return:
        0: all right
        1: uninitialized project
        2: uninstalled project
    """
    app_pkg = os.path.basename(target)
    app_dir = os.path.join(target, app_pkg)
    if not os.path.exists(app_dir):
        return 1
    data = pyrustic.dist(app_pkg)
    if not data:
        return 2
    return 0


def copyto(src, dest):
    """
    Please make sure that DEST doesn't exist yet !
    Copy a file or contents of directory (src) to a destination file or folder (dest)
    """
    if not os.path.exists(src) or os.path.exists(dest):
        return False
    if os.path.isdir(src):
        try:
            shutil.copytree(src, dest)
        except Exception as e:
            return False
    else:
        try:
            shutil.copy2(src, dest)
        except Exception as e:
            return False
    return True


def moveto(src, dest):
    """
    If the DEST exists:
        * Before moveto *
        - /home/lake (SRC)
        - /home/lake/fish.txt
        - /home/ocean (DEST)
        * Moveto *
        moveto("/home/lake", "/home/ocean")
        * After Moveto *
        - /home/ocean
        - /home/ocean/lake
        - /home/ocean/lake/fish.txt
    Else IF the DEST doesn't exist:
        * Before moveto *
        - /home/lake (SRC)
        - /home/lake/fish.txt
        * Moveto *
        moveto("/home/lake", "/home/ocean")
        * After Moveto *
        - /home/ocean
        - /home/ocean/fish.txt


    Move a file or directory (src) to a destination folder (dest)
    """
    if not os.path.exists(src) or os.path.exists(dest):
        return False
    try:
        shutil.move(src, dest)
    except Exception as e:
        return False
    return True


def package_name_to_path(target, package_name, prefix=""):
    # returns a dotted package name to a regular pathname
    # example: package_name_to_path("/home/proj", "view.lol", prefix="tests.")
    return os.path.join(target, *((prefix + package_name).split(".")))


def build_package(target, package_name, prefix=""):
    """
    Literally build a package, returns None or the string pathname
    package represented by prefix must already exist
    """
    splitted = package_name.split(".")
    dir = package_name_to_path(target, prefix) if prefix else target
    for item in splitted:
        dir = os.path.join(dir, item)
        if os.path.exists(dir):
            continue
        try:
            os.mkdir(dir)
            with open(os.path.join(dir, "__init__.py"), "w") as file:
                pass
        except Exception as e:
            return None
    if not os.path.isdir(dir):
        return None
    return dir


def module_name_to_class(module_name):
    """
    Convert a module name like my_module.py to a class name like MyModule
    """
    name = os.path.splitext(module_name)[0]
    # ...
    if not "_" in name:
        return strictly_capitalize(name)
    else:
        splitted = name.split("_")
        cache = []
        for x in splitted:
            cache.append(strictly_capitalize(x))
        return "".join(cache)


def strictly_capitalize(string):
    # I don't remember why I haven't used str.capitalize()
    return string[0].upper() + string[1:]


def get_root_from_package(package_name):
    """
    Return the root from a dotted package name.
    Example the root here "my.package.is.great" is "my".
    """
    splitted = package_name.split(".")
    root = None
    for x in splitted:
        if x == "" or x.isspace():
            continue
        root = x
        break
    return root


def get_manager_jasonix(readonly=True):
    jasonix = Jasonix(constant.MANAGER_SHARED_DATA_FILE,
                      readonly=readonly)
    return jasonix


def get_sqleditor_jasonix(readonly=True):
    jasonix = Jasonix(constant.SQLEDITOR_SHARED_DATA_FILE,
                      readonly=readonly)
    return jasonix


def get_runtest_jasonix(readonly=True):
    jasonix = Jasonix(constant.RUNTEST_SHARED_DATA_FILE,
                      readonly=readonly)
    return jasonix


def get_hub_jasonix(readonly=True):
    jasonix = Jasonix(constant.HUB_SHARED_DATA_FILE,
                      readonly=readonly)
    return jasonix


def create_gurl():
    headers = {"Accept": "application/vnd.github.v3+json",
               "User-Agent": "Pyrustic"}
    gurl = Gurl(headers=headers)
    return gurl


def get_hub_url(res):
    target = "https://api.github.com"
    return "{}{}".format(target, res)
