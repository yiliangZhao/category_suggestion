#coding: utf-8
import sys
import requests
import time

if __name__ == '__main__':
    url = "http://localhost:5000/category/v1.1/item?itemname=日本%20takara%20tomy%20可%20愛達%20草莓%20水果%20屋%20臺中%20現貨%20可自取"
    for i in range(1000):
    	start = time.time()
    	response = requests.get(url)
    	result = response.json()
    	# print(response.status_code, result)
    	print (time.time() -start)

