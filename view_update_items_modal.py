#import pymysql
#import pandas as pd
from class_db_data import DbData
import os

def build_update_items_modal(mysql_cn,user_id):
    update_items_modal={
            "type": "modal",
            "callback_id": "update_items_modal",
            "title": {"type": "plain_text", "text": "Update Items"},
            "submit": {"type": "plain_text", "text": "Submit"}
            }

    update_items_modal_blocks=[
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Update the list of items to buy!"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Up-to-date informatoin about list of items is here:"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Link to GS"
				},
				"url": f"https://docs.google.com/spreadsheets/d/{os.environ.get('SPREADSHEETS_MERCH_FILE')}/edit#gid=0",
				"action_id": "update_items_link_button"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Update the data in spreadsheets and click submit to update the information in the database."
			}
		}
	]
    update_items_modal['blocks']=update_items_modal_blocks
    return(update_items_modal)
