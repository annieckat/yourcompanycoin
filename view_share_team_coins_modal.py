import pymysql
import pandas as pd
from class_db_data import DbData

def build_share_team_coins_modal(mysql_cn,user_id):
    share_team_coins_modal={
            "type": "modal",
            "callback_id": "share_team_coins_modal",
            "title": {"type": "plain_text", "text": "Share Team Coins"},
            "submit": {"type": "plain_text", "text": "Submit"}
            }
    db_data=DbData(mysql_cn)
    team_id=db_data.get_user_info(user_id).get_team_id()
    #users_list=db_data.get_team_users_list(team_id)
    team_balance=db_data.get_team_balance(team_id)
    share_team_coins_modal_blocks=[
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Here you can share some coins with your team! \n Your current team balance: \n Coins for share: *{team_balance}*"
			}
		},
		{
			"type": "input",
			"block_id": "share_team_coins_select_user_block",
			"element": {
				"type": "users_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select users"
				},
				"action_id": "share_team_coins_select_user"
			},
			"label": {
				"type": "plain_text",
				"text": "Who you wanna share it with?"
			}
		},
		{
			"type": "input",
			"block_id": "share_team_coins_enter_amount_block",
			"hint": {
				"type": "plain_text",
				"text": "Attention! If you enter amount that exceeds your CFS balance, remaining coins will be retrieved from your FUC balance"
			},
			"element": {
				"type": "plain_text_input",
				"action_id": "share_team_coins_enter_amount"
			},
			"label": {
				"type": "plain_text",
				"text": "How many coins would you like to share?"
			}
		},
		{
			"type": "input",
			"block_id": "share_team_coins_enter_comment_block",
            "optional":True,
			"element": {
				"type": "plain_text_input",
				"multiline": True,
                "max_length":200,
				"action_id": "share_team_coins_enter_comment"
			},
			"label": {
				"type": "plain_text",
				"text": "You can leave a comment for the reciever here:"
			}
		}
	]
    share_team_coins_modal['blocks']=share_team_coins_modal_blocks
    return(share_team_coins_modal)
