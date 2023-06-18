import pandas as pd
import logging
from class_services_connector import ServicesConnector
import os

def update_items(mysql_cn,user_id):
    def stream_to_db(df,table_,insert_type):
        try:
            columns=str(df.columns.to_list()).replace("'","").replace("[","").replace("]","")
            columns_mapping=('%s, '*len(df.columns))[:-2]
            sql_insert =f"""{insert_type} INTO {ServicesConnector().DB_NAME}.{table_} ({columns})
                    VALUES ({columns_mapping})"""
            data_to_insert = [tuple(x) for x in df.values]
            mycursor.executemany(sql_insert, data_to_insert)
        except Exception as e:
            logging.exception(f'{insert_type} Error {table_}: '+str(e))

    gs_cn=ServicesConnector().gs_connect()

    sh = gs_cn.open_by_key(os.environ.get('SPREADSHEETS_MERCH_FILE'))
    wk=sh.worksheet('title','items')
    items = wk.get_as_df(has_header=True)

    mysql_cn.ping(reconnect=True)
    mycursor = mysql_cn.cursor()
    try:
        mycursor.execute('truncate table items;')
        stream_to_db(items,'items','INSERT')
    except Exception as e:
        logging.exception(f'{user_id} Items update: '+str(e))
        mysql_cn.rollback()
        mycursor.close()
        return('error','')
    mysql_cn.commit()
    mycursor.close()
    return('ok')