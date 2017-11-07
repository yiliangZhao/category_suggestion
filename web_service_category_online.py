#coding=utf-8
from flask import Flask, jsonify, abort, make_response, request
import time
import json
import pickle
import numpy
import requests
from feature_extraction import extract_information_bulk, extract_information
from prediction_pipeline import predict
from tokenization_local import tokenization

    
app = Flask(__name__)

"""
curl -i -H "Accept: application/json" "203.116.23.21:5001/category/v1.1/items{'itemid':556324, 'shopid':67000}"
curl "http://203.116.23.21:5001/category/v1.1/items?itemid=556324&shopid=67000"
curl "http://203.116.23.21:5001/category/v1.1/items?itemid=556324&shopid=67000"
"""
@app.route("/")
def hello_world():
    return "Hello World!"

@app.route('/category-suggestion/v1.1/item', methods=['GET'])
def get_items():
    start_time = time.time()
    itemname = tokenization(request.args.get('title'))
    results = predict(0, itemname, '')
    status = 200
    return jsonify(results), status


@app.route('/category/v1.1/list_items', methods=['POST'])
def post_items():
    if not request.json or not 'items' in request.json:
        abort(400)

    # items is a list of tuples [(itemid, shopid), (itemid, shopid),... (itemid, shopid)]
    items = list()
    for item in request.json['items']:
        items.append(item)

    print ('# of items in the list: ', len(items))
    if len(items) < 1:
        return jsonify({}), 301

    df_features = extract_information_bulk(items)
    print ('length of dataframe: ', len(df_features))
    # df_features.to_csv('debug_web_services_before.csv', index=None, encoding='utf-8')
    
    df_features['tokened_name'] = df_features['name'].apply(tokenization)
    df_features['tokened_description'] = df_features['description'].apply(tokenization) 
    df_features['category_suggestions'] = df_features.apply(
        lambda row: predict(row['itemid'], row['tokened_name'], row['tokened_description'], True), axis=1)

    df_results = df_features[['itemid', 'shopid', 'category_suggestions']]
    # print('time elapsed: %s' % (time.time() - start_time))
    # df_results.to_csv('debug_web_services_after.csv', index=None, encoding='utf-8')
    result = df_results.to_dict(orient='records')

    return jsonify(result), 200
    # return json.dumps(result, ensure_ascii=False, default=default), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=32143, threaded=True)
