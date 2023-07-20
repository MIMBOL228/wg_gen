import pyqrcode

import subprocess
import re
import os

from requests import get

CONF_FILENAME = "int.conf"

def get_client_text(ip,csk,dns,spk, s_allowed_ip, endpoint):
    return "\n".join([
        "",
        "[Interface]",
        "Address = "+ip+"/24",
        "PrivateKey = "+csk,
        "DNS = "+dns,
        "",
        "[Peer]",
        "PublicKey = "+spk,
        "AllowedIPs = "+s_allowed_ip,
        "Endpoint = "+endpoint,
        "PersistentKeepalive = 20",
    ])

def get_server_text(name, cpk, c_allowed_ip):
    return "\n".join([
        "",
        "# " + name +  " Node",
        "[Peer]",
        "PublicKey = "+cpk,
        "AllowedIPs = "+c_allowed_ip,
    ])


client_keys = subprocess.check_output(['bash','./gen.sh']).decode("utf-8").split(" ") # Генерирование ключей


file = open(CONF_FILENAME).read()

server_keys = re.search(r"PrivateKey \= ([a-zA-Z0-9\/=]+) \#([a-zA-Z0-9\/=]+)", file)
server_keys = [server_keys.group(1), server_keys.group(2)]

server_port = re.search(r"ListenPort \= ([0-9]{1,5})", file).group(1)
server_ip = get('https://api.ipify.org').content.decode('utf8')

client_name = input("Название клиента:")
client_ip = input("IP клиента:")
aipk = input("Allowed IP в Peer клиента [0.0.0.0/0]") or "0.0.0.0/0" # Allowed IP Type
dns = input("DNS сервер [8.8.8.8]:") or "8.8.8.8"
echo_type=int(input("Тип вывода (0 - Консоль, 1 - Файл, 3 - QR код)"))

client_text = get_client_text(client_ip,client_keys[0],dns,server_keys[1], aipk , server_ip + ":" + server_port)
server_text = get_server_text(client_name, client_keys[1], client_ip+"/32")

if echo_type == 0:
    print(client_text)

file = open("client.conf", "w")
file.write(client_text)
file.close()

if echo_type == 3:
    os.system("bash ./qr.sh")

with open(CONF_FILENAME, 'a') as f:
    f.write('\n'+server_text)
r