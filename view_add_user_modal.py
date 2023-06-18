from class_db_data import DbData
import os

def build_add_user_modal(mysql_cn):
    add_user_modal={
            "type": "modal",
            "callback_id": "add_user_modal",
            "title": {"type": "plain_text", "text": "Add User"},
            "submit": {"type": "plain_text", "text": "Submit"}
            }

    db_data=DbData(mysql_cn)
    teams_list=db_data.get_teams_list()

    teams_options = []
    for team in teams_list:
        teams_options += [{"text": {"type": "plain_text", "text": team}, "value": team}]

    add_user_modal_blocks=[
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Here you can add your new coworker!"
			}
		},
		{
			"type": "input",
			"block_id": "add_user_select_user_block",
			"element": {
				"type": "users_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select user"
				},
				"action_id": "add_user_select_user"
			},
			"label": {
				"type": "plain_text",
				"text": "Who you want to add to YourCorpCoin app?"
			}
		},
		{
			"type": "input",
			"block_id": "add_user_select_team_block",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select a team"
				},
                "options": teams_options,
				"action_id": "add_user_select_team"
			},
			"label": {
				"type": "plain_text",
				"text": "Which team do you want to add a coworker to?"
			}
		},
        {
			"type": "input",
            "block_id": "add_user_is_teamlead_block",
			"element": {
				"type": "radio_buttons",
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "Yes"
						},
						"value": "1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "No"
						},
						"value": "0"
					}
				],
				"action_id": "add_user_is_teamlead"
			},
			"label": {
				"type": "plain_text",
				"text": "Is teamlead?"
			}
        },
		{
			"type": "input",
            "block_id": "add_user_is_admin_block",
			"element": {
				"type": "radio_buttons",
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "Yes"
						},
						"value": "1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "No"
						},
						"value": "0"
					}
				],
				"action_id": "add_user_is_admin"
			},
			"label": {
				"type": "plain_text",
				"text": "Is admin?"
			}
        },
		{
			"type": "input",
			"block_id": "add_user_monthly_coins_for_share_block",
			"element": {
				"type": "plain_text_input",
				"action_id": "add_user_monthly_coins_for_share"
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
				"action_id": "add_user_link_button"
			}
		}
	]
    add_user_modal['blocks']=add_user_modal_blocks
    return(add_user_modal)
