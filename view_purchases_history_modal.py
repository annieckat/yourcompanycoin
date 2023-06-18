import pandas as pd
from class_db_data import DbData

def build_purchases_history_modal(mysql_cn,user_id):
    purchases_history_modal={
            "type": "modal",
            "callback_id": "purchases_history_modal",
            "title": {"type": "plain_text", "text": "Purchases History"},
            "submit": {"type": "plain_text", "text": "OK"}
            }
    purchases=DbData(mysql_cn).get_user_info(user_id).get_purchases()
    purchases_history_modal_blocks=[
    		{
    			"type": "section",
    			"text": {
    				"type": "mrkdwn",
    				"text": "Here is your purchases history: \n "
    			}
    		},
		    {
			    "type": "divider"
		    }
    	]
    if len(purchases)>0:
        purchases_list=[{
    			"type": "section",
    			"text": {
    				"type": "mrkdwn",
    				"text": ',\n\n'.join(purchases)
    			}
    		}]
        purchases_history_modal_blocks=purchases_history_modal_blocks+purchases_list
    
    purchases_history_modal['blocks']=purchases_history_modal_blocks
    return(purchases_history_modal)
