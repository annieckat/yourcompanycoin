import os
import pandas as pd
import logging
from class_services_connector import ServicesConnector

def update_user(client,mysql_cn,user_id,user_to_update_id,user_to_update_team_id,user_to_update_is_teamlead,user_to_update_is_admin,user_to_update_monthly_coins_for_share):
    mysql_cn.ping(reconnect=True)
    mycursor = mysql_cn.cursor()
    try:
        mycursor.execute(f'''
        set @current_datetime=UTC_TIMESTAMP()''')
        mycursor.execute(f'''
        update users set team_id = '{user_to_update_team_id}', is_teamlead = '{user_to_update_is_teamlead}',is_admin = '{user_to_update_is_admin}', monthly_coins_for_share = {int(user_to_update_monthly_coins_for_share)}, updated_at = @current_datetime
        where user_id = '{user_to_update_id}';
        ''')
    except Exception as e:
        logging.exception(f'{user_id} update user Error: '+str(e))
        mysql_cn.rollback()
        mycursor.close()
        return('error')
    mysql_cn.commit()
    mycursor.close()
    users=pd.read_sql(f"""select user_id, user_name, team_id, is_teamlead, is_admin, monthly_coins_for_share from users where is_deleted=0""",con=mysql_cn)
    try:
        gs_cn=ServicesConnector().gs_connect()
        sh = gs_cn.open_by_key(os.environ.get('SPREADSHEETS_USERS_FILE'))
        wk=sh.worksheet('title','users')
        wk.clear()
        wk.set_dataframe(users, start = 'A1')
    except Exception as e:
        logging.exception(f'Failed googlesheets update: '+str(e))
        client.chat_postMessage(channel=os.environ.get('ERRORS_CHANNEL_ID'), text=f'''{os.environ.get('DEVELOPERS_SLACK_MENTION')} Failed googlesheets update''')
    return('ok')
