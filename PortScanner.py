import sys
import socket
import threading
from datetime import datetime
from queue import Queue

print_lock = threading.Lock()

if len(sys.argv) == 2:
    target = socket.gethostbyname(sys.argv[1]) 

else:
    print("[X] IP Invalid | Usage: python port-scanner <IP>")

    sys.exit()

print("[✓] Lancement du scan sur :" + target)

def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            with print_lock:
                print("[✓] Le Port {} est ouvert.".format(port))
        s.close()

    except KeyboardInterrupt:
        print("\nFin de la recherche des ports !")
        sys.exit()

    except socket.gaierror:
        print("Le nom d'hôte n'a pas pu être résolu.")
        sys.exit()

    except socket.error:
        print("Impossible de se connecter au serveur.")
        sys.exit()

def dispatch_thread():
    while True:
        portNumber = ports.get()
        scan_port(portNumber)
        ports.task_done()

ports = Queue()

for i in range(0, 30):
    t = threading.Thread(target=dispatch_thread)
    t.daemon = True
    t.start()

for portNumber in range(1, 101):
    ports.put(portNumber)

ports.join()
