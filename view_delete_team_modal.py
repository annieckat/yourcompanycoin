from class_db_data import DbData
import os

def build_delete_team_modal(mysql_cn):
    delete_team_modal={
            "type": "modal",
            "callback_id": "delete_team_modal",
            "title": {"type": "plain_text", "text": "Delete Team"},
            "submit": {"type": "plain_text", "text": "Delete"}
            }

    db_data=DbData(mysql_cn)
    teams_list=db_data.get_teams_list()

    teams_options = []
    for team in teams_list:
        teams_options += [{"text": {"type": "plain_text", "text": team}, "value": team}]

    delete_team_modal_blocks=[
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Here you can delete empty team"
			}
		},
		{
			"type": "input",
			"block_id": "delete_team_select_team_block",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select the team"
				},
                "options": teams_options,
				"action_id": "delete_team_select_team"
			},
			"label": {
				"type": "plain_text",
				"text": "Which team do you want to delete?"
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
				"action_id": "delete_team_link_button"
			}
		}
	]
    delete_team_modal['blocks']=delete_team_modal_blocks
    return(delete_team_modal)
