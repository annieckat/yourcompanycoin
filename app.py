import os
from slack_bolt import App

import logging
import json
import requests
import datetime
import numpy as np
import pandas as pd
import pygsheets
import pymysql

from func_make_purchase import make_purchase
from func_share_coins import share_coins
from func_share_team_coins import share_team_coins
from func_add_user import add_user
from func_delete_user import delete_user
from func_update_user import update_user
from func_add_team import add_team
from func_delete_team import delete_team
from func_update_team import update_team
from func_update_items import update_items
from func_make_refund import make_refund

from class_services_connector import ServicesConnector
from class_db_data import DbData

from view_home_screen import  build_home_screen
from view_buy_merch_modal import build_buy_merch_modal
from view_share_coins_modal import build_share_coins_modal
from view_transfers_history_modal import build_transfers_history_modal
from view_purchases_history_modal import build_purchases_history_modal
from view_team_transfers_history_modal import build_team_transfers_history_modal
from view_share_team_coins_modal import build_share_team_coins_modal
from view_add_user_modal import build_add_user_modal
from view_add_team_modal import build_add_team_modal
from view_delete_user_modal import build_delete_user_modal
from view_update_user_modal import build_update_user_modal
from view_delete_team_modal import build_delete_team_modal
from view_update_team_modal import build_update_team_modal
from view_view_purchases_modal import build_view_purchases_modal
from view_update_items_modal import build_update_items_modal
from view_make_refund_modal import build_make_refund_modal

logging.basicConfig(level=logging.DEBUG)

mysql_cn=ServicesConnector().mysql_connect()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

#HOME SCREEN
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        user_id=event["user"]
        home_screen=build_home_screen(user_id,mysql_cn)
        client.views_publish(user_id=user_id,view=home_screen)
    except Exception as e:
        print('APP.PY ERROR: '+ str(e))
        logger.error(f"Error publishing home tab: {e}")


#MAIN BUTTONS

##user commands
@app.action("share_coins")
def share_coins_click(ack, client, body, respond):
    ack()
    user_id = body["user"]["id"]
    share_coins_modal=build_share_coins_modal(mysql_cn,user_id)
    client.views_open(trigger_id=body["trigger_id"], view=share_coins_modal)

@app.action("buy_merch")
def buy_merch_click(ack, client, body, respond):
    ack()
    user_id = body["user"]["id"]
    buy_merch_modal=build_buy_merch_modal(mysql_cn,user_id)
    client.views_open(trigger_id=body["trigger_id"], view=buy_merch_modal)

@app.action("transfers_history")
def transfers_history_click(ack, client, body, respond):
    ack()
    user_id = body["user"]["id"]
    transfers_history_modal=build_transfers_history_modal(mysql_cn,user_id)
    client.views_open(trigger_id=body["trigger_id"], view=transfers_history_modal)

@app.action("purchases_history")
def purchases_history_click(ack, client, body, respond):
    ack()
    user_id = body["user"]["id"]
    purchases_history_modal=build_purchases_history_modal(mysql_cn,user_id)
    client.views_open(trigger_id=body["trigger_id"], view=purchases_history_modal)

##team commands
@app.action("share_team_coins")
def share_team_coins_click(ack, client, body, respond):
    ack()
    user_id = body["user"]["id"]
    share_team_coins_modal=build_share_team_coins_modal(mysql_cn,user_id)
    client.views_open(trigger_id=body["trigger_id"], view=share_team_coins_modal)

@app.action("team_transfers_history")
def team_transfers_history_click(ack, client, body, respond):
    ack()
    user_id = body["user"]["id"]
    team_transfers_history_modal=build_team_transfers_history_modal(mysql_cn,user_id)
    client.views_open(trigger_id=body["trigger_id"], view=team_transfers_history_modal)

##admin commands
@app.action("add_user")
def add_user_click(ack, client, body, respond):
    ack()
    add_user_modal=build_add_user_modal(mysql_cn)
    client.views_open(trigger_id=body["trigger_id"], view=add_user_modal)

@app.action("update_user")
def update_user_click(ack, client, body, respond):
    ack()
    update_user_modal=build_update_user_modal(mysql_cn)
    client.views_open(trigger_id=body["trigger_id"], view=update_user_modal)
    
@app.action("delete_user")
def delete_user_click(ack, client, body, respond):
    ack()
    delete_user_modal=build_delete_user_modal()
    client.views_open(trigger_id=body["trigger_id"], view=delete_user_modal)

@app.action("add_team")
def add_team_click(ack, client, body, respond):
    ack()
    add_team_modal=build_add_team_modal(client)
    client.views_open(trigger_id=body["trigger_id"], view=add_team_modal)

@app.action("update_team")
def update_team_click(ack, client, body, respond):
    ack()
    user_id = body["user"]["id"]
    update_team_modal=build_update_team_modal(mysql_cn)
    client.views_open(trigger_id=body["trigger_id"], view=update_team_modal)
    
@app.action("delete_team")
def delete_team_click(ack, client, body, respond):
    ack()
    user_id = body["user"]["id"]
    delete_team_modal=build_delete_team_modal(mysql_cn)
    client.views_open(trigger_id=body["trigger_id"], view=delete_team_modal)

@app.action("view_purchases")
def view_purchases_click(ack, client, body, respond):
    ack()
    view_purchases_modal=build_view_purchases_modal(mysql_cn)
    client.views_open(trigger_id=body["trigger_id"], view=view_purchases_modal)

@app.action("update_merch_list")
def update_merch_list_click(ack, client, body, respond):
    ack()
    user_id = body["user"]["id"]
    update_items_modal=build_update_items_modal(mysql_cn,user_id)
    client.views_open(trigger_id=body["trigger_id"], view=update_items_modal)

@app.action("make_refund")
def make_refund_click(ack, client, body, respond):
    ack()
    user_id = body["user"]["id"]
    make_refund_modal=build_make_refund_modal(mysql_cn,user_id)
    client.views_open(trigger_id=body["trigger_id"], view=make_refund_modal)


#MODAL SUBMISSIONS

##user commands
@app.view("share_coins_modal")
def view_submission(ack, body, client, view):
    user_id = body["user"]["id"]
    receiver_id = view["state"]["values"]['share_coins_select_user_block']['share_coins_select_user']['selected_user']
    amount = view["state"]["values"]['share_coins_enter_amount_block']['share_coins_enter_amount']['value']
    comment = view["state"]["values"]['share_coins_enter_comment_block']['share_coins_enter_comment']['value']
    db_data=DbData(mysql_cn)
    users_list=db_data.get_users_list()
    user_db_data=db_data.get_user_info(user_id)
    cfs_balance=user_db_data.get_cfs_balance()
    fuc_balance=user_db_data.get_fuc_balance()
    errors={}
    if receiver_id not in users_list:
        errors["share_coins_select_user_block"] = f"This user doesn't have YourCompanyCoin account yet. Please, contact HR"
    elif receiver_id==user_id:
        errors["share_coins_select_user_block"] = f"You can't transfer coins to yourself"
    if not amount.isdigit():
        errors["share_coins_enter_amount_block"] = "Please, enter an integer"
    elif int(amount)>cfs_balance+fuc_balance:
        errors["share_coins_enter_amount_block"] = "You don't have enough coins"
    if len(errors)>0:
         ack(response_action="errors", errors=errors)
    else:
        ack()
        try:
            response,transfer_id=share_coins(client,mysql_cn,user_id,receiver_id,int(amount),comment,cfs_balance,fuc_balance)
            if response=='ok':
                msg = f"""Your transfer went smoothly. Transfer id is {transfer_id}"""
            if response=='error':
                msg = "There was an error with your transfer. Please, try again later or contact HR"
        except Exception as e:
            print('APP.PY ERROR: '+ str(e))
            msg = "There was an error with your transfer. Please, try again later or contact HR"
        client.chat_postMessage(channel=user_id, text=msg)

@app.view("buy_merch_modal")
def view_submission(ack, body, client, view):
    user_id = body["user"]["id"]
    item_id = view["state"]["values"]['buy_merch_choose_item_block']['buy_merch_choose_item']['selected_option']['value']
    db_data=DbData(mysql_cn)
    user_db_data=db_data.get_user_info(user_id)
    fuc_balance=user_db_data.get_fuc_balance()
    item_cost=db_data.get_merch_item_cost(item_id)
    if fuc_balance<item_cost:
        errors={}
        errors["buy_merch_choose_item_block"] = "You don't have enough coins yet"
        ack(response_action="errors", errors=errors)
    else:
        ack()
        try:
            response,purchase_id=make_purchase(client,mysql_cn,user_id,item_id)
            if response=='ok':
                msg = f"""Your purchase went smoothly. Purchase id is {purchase_id}. HR will deliver your purchase as soon as possible"""
            if response=='error':
                msg = "There was an error with your purchase. Please, try again later or contact HR"
        except Exception as e:
            print('APP.PY ERROR: '+ str(e))
            msg = "There was an error with your purchase. Please, try again later or contact HR"
        client.chat_postMessage(channel=user_id, text=msg)

@app.view("transfers_history_modal")
def view_submission(ack):
    ack()

@app.view("purchases_history_modal")
def view_submission(ack):
    ack()

##team commands
@app.view("share_team_coins_modal")
def view_submission(ack, body, client, view):
    user_id = body["user"]["id"]
    receiver_id = view["state"]["values"]['share_team_coins_select_user_block']['share_team_coins_select_user']['selected_user']
    amount = view["state"]["values"]['share_team_coins_enter_amount_block']['share_team_coins_enter_amount']['value']
    comment = view["state"]["values"]['share_team_coins_enter_comment_block']['share_team_coins_enter_comment']['value']
    db_data=DbData(mysql_cn)
    users_list=db_data.get_users_list()
    team_id=db_data.get_user_info(user_id).get_team_id()
    team_users_list=db_data.get_team_users_list(team_id)
    team_balance=db_data.get_team_balance(team_id)
    errors={}
    if receiver_id not in users_list:
        errors["share_team_coins_select_user_block"] = f"This user doesn't have YourCompanyCoin account yet. Please, contact HR"
    elif receiver_id not in team_users_list:
        errors["share_team_coins_select_user_block"] = f"This user is not in your team. Please, contact HR in case of mistake"
    if not amount.isdigit():
        errors["share_team_coins_enter_amount_block"] = "Please, enter an integer"
    elif int(amount)>team_balance:
        errors["share_team_coins_enter_amount_block"] = "You don't have enough coins"
    if len(errors)>0:
         ack(response_action="errors", errors=errors)
    else:
        ack()
        try:
            response,transfer_id=share_team_coins(client,mysql_cn,user_id,team_id,receiver_id,int(amount),comment,team_balance)
            if response=='ok':
                msg = f"""Your team transfer went smoothly. Transfer id is {transfer_id}"""
            if response=='error':
                msg = "There was an error with your team transfer. Please, try again later or contact HR"
        except Exception as e:
            print('APP.PY ERROR: '+ str(e))
            msg = "There was an error with your team transfer. Please, try again later or contact HR"
        client.chat_postMessage(channel=user_id, text=msg)

@app.view("team_transfers_history_modal")
def view_submission(ack):
    ack()

##admin commands
@app.view("add_user_modal")
def view_submission(ack, body, client, view):
    user_id = body["user"]["id"]
    new_user_id = view["state"]["values"]['add_user_select_user_block']['add_user_select_user']['selected_user']
    new_user_info=client.users_info(user=str(new_user_id))
    new_user_name=new_user_info["user"]['name']
    new_user_team_id = view["state"]["values"]['add_user_select_team_block']['add_user_select_team']['selected_option']['value']
    new_user_is_teamlead = view["state"]["values"]['add_user_is_teamlead_block']['add_user_is_teamlead']['selected_option']['value']
    new_user_is_admin = view["state"]["values"]['add_user_is_admin_block']['add_user_is_admin']['selected_option']['value']
    new_user_monthly_coins_for_share = view["state"]["values"]['add_user_monthly_coins_for_share_block']['add_user_monthly_coins_for_share']['value']
    db_data=DbData(mysql_cn)
    users_list=db_data.get_users_list()
    errors={}
    if new_user_id in users_list:
        errors["add_user_select_user_block"] = f"This user has already YourCompanyCoin account."
    if not new_user_monthly_coins_for_share.isdigit():
        errors["add_user_monthly_coins_for_share_block"] = "Please, enter an integer"
    if len(errors)>0:
        ack(response_action="errors", errors=errors)
    else:
        ack()
        teamleads_list=db_data.get_team_teamleads_list(new_user_team_id)
        warning=''
        if new_user_is_teamlead == "1" and len(teamleads_list) >0:
            warning=' WARNING: Team of the added user already had a teamlead. Consider updating "is teamlead" parameter for someone.'
        try:
            response=add_user(client,mysql_cn,user_id,new_user_id,new_user_name,new_user_team_id,new_user_is_teamlead,new_user_is_admin,new_user_monthly_coins_for_share)
            if response=='ok':
                msg = f"""New user <@{new_user_id}> has been added to YourCompanyCoin successfully!"""+warning
            if response=='error':
                msg = "Something went wrong while adding a user. :sad_pepe: Please, try again later or contact developer."
        except Exception as e:
            print('APP.PY ERROR: '+ str(e))
            msg = "Something went wrong while adding a user. :sad_pepe: Please, try again later or contact developer."
        client.chat_postMessage(channel=user_id, text=msg)

@app.view("update_user_modal")
def view_submission(ack, body, client, view):
    user_id = body["user"]["id"]
    user_to_update_id = view["state"]["values"]['update_user_select_user_block']['update_user_select_user']['selected_user']
    user_to_update_team_id = view["state"]["values"]['update_user_select_team_block']['update_user_select_team']['selected_option']['value']
    user_to_update_is_teamlead = view["state"]["values"]['update_user_is_teamlead_block']['update_user_is_teamlead']['selected_option']['value']
    user_to_update_is_admin = view["state"]["values"]['update_user_is_admin_block']['update_user_is_admin']['selected_option']['value']
    user_to_update_monthly_coins_for_share = view["state"]["values"]['update_user_monthly_coins_for_share_block']['update_user_monthly_coins_for_share']['value']
    db_data=DbData(mysql_cn)
    users_list=db_data.get_users_list()
    errors={}
    if user_to_update_id not in users_list:
        errors["update_user_select_user_block"] = f"This user doesn't have YourCompanyCoin account yet. Please, add user to app." 
    if (not user_to_update_monthly_coins_for_share.isdigit()) and user_to_update_monthly_coins_for_share!="-":
        errors["update_user_monthly_coins_for_share_block"] = "Please, enter an integer"
    if len(errors)>0:
        ack(response_action="errors", errors=errors)
    else:
        ack()
        team_id=db_data.get_user_info(user_to_update_id).get_team_id()
        is_teamlead=db_data.get_user_info(user_to_update_id).is_teamlead()
        is_admin=db_data.get_user_info(user_to_update_id).is_admin()
        monthly_coins_for_share=db_data.get_user_info(user_to_update_id).get_monthly_coins_for_share()
        if user_to_update_team_id=="-":
            user_to_update_team_id=str(team_id)
        if user_to_update_is_teamlead=="-":
            user_to_update_is_teamlead=str(is_teamlead)
        if user_to_update_is_admin=="-":
            user_to_update_is_admin=str(is_admin)
        if user_to_update_monthly_coins_for_share=="-":
            user_to_update_monthly_coins_for_share=str(monthly_coins_for_share)
        warning=''
        if is_teamlead == 1 and (user_to_update_is_teamlead == "0" or (user_to_update_team_id != team_id)):
            warning=f' WARNING: You removed the teamlead of {team_id} team. Check if there is another teamlead'
        if user_to_update_is_teamlead == "1" and (is_teamlead == 0 or (user_to_update_team_id != team_id)):
            warning=f' WARNING: You added the teamlead to {user_to_update_team_id} team. Check if there is another teamlead'
        try:
            response=update_user(client,mysql_cn,user_id,user_to_update_id,user_to_update_team_id,user_to_update_is_teamlead,user_to_update_is_admin,user_to_update_monthly_coins_for_share)
            if response=='ok':
                msg = f"""User <@{user_to_update_id}> has been updated successfully!"""+warning
            if response=='error':
                msg = "Something went wrong during update. :sad_pepe: Please, try again later or contact developer."
        except Exception as e:
            print('APP.PY ERROR: '+ str(e))
            msg = "Something went wrong during update. :sad_pepe: Please, try again later or contact developer."
        client.chat_postMessage(channel=user_id, text=msg)

@app.view("delete_user_modal")
def view_submission(ack, body, client, view):
    user_id = body["user"]["id"]
    user_to_delete_id = view["state"]["values"]['delete_user_select_user_block']['delete_user_select_user']['selected_user']
    db_data=DbData(mysql_cn)
    users_list=db_data.get_users_list()
    errors={}
    if user_to_delete_id not in users_list:
        errors["delete_user_select_user_block"] = f"This user doesn't have YourCompanyCoin account yet. Please, add user to app." 
    if len(errors)>0:
        ack(response_action="errors", errors=errors)
    else:
        ack()
        team_id=db_data.get_user_info(user_to_delete_id).get_team_id()
        teamleads_list=db_data.get_team_teamleads_list(team_id)
        warning=''
        if user_to_delete_id in teamleads_list:
            warning=f' WARNING: You have deleted the teamlead of {team_id} team. Check if there is another teamlead'
        try:
            response=delete_user(client,mysql_cn,user_id,user_to_delete_id)
            if response=='ok':
                msg = f"""User <@{user_to_delete_id}> has been deleted successfully!"""+warning
            if response=='error':
                msg = "Something went wrong during deletion. :sad_pepe: Please, try again later or contact developer."
        except Exception as e:
            print('APP.PY ERROR: '+ str(e))
            msg = "Something went wrong during deletion. :sad_pepe: Please, try again later or contact developer."
        client.chat_postMessage(channel=user_id, text=msg)

@app.view("add_team_modal")
def view_submission(ack, body, client, view):
    user_id = body["user"]["id"]
    new_team_id = view["state"]["values"]['add_team_enter_team_block']['add_team_enter_team']['value']
    monthly_transfer = view["state"]["values"]['add_team_enter_monthly_transfer_block']['add_team_enter_monthly_transfer']['value']
    db_data=DbData(mysql_cn)
    teams_list=db_data.get_teams_list()
    errors={}
    if new_team_id in teams_list:
        errors["add_team_enter_team_block"] = f"This team has already YourCompanyCoin account."
    if not monthly_transfer.isdigit():
        errors["add_team_enter_monthly_transfer_block"] = "Please, enter an integer"
    if len(errors)>0:
        ack(response_action="errors", errors=errors)
    else:
        ack()
        try:
            response=add_team(client,mysql_cn,user_id,new_team_id,int(monthly_transfer))
            if response=='ok':
                msg = f"""New team "{new_team_id}" has been added to YourCompanyCoin successfully! :rocket_ch:"""
            if response=='error':
                msg = "Something went wrong while adding a team. :sad_pepe: Please, try again later or contact developer."
        except Exception as e:
            print('APP.PY ERROR: '+ str(e))
            msg = "Something went wrong while adding a team. :sad_pepe: Please, try again later or contact developer."
        client.chat_postMessage(channel=user_id, text=msg)

@app.view("update_team_modal")
def view_submission(ack, body, client, view):
    user_id = body["user"]["id"]
    team_to_update_id = view["state"]["values"]['update_team_select_team_block']['update_team_select_team']['selected_option']['value']
    team_to_update_monthly_transfer = view["state"]["values"]['update_team_enter_monthly_transfer_block']['update_team_enter_monthly_transfer']['value']
    errors={}
    if not team_to_update_monthly_transfer.isdigit():
        errors["update_team_enter_monthly_transfer_block"] = "Please, enter an integer"
    if len(errors)>0:
        ack(response_action="errors", errors=errors)
    else:
        ack()
        try:
            response=update_team(client,mysql_cn,user_id,team_to_update_id,team_to_update_monthly_transfer)
            if response=='ok':
                msg = f"""Team "{team_to_update_id}" has been updated successfully!"""
            if response=='error':
                msg = "Something went wrong during update. :sad_pepe: Please, try again later or contact developer."
        except Exception as e:
            print('APP.PY ERROR: '+ str(e))
            msg = "Something went wrong during update. :sad_pepe: Please, try again later or contact developer."
        client.chat_postMessage(channel=user_id, text=msg)
        
@app.view("delete_team_modal")
def view_submission(ack, body, client, view):
    user_id = body["user"]["id"]
    team_to_delete_id = view["state"]["values"]['delete_team_select_team_block']['delete_team_select_team']['selected_option']['value']
    db_data=DbData(mysql_cn)
    team_users_list=db_data.get_team_users_list(team_to_delete_id)
    errors={}
    if len(team_users_list)>0:
        errors["delete_team_select_team_block"] = f"There are still users in this team. Delete or update users first"
    if len(errors)>0:
        ack(response_action="errors", errors=errors)
    else:
        ack()
        try:
            response=delete_team(client,mysql_cn,user_id,team_to_delete_id)
            if response=='ok':
                msg = f"""Team "{team_to_delete_id}" has been deleted successfully!"""
            if response=='error':
                msg = "Something went wrong during deletion. :sad_pepe: Please, try again later or contact developer."
        except Exception as e:
            print('APP.PY ERROR: '+ str(e))
            msg = "Something went wrong during deletion. :sad_pepe: Please, try again later or contact developer."
        client.chat_postMessage(channel=user_id, text=msg)

@app.view("view_purchases_modal")
def view_submission(ack):
    ack()

@app.view("update_items_modal")
def view_submission(ack, body, client):
    user_id = body["user"]["id"]
    ack()
    try:
        response=update_items(mysql_cn,user_id)
        if response=='ok':
            msg = f"""Merch list has been updated successfully! :rocket_ch:"""
        if response=='error':
            msg = "Something went wrong during update merch list. :sad_pepe: Please, try again later or contact developer."
    except Exception as e:
        print('APP.PY ERROR: '+ str(e))
        msg = "Something went wrong during update merch list. :sad_pepe: Please, try again later or contact developer."
    client.chat_postMessage(channel=user_id, text=msg)

@app.view("make_refund_modal")
def view_submission(ack, body, client, view):
    user_id = body["user"]["id"]
    receiver_id = view["state"]["values"]['make_refund_select_user_block']['make_refund_select_user']['selected_user']
    amount = view["state"]["values"]['make_refund_enter_amount_block']['make_refund_enter_amount']['value']
    comment = view["state"]["values"]['make_refund_enter_comment_block']['make_refund_enter_comment']['value']
    db_data=DbData(mysql_cn)
    users_list=db_data.get_users_list()
    errors={}
    if receiver_id not in users_list:
        errors["make_refund_select_user_block"] = f"This user doesn't have YourCompanyCoin account yet."
    elif receiver_id==user_id:
        errors["make_refund_select_user_block"] = f"You can't transfer coins to yourself"
    if not amount.isdigit():
        errors["make_refund_enter_amount_block"] = "Please, enter an integer"
    if len(errors)>0:
         ack(response_action="errors", errors=errors)
    else:
        ack()
        try:
            response,transfer_id=make_refund(client,mysql_cn,user_id,receiver_id,int(amount),comment)
            if response=='ok':
                msg = f"""Your transfer went smoothly. Transfer id is {transfer_id}"""
            if response=='error':
                msg = "There was an error with your transfer. Please, try again later or contact developer"
        except Exception as e:
            print('APP.PY ERROR: '+ str(e))
            msg = "There was an error with your transfer. Please, try again later or contact developer"
        client.chat_postMessage(channel=user_id, text=msg)

#IN-MODAL INTERACTIONS
@app.action("add_user_link_button")
def add_user_link_button_click(ack, body, respond):
    ack() 

@app.action("update_user_link_button")
def update_user_link_button_click(ack, body, respond):
    ack() 
    
@app.action("delete_user_link_button")
def delete_user_link_button_click(ack, body, respond):
    ack() 
    
@app.action("add_team_link_button")
def add_team_link_button_click(ack, body, respond):
    ack() 

@app.action("update_team_link_button")
def update_team_link_button_click(ack, body, respond):
    ack()
    
@app.action("delete_team_link_button")
def delete_team_link_button_click(ack, body, respond):
    ack()  
    
@app.action("view_purchases_link_button")
def view_purchases_link_button_click(ack, body, respond):
    ack()  
    
@app.action("update_items_link_button")
def update_items_link_button_click(ack, body, respond):
    ack()  


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
