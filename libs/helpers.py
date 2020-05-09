# coding=utf-8
#!/usr/bin/env python3

from time import strftime
from colorama import init, Fore, Back, Style
from os import system, name
from ipaddress import ip_address

def is_ip(_str):
    try:
        ip_address(_str)
        return True
    except:
        return False
def clear_screen():
    system('cls' if name=='nt' else 'clear')
def success(message):
    print("{0}[{1}]{2} [ OK ] {3}{4}{5}".format(
        Style.BRIGHT + Fore.YELLOW,
        strftime("%d.%m.%y %X"),
        Fore.GREEN,
        Fore.WHITE + Style.BRIGHT,
        message,
        Style.RESET_ALL
    ))
def error(message):
    print("{0}[{1}]{2} [ ER ] {3}{4}{5}".format(
        Style.BRIGHT + Fore.YELLOW,
        strftime("%d.%m.%y %X"),
        Fore.RED,
        Fore.WHITE,
        message,
        Style.RESET_ALL
    ))
def info(message):
    print("{0}[{1}]{2} [INFO] {3}{4}{5}".format(
        Style.BRIGHT + Fore.YELLOW,
        strftime("%d.%m.%y %X"),
        Fore.CYAN,
        Fore.WHITE,
        message,
        Style.RESET_ALL
    ))
def get_os():
    if (name == "nt"):
        return "Windows"
    else:
        return "Linux"
def print_logo():
    logo = """
    _____  ________ __________  ___ ___  ____ __________________________________________ 
   /  _  \ \______ \\\\______   \/   |   \|    |   \      \__    ___/\_   _____/\______   \\
  /  /_\  \ |    |  \|    |  _/    ~    \    |   /   |   \\|    |    |    __)_  |       _/
 /    |    \|    `   \    |   \    Y    /    |  /    |    \    |    |        \ |    |   \\
 \____|__  /_______  /______  /\___|_  /|______/\____|__  /____|   /_______  / |____|_  /
         \\/        \\/       \\/       \\/                 \\/                 \\/         \\/ 

    Hichigo THT version 1.0
    
    """
    print(Style.BRIGHT + Fore.RED + logo +Style.RESET_ALL)