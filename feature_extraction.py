# This file contains a function to obtain model results from itemid and shopid
import os
import sys
import time
import numpy as np
import re
import pandas as pd
import pymysql
import pymysql.cursors
import datetime

NUM_TABLE = 1000  # number of item tables in version 2 in production

# function to obtain connection to the database
def connect_db():
    """
    This function returns a connection to database
    :param host: IP of database
    :param db: name of database
    :return: connection to the database
    """
    conn_dict = {
        'host': os.environ['HOST_ITEM_DB'],
        'user': os.environ['SQL_DB_USER'],
        'password': os.environ['SQL_DB_PASSWORD'],
        'port': 6606,
        'db': 'shopee_item_v2_db',
        'charset': 'utf8' 
    }
    conn_ = pymysql.connect(**conn_dict, cursorclass=pymysql.cursors.DictCursor)
    return conn_


# function to get name, description and main_cat from itemid and shopid
def extract_information(itemid, shopid):
    conn_item = connect_db()
    shop_hash = shopid % NUM_TABLE
    cursor = conn_item.cursor()
    query = "SELECT itemid, shopid, name, description FROM item_v2_tab_%08d WHERE itemid = %d;" % (shop_hash, itemid)
    print (query)
    cursor.execute(query)
    
    if cursor.rowcount < 1:
        return None, None, None
    row = cursor.fetchone()
    itemid_fi, shopid_fi, name_fi, description_fi = int(row['itemid']), int(row['shopid']), row['name'], row['description']
    return name_fi, description_fi


def extract_information_bulk(list_items):
    """
    Return a dataframe with columns: itemid, shopid, name, description, main_cat
    :param items:
    :return:
    """
    list_itemid = [x[0] for x in list_items]

    table_item_dict = dict()
    for itemid in list_itemid:
        key = itemid % 1000
        if key in table_item_dict:
            table_item_dict[key].append(str(itemid))
        else:
            table_item_dict[key] = [str(itemid)]

    table_shop_dict = dict()
    for pair in list_items:
        itemid = pair[0]
        shopid = pair[1]
        key = shopid % 1000
        if key in table_shop_dict:
            table_shop_dict[key].append(str(itemid))
        else:
            table_shop_dict[key] = [str(itemid)]

    conn_item = connect_db()

    list_items = list()
    column_names = ['itemid', 'shopid', 'name', 'description']
    for shop_hash, items in table_shop_dict.items():
        cursor = conn_item.cursor()
        query = "SELECT itemid, shopid, name, description FROM item_v2_tab_%08d WHERE itemid in (%s);" % (shop_hash, ','.join(list(set(items))))
        rows = cursor.execute(query)

        for row in cursor:
            itemid_fi, shopid_fi, name_fi, description_fi = int(row['itemid']), int(row['shopid']), row['name'], row['description']
            info = (itemid_fi, shopid_fi, name_fi.decode('utf-8'), description_fi.decode('utf-8'))
            list_items.append(info)
    df_information = pd.DataFrame.from_records(list_items, columns=column_names)
    return df_information



if __name__ == '__main__':
    list_items = [[556324, 67000], [982869, 67000], [1919083, 67000], [1919522, 67000], [1920312, 67000],
                  [1920598, 67000], [1920740, 67000], [1921333, 67000], [1922152, 67000], [5580304, 1621000], [6110398, 1621000],
                  [6161116, 1621000], [6395354, 1621000], [6396373, 1621000], [6396724, 1621000], [6747041, 1621000], [7495889, 1621000],
                  [7579054, 1621000], [7810626, 67000], [8071410, 1621000], [9995789, 1621000], [10003314, 2543000], [11278655, 1621000]]

    name, descriptino = (extract_information(556324, 67000))
    print (name.decode('utf-8'))
    df_features = extract_information_bulk(list_items)

    # df_features['category_suggestions'] = df_features.apply(
    #     lambda row: predict(row['tokened_name'], row['tokened_description']),
    #     axis=1)

    # prediction = list()
    # for index, row in df_features.iterrows():
    #    prediction.append(predict(row['tokened_name'], row['tokened_description']))
    # df_features['category_suggestions'] = prediction
    df_features.to_csv('debug_category_recommendation.csv', index=None, encoding='utf-8')
