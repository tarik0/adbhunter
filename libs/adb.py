# coding=utf-8
#!/usr/bin/env python3

from libs.helpers import error, success, get_os, info
from libs.adbwrapper import AdbWrapper

class adb_client:
    def __init__(self, ip):
        self.ip = ip
        self.port = 5555
        self.device = None
        self.connected = False   
    def connect(self, auth_timeout=5):
        try:
            self.device = AdbWrapper()
            self.device.disconnect_all()
            success("{} adresine ADB ile bağlantı yapılıyor!".format(self.ip))
            self.device.connect(self.ip, timeout=auth_timeout)
            self.connected = True
            success("{} adresine ADB ile bağlantı yapıldı!".format(self.ip))
            return True
        except Exception as e:
            error(e)
            return False
    def close(self):
        try:
            self.device.disconnect_all()
            success("[{}] Bağlantı kapatıldı!".format(self.ip))
            return True
        except Exception as e:
            error(e)
            return False
    def pull(self, filename, dest_file_name, timeout=30):
        if (self.connected == False): return False
        try:
            info("[{0}] Dosya alınıyor: '{1}'".format(self.ip, filename))
            self.device.pull(filename, dest_file_name, timeout=timeout)
            success("[{0}] Dosya alınındı: '{1}'".format(self.ip, filename))
            return True
        except Exception as e:
            error(str(e))
            return False
    def send(self, command, timeout=5):
        if (self.connected == False): return False
        try:
            info("[{0}] Komut gönderiliyor: '{1}'".format(self.ip, command))
            tmp = self.device.shell(command, timeout=timeout)
            success("[{0}] '{1}' çıktısı: {2}".format(self.ip, command, tmp))
            return tmp
        except Exception as e:
            error(e)
            return False
    def upload_payload(self, timeout=180):
        if (self.connected == False): return False
        info("[{0}] Payload yükleniyor.".format(self.ip))
        try:
            tmp = self.device.install(timeout=180)
            if (not tmp): return False
            success("[{0}] Payload yüklendi.".format(self.ip))
            return True
        except Exception as e:
            error(e)
            return False

current_adb_client = None