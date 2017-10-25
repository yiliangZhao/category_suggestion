#prereq: python3 setup.py install
from textproc import textproc
import gc
import ast

initResult = textproc.init("./conf/textproc.xml", "index_and_search")
print(initResult)
result = textproc.processQuery('{"country": "TW", "Keyword": "ARZ [保證原廠] Apple 原廠線控耳機 EarPods 原廠耳機 iPhone 7 Plus i6s 蘋果耳機"}')
result1 = textproc.processQuery('{"country": "TW", "Keyword": "ARZ [保證原廠] Apple 原廠線控耳機 EarPods 原廠耳機 iPhone 7 Plus i6s 蘋果耳機"}')
data = ast.literal_eval(result.decode('utf-8'))['query']
print (' '.join(data))

