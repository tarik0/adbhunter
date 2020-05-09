# coding=utf-8
#!/usr/bin/env python3

from libs.helpers import success, error, info

from requests import get
from subprocess import Popen, PIPE
from os import path, name, mkdir
from zipfile import ZipFile
from io import BytesIO

WINDOWS_DOWNLOAD_LINK = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
LINUX_DOWNLOAD_LINK = "https://dl.google.com/android/repository/platform-tools-latest-linux.zip"

DEFAULT_ADB_PATH = path.join(path.dirname(path.realpath(__file__)), "platform-tools", "adb")
DEFAULT_PULL_PATH = path.join(path.dirname(path.realpath(__file__)), "templates", "static", "pulls")
DEFAULT_APK_PATH = path.join(path.dirname(path.realpath(__file__)), "payload.apk")

class AdbInstaller:
    def __init__(self):
        self.default_download_path = path.join(
            path.dirname(path.realpath(__file__)),
            "platform-tools"
            )

    def __enter__(self):
        self.default_download_path = path.join(
            path.dirname(path.realpath(__file__)),
            "platform-tools"
            )
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    def is_installed(self):
        return path.exists(
            path.join(self.default_download_path)
        )

    def install(self):
        if (self.is_installed()):
            return

        info("ADB bulunamadı!")
        if (name == "nt"):
            info("Windows için ADB indiriliyor!")
            link = WINDOWS_DOWNLOAD_LINK
        else:
            info("Linux için ADB indiriliyor!")
            link = LINUX_DOWNLOAD_LINK
        
        try:
            mkdir(self.default_download_path)
            with get(link) as res:
                with ZipFile(BytesIO(res.content)) as zip_file:
                    zip_file.extractall(path.join(path.dirname(path.realpath(__file__))))
                    success("ADB Yüklendi")
        except Exception as e:
            error(e)
            
class AdbWrapper:
    def __init__(self, adb_path=DEFAULT_ADB_PATH):
        self.adb_path = adb_path    
    def disconnect_all(self):
        p = Popen([self.adb_path, "disconnect"], stdout=PIPE)
        out, err = p.communicate()
        
        if (err is not None):
            raise Exception(err.decode("utf8").replace("\r\r",""))
        
        return out.decode("utf8").replace("\r\r","")
    def connect(self, ip, timeout=5):
        p = Popen([self.adb_path, "connect", ip], stdout=PIPE)
        out, err = p.communicate(timeout=timeout)
        
        if (err is not None and out is None):
            raise Exception(err.decode("utf8").replace("\r\r",""))

        return out.decode("utf8").replace("\r\r","")
    def shell(self, command, timeout=5):
        cmd = command.split(" ")
        cmd.insert(0, self.adb_path)
        cmd.insert(1, "shell")
        p = Popen(cmd, stdout=PIPE)
        out, err = p.communicate(timeout=timeout)
        
        if (err is not None and out is None):
            raise Exception(err.decode("utf8").replace("\r\r",""))
        
        return out.decode("utf8").replace("\r\r","")    
    def pull(self, target_file_path, saved_file_name, timeout=30, default_pull_path=DEFAULT_PULL_PATH):
        p = Popen([self.adb_path, "pull", target_file_path, path.join(default_pull_path)], stdout=PIPE)
        out, err = p.communicate(timeout=timeout)
        
        if (err is not None and out is None):
            raise Exception(err.decode("utf8").replace("\r\r",""))
        
        return out.decode("utf8").replace("\r\r","")       
    def install(self, target_apk_path=DEFAULT_APK_PATH, timeout=180):
        p = Popen([self.adb_path, "install", target_apk_path], stdout=PIPE)
        out, err = p.communicate(timeout=timeout)
        
        if (err is not None and out is None):
            raise Exception(err.decode("utf8").replace("\r\r",""))
        
        return out.decode("utf8").replace("\r\r","")