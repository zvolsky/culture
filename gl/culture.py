import urllib2
from hashlib import md5

from bs4 import BeautifulSoup

def url_list(modul):
    '''list of urls to be searched
    '''
    return [url for url in modul.gen_urls()]

def get_html(url, decode_from='utf8'):
    '''default method to get html from url
    '''
    if not '://' in url:
        url = 'http://' + url
    html = u''
    try:
        html = urllib2.urlopen(url).read()
        html = html.decode(decode_from)
        ok = True
    except (urllib2.URLError, LookupError, UnicodeDecodeError), e:
        ok = False
    return ok, html

def cut_program(modul, html):
    '''default method to get program part of the page (from whole html)
    '''
    soup = BeautifulSoup(html)
    return modul.cut_program(soup)        

def ask_provider(modul, decode_from='utf8',
                      get_html=get_html, cut_program=cut_program):
    '''retrieves information (cultural events) from one provider
    '''
    ok = True
    for url in modul.gen_urls():
        ok1, html = get_html(url, decode_from)
        ok = ok and ok1
        program = cut_program(modul, html)
        
        
        ###########
        print md5(str(program)).hexdigest()
