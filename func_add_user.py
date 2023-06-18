import os
import pandas as pd
import logging
from class_services_connector import ServicesConnector

def add_user(client,mysql_cn,user_id,new_user_id,new_user_name,new_user_team_id,new_user_is_teamlead,new_user_is_admin,new_user_monthly_coins_for_share):
    mysql_cn.ping(reconnect=True)
    mycursor = mysql_cn.cursor()
    try:
        mycursor.execute(f'''
        set @current_datetime=UTC_TIMESTAMP()''')
        mycursor.execute(f'''
        insert into users (user_id, user_name, team_id, is_teamlead, is_admin, monthly_coins_for_share, created_at, updated_at)
        select '{new_user_id}' as user_id, '{new_user_name}' as user_name, '{new_user_team_id}' as team_id, {int(new_user_is_teamlead)} as is_teamlead, {int(new_user_is_admin)} as is_admin, {int(new_user_monthly_coins_for_share)} as monthly_coins_for_share, @current_datetime as created_at, @current_datetime as updated_at
        on duplicate key update user_name = '{new_user_name}', team_id = '{new_user_team_id}', is_teamlead = {int(new_user_is_teamlead)}, is_admin = {int(new_user_is_admin)}, monthly_coins_for_share = {int(new_user_monthly_coins_for_share)}, updated_at = @current_datetime, is_deleted = 0;
        ''')
        mycursor.execute(f'''
        insert into accounts (account_id, account_type, user_id, team_id, coins_for_share, free_use_coins, updated_at)
        select 'user:{new_user_id}' as account_id, 'user' as account_type, '{new_user_id}' as user_id, null as team_id, {int(new_user_monthly_coins_for_share)} as coins_for_share, 100 as free_use_coins, @current_datetime as updated_at
        on duplicate key update coins_for_share = {int(new_user_monthly_coins_for_share)}, updated_at = @current_datetime;
        ''')
    except Exception as e:
        logging.exception(f'{user_id} adding user Error: '+str(e))
        mysql_cn.rollback()
        mycursor.close()
        return('error')
    mysql_cn.commit()
    mycursor.close()
    new_user=pd.read_sql(f"""select user_id, user_name, team_id, is_teamlead, is_admin, monthly_coins_for_share from users where user_id='{new_user_id}'""",con=mysql_cn)
    new_user=list(new_user.to_records())[0]
    new_user=[str(i) for i in new_user][1:]
    msg=f'''Welcome to YourCompanyCoin! :tada:'''
    client.chat_postMessage(channel=new_user_id, 
                            text=msg)
    try:
        gs_cn=ServicesConnector().gs_connect()
        sh = gs_cn.open_by_key(os.environ.get('SPREADSHEETS_USERS_FILE'))
        wk=sh.worksheet('title','users')
        wk.append_table(new_user)
    except Exception as e:
        logging.exception(f'Failed to add user in googlesheets: '+str(e))
        client.chat_postMessage(channel=os.environ.get('ERRORS_CHANNEL_ID'), text=f'''{os.environ.get('DEVELOPERS_SLACK_MENTION')} Failed to add a user with id={new_user_id} to googlesheets''')
    return('ok')
