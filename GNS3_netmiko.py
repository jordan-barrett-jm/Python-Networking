"""
In this program I will be doing the following:
1) Set SW1 as VTP Server with the domain name of Jordan.Local
2) Set up 4 VLANs:
        10 - Management
        15 - Sales
        20 - Tech
        40 - CSR
3) Make SW1 the root bridge with a priority of 4096 in all VLANs (including VLAN 1)



ALL TO BE DONE WITH NETMIKO
"""

from netmiko import ConnectHandler
host = "192.168.0.50"
username = '[username]'
password = '[password]'
device_type = 'cisco_ios'
ssh_connect = ConnectHandler(ip = host, username=username, device_type = device_type, password=password)
vlan_commands = ["vtp domain jordan.local", "vlan 10", "name Management", "vlan 20", "name Tech", "vlan 15", "name Sales", "vlan 40", "name CSR"]
ssh_connect.send_config_set(vlan_commands)
vlans = ["1", "15", "10", "20", "40"]
for vlan in vlans:
    #print "\nSetting up STP for Vlan %s" % (vlan)
	stp = ["spanning-tree vlan %s priority 4096" % vlan]
	ssh_connect.send_config_set(stp)
hosts = ["192.168.0.50", "192.168.0.51", "192.168.0.52"]
for host in hosts:
    ssh_connect = ConnectHandler(ip = host, username=username, device_type = device_type, password=password)
    vtp_state = ssh_connect.send_command("sh vtp status")
    print "\n\nCURRENT HOST: %s" % host
    print vtp_state
    vlans = ssh_connect.send_command("sh vlan br")
    print vlans
    stp_state = ssh_connect.send_command("sh spanning-tree")
    print stp_state
