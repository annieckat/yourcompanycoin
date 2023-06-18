import os
def build_delete_user_modal():
    delete_user_modal={
            "type": "modal",
            "callback_id": "delete_user_modal",
            "title": {"type": "plain_text", "text": "Delete User"},
            "submit": {"type": "plain_text", "text": "Delete"}
            }

    delete_user_modal_blocks=[
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Here you can delete user permanently"
			}
		},
		{
			"type": "input",
			"block_id": "delete_user_select_user_block",
			"element": {
				"type": "users_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select user"
				},
				"action_id": "delete_user_select_user"
			},
			"label": {
				"type": "plain_text",
				"text": "Select user to delete."
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
				"action_id": "delete_user_link_button"
			}
		}
	]
    delete_user_modal['blocks']=delete_user_modal_blocks
    return(delete_user_modal)
