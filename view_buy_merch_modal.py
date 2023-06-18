import pymysql
import pandas as pd
from class_db_data import DbData

def build_buy_merch_modal(mysql_cn,user_id):
    buy_merch_modal={
            "type": "modal",
            "callback_id": "buy_merch_modal",
            "title": {"type": "plain_text", "text": "Buy Merch"},
            "submit": {"type": "plain_text", "text": "Submit"}
            }
    db_data=DbData(mysql_cn)
    merch_items_df=db_data.get_merch_items_df()
    user_db_data=db_data.get_user_info(user_id)
    fuc_balance=user_db_data.get_fuc_balance()
    buy_merch_modal_blocks=[
    		{
    			"type": "section",
    			"text": {
    				"type": "mrkdwn",
    				"text": f"""Choose item you like and click *submit* to buy it!
HR representative will deliver your purchase shortly:gift:
Your current 'Free use coins' balance is *{fuc_balance}* :dollar:"""
    			}
    		},
    		{
    			"type": "input",
                "block_id":"buy_merch_choose_item_block",
    			"element": {
    				"type": "radio_buttons",
    				"options": [{"text": {"type": "mrkdwn","text": f"{row[2]} - {int(row[3])} :dollar:"},"value": f"{row[1]}"} for row in list(merch_items_df.to_records())],
    				"action_id": "buy_merch_choose_item"
    			},
    			"label": {
    				"type": "plain_text",
    				"text": "Merch List"
    			}
    		}
    	]
    buy_merch_modal['blocks']=buy_merch_modal_blocks
    return(buy_merch_modal)
