from class_db_data import DbData
import os

def build_update_team_modal(mysql_cn):
    update_team_modal={
            "type": "modal",
            "callback_id": "update_team_modal",
            "title": {"type": "plain_text", "text": "Update Team"},
            "submit": {"type": "plain_text", "text": "Submit"}
            }

    db_data=DbData(mysql_cn)
    teams_list=db_data.get_teams_list()

    teams_options = []
    for team in teams_list:
        teams_options += [{"text": {"type": "plain_text", "text": team}, "value": team}]

    update_team_modal_blocks=[
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Choose parameter to change"
			}
		},
        {
			"type": "input",
			"block_id": "update_team_select_team_block",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select the team"
				},
                "options": teams_options,
				"action_id": "update_team_select_team"
			},
			"label": {
				"type": "plain_text",
				"text": "Which team do you want to update?"
			}
		},
        {
			"type": "input",
			"block_id": "update_team_enter_monthly_transfer_block",
			"element": {
				"type": "plain_text_input",
				"action_id": "update_team_enter_monthly_transfer"
			},
			"label": {
				"type": "plain_text",
				"text": "How many coins to accrue monthly?"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Up-to-date informatoin about teams:"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Link to GS"
				},
				"url": f"https://docs.google.com/spreadsheets/d/{os.environ.get('SPREADSHEETS_USERS_FILE')}/edit#gid=380478362",
				"action_id": "update_team_link_button"
			}
		}
	]
    update_team_modal['blocks']=update_team_modal_blocks
    return(update_team_modal)
