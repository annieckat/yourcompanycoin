import pymysql
import pandas as pd
from class_db_data import DbData

def build_transfers_history_modal(mysql_cn,user_id):
    transfers_history_modal={
            "type": "modal",
            "callback_id": "transfers_history_modal",
            "title": {"type": "plain_text", "text": "Transfers History"},
            "submit": {"type": "plain_text", "text": "OK"}
            }
    external_transfers=DbData(mysql_cn).get_user_info(user_id).get_external_transfers()
    transfers_history_modal_blocks=[
    		{
    			"type": "section",
    			"text": {
    				"type": "mrkdwn",
    				"text": "Here is your transfers history: \n "
    			}
    		},
		    {
			    "type": "divider"
		    },
            {
    			"type": "section",
    			"text": {
    				"type": "mrkdwn",
    				"text": ',\n\n'.join(external_transfers)
    			}
    		}
    	]
    transfers_history_modal['blocks']=transfers_history_modal_blocks
    return(transfers_history_modal)
