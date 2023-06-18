#import pymysql
#import pandas as pd
#from class_db_data import DbData

def build_make_refund_modal(mysql_cn,user_id):
    make_refund_modal={
            "type": "modal",
            "callback_id": "make_refund_modal",
            "title": {"type": "plain_text", "text": "Make Refund"},
            "submit": {"type": "plain_text", "text": "Submit"}
            }
    
    make_refund_modal_blocks=[
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Here you can refund coins to your coworkers!"
			}
		},
		{
			"type": "input",
			"block_id": "make_refund_select_user_block",
			"element": {
				"type": "users_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select user"
				},
				"action_id": "make_refund_select_user"
			},
			"label": {
				"type": "plain_text",
				"text": "Who you wanna to make refund?"
			}
		},
		{
			"type": "input",
			"block_id": "make_refund_enter_amount_block",
			"element": {
				"type": "plain_text_input",
				"action_id": "make_refund_enter_amount"
			},
			"label": {
				"type": "plain_text",
				"text": "How much would you like to refund?"
			}
		},
		{
			"type": "input",
			"block_id": "make_refund_enter_comment_block",
			"element": {
				"type": "plain_text_input",
				"action_id": "make_refund_enter_comment"
			},
			"label": {
				"type": "plain_text",
				"text": "What purchase is the return for?"
			}
		}
	]
    make_refund_modal['blocks']=make_refund_modal_blocks
    return(make_refund_modal)