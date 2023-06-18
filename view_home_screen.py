import os
from class_db_data import DbData
def build_home_screen(user_id,mysql_cn):
    home_screen={"type": "home","callback_id": "home_view"}
    db_data=DbData(mysql_cn)
    users_list=db_data.get_users_list()
    if user_id in users_list:
        user_db_data=db_data.get_user_info(user_id)
        cfs_balance=user_db_data.get_cfs_balance()
        fuc_balance=user_db_data.get_fuc_balance()
        is_teamlead=user_db_data.is_teamlead()
        is_admin=user_db_data.is_admin()
        team_id=user_db_data.get_team_id()
        home_screen_blocks= [
        		{
        			"type": "section",
        			"text": {
        				"type": "mrkdwn",
        				"text": f"Hey, <@{user_id}>! Welcome to your personal YourCompanyCoin account! You can view you balance and manage your coins right here. What are you planning on doing now?"
        			}
        		},
                {
        			"type": "section",
        			"text": {
        				"type": "mrkdwn",
        				"text": "\n\n*USER SECTION*"
        			}
        		},
        		{
        			"type": "divider"
        		},
        		{
        			"type": "section",
        			"text": {
        				"type": "mrkdwn",
        				"text": f"Your personal balance: \n Coins for share: *{cfs_balance}* :dollar: \n Free use coins: *{fuc_balance}* :dollar:"
        			}
        		},
        		{
        			"type": "actions",
        			"elements": [
        				{
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "Share Coins"
        					},
        					"value": "share_coins_home_button",
        					"action_id": "share_coins"
        				},
        				{
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "Buy Merch"
        					},
        					"value": "buy_merch_home_button",
        					"action_id": "buy_merch"
        				},
                        {
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "Transfers History"
        					},
        					"value": "transfers_history_home_button",
        					"action_id": "transfers_history"
        				},
                        {
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "Purchases History"
        					},
        					"value": "purchases_history_home_button",
        					"action_id": "purchases_history"
        				}
        			]
        		}]
        if is_teamlead==1:
            team_balance=db_data.get_team_balance(team_id)
            home_screen_blocks= home_screen_blocks+[
                {
        			"type": "section",
        			"text": {
        				"type": "mrkdwn",
        				"text": "\n\n*TEAMLEAD SECTION*"
        			}
        		},
                {
        			"type": "divider"
        		},
        		{
        			"type": "section",
        			"text": {
        				"type": "mrkdwn",
        				"text": f"Your team balance: \n Coins for share: *{team_balance}* :dollar:"
        			}
        		},
        		{
        			"type": "actions",
        			"elements": [
        				{
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "Share Team Coins"
        					},
        					"value": "share_team_coins_home_button",
        					"action_id": "share_team_coins"
        				},
                        {
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "Team transfer history"
        					},
        					"value": "team_transfers_history_home_button",
        					"action_id": "team_transfers_history"
        				}
        			]
        		}]
        if is_admin==1:
            home_screen_blocks= home_screen_blocks+[
                {
        			"type": "section",
        			"text": {
        				"type": "mrkdwn",
        				"text": "\n\n*ADMIN SECTION*"
        			}
        		},
                {
        			"type": "divider"
        		},
        		{
        			"type": "actions",
        			"elements": [
        				{
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "Add user"
        					},
        					"value": "add_user_home_button",
        					"action_id": "add_user"
        				},
                        {
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "Update user"
        					},
        					"value": "update_user_home_button",
        					"action_id": "update_user"
        				},
                        {
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "Delete user"
        					},
        					"value": "delete_user_home_button",
        					"action_id": "delete_user"
        				},
        				{
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "Add Team"
        					},
        					"value": "add_team_home_button",
        					"action_id": "add_team"
        				},
        				{
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "Update Team"
        					},
        					"value": "update_team_home_button",
        					"action_id": "update_team"
        				},
                        {
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "Delete Team"
        					},
        					"value": "delete_team_home_button",
        					"action_id": "delete_team"
        				},
                        {
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "View Purchases"
        					},
        					"value": "view_purchases_home_button",
        					"action_id": "view_purchases"
        				},
                        {
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "Update merch list"
        					},
        					"value": "update_merch_list_home_button",
        					"action_id": "update_merch_list"
        				},
                        {
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "Make refund"
        					},
        					"value": "make_refund_home_button",
        					"action_id": "make_refund"
        				}

        			]
        		}]
    else:
        home_screen_blocks= [
        		{
        			"type": "section",
        			"text": {
        				"type": "mrkdwn",
        				"text": "Sorry, you don't have an access to YourCompanyCoin service. Please, contact HR for more information"
        			}
        		}]
    home_screen['blocks']=home_screen_blocks
    return(home_screen)
