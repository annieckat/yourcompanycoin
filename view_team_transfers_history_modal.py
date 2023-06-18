import pymysql
import pandas as pd
from class_db_data import DbData

def build_team_transfers_history_modal(mysql_cn,user_id):
    db_data=DbData(mysql_cn)
    team_id=db_data.get_user_info(user_id).get_team_id()
    team_transfers_history_modal={
            "type": "modal",
            "callback_id": "team_transfers_history_modal",
            "title": {"type": "plain_text", "text": "Team transfers History"},
            "submit": {"type": "plain_text", "text": "OK"}
            }
    external_transfers=db_data.get_team_transfers(team_id)
    team_transfers_history_modal_blocks=[
    		{
    			"type": "section",
    			"text": {
    				"type": "mrkdwn",
    				"text": "Here is your team transfers history: \n "
    			}
    		},
		    {
			    "type": "divider"
		    }
    	]
    if len(external_transfers)>0:
        external_transfers_list=[{
    			"type": "section",
    			"text": {
    				"type": "mrkdwn",
    				"text": ',\n\n'.join(external_transfers)
    			}
    		}]
        team_transfers_history_modal_blocks= team_transfers_history_modal_blocks+external_transfers_list
    team_transfers_history_modal['blocks']=team_transfers_history_modal_blocks
    return(team_transfers_history_modal)
