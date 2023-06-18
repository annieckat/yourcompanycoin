import os
import pygsheets
import numpy as np
import pandas as pd
import pymysql
import logging
from class_services_connector import ServicesConnector

def share_coins(client,mysql_cn,user_id,receiver_id,amount,comment,cfs_balance,fuc_balance):
    comment=str(comment).replace("'","`")
    mysql_cn.ping(reconnect=True)
    mycursor = mysql_cn.cursor()
    try:
        mycursor.execute(f'''
        set @current_datetime=UTC_TIMESTAMP()''')
        mycursor.execute(f'''
        set @sender_account_id=(select account_id from accounts where user_id='{user_id}')''')
        mycursor.execute(f'''
        set @receiver_account_id=(select account_id from accounts where user_id='{receiver_id}')''')
        if amount>cfs_balance:
            mycursor.execute(f'''
            set @internal_transfer_amount=(select ({amount}-coins_for_share) from accounts where account_id=@sender_account_id)''')
            mycursor.execute(f'''
            update accounts 
            set free_use_coins = free_use_coins - @internal_transfer_amount,
                coins_for_share= coins_for_share + @internal_transfer_amount
            where account_id=@sender_account_id
            ''')
            mycursor.execute(f'''
            insert into internal_transfers (account_id, coins_sent, created_at)
            select @sender_account_id as account_id, @internal_transfer_amount as coins_sent, @current_datetime as created_at;
            ''')
        mycursor.execute(f'''
        update accounts 
        set coins_for_share = coins_for_share - {amount}
        where account_id=@sender_account_id
        ''')
        mycursor.execute(f'''
        update accounts 
        set free_use_coins = free_use_coins + {amount}
        where account_id=@receiver_account_id
        ''')
        mycursor.execute(f'''
        insert into external_transfers (sender_account_id, receiver_account_id, receiver_subaccount_type, transfer_type, coins_sent, created_at, comment)
        select @sender_account_id as sender_account_id, @receiver_account_id as receiver_account_id, 'free_use_coins' as receiver_subaccount_type, 'user' as transfer_type, {amount} as coins_sent, @current_datetime as created_at, (case when '{comment}'='None' then null else '{comment}' end) as comment;
        ''')
        transfer_id=mycursor.lastrowid
    except Exception as e:
        logging.exception(f'{user_id} transfer Error: '+str(e))
        mysql_cn.rollback()
        mycursor.close()
        return('error','')
    mysql_cn.commit()
    mycursor.close()
    msg=f'''<@{user_id}> has just transferred you {amount} YourCompanyCoins.'''
    if comment!=None:
        msg=msg+f''' With comment: "{comment}"'''  
    client.chat_postMessage(channel=receiver_id, 
                            text=msg)
    return('ok',transfer_id)
