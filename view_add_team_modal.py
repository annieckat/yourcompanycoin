import os
def build_add_team_modal(client):
    add_team_modal={
            "type": "modal",
            "callback_id": "add_team_modal",
            "title": {"type": "plain_text", "text": "Add Team"},
            "submit": {"type": "plain_text", "text": "Submit"}
            }

    add_team_modal_blocks=[
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Here you can add new team."
			}
		},
		{
			"type": "input",
			"block_id": "add_team_enter_team_block",
			"element": {
				"type": "plain_text_input",
				"action_id": "add_team_enter_team"
			},
			"label": {
				"type": "plain_text",
				"text": "What is the name of the team?"
			}
		},
        {
			"type": "input",
			"block_id": "add_team_enter_monthly_transfer_block",
			"element": {
				"type": "plain_text_input",
				"action_id": "add_team_enter_monthly_transfer"
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
				"action_id": "add_team_link_botton"
			}
		}
	]
    add_team_modal['blocks']=add_team_modal_blocks
    return(add_team_modal)