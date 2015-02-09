#coding=utf-8
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import FormRequest
import os,time
class RmDailySpider(Spider):
    name = 'rmdaily'
    allowed_domains = ['rmrbw.info']
    _main_site = "http://rmrbw.info/"
    start_urls = ['http://rmrbw.info/read.php?tid=109243&fpage=3']
    
    #def start_requests(self):
        #urls = []
        #with open("/home/frank/sinaweibo/urls.txt","r+") as fread:
            #urls = fread.read().split("!")
            
        #form_request = []
        #for url in urls:
            #form_request.append(FormRequest(url,callback=self.parse))
            
        #return form_request
    def write_to_file(self,dict): 
        os.chdir('/home/frank/sinaweibo/rm_result')
        date = dict['date'].split('-')
        year = date[0]
        month = date[1]
        
        if os.path.exists(year) == False:
            os.mkdir(year)
        os.chdir(year)
        if os.path.exists(month) == False:
            os.mkdir(month)
        os.chdir(month)
        title = dict['title']
        with open(title,'w+') as f:
            date = dict['date']
            author = dict['author']
            url = dict['url']
            file_content = u"标题: "+title+"\n"+u"时间: "+date+u"\t作者: "+author+"\tURL:"+url+"\n"+dict['content']
            f.write(file_content.encode('gbk'))    
   
    def parse(self,response):
        stime = time.time()
        sel = Selector(response)
        contents = sel.xpath("//div[@class='tpc_content']/text()").extract()
        content = ""
        for con in contents:
            content+=con
        item = {}
        item['url']='abc'
        item['title']=u'\u6f5e\u57ce\u53d1\u73b0\u5927\u6279\u8757\u877b  \u9762\u79ef\u8fbe\u5341\u9877\u519c\u4f5c\u591a\u88ab\u5bb3'
        item['author']=u'\u7f05\u4eba\u53cd\u5bf9\u82f1\u56fd\u9ad8\u538b\u653f\u7b56'
        item['date']='2003-12-01'
        item['content']=content
        self.write_to_file(item)
        etime = time.time()
        print str(etime-stime)
        
        
         
    