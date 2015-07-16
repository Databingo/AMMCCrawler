#coding=utf-8
import csv
import time
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')#设定默认编码适应中文


import urllib2
url='https://pf.amac.org.cn/open/fundNotice?query_productName=%E6%96%B0%E4%B8%89%E6%9D%BF&currentPage=4'
#page 1,2,3,4 have to change handly
page=urllib2.urlopen(url).read()

from lxml import etree   
tree = etree.HTML(page)
td1s= tree.xpath("//tr//td[1]")#获取排序  
td2s= tree.xpath("//tr//td[2]/a")#获取基金编号
td3s= tree.xpath("//tr//td[3]/a")#获取基金管理人编号
      
for x,y,z in zip(td1s,td2s,td3s):
    with open('csv1.csv','a') as csvfile:
        spanwriter=csv.writer(csvfile, dialect='excel',delimiter='`')
        spanwriter.writerow([x.text,y.attrib.get('href')[-7:-1],z.attrib.get('href')[19:-1]])
    csvfile.close



with open('csv1.csv','rb') as csvfile:
    spanreader=csv.reader(csvfile, delimiter='`', dialect='excel')
    for row in spanreader:
        number=row[0]
        jijin=row[1]
        jijinren=row[2]
        #print jijinren
        link= 'https://pf.amac.org.cn/open/fundNotice/fundPeNotice?id=' + jijin
        jijininfo = urllib2.urlopen(link).read()
        treej = etree.HTML(jijininfo)
        jijinName= treej.xpath("//tr[1]//td[2]")[0].text#获取基金名称 
        jjcltime= treej.xpath("//tr[4]//td[2]")[0].text#获取基金成立时间
        jjlx = treej.xpath("//tr[6]//td[2]")[0].text.strip()#获取基金类型
        jjmanager = treej.xpath("//tr[8]//td[2]/a")[0].text.strip()#获取基金管理人名称
        tzarea = treej.xpath("//tr[12]//td[2]")[0].text
        if tzarea:
            tzarea=tzarea.strip()#获取主要投资领域
        #print jijinName,jjcltime,jjlx,jjmanager,tzarea,"|"
        
        managerlink= 'https://pf.amac.org.cn/open/comNotice/view?userId=' + jijinren
        mangerinfo = urllib2.urlopen(managerlink).read()
        treePeople = etree.HTML(mangerinfo)
        zcAddress= treePeople.xpath("//tr[3]//td[2]")[0].text.strip()#获取注册地址
        bgAddress= treePeople.xpath("//tr[4]//td[2]")[0].text.strip()#获取办公地址
        
        zcj=''.join(zcAddress.split())
        bgj=''.join(bgAddress.split())
        zc1=zcAddress.split()[0]
        zc2=zcAddress.split()[1]
        bg1=bgAddress.split()[0]
        bg2=bgAddress.split()[1]
        
        time.sleep(1)
        
        with open('csv2.csv','a') as csvfile:
            spanwriter=csv.writer(csvfile, dialect='excel')
            spanwriter.writerow([number,jijinName,jjcltime,jjlx,jjmanager,tzarea,zc1,zc2,bg1,bg2])
        csvfile.close
