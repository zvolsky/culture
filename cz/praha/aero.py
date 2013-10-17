'''
cz,Praha, kino Aero
'''

url = 'http://www.kinoaero.cz/cz/program/startdate/'  # + %Y-%m-%d/

from datetime import datetime, date, timedelta

def gen_urls():
    '''generator of urls for analyze
    '''
    dnes = date.today() 
    od = dnes - timedelta(dnes.isoweekday()-1)
    for tyden in xrange(10):
        yield url + od.strftime('%Y-%m-%d')
        od = od + timedelta(7)

def cut_program(soup):
    return soup('div', 'program-box')[0]