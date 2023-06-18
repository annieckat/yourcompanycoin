import os
import numpy as np
import pandas as pd
import logging
from class_services_connector import ServicesConnector

def make_refund(client,mysql_cn,user_id,receiver_id,amount,comment):
    mysql_cn.ping(reconnect=True)
    mycursor = mysql_cn.cursor()
    try:
        mycursor.execute(f'''
        set @current_datetime=UTC_TIMESTAMP()''')
        mycursor.execute(f'''
        set @receiver_account_id=(select account_id from accounts where user_id='{receiver_id}')''')
        mycursor.execute(f'''
        update accounts 
        set free_use_coins = free_use_coins + {amount}
        where account_id=@receiver_account_id
        ''')
        mycursor.execute(f'''
        insert into external_transfers (sender_account_id, receiver_account_id, receiver_subaccount_type, transfer_type, coins_sent, created_at, comment)
        select 'tech' as sender_account_id, @receiver_account_id as receiver_account_id, 'free_use_coins' as receiver_subaccount_type, 'refund' as transfer_type, {amount} as coins_sent, @current_datetime as created_at, '{comment}' as comment;
        ''')
        transfer_id=mycursor.lastrowid
    except Exception as e:
        logging.exception(f'{user_id} transfer Error: '+str(e))
        mysql_cn.rollback()
        mycursor.close()
        return('error','')
    mysql_cn.commit()
    mycursor.close()
    msg=f'''<@{user_id}> has refunded you {amount} YourCompanyCoins for {comment}.'''
    client.chat_postMessage(channel=receiver_id, 
                            text=msg)
    return('ok',transfer_id)