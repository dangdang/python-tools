#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 2.7
'''
这个脚 本用来实现 Openstack Essex 版本双线双IP的iptables出站路由转发功能，
请提前准备好路由表，格式为 : ip/netmask
如：
1.1.0.0/255.255.0.0
2.2.2.2/255.255.255.255

Lion@syscloud.cn  QQ:11315889
 
'''

import os
import sys
import re

ip_regex=r'(([12][0-9][0-9]|[1-9][0-9]|[1-9])\.){3,3}([12][0-9][0-9]|[1-9][0-9]|[1-9])' 
re_ip=re.compile(ip_regex);

def getip():
    '''get and validation ip address'''
    ip=sys.stdin.readline().rstrip()
    
    if re_ip.match(ip):
        return ip
    else:
        print 'You sure? '
        getip()

print 'Please input route file path and name  (default:ip_pool.txt):'
filename=sys.stdin.readline().rstrip()
if(len(filename)<1):
    filename="ip_pool.txt"
try:    
    f = open(filename)
except IOError:
    print 'File %s does not exist!' % filename
    sys.exit()
    
print 'Please input snat source ip:'
from_source=getip()
print 'Please input snat destination ip:'
to_source=getip()
print 'Delete or Insert? input I/D,case sensitive(default:I):'
action=sys.stdin.readline().rstrip()
if(action!='D'):
    action='I'


i=0
while 1:
    line = f.readline().rstrip()
    if not line:
        break
    if(not re_ip.match(line)):
        print 'Line is invalid.--- %s' % line
        break
    cmd="iptables -t nat -%s nova-network-float-snat -s %s -d %s -j SNAT --to-source %s" % (action,from_source,line,to_source)
    r=os.popen(cmd)
    print cmd
    i=i+1

f.close()
print 'Congratuation: %s Command finished !' % i


