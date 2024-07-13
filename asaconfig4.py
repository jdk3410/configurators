# asaconfig4.py, a script to create configs for Cisco ASAs by @jdk3410
# Version 0.0.1                          
# Python 3 compatiblity only
# Sanitized for external use
# TODO: input validation, VPN addition, might be good to automatically calculate number of NAT statements
# TODO: add logging framework, error handling, unit tests, integration tests, continuous integration, flask web interface on heroku


import os
from time import sleep
import platform
from time import ctime
from sys import exit


if os.name == "posix":
	import readline
else:
	pass
	
def clr():
	if os.name == "posix":
		os.system('clear')
	elif os.name == "nt":
		os.system('cls')
	else:
		pass


def ha_print():
	print("###################")
	print("optional for H/A")
	print("paste this into primary unit")
	print("##################")
	print("")
	print("conf t")
	print("failover lan unit primary")
	print("failover lan interface failover Vlan10")
	print("failover interface ip failover 10.0.1.2 255.255.255.0 standby 10.0.1.4")
	print("")
	print("int vlan10")
	print("no shut")
	print("exit")
	print("")
	print("int e0/7")
	print("switchport access vlan 10")
	print("exit")
	print("failover")
	print()
	print("exit")
	print("wr mem")
	print()
	print("##################")
	print("paste this into secondary unit")
	print("##################")
	print()
	print("conf t")
	print("failover lan interface failover Vlan10")
	print("failover interface ip failover 10.0.1.2 255.255.255.0 standby 10.0.1.4")
	print() 
	print("int vlan10")
	print("no shut")
	print("exit")
	print()
	print("int e0/7")
	print("switchport access vlan 10")
	print("exit")
	print("failover lan unit secondary")
	print()
	print("failover")
	print()
	print("####################################################################")
	print("#		end HA config                                      #")
	print("####################################################################")
		
def nat(arg1):
	mode = arg1
	nat1 = []
	while True:
		tffw = input("Enter tffw short hostname(eg, tffw2020): ")
		password = input("Enter 'enable' and 'pix' password: ")
		print_ha = input("Enter 'ha' for high-availability or just press enter to skip: ")
		ext_network = input("Enter external network and netmask (eg, 4.2.2.0 255.255.255.0): ")
		fw_ext = input("Enter firewall external IP and netmask (eg, 4.2.2.2 255.255.255.0): ")
		int_network = input("Enter internal network and netmask (eg, 10.0.0.0 255.255.255.0): ")
		fw_int = input("Enter firewall internal IP and netmask (eg, 10.0.0.1 255.255.255.0): ")
		gateway = input("Enter default gateway for firewall: ")
		numnats = int(input("Enter numerical value for number of NAT statements you want ('0' for none): "))
		nat1 = []
		for i in range(numnats):
			if numnats == "0":
				break
			print("")
			print("Enter NAT statements as follows: <external IP> <internal IP>")
			print("")
			nats = input(('NAT # ',i ))
			if not nats:
				break
			nat1.append(nats)
		print("")
		print("Displaying your chosen configuration options before doing anything.")
		print("")
		print(".------------------------------------------------------.")
		print("| Hostname: %s, password: %s, mode: %s" % (tffw, password, mode))
		print("| Cisco external IP: %s, Cisco internal IP: %s" % (fw_ext, fw_int))
		print("| Cisco gateway: %s" % gateway)
		print("| NATs: %r " % numnats)
		print("| NAT IPs: %s " % nat1)
		print(".------------------------------------------------------.")
		print("")
		decision = input("If that's correct press enter to display the config, 's' to display and save, or press 'q' to start over. Choice:> ")
		print("")
		if decision == '':
			clr()
			print("")
			print("OK, starting configuration build.")
			print("")
			break
		if decision == "s":
			clr()
			print("")
			print("OK, starting configuration build. Saving file as '%s' in" % tffw, os.getcwd())
			print("")
			nat_save(tffw, password, ext_network, fw_ext, int_network, fw_int, gateway, nat1, numnats)
			break
		else:
			print("OK, restarting %s configuration options. \n" % mode)
			pass
	nat_print(tffw, password, ext_network, fw_ext, int_network, fw_int, gateway, nat1, numnats)
	if print_ha == "ha":
		ha_print()
	else:
		pass
	exit(0)
	
def nat_print(*args):
	tffw, password, ext_network, fw_ext, int_network, fw_int, gateway, nat1, numnats = args
	print("")
	print("####################################################################")
	print("#		Cisco ASA config file generator			   #")
	print("#		By j			                #")
	print("#		Only use this on a fresh ASA unit.		   #")
	print("#		Not responsible for bricked units.		   #")
	print("#		If you're using a previously used unit		   #")
	print("#		Run 'conf t' and then 'configure factory-default'  #")
	print("#		Paste everything after this.		           #")
	print("####################################################################")
	print("")
	print("conf t")
	print("")
	print("enable password %s" % password)
	print("password %s" % password)
	print("hostname %s" % tffw)	
	print("")
	print("domain-name nothing.com") 
	print("no dhcpd enable inside") 
	print("no dhcpd address 192.168.1.5-192.168.1.36 inside")
	print("no dhcpd address 192.168.1.2-192.168.1.33 inside")
	print("no dhcpd auto_config outside")
	print("crypto key generate rsa modulus 1024 noconfirm")
	print("")
	print("int vlan1")
	print("ip address %s" % fw_int)
	print("no shut")
	print("exit")
	print("")
	print("int vlan2")
	print("ip address %s" % fw_ext)
	print("no shut")
	print("exit")
	print("")
	print("route outside 0.0.0.0 0.0.0.0 %s 1" % gateway)
	print("")
	for i in nat1:
		print("static (inside,outside) %s netmask 255.255.255.255" % i)
	print("")
	print("object-group service standard tcp-udp")
	print("description Standard web services")
	print("port-object range 20 25")
	print("port-object eq 80")
	print("port-object eq 443")
	print("port-object eq 1167")
	print("port-object eq 3389")
	print("object-group network admin")
	print("network-object 1.1.1.0 255.255.255.0")
	print("network-object host 1.1.11.2")
	print("access-list outside_access_in extended permit ip object-group admin %s" % ext_network)
	print("access-list outside_access_in extended permit tcp any %s object-group standard" % ext_network)
	print("access-list outside_access_in extended permit icmp any %s" % ext_network)
	print("access-group outside_access_in in interface outside")
	print("")
	print("logging trap warnings")
	print("logging asdm informational")
	print("logging host outside 1.1.11.2")
	print("logging trap 6")
	print("logging enable")
	print("")
	print("ip verify reverse-path interface inside")
	print("ip verify reverse-path interface outside")
	print("")
	print("http server enable")
	print("no http 192.168.1.0 255.255.255.0 inside")
	print("http 1.1.1.0 255.255.255.0 outside")
	print("http %s inside" % int_network)
	print("")
	print("ssh %s inside" % int_network)
	print("ssh 1.1.1.0 255.255.255.0 outside")
	print("ssh timeout 60")
	print("")
	print("ntp server 1.1.11.2 source outside prefer")
	print("")
								 
							
					
	print("exit")
	print("")
										 
		 
			 
		 
	print("wr mem")
	print("")
	print("####################################################################")
	print("#                end stand alone config                            #")
	print("####################################################################")	
		

def nat_save(*args):
	tffw, password, ext_network, fw_ext, int_network, fw_int, gateway, nat1, numnats = args
	save = open(tffw, 'w+') 
	print("#config file for %s.nothing.com written at" % tffw, ctime(), file=save)
	print("", file=save)
	print("conf t", file=save)
	print("", file=save)
	print("enable password %s" % password, file=save)
	print("password %s" % password, file=save)
	print("hostname %s" % tffw, file=save)	
	print("", file=save)
	print("domain-name nothing.com", file=save) 
	print("no dhcpd enable inside", file=save) 
	print("no dhcpd address 192.168.1.5-192.168.1.36 inside", file=save)
	print("no dhcpd address 192.168.1.2-192.168.1.33 inside", file=save)
	print("no dhcpd auto_config outside", file=save)
	print("crypto key generate rsa modulus 1024 noconfirm", file=save)
	print("", file=save)
	print("int vlan1", file=save)
	print("ip address %s" % fw_int, file=save)
	print("no shut", file=save)
	print("exit", file=save)
	print("", file=save)
	print("int vlan2", file=save)
	print("ip address %s" % fw_ext, file=save)
	print("no shut", file=save)
	print("exit", file=save)
	print("", file=save)
	print("route outside 0.0.0.0 0.0.0.0 %s 1" % gateway, file=save)
	print("", file=save)
	for i in nat1:
		print("static (inside,outside) %s netmask 255.255.255.255" % i, file=save)
	print("", file=save)
	print("object-group service standard tcp-udp", file=save)
	print("description Standard web services", file=save)
	print("port-object range 20 25", file=save)
	print("port-object eq 80", file=save)
	print("port-object eq 443", file=save)
	print("port-object eq 1167", file=save)
	print("port-object eq 3389", file=save)
	print("object-group network admin", file=save)
	print("network-object 1.1.1.0 255.255.255.0", file=save)
	print("network-object host 1.1.11.2", file=save)
	print("access-list outside_access_in extended permit ip object-group admin %s" % ext_network, file=save)
	print("access-list outside_access_in extended permit tcp any %s object-group standard" % ext_network, file=save)
	print("access-list outside_access_in extended permit icmp any %s" % ext_network, file=save)
	print("access-group outside_access_in in interface outside", file=save)
	print("", file=save)
									   
											
													 
								
				  
														 
														  
				  
									
														  
														
											  
				  
											 
													   
								
				  
															   
				  
										  
									 
							 
					  
				  
												  
				  
					  
				  
						
				  
	print("logging trap warnings", file=save)
	print("logging asdm informational", file=save)
	print("logging host outside 1.1.11.2", file=save)
	print("logging enable", file=save)
	print("logging trap 6", file=save)
	print("", file=save)
	print("ip verify reverse-path interface inside", file=save)
	print("ip verify reverse-path interface outside", file=save)
	print("", file=save)
	print("http server enable", file=save)
	print("no http 192.168.1.0 255.255.255.0 inside", file=save)
	print("http 1.1.1.0 255.255.255.0 outside", file=save)
	print("http %s inside" % int_network, file=save)
	print("", file=save)
	print("ssh %s inside" % int_network, file=save)
	print("ssh 1.1.1.0 255.255.255.0 outside", file=save)
	print("ssh timeout 60", file=save)
	print("", file=save)
	print("ntp server 1.1.11.2 source outside prefer", file=save)
	print("", file=save)
	print("exit", file=save)
	print("", file=save)
	print("wr mem", file=save)
	print("", file=save)
	print("####################################################################", file=save)
	print("#                end of config.                                    #", file=save)
	print("####################################################################\n", file=save)
	save.close()
	
		
def transparent(arg1):
	mode = arg1
	while True:
		tffw = input("Enter tffw short hostname(eg, tffw2020): ")
		password = input("Enter 'enable' and 'pix' password: ")
		print_ha = input("Enter 'ha' for high-availability or just press enter to skip: ")
		ext_network = input("Enter external network and netmask (eg, 4.2.2.0 255.255.255.0): ")
		fw_ext = input("Enter firewall external IP (eg, 4.2.2.2): ")
		gateway = input("Enter default gateway for firewall: ")
		print("")
		print("Displaying configuration options before doing anything. \n") 
		print(".------------------------------------------------------.")
		print("| Hostname: %s, password: %s, mode: %s" % (tffw, password, mode))
		print("| Cisco IP: %s, Cisco gateway: %s" % (fw_ext, gateway))
		print(".------------------------------------------------------. \n")
		decision = input("If that's correct press enter to display the config, 's' to display and save, or press 'q' to start over. Choice:> ")
		if decision == '':
			clr()
			print("")
			print("OK, starting configuration build.")
			print("")
			break
		if decision == "s":
			clr()
			print("")
			print("OK, starting configuration build. Saving file as '%s' in" % tffw, os.getcwd())
			print("")
			transparent_save(tffw, password, ext_network, fw_ext, gateway)
			break
		else:
			print("")
			print("OK, restarting %s configuration options." % mode)
			print("")
			pass
	transparent_print(tffw, password, ext_network, fw_ext, gateway)
	if print_ha == "ha":
		ha_print()
	else:
		pass
	exit(0)



	
def transparent_print(*args):
	tffw, password, ext_network, fw_ext, gateway = args
	print("")
	print("####################################################################")
	print("#		Cisco ASA config file generator			   #")
	print("#		By j			   #")
	print("#		Only use this on a fresh ASA unit.		   #")
	print("#		Not responsible for bricked units.		   #")
	print("#		If you're using a previously used unit		   #")
	print("#		Run 'conf t' and then 'configure factory-default'  #")
	print("#		Paste everything after this.		           #")
	print("####################################################################")
	print()
	print("conf t")
	print("")
	print("firewall transparent")
	print("enable password %s" % password)
	print("password %s" % password)
	print("hostname %s" % tffw) 
	print("domain-name nothing.com") 
	print("ip address %s" % fw_ext)
	print("crypto key generate rsa modulus 1024 noconfirm")
	print("")
	print("int e0/0")
	print("switchport access vlan 2")
	print("no shut")
	print("exit")
	print("")
	print("int e0/1")
	print("switchport access vlan 1")
	print("no shut")
	print("exit")
	print("")
	print("int vlan 2")
	print("nameif outside")
	print("exit")
	print("")
	print("int vlan 1")
	print("nameif inside")
	print("exit")
	print("")
	print("route outside 0.0.0.0 0.0.0.0 %s 1" % gateway)
	print("")
	print("object-group service standard tcp-udp")
	print("description Standard web services")
	print("port-object range 20 25")
	print("port-object eq 80")
	print("port-object eq 443")
	print("port-object eq 1167")
	print("port-object eq 3389")
	print("object-group network admin")
	print("network-object 1.1.1.0 255.255.255.0")
	print("network-object 1.1.1.1")
	print("access-list outside_access_in extended permit ip object-group admin %s" % ext_network)
	print("access-list outside_access_in extended permit tcp any %s object-group standard" % ext_network)
	print("access-list outside_access_in extended permit icmp any %s" % ext_network)
	print("access-group outside_access_in in interface outside")
	print("")
	print("logging trap warnings")
	print("logging asdm informational")
	print("logging host outside 1.1.11.2")
	print("logging enable")
	print("logging trap 6")
	print("")
	print("http server enable")
	print("no http 192.168.1.0 255.255.255.0 inside")
	print("http 1.1.1.0 255.255.255.0 outside")
	print("")
	print("ssh 1.1.1.0 255.255.255.0 outside")
	print("ssh timeout 60")
	print("")
	print("ntp server 1.1.11.2 source outside prefer")
	print("")
	print("exit")
	print()
	print("wr mem")
	print("")
	print("####################################################################")
	print("#		end stand alone config				   #")
	print("####################################################################")
	
	
		
def transparent_save(*args):
	tffw, password, ext_network, fw_ext, gateway = args
	save = open(tffw, 'w+') 
	print("#config file for %s.nothing.com written at" % tffw, ctime(), file=save)
	print("", file=save)
	print("", file=save)
	print("conf t", file=save)
	print("", file=save)
	print("firewall transparent", file=save)
	print("enable password %s" % password, file=save)
	print("password %s" % password, file=save)
	print("hostname %s" % tffw, file=save) 
	print("domain-name nothing.com", file=save) 
	print("ip address %s" % fw_ext, file=save)
	print("crypto key generate rsa modulus 1024 noconfirm", file=save)
	print("", file=save)
	print("int e0/0", file=save)
	print("switchport access vlan 2", file=save)
	print("no shut", file=save)
	print("exit", file=save)
	print("", file=save)
	print("int e0/1", file=save)
	print("switchport access vlan 1", file=save)
	print("no shut", file=save)
	print("exit", file=save)
	print("", file=save)
	print("int vlan 2", file=save)
	print("nameif outside", file=save)
	print("exit", file=save)
	print("", file=save)
	print("int vlan 1", file=save)
	print("nameif inside", file=save)
	print("exit", file=save)
	print("", file=save)
	print("route outside 0.0.0.0 0.0.0.0 %s 1" % gateway, file=save)
	print("", file=save)
	print("object-group service standard tcp-udp", file=save)
	print("description Standard web services", file=save)
	print("port-object range 20 25", file=save)
	print("port-object eq 80", file=save)
	print("port-object eq 443", file=save)
	print("port-object eq 1167", file=save)
	print("port-object eq 3389", file=save)
	print("object-group network admin", file=save)
	print("network-object 1.1.1.0 255.255.255.0", file=save)
	print("network-object host 1.1.11.2", file=save)
	print("access-list outside_access_in extended permit ip object-group admin %s" % ext_network, file=save)
	print("access-list outside_access_in extended permit tcp any %s object-group standard" % ext_network, file=save)
	print("access-list outside_access_in extended permit icmp any %s" % ext_network, file=save)
	print("access-group outside_access_in in interface outside", file=save)
	print("", file=save)
	print("logging trap warnings", file=save)
	print("logging asdm informational", file=save)
	print("logging host outside 1.1.11.2", file=save)
	print("logging enable", file=save)
	print("logging trap 6", file=save)
	print("", file=save)
	print("http server enable", file=save)
	print("no http 192.168.1.0 255.255.255.0 inside", file=save)
	print("http 1.1.1.0 255.255.255.0 outside", file=save)
	print("", file=save)
	print("ssh 1.1.1.0 255.255.255.0 outside", file=save)
	print("ssh timeout 60", file=save)
	print("", file=save)
	print("ntp server 1.1.11.2 source outside prefer", file=save)
	print("", file=save)
	print("exit", file=save)
	print("", file=save)
	print("wr mem", file=save)
	print("", file=save)
	print("####################################################################", file=save)
	print("#		end of config.			                                   #", file=save)
	print("####################################################################\n", file=save)
	save.close()

	
	
	

print(".----------------------------------------------.")
print("|                                              |")
print("|                                              |")
print("|                       \`\  F    Cisco        |")
print("|            /./././.   | |  i    Advanced     |")
print("|          /        `/. | |  r    Terminal     |")
print("|         /     __    `/'/'  e                 |")
print("|      /\__/\ /'  `\    /    w                 |")
print("|     |  00  |      `.,.|    a                 |")
print("|      \Vvvv/        ||||    l                 |")
print("|        ||||        ||||    l                 |")
print("|        ||||        ||||                      |")
print("|        `'`'        `'`'                      |")
print(".----------------------------------------------.")
print("")
print("Beginning program execution on", ctime())
print("Execution environment:","||",platform.system(),"||", "Program ID:","||",os.getpid(),"||","Running on an",platform.processor())
print("")
input("You are entering a powerful Cisco ASA configuration program. Press Enter to continue.")
print("")
print("First we need to gather a few variables to generate the configuration.\n")
print("You will have a chance to review and correct the options you have selected before the configuration is built.\n")

mode = False


while mode != "transparent" or mode != "nat":
	mode = input("Enter 'nat' for NAT mode for 'transparent' for transparent mode: ")
	if mode == "nat":
		print("")
		print("NAT mode selected. You will be asked for the number of NAT statements later.")
		print("")
		nat("nat")
	if mode == "transparent":
		print("")
		print("Transparent mode selected. You will not be asked for any NAT statements.")
		print("")
		transparent("transparent")
	else: 
		print("Operating mode must be selected before continuing. Try again.")
	



