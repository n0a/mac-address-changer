
# scripts repo
This repo for temporary saving different code scatches.

## MAC changer

**mac_changer.py** — Linux/macOS MAC-address random changer with vendor choices and automatic backups original address.

**Use own MAC address**
Use *-m --mac* option.
Example usage: 

> sudo ./mac_changer -i en0 -m 02:00:00:8a:09:ca

**Generage random MAC address**

The Default vendor for generating MAC is xen, because it's safety.
Example usage: 

> sudo ./mac_changer -i en0

**Generage random MAC address with vendor**
If you want to generate MAC-address with needed vendor, just use option *-v --vendor*.

**Supported vendors:** xen, huawei, cisco, samsung, google, juniper, dell, 
broadcom, tplink, hp, indel, dlink, zte, nokia, netgear, microsoft, xiaomi, apple
Example usage: 
```sh
sudo ./mac_changer.py -i en0 -v apple
[+] Interface seems good: en0
[+] Random MAC address for this case: [apple] D4:61:9D:dc:70:5d
[+] Backup: en0: 02:00:00:8a:09:ca -> D4:61:9D:dc:70:5d write in backup.txt
[+] Changing MAC from 02:00:00:8a:09:ca ->
D4:61:9D:dc:70:5d successful.
```

**To do:**
 - Windows support
 - Quiet mode
