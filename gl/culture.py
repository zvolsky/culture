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

def changed_page(md5, same_pages, same_events):
    '''have to return True, if there are changes from previous run,
    False if content remained same;
    If explicit definition of this function return False, it should update
      the list same_pages with current md5 and same_events with md5's of
      contained events;
      you can later let same_pages and same_events in database
        and remove (and re-insert) changed entries only
    '''
    return True # if no explicit function defined, always understand as changed

def changed_event(md5, same_events):
    '''have to return True, if there are changes from previous run,
    False if content remained same;
    If explicit definition of this function return False, it should update
      the list same_events with md5's of contained events;
      you can later let same_events in database
        and remove (and re-insert) changed entries only
    '''
    return True # if no explicit function defined, always understand as changed

def ask_provider(modul, decode_from='utf8',
           get_html=get_html, cut_program=cut_program,
           changed_page=changed_page, changed_event=changed_event):
    '''retrieves information (cultural events) from one provider
    '''
    ok = True
    same_pages = []     # list of md5 of pages without any change
    same_events = []    # list of md5 of events without any change
    changes = []        # tuples: [0]=md5, [1]=changed content
    for url in modul.gen_urls():
        ok1, html = get_html(url, decode_from)
        ok = ok and ok1
        program = cut_program(modul, html)
        md5p = md5(str(program)).hexdigest()
        if changed_page(md5p, same_pages, same_events):
            changes.append((md5p, []))
            for event in modul.get_events(program):
                md5e = md5(str(event)).hexdigest()
                if changed_event(md5e, same_events): 
                    changes[-1][0].append((md5e, modul.parse_event(event)))
    return changes