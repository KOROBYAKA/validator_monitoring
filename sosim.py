#!/bin/python3
import subprocess
import argparse


def get_label(index):
    """
    Converts a 0-based index to a letter ID like A, B, ..., Z, AA, AB, ..., etc.
    """
    result = ""
    index += 1  # To make it 1-based like Excel

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
    shift = 0
    parser = argparse.ArgumentParser(prog='sosim',description="Solana validator Simulation",
                                     epilog="If you encounter some bug, I wish you a luck ©No-Manuel Macros")
    parser.add_argument('hosts_amount')
    parser.add_argument('loss_percentage')
    args = parser.parse_args()

    print("Creating server namespace with a single host")
    subprocess.run("./ns.sh", shell=True)
    for x in range(0,int(args.hosts_amount)):
        name = get_label(x)
        link_delay = link_delays[(x//len(link_delays)-1)]
        delay_distribution = delay_distributions[(x // len(delay_distributions) - 1)]
        print(f"./client.sh {name} {x} {link_delay} {delay_distribution} {args.loss_percentage}")
        subprocess.run(f"./client.sh {name} {x} {link_delay} {delay_distribution} {args.loss_percentage}",shell=True)

    print("success")





if __name__ == '__main__':
    main()

