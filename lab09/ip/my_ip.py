import subprocess

text = subprocess.check_output("ipconfig").decode('utf-8')

addr = 'None'
subnet = 'None'
for line in text.split('\n'):
    if 'IPv4 Address' in line:
        addr = line.strip()
    if 'Subnet Mask' in line:
        subnet = line.strip()
print(addr, subnet, sep='\n')
