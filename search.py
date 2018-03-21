# -*- coding:utf-8 -*-
# @Time    : 2018/3/20 15:48
# @Author  : zlmfslx
# @Oath    : Your happiness is my greatest satisfaction
# @File    : search.py
#参照 python search.py baidu.com 格式输入
import sys
import requests
from bs4 import BeautifulSoup as BS

reload(sys)
sys.setdefaultencoding('UTF-8')


dict  = {}
mails=[]
domains=[]
#根据域名通过ICP 搜索其域名下公司相关信息
def searchIcpUrl(url):
    print '查询中......'
    rsp =  requests.get(url)
    soup = BS(rsp.text,'lxml')
    if soup.get_text().find('没有符合条件的记录') > 0:
        print '没有符合条件的记录'
        exit(1)
    else:
        Td =soup.table.select('td')
        compnyName = Td[1].text# 公司名称
        if compnyName !='':
            icpHao = Td[3].text#ICP号
            icpHao = icpHao[:icpHao.index('[')]
            domainS = Td[5].text#公司名称
            aTag = Td[8].a.get('href')#详情链接
            dict['icpHao'] = icpHao
            dict['domainS'] = domainS

            print icpHao
            detailsUrl = 'http://www.beianbeian.com'+aTag
            searchName(detailsUrl)#  找一个网站负责人就行

            #企查查根据企业名称查询
            searchQcCompnyName(compnyName)
        else:
            exit(1)

        exit(1)

#获取某个企业公司旗下的域名
def searchIcpCompanyName(compnyName):
    url = 'http://www.beianbeian.com/s?keytype=2&q=%s'%(compnyName,)#ICP站点 根据企业名称查询相关信息
    rsp = requests.get(url)
    soup  = BS(rsp.text,'lxml')
    for div in soup.select('div[id="home_url"]'):
        domains.append(div.a.text)
        print div.a.text #相关域名
    #print domains
    #企查查根据企业名称查询
def searchQcCompnyName(name):
    headers = {
               'Cookie':'PHPSESSID=u5t9tjbal26pslqlk3cfau0a65; UM_distinctid=162425b7134711-00bdcec441a79-3e3d5f01-1fa400-162425b7137136; CNZZDATA1254842228=1944501181-1521531430-https%253A%252F%252Fwww.baidu.com%252F%7C1521531430; zg_did=%7B%22did%22%3A%20%22162425b715771c-0900160a348ab2-3e3d5f01-1fa400-162425b7159112b%22%7D; hasShow=1; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1521531712; acw_tc=AQAAAGAPzj+VjggAKgh4e8aCvZDXPK0h; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1521531737; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201521531711849%2C%22updated%22%3A%201521532366242%2C%22info%22%3A%201521531711855%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%7D',
               'grade-Insecure-Requests': '1',
               'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding':'gzip, deflate',
               'Accept-Language':'zh-CN,zh;q=0.9',
               'Connection':'Keep-Alive',
               'Host':'www.qichacha.com',
               'Referer':'http://www.qichacha.com/search?key=%E5%8C%97%E4%BA%AC%E5%88%9B%E6%96%B0%E6%B8%A0%E6%88%90%E6%8A%80%E6%9C%AF%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
    url='http://www.qichacha.com/search?key=%s'%(name,)
    rsp = requests.get(url,headers=headers)
    soup = BS(rsp.text,'lxml')

    try:
        for mail in soup.select('.m-t-xs .m-l'):
            if mail.get_text().find('@') > 0:
                mails.append(mail.get_text()[3:])#添加企查查的相关公司邮箱
        maileQc = list(set(mails))#读取企查查的相关公司邮箱 进行去重操作
        #print maileQc
        for M in maileQc:
            print M


        dict['compnyName']={}
        for i,comp_name in  enumerate(soup.select('.ma_h1')):
            comp_name = comp_name.get_text()
            if comp_name !='':
                print comp_name
                dict['compnyName'].update({i:comp_name})

                searchIcpCompanyName(comp_name)# comp_name.get_text()读取企查查的相关公司名称
    except AttributeError:
        pass
    #print dict

    #搜索公司相关负责人名
def searchName(url):
    rsp = requests.get(url)
    soup = BS(rsp.text,'lxml')
    table =soup.find_all('table')[1]
    dict['name'] = table.findAll('td')[6].text
    print dict['name']



def main():
        #domain = raw_input('please your a domain:')
    if len(sys.argv) < 2:
           banner ='''
            # Purpose:通过输入一个域名可查其相关公司信息   如 网站负责人   相关公司  及相关公司对应域名  邮箱等信息
            # Help:输入格式  python search.py baidu.com
           '''
           print banner
    else:
        domain = sys.argv[1]
    #domain = 'baidu.com'
    #domain = 'xiaoh.org'
    try:
        url = 'http://www.beianbeian.com/search/%s'%(domain,)
        searchIcpUrl(url)
    except:
        pass



if __name__=='__main__':
    main()







