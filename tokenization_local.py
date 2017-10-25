import re
import numpy as np
from textproc import textproc
import gc
import ast
import datetime

initResult = textproc.init("./conf/textproc.xml", "index_and_search")

def remove_symbols(source):
    """
    Keep only Chinese Characters and letters of a string
    """
    if source is np.nan:
        return " "
    if type(source) in [int, datetime.datetime, float]:
        return str(source)
        # print source.encode('utf-8')
    # print 'source:', source
    try:
        temp = source.encode('utf-8').decode('utf-8')
    except:
        temp = source.decode('utf-8')
    # print temp
    reg = u"([\u4e00-\u9fa5a-zA-Z]+)"
    pattern = re.compile(reg)
    results = pattern.findall(temp)
    return " ".join(results)


def remove_new_line(string):
    if type(string) != str:
        unicode_str = str(str(string), 'utf-8')
    else:
        unicode_str = string
    return unicode_str.replace('\n', ' ').replace('\r', ' ')


def tokenization(text):
    text = remove_symbols(text)
    # print ('after remove symbol:' + text)
    text = remove_new_line(text)
    raw = '{"country":"TW", "Keyword": "%s"}' %text
    # print (raw)
    data = textproc.processQuery(raw)
    # print (data.decode('utf-8'))
    query = ast.literal_eval(data.decode('utf-8'))['query']
    return ' '.join(query)

