import os
import pandas as pd
import logging
from class_services_connector import ServicesConnector

def delete_team(client,mysql_cn,user_id,team_to_update_id):
    mysql_cn.ping(reconnect=True)
    mycursor = mysql_cn.cursor()
    try:
        mycursor.execute(f'''
        set @current_datetime=UTC_TIMESTAMP()''')
        mycursor.execute(f'''
        update teams set is_deleted = 1,updated_at = @current_datetime where team_id = '{team_to_update_id}';
        ''')
    except Exception as e:
        logging.exception(f'{user_id} deletion team Error: '+str(e))
        mysql_cn.rollback()
        mycursor.close()
        return('error')
    mysql_cn.commit()
    mycursor.close()
    teams=pd.read_sql(f"""select team_id, monthly_transfer from teams where is_deleted=0""",con=mysql_cn)
    try:
        gs_cn=ServicesConnector().gs_connect()
        sh = gs_cn.open_by_key(os.environ.get('SPREADSHEETS_USERS_FILE'))
        wk=sh.worksheet('title','teams')
        wk.clear()
        wk.set_dataframe(teams, start = 'A1')
    except Exception as e:
        logging.exception(f'Failed googlesheets update: '+str(e))
        client.chat_postMessage(channel=os.environ.get('ERRORS_CHANNEL_ID'), text=f'''{os.environ.get('DEVELOPERS_SLACK_MENTION')} Failed googlesheets update''')
    return('ok')