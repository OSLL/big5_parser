import requests
from bs4 import BeautifulSoup
import json


def set_file(res):
    with open('result.json', 'w') as f:
        json.dump(res, f, ensure_ascii = False)


def get_html(url):
    session = requests.Session()
    request = session.get(url)
    request.encoding = 'cp1251'
    return request.text


def parse_html(data, res):
    soup = BeautifulSoup(data, 'html.parser')
    print(soup)
    row_list = soup.find('div', {'class':'stdTbl'}).find('table')
    
    for itr in row_list:
        if not ( itr.find('td', {'class':'jFL jBF'}) == None ):
            left = itr.find('td', {'class':'jFL jBF'}).find('a').string
            right = itr.find('td', {'class':'jFR jBF'}).find('a').string
            res_buf = itr.find('td', {'class':'jCell jCellF1L'}).nextSibling.string
            print(left+'_'+right)
            res[left+'_'+right] = res_buf
        elif not ( itr.find('td', {'class':'jFL'}) == None ):
            left = itr.find('td', {'class':'jFL'}).string
            right = itr.find('td', {'class':'jFR'}).string
            res_buf = itr.find('td', {'class':'jCell jCellF2L'}).nextSibling.string
            res[left+'_'+right] = res_buf
            
    return res
        
    
def parse(url):
    res = {}
    data = get_html(url)
    res = parse_html(data, res)
    set_file(res)


if __name__ == "__main__":
    url = input()
    parse(url)
    
    
