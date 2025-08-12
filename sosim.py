#!/bin/python3
import subprocess
import argparse
import time

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
    parser.add_argument('hosts_amount')
    parser.add_argument('loss_percentage')
    args = parser.parse_args()
    nodes = [Node("10.0.1.2","A","10.0.1.1")]
    #print("Creating server namespace with a single host")
    subprocess.run("./server.sh", shell=True)
    for x in range(1,int(args.hosts_amount)):
        name = get_label(x)
        link_delay = link_delays[(x//len(link_delays)-1)]
        delay_distribution = delay_distributions[(x//len(delay_distributions)-1)]
        #print(f"./client.sh {name} {x} {link_delay} {delay_distribution} {args.loss_percentage}")
        nodes.append(Node(f"10.0.1{x+2}",name,"10.0.1.1"))
        subprocess.run(f"./client.sh {name} {x+2} {link_delay} {delay_distribution} {args.loss_percentage}",shell=True)


    print("Environment is up.\nRunning a server")
    #run mock-server
    cli = f"ip netns exec server"
    args = f"--listen 10.0.1.1:8009 --receive-window-size 630784  --max-concurrent-streams 512 --stream-receive-window-size 1232"
    server = subprocess.Popen(f"{cli} ./mock_server/target/debug/server {args}",
        shell=True, text=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    for node in nodes:
        node.run_agave_client()

    time.sleep(7)
    server.kill()



if __name__ == '__main__':
    main()
