import time
import socket
import multiprocessing
import os
import threading
from queue import Queue
from colorama import Fore ,Back, Style
import subprocess
import sys

top = """
          _____      _____   ___________
         |    _+    |     |  |___   __ |
         |  _  +    |     |      |  |
         |_   +     |     |      |  |     
         ||         |     |      |  | SCANNER
         ||         |_____|      |__| _____ 

"""
print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + top)
print( Fore.CYAN + "      [---]          " + Fore.RED + Style.BRIGHT + "Network _Port Scanner " + Fore.YELLOW + "(NPS)   ")
print(Fore.CYAN + "      [---]          " + Fore.CYAN + Style.BRIGHT + "Created by: " + Fore.RED + "Lukwago Hamidu" + Fore.YELLOW + "  (CMD)")
print(Fore.CYAN + Style.BRIGHT + "                     Version   :" + Fore.LIGHTBLUE_EX + "  1.0.1.0")
print(Fore.CYAN + "      [---]          " + Fore.RED + Style.BRIGHT + "Follow Me On Twitter : " + Fore.YELLOW + "@RashidCmd   ")
print(Fore.CYAN + "      [---]          " + Fore.CYAN + Style.BRIGHT + "Follow me on Facebook : " + Fore.RED + " localhost Vcmd Cmd Rashid" + Fore.YELLOW + "  (CMD)")
print(Fore.CYAN + Style.BRIGHT + "      [---]          Email   :" + Fore.LIGHTBLUE_EX + "  lkwg39@gmail.com")
vcm = """
         |HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH|
         |HHHHHHH__))____________((_ HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH|
         |HHHHHH|                   | HHHPHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH|     
         |HHHHHHH|        " "       | HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH|    
         |HHHHHHH|                  | HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH|   
         |HHHHHHH@|    _       _    |@HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH|
         |HHHHHHHH@|  "      "    |@      |+++++   |  | |  |   |      +)   |  
         |HHHHHHHHHH|              |      |+       |  |_|  |   |       +   |
         |HHHHHHHHHHH|           |        |+       |       |   |      +  =====;
         |HHHHHHHHHHHH__ |"" | __         |____    |       |   |___ +      | ||
         |HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH|  ''
         |HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH|  '
         |_________________________________________________________________|

usage : python3 scanner.py
"""
print(Fore.LIGHTYELLOW_EX+ vcm)

print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "                    WELCOME TO THE NETWORK _  PORT SCANNER ")
print(Style.BRIGHT+ Fore.RED + '                  CMD INTERNATIONAL NETWORK PORT SCANNER  ')
print(Style.BRIGHT+Fore.YELLOW + '_' *79)
print(Fore.LIGHTRED_EX + Style.BRIGHT+"[*] Select Scanning  to continue ")
usage = """

[1]  Scan host Ip Address 
[2]  Scan live host 
[3]  Scan TCP Open ports 
[4]  Exit
"""
print(Style.BRIGHT + Fore.CYAN+ usage)
print(Fore.YELLOW + '_'* 80)
option = int(input (Fore.LIGHTYELLOW_EX + "Select option from the menu to continue:   "))
if option == 1:

    try:



        def pinger(job_q, results_q):
            
            DEVNULL = open(os.devnull, 'w')
            while True:

                ip = job_q.get()

                if ip is None:
                    break

                try:
                    subprocess.check_call(['ping', '-c1', ip],
                                          stdout=DEVNULL)
                    results_q.put(ip)
                except:
                    pass


        def get_my_ip():
            """
            Find my IP address
            :return:
            """
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip


        def map_network(pool_size=255):

            ip_list = list()

            # get my IP and compose a base like 192.168.1.xxx
            ip_parts = get_my_ip().split('.')
            base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

            # prepare the jobs queue
            jobs = multiprocessing.Queue()
            results = multiprocessing.Queue()

            pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]

            for p in pool:
                p.start()

            # cue hte ping processes
            for i in range(1, 255):
                jobs.put(base_ip + '{0}'.format(i))

            for p in pool:
                jobs.put(None)

            for p in pool:
                p.join()

            # collect he results
            while not results.empty():
                ip = results.get()
                ip_list.append(ip)

            return ip_list


        if __name__ == '__main__':
            print('Scanning ip Address ...')
            print("[*] it will take time according  size of the machine  on  the network .......")
            lst = map_network()
            print(lst)
    except KeyboardInterrupt:
        print("Program exiting ...")


elif option == 2:
    try:
        for ping in range(1, 25):
            address = input("[*] Enter Ip Address " + str(ping) + "\n")
            res = subprocess.call(['ping', '-c', '3', address])
            if res == 0:
                print("ping to", address, "Host is live")
            elif res == 2:
                print("no response from", address)
            else:
                print("ping to", address, "failed!")
    except KeyboardInterrupt:
        print("Program exiting.... ")


elif option == 3:
    print(Fore.YELLOW + '_' * 20)
    try:

        socket.setdefaulttimeout(1127.1000)
        print_lock = threading.Lock()

        target = input(Fore.RED + "[*] Enter Ip To Scan: ")
        print(Fore.YELLOW + " [*]  Scanning Tcp port......")
        def portscan(port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                con = s.connect((target, port))
                with print_lock:
                    print(Fore.LIGHTCYAN_EX +'_'* 20)
                    print(Fore.RED +'Port', port, Fore.LIGHTYELLOW_EX+'is open')
                    con.close()
            except:
                pass
        def threader():
                    while True:
                     cmd = q.get()
                     portscan(cmd)
                     q.task_done()


        q = Queue()
        startTime = time.time()

        for x in range(100):
            t = threading.Thread(target=threader)
            t.daemon = True
            t.start()

        for cmd in range(1, 65536):
            q.put(cmd)

        q.join()

        print(Fore.YELLOW + '-' * 75)

        print(Fore.CYAN + '[*] Time taken during scanning:', time.time() - startTime )
        print(Fore.RED+"[*] Have a nice day !!!.... CMD International (Respect)")
        print(Fore.YELLOW + '-' * 75)
    except KeyboardInterrupt:
        print("Program exiting ......")



elif option == 4:
    try:
        sys.exit(ChildProcessError)
    except KeyboardInterrupt:
        print("Program exiting......")


else:
    print("please choose right option ,ie,1,2,3,!!!!!")
    sys.exit("program exiting !!!!!")





