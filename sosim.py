#!/bin/python3
import subprocess
import argparse
import time
from random import randint

class Node():
    def __init__(self, ip:str, label:str, target_ip:str):
        self.ip = ip
        self.label = label
        self.target_ip = target_ip

    def run_agave_client(self):
        cli = f"ip netns exec client{self.label}"
        args = f"--target {self.target_ip}:8009 --duration 3.3 --host-name {self.label}"
        subprocess.Popen(f"{cli} ./mock_server/target/debug/client {args}",
                                shell=True, text=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                                )

def get_label(index):
    result = ""
    index += 1
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result

    return result

def main():
    if (subprocess.run("whoami",shell=True,text=True,capture_output=True)).stdout != "root\n":
        print("This script should be run as root")
        exit()

    #Link qualities
    link_delays = [35,100,200]
    delay_distributions = [15,45,50]
    parser = argparse.ArgumentParser(prog='sosim',description="Solana validator Simulation",
                                     epilog="If you encounter some bug, I wish you a luck ©No-Manuel Macros")
    parser.add_argument('hosts_amount',type=int, help='1–253 allowed')
    parser.add_argument('loss_percentage',type=int,help='0-100 allowed')
    args = parser.parse_args()
    if args.hosts_amount not in range(1,253) or args.loss_percentage not in range(0,100):
        print("run 'sudo ./sosim -h'")
        exit()
    nodes = [Node("10.0.1.2","A","10.0.1.1")]
    subprocess.run("./server.sh", shell=True)
    for x in range(1,int(args.hosts_amount)):
        name = get_label(x)
        link_delay = link_delays[(x%len(link_delays)-1)]
        delay_distribution = delay_distributions[((x+randint(0,2))%len(delay_distributions)-1)]
        nodes.append(Node(f"10.0.1{x+2}",name,"10.0.1.1"))
        subprocess.run(f"./client.sh {name} {x+2} {link_delay} {delay_distribution} {args.loss_percentage}",shell=True)


    print("Environment is up")
    #run mock-server
    cli = f"ip netns exec server"
    args = f"--listen 10.0.1.1:8009 --receive-window-size 630784  --max-concurrent-streams 512 --stream-receive-window-size 1232"
    server = subprocess.Popen(f"{cli} ./mock_server/target/debug/server {args}",
        shell=True, text=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    print("Server is up")

    for node in nodes:
        node.run_agave_client()
    print("Clients are up")

    time.sleep(3.5)
    server.kill()
    print("Server killed")
    subprocess.run("chmod 666 ./results/*", shell=True, text=True)
    print("Results are stored in directory ./results")

    subprocess.run("python3 ./UDP-parse/main.py",shell=True, text= True)


if __name__ == '__main__':
    main()
