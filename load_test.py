#coding: utf-8
import sys
#from urllib.parse import urlparse
from threading import Thread
# import http.client, sys
from queue import Queue
import requests
import time

# concurrent = 200
timings = list()

def doWork():
    while True:
        url = q.get()
        start = time.time()
        status, url = getStatus(url)
        doSomethingWithResult(status, url)
        q.task_done()
        end = time.time()
        timings.append(end - start)
        print ('start time: %d, end time: %d' %(start, end))

def getStatus(url):
    try:
        # url = urlparse(ourl)
        # conn = httplib.HTTPConnection(url.netloc)   
        # conn.request("HEAD", url.path)
        # res = conn.getresponse()
        response = requests.get(url)
        result = response.json()
        return response.status_code, result
    except:
        return "error"

def doSomethingWithResult(status, url):
    # print(status, url)
    pass

if __name__ == '__main__':
	concurrent = int(sys.argv[1])
	start_global = time.time()
	q = Queue(concurrent * 2)
	for i in range(concurrent):
	    t = Thread(target=doWork)
	    t.daemon = True
	    t.start()
	try:
	    for i in range(600):
	        q.put("http://203.116.23.228:5000/category/v1.1/item?itemname=日本%20takara%20tomy%20可%20愛達%20草莓%20水果%20屋%20臺中%20現貨%20可自取")
	    q.join()
	    print(concurrent, time.time() - start_global, sum(timings) / float(len(timings)))
	    import pandas
	    df = pandas.DataFrame(data={"response_time": timings})
	    df.to_csv("./response_time_%d.csv" % concurrent, sep=',',index=False)
	except KeyboardInterrupt:
	    sys.exit(1)

