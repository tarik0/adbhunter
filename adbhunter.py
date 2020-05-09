# coding=utf-8
#!/usr/bin/env python3

__author__ = "Hichigo TurkHackTeam"
__license__ = "GPLv3"
__version__ = "1.0.0"

from os import _exit
from libs.website import website_app
from libs.libshodan import web
from libs.helpers import error, success, clear_screen, print_logo
from libs.adbwrapper import AdbInstaller, AdbWrapper

try:
    from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher
except ImportError:
    from cherrypy.wsgiserver import CherryPyWSGIServer as WSGIServer, WSGIPathInfoDispatcher 

def main():
    clear_screen()
    print_logo()

    with AdbInstaller() as installer:
        installer.install()
    
    AdbWrapper().disconnect_all()
    success("Açık kalan ADB bağlantıları kapatıldı!")

    web.api_key = "Girilmedi!"
    success("Sunucu başlatılıyor!")
    
    try:
        http_server = WSGIServer(("127.0.0.1", 5000), PathInfoDispatcher({'/': website_app}))
        success("Sunucu başlatıldı!")
        success("Arayüz adresi: http://localhost:5000")
        http_server.start()
    except KeyboardInterrupt:
        clear_screen()
        success("Kapatılıyor!")
        _exit(0)

if __name__ == "__main__":
    main()