#!/usr/bin/env python3
'''

This is Linux/macOS MAC (random) address changer.
by n0a https://n0a.pw

=====================================================================
Run without args will show available network interfaces with MAC only 
=====================================================================
[-] Error: specify interface
[!] Available interfaces:
en0: e4:d7:f4:ee:42:4d
en3: d0:37:35:18:48:79

===========================================================
ex. MAC random generation (-v vendor for vendor mac prefix)
===========================================================
sudo ./mac_changer.py -i en0 -v apple
[+] Interface seems good: en0
[+] Random MAC address for this case: [apple] D4:61:9D:dc:70:5d
[+] Backup: en0: 02:00:00:8a:09:ca -> D4:61:9D:dc:70:5d write in backup.txt
[+] Changing MAC from 02:00:00:8a:09:ca -> D4:61:9D:dc:70:5d successful.

===================
ex. with custom MAC
===================
sudo ./mac_changer.py -i en0 -m e4:d7:f4:ee:42:4d
[+] Interface seems good: en0
[+] MAC address seems good: e4:d7:f4:ee:42:4d
[+] Backup: en0: 76:bf:25:3a:b1:bd -> e4:d7:f4:ee:42:4d write in backup.txt
[+] Changing MAC from 76:bf:25:3a:b1:bd -> e4:d7:f4:ee:42:4d is OK.

======================
cat backup.txt example
======================
en0: e0:3f:49:86:51:0d -> cb:48:34:6f:a6:80
en0: cb:48:34:6f:a6:80 -> e0:3f:49:86:51:0d
en0: e0:3f:49:86:51:0d -> 76:bf:25:3a:b1:bd
en0: 76:bf:25:3a:b1:bd -> e4:d7:f4:ee:42:4d
'''

import os
import re
import sys
import random
import argparse
import subprocess
from platform import system

# default_vendor object can be: xen, huawei, cisco, samsung, google, juniper, dell, 
# broadcom, tplink, hp, indel, dlink, zte, nokia, netgear, microsoft, xiaomi, apple

default_vendor	= "xen"
backup_file 	= "backup.txt"
backup_enable	= True

def is_tool(name):
	# Check whether `name` is on PATH and marked as executable.
	from shutil import which
	return which(name) is not None

def get_avialible_ifaces():
	current_os = system()
	# Because macOS ipconfig output has't splin network interface with \n\n
	if current_os == 'Linux':
		if is_tool("ifconfig"):
			out = os.popen("ifconfig").read().split('\n\n')
		else:
			sys.exit("[-] Can't find Linux ifconfig tool.")
	elif current_os == 'Darwin':
		if is_tool("netstat"):
			out = os.popen("netstat -i").read().split('\n')
		else:
			sys.exit("[-] Can't find macOS netstat tool.")
	else:
		sys.exit('MAC address change on this OS not supported :(')

	result = []
	for paragraph in out:
		d = {}
		iface = re.search('^([A-z]*\d)', paragraph)
		mac = re.search('([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', paragraph)
		if mac and iface:	
			d['iface'] = iface[0]
			d['mac'] = mac[0]
			result.append(d)
	return result

def avialible_ifaces_format():
	ifaces = get_avialible_ifaces()
	print("[!] Available interfaces:")
	for i in ifaces:
		iface = i['iface']
		mac = i['mac']
		print(f"{iface}: {mac}")
		
def mac_check(mac):
	if re.match(r"([0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2}$", mac):
		return 1
	else:
		return 0

def mac_random(m_type):
	'''
	More vendors: http://standards-oui.ieee.org/oui.txt
	Check MAC vendor: https://www.ipchecktool.com/tool/macfinder
	'''
	
	d = {'vendor': 'apple', 'mac': 'D4:61:9D'}, {'vendor': 'xen', 'mac': '02:00:00'}, {'vendor': 'huawei', 'mac': 'CC:05:77'}, {'vendor': 'cisco', 'mac': '30:8B:B2'}, {'vendor': 'samsung', 'mac': '8C:B8:4A'}, {'vendor': 'google', 'mac': '30:FD:38'}, {'vendor': 'juniper', 'mac': '20:D8:0B'}, {'vendor': 'dell', 'mac': 'E0:D8:48'}, {'vendor': 'broadcom', 'mac': 'BC:97:E1'}, {'vendor': 'tplink', 'mac': '54:A7:03'}, {'vendor': 'hp', 'mac': '40:B0:34'}, {'vendor': 'indel', 'mac': '00:E1:8C'}, {'vendor': 'dlink', 'mac': '10:62:EB'}, {'vendor': 'zte', 'mac': 'D0:71:C4'}, {'vendor': 'nokia', 'mac': '40:7C:7D'}, {'vendor': 'netgear', 'mac': '08:BD:43'}, {'vendor': 'microsoft', 'mac': '6C:5D:3A'}, {'vendor': 'xiaomi', 'mac': '2C:D0:66'}

	for i in d:
		if i["vendor"] == m_type:
			mac_part = i["mac"]

	try:
		mac_part
	except NameError:
		print(f"[-] Incorrect vendor: {m_type}")
		print(f"[!] Possible vendors: xen, huawei, cisco, samsung, google, juniper, dell, broadcom, tplink, hp, indel, dlink, zte, nokia, netgear, microsoft, xiaomi")
		sys.exit(0)
	else:
		random_mac = mac_part + ":%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		return random_mac

def do_backup(interface, old_mac, new_mac):
	# without checking permission because ifconfig needs root in all ways
	print(f"[+] Backup: {interface}: {old_mac} -> {new_mac} write in {backup_file}")
	file_to_write = open(backup_file, "a") 
	file_to_write.write(interface + ": " + old_mac + " -> " + new_mac)
	file_to_write.write("\n")
	file_to_write.close()

def change_mac(interface, old_mac, new_mac):
	current_os = system()
	
	if is_tool("ifconfig"):
		if current_os == 'Linux':
			subprocess.call(["ifconfig", interface, "down"])
			subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
			subprocess.call(["ifconfig", interface, "up"]) 
			
		if current_os == 'Darwin': # a little bit different way on macOS
			subprocess.call(["ifconfig", interface, "ether", new_mac])
	else:
		print("[-] Error: ifconfig isn't installed. Try apt/yum install -y net-tools first.")
		sys.exit(0)
	
	ifaces = get_avialible_ifaces()
	
	for i in ifaces:
		if i["iface"] == interface:
			current_mac = i["mac"]
	
	if old_mac != current_mac:
		return 1
	else:
		return 0		
		
def main():
	parser = argparse.ArgumentParser("Linux/macOS MAC address changer by n0a")
	parser.add_argument("-i", "--interface", help="set network interface")
	parser.add_argument("-m", "--mac", help="set new MAC. If not set MAC will be randomly generated.")
	parser.add_argument("-v", "--vendor", help="Set vendor for MAC: xen (default), huawei, cisco, samsung, google, juniper, dell, broadcom, tplink, hp, indel, dlink, zte, nokia, netgear, microsoft, xiaomi")
	
	options = parser.parse_args()
	
	iface_is_good	= False
	mac_is_good		= False
	random_enable	= False
	
	if options.interface is not None:
		interface 	= options.interface
		newmac 		= options.mac
		
		ifaces = get_avialible_ifaces()
		for i in ifaces:
			if i["iface"] == interface:
				old_mac = i["mac"]
				iface_is_good = True
		
		if iface_is_good:
			print(f"[+] Interface seems good: {interface}")
		else:
			print(f"[-] Interface {interface} can't do this shit.")
			avialible_ifaces_format()
			sys.exit(0)
			
		if options.mac is not None:
			if mac_check(newmac):
				mac_is_good = True
				print(f"[+] MAC address seems good: {newmac}")
			else:
				print(f"[+] But yours MAC address looks like shit: {newmac}")
				sys.exit(0)
		else:
			random_enable = True
			if options.vendor is not None:
				vendor = options.vendor
				random_mac = mac_random(options.vendor)
			else:
				vendor = default_vendor
				random_mac = mac_random(default_vendor)
			
			print(f"[+] Random MAC address for this case: [{vendor}] {random_mac}")
			
		if iface_is_good and mac_is_good:
			working_mac = newmac					
		
		if iface_is_good and random_enable:
			working_mac = random_mac		
		
		run = change_mac(interface, old_mac, working_mac)

		if run:
			if backup_enable:
				do_backup(interface, old_mac, working_mac)
			print(f"[+] Changing MAC from {old_mac} -> {working_mac} successful.")
		else:
			print(f"[-] Something wrong. Try run with sudo.")
		
	else:
		print("[-] Error: what about set network interface?")
		avialible_ifaces_format()
		print("")
		parser.print_help()
		sys.exit(0)
	
if __name__== "__main__":
	main()
