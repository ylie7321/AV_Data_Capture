import re
from lxml import etree
import json
from bs4 import BeautifulSoup
from ADC_function import *


def getTitle(a):
    try:
        html = etree.fromstring(a, etree.HTMLParser())
        result = str(html.xpath('/html/body/section/div/h2/strong/text()')).strip(" ['']")
        return re.sub('.*\] ', '', result.replace('/', ',').replace('\\xa0', '').replace(' : ', ''))
    except:
        return re.sub('.*\] ', '', result.replace('/', ',').replace('\\xa0', ''))


def getActor(a):  # //*[@id="center_column"]/div[2]/div[1]/div/table/tbody/tr[1]/td/text()
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//strong[contains(text(),"演員")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath('//strong[contains(text(),"演員")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+').replace(",\\xa0", "").replace("'", "").replace(' ', '').replace(',,',
                                                                                                             '').lstrip(
        ',').replace(',', ', ')


def getStudio(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//strong[contains(text(),"片商")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath('//strong[contains(text(),"片商")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+').replace("', '", '').replace('"', '')


def getRuntime(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//strong[contains(text(),"時長")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath('//strong[contains(text(),"時長")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+').rstrip('mi')


def getLabel(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//strong[contains(text(),"系列")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath('//strong[contains(text(),"系列")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+').replace("', '", '').replace('"', '')


def getNum(a):
    html = etree.fromstring(a, etree.HTMLParser())
    result1 = str(html.xpath('//strong[contains(text(),"番號")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath('//strong[contains(text(),"番號")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result2 + result1).strip('+')


def getYear(getRelease):
    try:
        result = str(re.search('\d{4}', getRelease).group())
        return result
    except:
        return getRelease


def getRelease(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//strong[contains(text(),"時間")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath('//strong[contains(text(),"時間")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+')


def getTag(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//strong[contains(text(),"类别")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath('//strong[contains(text(),"类别")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+').replace(",\\xa0", "").replace("'", "").replace(' ', '').replace(',,',
                                                                                                             '').lstrip(
        ',')


def getCover_small(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result = 'http:' + html.xpath(
        '//div[@id=\'videos\']/div[@class=\'grid columns\']/div[@class=\'grid-item column\'][1]/a['
        '@class=\'box\']/div[@class=\'item-image fix-scale-cover\']/img/@src')[0]
    return result


def getCover(htmlcode):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/section/div/div[2]/div[1]/a/img/@src')).strip(" ['']")
    if result == '':
        result = str(html.xpath('/html/body/section/div/div[3]/div[1]/a/img/@src')).strip(" ['']")
    return result


def getDirector(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//strong[contains(text(),"導演")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath('//strong[contains(text(),"導演")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+').replace("', '", '').replace('"', '')


def getOutline(htmlcode):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('//*[@id="introduction"]/dd/p[1]/text()')).strip(" ['']")
    return result


def main(number):
    try:
        a = get_html('https://javdb.com/search?q=' + number + '&f=all').replace(u'\xa0', u' ')
        html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
        result1 = html.xpath('//*[@id="videos"]/div/div/a/@href')[0]
        b = get_html('https://javdb.com' + result1).replace(u'\xa0', u' ')
        dic = {
            'actor': getActor(b),
            'title': getTitle(b).replace("\\n", '').replace('        ', '').replace(getActor(a), '').replace(getNum(a),
                                                                                                             '').replace(
                '无码', '').replace('有码', '').lstrip(' ').replace(number, ''),
            'studio': getStudio(b),
            'outline': getOutline(b),
            'runtime': getRuntime(b),
            'director': getDirector(b),
            'release': getRelease(b),
            'number': getNum(b),
            'cover': getCover(b),
            'cover_small': getCover_small(a),
            'imagecut': 3,
            'tag': getTag(b),
            'label': getLabel(b),
            'year': getYear(getRelease(b)),  # str(re.search('\d{4}',getRelease(a)).group()),
            'actor_photo': '',
            'website': 'https://javdb.com' + result1,
            'source': 'javdb.py',
        }
        if getNum(b) != number:  # 与搜索到的番号不匹配
            dic['title'] = ''
            dic['number'] = ''
        js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'), )  # .encode('UTF-8')
        return js
    except:
        a = get_html('https://javdb.com/search?q=' + number + '&f=all').replace(u'\xa0', u' ')
        html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
        result1 = html.xpath('//*[@id="videos"]/div/div/a/@href')[0]
        b = get_html('https://javdb.com' + result1).replace(u'\xa0', u' ')
        dic = {
            'actor': getActor(b),
            'title': getTitle(b).replace("\\n", '').replace('        ', '').replace(getActor(a), '').replace(
                getNum(b),
                '').replace(
                '无码', '').replace('有码', '').lstrip(' ').replace(number, ''),
            'studio': getStudio(b),
            'outline': getOutline(b),
            'runtime': getRuntime(b),
            'director': getDirector(b),
            'release': getRelease(b),
            'number': getNum(b),
            'cover': getCover(b),
            'cover_small': getCover_small(a),
            'imagecut': 3,
            'tag': getTag(b),
            'label': getLabel(b),
            'year': getYear(getRelease(b)),  # str(re.search('\d{4}',getRelease(a)).group()),
            'actor_photo': '',
            'website': 'https://javdb.com' + result1,
            'source': 'javdb.py',
        }
        if getNum(b) != number:  # 与搜索到的番号不匹配
            dic['title'] = ''
            dic['number'] = ''
        js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'), )  # .encode('UTF-8')
        return js

# print(get_html('https://javdb1.com/v/WwZ0Q'))
