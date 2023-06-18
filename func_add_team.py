import os
import pandas as pd
import logging
from class_services_connector import ServicesConnector

def add_team(client,mysql_cn,user_id,new_team_id,monthly_transfer):
    mysql_cn.ping(reconnect=True)
    mycursor = mysql_cn.cursor()
    try:
        mycursor.execute(f'''
        set @current_datetime=UTC_TIMESTAMP()''')
        mycursor.execute(f'''
        insert into teams (team_id, monthly_transfer, created_at, updated_at)
        select '{new_team_id}' as team_id, {monthly_transfer} as monthly_transfer, @current_datetime as created_at, @current_datetime as updated_at
        on duplicate key update monthly_transfer = {monthly_transfer}, updated_at = @current_datetime, is_deleted = 0;
        ''')
        mycursor.execute(f'''
        insert into accounts (account_id, account_type, user_id, team_id, coins_for_share, free_use_coins, updated_at)
        select 'team:{new_team_id}' as account_id, 'team' as account_type, null as user_id, '{new_team_id}' as team_id, {monthly_transfer} as coins_for_share, null as free_use_coins, @current_datetime as updated_at
        on duplicate key update coins_for_share = {monthly_transfer}, updated_at = @current_datetime;
        ''')
    except Exception as e:
        logging.exception(f'{user_id} adding user Error: '+str(e))
        mysql_cn.rollback()
        mycursor.close()
        return('error')
    mysql_cn.commit()
    mycursor.close()
    new_team=pd.read_sql(f"""select team_id, monthly_transfer from teams where team_id='{new_team_id}'""",con=mysql_cn)
    new_team=list(new_team.to_records())[0]
    new_team=[str(i) for i in new_team][1:]
    try:
        gs_cn=ServicesConnector().gs_connect()
        sh = gs_cn.open_by_key(os.environ.get('SPREADSHEETS_USERS_FILE'))
        wk=sh.worksheet('title','teams')
        wk.append_table(new_team)
    except Exception as e:
        logging.exception(f'Failed to add team in googlesheets: '+str(e))
        client.chat_postMessage(channel=os.environ.get('ERRORS_CHANNEL_ID'), text=f'''{os.environ.get('DEVELOPERS_SLACK_MENTION')} Failed to add a team with id={new_team_id} to googlesheets''')
    return('ok')
