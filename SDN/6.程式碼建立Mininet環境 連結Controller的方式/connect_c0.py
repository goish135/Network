from mininet.cli import CLI
from mininet.net import Mininet

if '__main__' == __name__:
    net = Mininet(controller=None)
	
	# c0 = net.addController('c0',ip='Controller ip', port=6633)
	
	s1 = net.addSwitch('s1')
	
	h1 = net.addHost('h1', mac='00:00:00:00:00:01')
	h2 = net.addHost('h2', mac='00:00:00:00:00:02')
	
	net.addLink(s1, h1, port1=1, port2=1)
	net.addLink(s1, h2, port1=2, port2=1)
	
	net.start()
	# c0.start()
	
	# s1.start([c0])
    
    s1.cmdPrint('ovs-ofctl add-flow s1 "in_port=1, actions=output:2"')
    s1.cmdPrint('ovs-ofctl add-flow s1 "in_port=2, actions=output:1"')
    
    CLI(net)
    net.stop()
    
    
    
