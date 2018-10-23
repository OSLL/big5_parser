#!usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import argparse
import csv

def set_file(res):
    colums = ['name', "расслабленность_напряженность",
 "обособленность_привязанность", "пассивность_активность",
 "неаккуратность_аккуратность", "отсутствие артистичности_артистичность",
 "эмоц. устойчивость_эмоц. неустойчивость", 
"эмоц. стабильность_эмоц. лабильность", "замкнутость_общительность",
 "отсутствие настойчивости_настойчивость", "самодостаточность_самокритика",
 "практичность_экспрессивность", "импульсивность_самоконтроль",
 "подчиненность_доминирование", "нечувствительность_сензитивность",
 "ригидность_пластичность", "непонимание_понимание", "интроверсия_экстраверсия",
 "самоуважение_уважение других", "реалистичность_любознательность",
 "импульсивность_самоконтроль поведения", "подозрительность_доверчивость",
 "равнодушие_теплота", "избегание впечатлений_поиск впечатлений", "безответственность_ответственность", "соперничество_сотрудничество",
 "эмоц. комфортность_депрессивность", "беззаботность_тревожность",
 "избегание внимания_привлечение внимания", "консерватизм_любопытство", "беспечность_предусмотрительность"]
    with open('result.csv', 'w') as f:
        headers = {}
        writer = csv.DictWriter(f, fieldnames = colums, delimiter = ';')
        writer.writeheader()
        writer.writerows(res)
        


def get_html(url):
    session = requests.Session()
    request = session.get(url)
    request.encoding = 'cp1251'
    return request.text


def parse_html(data, res):
    soup = BeautifulSoup(data, 'html.parser')
    row_list = soup.find('div', {'class':'stdTbl'}).find('table')
    
    for itr in row_list:
        if not ( itr.find('td', {'class':'jFL jBF'}) == None ):
            left = itr.find('td', {'class':'jFL jBF'}).find('a').string
            right = itr.find('td', {'class':'jFR jBF'}).find('a').string
            res_buf = itr.find('td', {'class':'jCell jCellF1L'}).nextSibling.string
            res[left+'_'+right] = res_buf
        elif not ( itr.find('td', {'class':'jFL'}) == None ):
            left = itr.find('td', {'class':'jFL'}).string
            right = itr.find('td', {'class':'jFR'}).string
            res_buf = itr.find('td', {'class':'jCell jCellF2L'}).nextSibling.string
            res[left+'_'+right] = res_buf
            
    return res

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-f', '--filename', required = True)
    return parser.parse_args().filename


def parse(url, name):
    res = {'name' : name}
    data = get_html(url)
    res = parse_html(data, res)
    return res


def main():
    result = []
    filename = get_args()
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter = ';')
        next(reader)
        for row in reader:
            result.append(parse(row[0], row[1]))
        set_file(result)
        

if __name__ == "__main__":
    main()
    
    
