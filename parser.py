#!usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import argparse
import csv

def set_file(res):
    colums = ["ФИО","Группа","Url","интроверсия_экстраверсия","пассивность_активность","подчиненность_доминирование","замкнутость_общительность", "избегание впечатлений_поиск впечатлений", "избегание внимания_привлечение внимания", "обособленность_привязанность", "равнодушие_теплота", "соперничество_сотрудничество", "подозрительность_доверчивость","непонимание_понимание", "самоуважение_уважение других","импульсивность_самоконтроль","неаккуратность_аккуратность", "отсутствие настойчивости_настойчивость", "безответственность_ответственность","импульсивность_самоконтроль поведения", "беспечность_предусмотрительность",  "эмоц. устойчивость_эмоц. неустойчивость", "беззаботность_тревожность","расслабленность_напряженность","эмоц. комфортность_депрессивность","самодостаточность_самокритика","эмоц. стабильность_эмоц. лабильность","практичность_экспрессивность", "консерватизм_любопытство","реалистичность_любознательность","отсутствие артистичности_артистичность","нечувствительность_сензитивность", "ригидность_пластичность"]
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
            res_buf = ((itr.find_all('td', {'class':'jCell jCellC'}))[1]).string
            res[left+'_'+right] = res_buf

        elif not ( itr.find('td', {'class':'jFL'}) == None ):

            left = itr.find('td', {'class':'jFL'}).string
            right = itr.find('td', {'class':'jFR'}).string
            res_buf = ((itr.find_all('td', {'class':'jCell jCellC'}))[1]).string
            res[left+'_'+right] = res_buf
            
    return res

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-f', '--filename', required = True)
    return parser.parse_args().filename


def parse(url, name, group):
    res = {'ФИО' : name, 'Группа' : group, 'Url' : url}
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
            result.append(parse(row[2], row[0], row[1]))
        set_file(result)
        

if __name__ == "__main__":
    main()
    
    
