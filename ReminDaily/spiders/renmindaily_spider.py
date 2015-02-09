#coding=utf-8
from scrapy.spider import Spider
from scrapy.selector import Selector
from ReminDaily.items import RmdailyItem
from scrapy import FormRequest
from scrapy import Request
import re,os,time
class ReMinDailySpider(Spider):
    """正式爬虫入口类"""
    name = 'rmdaily_spider'
    allowed_domains = ['rmrbw.info']
    start_urls=["http://rmrbw.info/"]  
    _main_site = "http://rmrbw.info/"
    
    def parse(self,response):
        """ 主回调函数,第一步是分析出首页符合条件的报道链接(1946-1956),
        同时由于每月的新闻报道数目都是固定每页15条,可根据新闻总条数计算出共有多少页,然后推断出每页的url"""
        sel = Selector(response)
        sites = sel.xpath("//div[@style='margin-left:40px']/table")
        #urls = []
        for site in sites:
            selector = site.xpath("./tr/td/h2/a") #分析出年月的报道<a>标签
            date = selector.xpath("text()").extract()[0] #取出其中的年月
            match = re.search("(\d+).*?",date,re.S) #用正则表达式根据该年月(19xx年x月)取出年份
            if match:
                year = int(match.group(1))
                if year>=1950 and year<= 1950: #判断年份是在1946和1956年之间
                    url = selector.xpath("@href").extract()[0] #取该年月的链接
                    news_num = site.xpath("./tr/td[@style='padding-left:13px']/span/text()").extract()[0] #取出该年月有多少条新闻记录
                    newsnum = int(news_num) 
                    pages = newsnum/15 + 1 #根据每页15条,推断出总共有多少页
                    for page in range(1,pages+1):                  
                        #urls.append(self._main_site+url+"&page="+str(page))
                        nurl = self._main_site+url+"&page="+str(page)#根据有多少页,知道该年月有多少个链接
                        yield Request(nurl,callback=self.parse_news_page) #请求该年月的某页链接
       
        #for url in urls:
            #yield Request(url,callback=self.parse_news_page)
            
    def parse_news_page(self,response):
        """ 在某年某月的新闻列表中析出具体每条新闻的链接"""
        sel = Selector(response)
        links = sel.xpath("//tr[@class='tr3 t_one']")
        #items = []
        stime = time.time()
        for link in links:
            item = RmdailyItem() #存储每则新闻的相关信息
            url = link.xpath("./td[@style='text-align:left;padding-left:8px']/h3/a/@href").extract()[0] #取出该报道的url
            item['url'] = self._main_site+url
            title = link.xpath("./td[@style='text-align:left;padding-left:8px']/h3/a/text()").extract()[0]#报道标题
            item['title'] = title
            asel = link.xpath("./td[@class='tal y-style']/a[@class='bl']/text()").extract() #报道作者
            if asel:
                author = asel[0]
            else: #如果没有作者,默认为'null'
                author = 'null'
            item['author'] = author
            date = link.xpath("./td[@class='tal y-style']/div/text()").extract()[0] #报道日期
            item['date'] = date
            yield Request(item['url'], callback=lambda response, item = item: self.parse_news(response,item)) #传给下一个回调函数
            #items.append(item)
        etime = time.time()
        print "parse_news_page:"+str(etime-stime)
        #for ritem in items:
            #yield Request(ritem['url'], callback=lambda response, item=ritem: self.parse_news(response,item))
            
    def parse_news(self,response,item):
        """取出报道的正文内容,写入到本地文件"""
        stime = time.time()
        sel = Selector(response)
        contents = sel.xpath("//div[@class='tpc_content']/text()").extract() 
        content = ""
        for con in contents:
            content+=con #xpath取出正文内容时,有<br/>标签的地方称为分隔符,所以要拼接正文的内容
        item['content'] = content
        print "获取新闻内容"
        self.write_to_file(item) #写入文件
        etime = time.time()
        print "parse_news:"+str(etime-stime)
    
    def write_to_file(self,dict): 
	file_path = "/home/frank/技术学习/web_spider/rm_result"
        os.chdir(file_path)
        date = dict['date'].split('-')
        year = date[0]
        month = date[1]
        
        if os.path.exists(year) == False: #如果没有该年的文件夹,则新建
            os.mkdir(year)
        os.chdir(year)
        if os.path.exists(month) == False: #没有该月的文件夹,则新建
            os.mkdir(month)
        os.chdir(month)
        title = dict['title']
        with open(title,'w+') as f:
            date = dict['date']
            author = dict['author']
            url = dict['url']
            file_content = u"标题: "+title+"\n"+u"时间: "+date+u"\t作者: "+author+"\tURL:"+url+"\n"+dict['content']
            f.write(file_content.encode('gbk'))    
            print "成功写入文件"
        
            
        
    
