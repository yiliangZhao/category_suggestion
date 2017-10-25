#coding: utf-8
import sys
from urlparse import urlparse
from threading import Thread
import httplib, sys
from Queue import Queue
import requests
import time

# concurrent = 200
timings = list()

def doWork():
    while True:
        data = q.get()
        start = time.time()
        status, url = getStatus(data)
        # doSomethingWithResult(status, url)
        q.task_done()
        timings.append(time.time() - start)

def getStatus(url):
    try:
        # url = urlparse(ourl)
        # conn = httplib.HTTPConnection(url.netloc)   
        # conn.request("HEAD", url.path)
        # res = conn.getresponse()
        url = url.encode('utf-8')
        response = requests.post('http://122.11.129.73:31200/queryproc?country=TW', data=url)
        return response.status_code, response.text
    except Exception as e:
        print e
        return "error", str(e)

def doSomethingWithResult(status, url):
    print status, url

if __name__ == '__main__':
	concurrent = int(sys.argv[1])
        start_global = time.time()
	q = Queue(concurrent * 2)
	for i in range(concurrent):
	    t = Thread(target=doWork)
	    t.daemon = True
	    t.start()
	try:
	    for i in range(300):
        	q.put(u"日本%20takara%20tomy%20可%20愛達%20草莓%20水果%20屋%20臺中%20現貨%20可自取")
	    q.join()
	    print concurrent, time.time() - start_global, sum(timings) / float(len(timings))
            import pandas
            df = pandas.DataFrame(data={"response_time": timings})
            df.to_csv("./tokenization_file.csv", sep=',',index=False)
	except KeyboardInterrupt:
	    sys.exit(1)
