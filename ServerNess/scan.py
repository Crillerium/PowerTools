try:
    import nmap
except:
    print('请先安装 python-nmap 库')

nm = nmap.PortScanner()
nm.scan(hosts='192.168.1.0/24', arguments='-sP')
print('局域网设备扫描结果(仅显示已设置hostname的设备):\n'+'-'*8)
for host in nm.all_hosts():
    if nm[host].hostname():
        print(f"{host} : {nm[host].hostname()}")