#!/bin/bash
DELAY_MS=35
DELAY_DISTRIBUTION_MS=15
LOSS_PERCENT=1
CLIA="ip netns exec clientA"
SRV="ip netns exec server"

echo "Creating a directory for result"
mkdir results

echo "Cleanup, ignore errors if this is first run"
ip netns del clientA
ip netns del server

echo "Add namespace"
ip netns add clientA
ip netns add server

echo "Add virtual ethernets"
ip link add veth_srv-A type veth peer name veth-A
ip link set dev veth-A netns clientA
ip link set dev veth_srv-A netns server


echo "Configuring server connection interfaces"
$SRV ip link add srv-br type bridge
$SRV ip l set srv-br up
$SRV ip link set veth_srv-A master srv-br
$SRV ip a a 10.0.1.1/24 dev srv-br
$SRV ip link set veth_srv-A up


echo "Configure IP addresses on clients"
$CLIA ip a a 10.0.1.2/24 dev veth-A
$CLIA ip link set veth-A up


echo "Set host A link quality"
echo "Set delay of ${DELAY_MS}ms, packet loss ${LOSS_PERCENT}%"
$SRV tc qdisc add dev veth_srv-A root handle 1: netem delay ${DELAY_MS}ms ${DELAY_DISTRIBUTION_MS}ms distribution normal
$SRV tc qdisc add dev veth_srv-A parent 1: handle 2: netem loss ${LOSS_PERCENT}

$CLIA tc qdisc add dev veth-A root handle 1: netem delay ${DELAY_MS}ms ${DELAY_DISTRIBUTION_MS}ms distribution normal
$CLIA tc qdisc add dev veth-A parent 1: handle 2: netem loss ${LOSS_PERCENT} rate 100Mbit corrupt 1% duplicate 1%

echo 'Run "ip netns exec server bash" to start a shell in namespace for SERVER'
echo 'Internet access is not configured inside the namespaces.'
