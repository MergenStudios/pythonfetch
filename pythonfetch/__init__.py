import os
import psutil
import platform
from colorama import Fore, Style
from subprocess import run, CalledProcessError
import subprocess
import re

__version__ = "0.1.0"
__license__ = "GPL-3.0"
__author__ = "Adil Gurbuz"
__contact__ = "beucismis@tutamail.com"
__source__ = "https://github.com/beucismis/pythonfetch"
__description__ = "Python and system information command-line tool"

this_dir, this_filename = os.path.split(__file__)

SPACE = " "
D_COLORS = [
    Fore.RED,
    Fore.YELLOW,
    Fore.GREEN,
    Fore.CYAN,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.BLACK,
    Fore.WHITE,
]
B_COLORS = [
    Fore.LIGHTRED_EX,
    Fore.LIGHTYELLOW_EX,
    Fore.LIGHTGREEN_EX,
    Fore.LIGHTCYAN_EX,
    Fore.LIGHTBLUE_EX,
    Fore.LIGHTMAGENTA_EX,
    Fore.LIGHTBLACK_EX,
    Fore.LIGHTWHITE_EX,
]


def get_processor_name():
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command = "sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command).strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True)
        for line in all_info.decode().split("\n"):
            if "model name" in line:
                return re.sub(".*model name.*:", "", line, 1)
    return ""


def red(text):
    return Fore.LIGHTRED_EX + text + Style.RESET_ALL


with open(os.path.join(this_dir, "data/ascii-art.txt"), encoding="utf-8") as file:
    ART = [SPACE + line[:-2] for line in file.readlines()]


def render(info):
    for (art_line, info_line) in zip(ART, info):
        print("{}   {}".format(art_line, info_line))


def main():
    uname = os.uname()
    mem = psutil.virtual_memory()
    mem_total = round(mem.total / 1048576)
    mem_used = round(mem.used / 1048576)

    try:
        p = run(["gcc", "--version"], capture_output=True)
        # if you wanted, you could regex only the version
        gcc_ver = p.stdout.decode().split("\n")[0]
    except CalledProcessError:
        gcc_ver = "no gcc found"
    python_ver = platform.python_version()
    pip_ver = __import__("pip").__version__
    try:
        p = run(["pip3", "list"], capture_output=True)
        # if you wanted, you could regex only the version
        pip_packages = len(p.stdout.decode().split("\n"))
    except CalledProcessError:
        pip_packages = "could not find pip3"

    userinfo = "{}{}{}".format(red(os.getlogin()), "@", red(uname.nodename))
    splitline = "═" * (len(os.getlogin()) + len(uname.nodename) + 1)
    gcc_ver = "{}: {}".format(red("gcc ver"), gcc_ver)
    python_ver = "{}: {}".format(red("python ver"), python_ver)
    pip_ver = "{}: {}".format(red("pip ver"), pip_ver)
    pip_packages = "{}: {}".format(red("pip packages"), pip_packages)
    os_ = "{}: {}".format(red("os"), uname.version)
    kernel = "{}: {}".format(red("kernel"), uname.release)
    cpu = "{}: {}".format(red("cpu"), get_processor_name())
    ram = "{}: {} / {} {}".format(red("ram"), mem_used, mem_total, "MiB")

    bright_colors = [color + "███" for color in B_COLORS]
    dark_colors = [color + "███" for color in D_COLORS]

    render(
        [
            SPACE,
            SPACE,
            userinfo,
            splitline,
            gcc_ver,
            python_ver,
            pip_ver,
            pip_packages,
            os_,
            kernel,
            cpu,
            ram,
            SPACE,
            "".join(bright_colors) + Style.RESET_ALL,
            "".join(dark_colors) + Style.RESET_ALL,
            SPACE,
            SPACE,
        ]
    )


if __name__ == "__main__":
    main()
