import os
import pygsheets
import numpy as np
import pandas as pd
import pymysql
import logging
from class_services_connector import ServicesConnector
from class_db_data import DbData

def make_purchase(client,mysql_cn,user_id,item_id):
    mysql_cn.ping(reconnect=True)
    mycursor = mysql_cn.cursor()
    try:
        mycursor.execute(f'''
        set @current_datetime=UTC_TIMESTAMP()''')
        mycursor.execute(f'''
        set @item_name=(select item_name from items where item_id={item_id})''')
        mycursor.execute(f'''
        set @item_cost=(select item_cost from items where item_id={item_id})''')
        mycursor.execute(f'''
        set @account_id=(select account_id from accounts where user_id='{user_id}')''')
        mycursor.execute(f'''
        update accounts 
        set free_use_coins = free_use_coins - @item_cost
        where account_id=@account_id
        ''')
        mycursor.execute('''
        insert into purchases (account_id, item_cost, item_name, created_at)
        select @account_id as account_id, @item_cost as item_cost, @item_name as item_name, @current_datetime as created_at;
        ''')
        purchase_id=mycursor.lastrowid
    except Exception as e:
        logging.exception(f'{user_id} Purchase Error: '+str(e))
        mysql_cn.rollback()
        mycursor.close()
        return('error','')
    mysql_cn.commit()
    mycursor.close()
    new_purchase=pd.read_sql(f"""select purchase_id,account_id,user_name,item_cost,item_name,purchases.created_at,purchases.status
    from purchases left join accounts using(account_id) left join users using(user_id)
    where purchase_id={purchase_id}""",con=mysql_cn)
    new_purchase=list(new_purchase.to_records())[0]
    new_purchase=[str(i) for i in new_purchase][1:]
    db_data=DbData(mysql_cn)
    admins_list=db_data.get_admins_list()
    for admin_id in admins_list:
        client.chat_postMessage(channel=admin_id, #later change to list of admins user_ids (from db) and add for-cycle
                                text=f'''<@{user_id}> purchased {new_purchase[4]} for {new_purchase[3]} YourCompanyCoins (id={purchase_id})''')
    try:
        gs_cn=ServicesConnector().gs_connect()
        sh = gs_cn.open_by_key(os.environ.get('SPREADSHEETS_MERCH_FILE'))
        wk=sh.worksheet('title','purchases')
        wk.append_table(new_purchase)
    except Exception as e:
        logging.exception(f'Failed to add purchase in googlesheets: '+str(e))
        client.chat_postMessage(channel=os.environ.get('ERRORS_CHANNEL_ID'), text=f'''{os.environ.get('DEVELOPERS_SLACK_MENTION')} Failed to add a purchase with id={purchase_id} to googlesheets''')
    return('ok',purchase_id)
