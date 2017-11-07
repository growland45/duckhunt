#!/usr/bin/python3
from html.parser import HTMLParser
import myio;
import sys

def dbg(text):
  print (text, file= sys.stderr)

class searchresultparser(HTMLParser):
  hrefurl= ''; inhref= False

  def __init__(self):
    HTMLParser.__init__(self)

  def handle_starttag(self, tag, attrs):
    if tag=='a':  return self.handle_startatag(tag, attrs)

  def handle_startatag(self, tag, attrs):
    self.hreftitle= ''
    for attr in attrs:
      ttype= attr[0];  val= attr[1]
      if ttype=='href':
        self.inhref= True; self.hrefurl= val

  def handle_data(self, data):
    if self.inhref:
      self.hreftitle= self.hreftitle+ ' '+ searchresultparser.html_decrappify(data)

  def handle_endtag(self, tag):
    if self.inhref:  self.handle_href()
    self.inhref= False;

  def handle_href(self):
    if (self.hrefurl.startswith('http')):  self.handle_search_result(self.hrefurl, self.hreftitle)
    self.hrefurl= '';  self.hreftitle= ''

  def html_decrappify(html):
    html = html.replace('\n', ' ').replace('\r', '')
    return html

  def handle_search_result(self, hrefurl, hreftitle):
    print(hrefurl, hreftitle)


url= 'https://duckduckgo.com/html'
keywords= sys.argv[1:]
dd= {};  dd['q']= ' '.join(keywords);

sp= searchresultparser()
status= myio.dourl(url, sp, dd)
dbg(status)


