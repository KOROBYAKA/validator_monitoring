from os import system
from sys import exit

from mininet.node import Host
from mininet.topo import Topo
from mininet.util import quietRun
from mininet.log import error
import sys
from functools import partial
from mininet.node import Controller
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.topo import SingleSwitchTopo
from mininet.log import setLogLevel
class VLANHost( Host ):
    "Host connected to VLAN interface"

    # pylint: disable=arguments-differ
    def config( self, vlan=100, **params ):
        """Configure VLANHost according to (optional) parameters:
           vlan: VLAN ID for default interface"""

        r = super( VLANHost, self ).config( **params )

        intf = self.defaultIntf()
        self.cmd( 'ifconfig %s inet 0' % intf )
        self.cmd( 'vconfig add %s %d' % ( intf, vlan ) )
        self.cmd( 'ifconfig %s.%d inet %s' % ( intf, vlan, params['ip'] ) )
        newName = '%s.%d' % ( intf, vlan )
        intf.name = newName
        self.nameToIntf[ newName ] = intf


        return r


hosts = { 'vlan': VLANHost }




class MyTopo( Topo ):

    def build( self, vlanBase=100 ):
        s1 = self.addSwitch('s1')
        hB = self.addHost('hB')

        vlan = vlanBase
        hA = self.addHost('hA',cls=VLANHost,vlan=vlan)

        x = 1
        for x in range (4):
            self.addLink('hB', 's1')
        self.addLink('hA', 's1')

topos = { 'mytopo': ( lambda: MyTopo() ) }

def test():
    net = Mininet(topo=MyTopo(), waitConnected=True)
    net.start()




    hA = net['hA']

    for x in range (0,4):
        hA.cmd(f'sudo ip link add link hA-eth0 name hA-eth0.10{x} type vlan id 10{x}')
        hA.cmd(f'ip addr add 10.0.0.{x}/24 brd 10.0.0.255 dev hA-eth0.10{x}')
        hA.cmd(f'ip link set dev hA-eth0.10{x} up')
     #   s1.cmd('')
      #  s1.cmd('')
       # s1.cmd('')
    CLI(net)
    net.stop()
def main():

   

    test()




if __name__ == "__main__":
    main()
