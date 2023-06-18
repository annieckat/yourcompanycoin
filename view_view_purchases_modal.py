import pandas as pd
from class_db_data import DbData
import os

def build_view_purchases_modal(mysql_cn):
    view_purchases_modal={
            "type": "modal",
            "callback_id": "view_purchases_modal",
            "title": {"type": "plain_text", "text": "Purchases"},
            "submit": {"type": "plain_text", "text": "OK"}
            }
    db_data=DbData(mysql_cn)
    purchases=db_data.get_all_purchases()

    view_purchases_modal_blocks=[
    		{
    			"type": "section",
    			"text": {
    				"type": "mrkdwn",
    				"text": "Here is purchases history: \n "
    			}
    		},
		    {
			    "type": "divider"
		    }
    	]

    view_purchases_modal_link=[
		    {
			    "type": "divider"
		    },
            {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Up-to-date informatoin about purchases:"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Link to GS"
				},
				"url": f"https://docs.google.com/spreadsheets/d/{os.environ.get('SPREADSHEETS_MERCH_FILE')}/edit#gid=1518685526",
				"action_id": "view_purchases_link_button"
			    }
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
        view_purchases_modal_blocks=view_purchases_modal_blocks+purchases_list+view_purchases_modal_link
    
    view_purchases_modal['blocks']=view_purchases_modal_blocks
    return(view_purchases_modal)
