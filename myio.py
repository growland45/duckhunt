import urllib.request, urllib.parse
import http.client
import os, sys

def attend_to_http_proxy():
  if 'http_proxy' in os.environ:
    http_proxy= os.environ['http_proxy'] 
    proxies = {'http':  http_proxy, 'https': http_proxy}
    proxy_support = urllib.request.ProxyHandler(proxies)
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    sys.stderr.write("myio proxy: "+ http_proxy+ "\n")

def dourl(url, htmlparser, postdict= None):
  # fetch the url and parse it through htmlparser
  # htmlparser should be some derived class of html.parser.HTMLParser
  # postdict is optional dictionary of post data
  attend_to_http_proxy()

  postdata= None
  if (postdict):  postdata = urllib.parse.urlencode(postdict).encode()

  try:
    req = urllib.request.Request(url, data= postdata, 
       headers= { 'User-Agent':
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) '+
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
       } )
    r1 = urllib.request.urlopen(req, timeout=20)
  except Exception as e:
    return "FAILED "+ url+ " EXCEPTION "+ str(e)
  if r1.status!= 200:
    return "STATUS "+ str(r1.status)+ ' '+ r1.reason

  data1 = r1.read(); # bytes object
  decoded= data1.decode("utf-8", errors='ignore')
  #print(decoded)
  htmlparser.feed(decoded)
  return "STATUS "+ str(r1.status)+ ' '+ r1.reason
 
