from class_db_data import DbData
import os

def build_update_user_modal(mysql_cn):
    update_user_modal={
            "type": "modal",
            "callback_id": "update_user_modal",
            "title": {"type": "plain_text", "text": "Update User"},
            "submit": {"type": "plain_text", "text": "Submit"}
            }

    db_data=DbData(mysql_cn)
    teams_list=db_data.get_teams_list()

    teams_options = []
    for team in teams_list:
        teams_options += [{"text": {"type": "plain_text", "text": team}, "value": team}]
    teams_options=[{"text": {"type": "plain_text", "text": "-"}, "value": "-"}]+teams_options
    
    update_user_modal_blocks=[
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Here you can update users info"
			}
		},
        {
    		"type": "section",
    		"text": {
    			"type": "mrkdwn",
    			"text": "Leave preselected '-' value for parameters you don't want to change"
    			}
    		},
        {
			"type": "input",
			"block_id": "update_user_select_user_block",
			"element": {
				"type": "users_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select user"
				},
				"action_id": "update_user_select_user"
			},
			"label": {
				"type": "plain_text",
				"text": "Select user to update."
			}
		},
		{
			"type": "input",
			"block_id": "update_user_select_team_block",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select team"
				},
                "options": teams_options,
                "initial_option": {"text": {"type": "plain_text", "text": "-"}, "value": "-"},
				"action_id": "update_user_select_team"
			},
			"label": {
				"type": "plain_text",
				"text": "Which team is this user from now?"
			}
		},
        {
			"type": "input",
			"block_id": "update_user_is_teamlead_block",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select teamlead status"
				},
                "options": [{"text": {"type": "plain_text", "text": "-"}, "value": "-"}, 
                            {"text": {"type": "plain_text", "text": "Yes"}, "value": "1"}, 
                            {"text": {"type": "plain_text", "text": "No"}, "value": "0"}],
                "initial_option": {"text": {"type": "plain_text", "text": "-"}, "value": "-"},
                "action_id": "update_user_is_teamlead"
			},
			"label": {
				"type": "plain_text",
				"text": "Is teamlead?"
			}
		},
        {
			"type": "input",
			"block_id": "update_user_is_admin_block",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select admin status"
				},
                "options": [{"text": {"type": "plain_text", "text": "-"}, "value": "-"},
                            {"text": {"type": "plain_text", "text": "Yes"}, "value": "1"}, 
                            {"text": {"type": "plain_text", "text": "No"}, "value": "0"}],
                "initial_option": {"text": {"type": "plain_text", "text": "-"}, "value": "-"},
                "action_id": "update_user_is_admin"
			},
			"label": {
				"type": "plain_text",
				"text": "Is admin?"
			}
		},
		{
			"type": "input",
			"block_id": "update_user_monthly_coins_for_share_block",
			"element": {
				"type": "plain_text_input",
                "initial_value": "-",
				"action_id": "update_user_monthly_coins_for_share",
			},
			"label": {
				"type": "plain_text",
				"text": "How many coins for share to accrue monthly?"
			}
		},
		{
			"type": "divider"
		},
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Up-to-date informatoin about users:"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Link to GS"
				},
				"url": f"https://docs.google.com/spreadsheets/d/{os.environ.get('SPREADSHEETS_USERS_FILE')}/edit#gid=0",
				"action_id": "update_user_link_button"
			}
		}
	]
    update_user_modal['blocks']=update_user_modal_blocks
    return(update_user_modal)
