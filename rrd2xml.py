#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Converto rrd database file to xml
@author: Lion 11315889@qq.com
'''
import logging
import os
import platform
import sys
import time


logger=logging.getLogger()
handler=logging.FileHandler("/var/log/rrd2xml.log")
logger.addHandler(handler)
logger.setLevel(logging.NOTSET)
if('Ubuntu' in platform.uname()[3]):
    rrdtool='/usr/bin/rrdtool'
else:
    rrdtool='/usr/local/rrdtool/bin/rrdtool'
if(not os.path.exists(rrdtool)):
    print '%s does not exist, please install rrdtool' % rrdtool
    sys.exit(0)
#rrd directory path
rrd_dir='/var/www/html/rra'
#xml directory path
xml_dir='/var/www/html/rraxml'


def rrd2xml(rrd_dir,xml_dir):
    if(not os.path.exists(rrd_dir)):
        print '%s does not exist.' % rrd_dir
        sys.exit(0)
    print 'Start dumping...'
    for root,dirs,files in os.walk(rrd_dir):               
        #print root,sub_dir,files            
        if(len(files)>0):
            sub_dir=root.replace(rrd_dir,'')
            if(not os.path.exists(xml_dir+sub_dir)):
                os.popen("mkdir -p %s%s" % (xml_dir,sub_dir))
            for f in files:
                rrd_file='%s/%s' % (root,f)
                if(rrd_file.endswith('rrd')):
                    xml_file='%s%s/%s.xml' % (xml_dir,sub_dir,f)
                    #print 'convert %s -> %s' % (rrd_file,xml_file)
                    cmd='%s dump %s > %s' % (rrdtool,rrd_file,xml_file)
                    os.popen(cmd)
                    sys.stdout.write('.')
                    sys.stdout.flush()
    print '\nRRDTOOL Dump Complete!'

def xml2rrd(rrd_dir,xml_dir):
    if(not os.path.exists(xml_dir)):
        print '%s does not exist.' % xml_dir
    print 'Start restoring...'
    for root,dirs,files in os.walk(xml_dir):
               
        #print root,sub_dir,files            
        if(len(files)>0):
            sub_dir=root.replace(xml_dir,'')
            if(not os.path.exists(rrd_dir+sub_dir)):
                os.popen("mkdir -p %s%s" % (rrd_dir,sub_dir))
            for f in files:
                xml_file='%s/%s' % (root,f)
                if(xml_file.endswith('xml')):
                    rrd_file='%s%s/%s' % (rrd_dir,sub_dir,f)
                    rrd_file=rrd_file[:-4]
                    #print 'convert %s -> %s' % (rrd_file,xml_file)
                    cmd='%s restore %s %s -f' % (rrdtool,xml_file,rrd_file)
                    os.popen(cmd)
                    sys.stdout.write('.')
                    sys.stdout.flush()
    print '\nRRDTOOL Restore Complete!'
    
    
if __name__=="__main__":
    if('dump' in sys.argv):
        rrd2xml(rrd_dir,xml_dir)
    elif("restore" in sys.argv):
        xml2rrd(rrd_dir,xml_dir)
    else:
        print "Useage: python rrd2xml.py dump | restore"
    x=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    logger.info("%s :rrd2xml excute finished!" % x )
       
    
    #
