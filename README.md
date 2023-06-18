# YourCorpCoin
Slack app that introduces your company's local currency that can be exchanged between workspace members, handed out as a reward by teamleads and used to buy merchandise. 

## Basic idea
Every user has 2 accounts: coins-for-share account and free-use-coins account. Also, every team has coins-for-share account. Each account is replenished monthly (unused coins can be saved). Users can transfer coins to each other as gifts or as a way of saying thank you. Coins can be transferred from any account but only free-use-coins account can be used to buy merch. Team coins can be distributed between team members by teamlead. When user receives coins from other user or team account they go to free-use-coins account, that way sharing is encouraged.

The app can execute different commands depending on user's permission level. There are 3 permission levels: user permission, teamlead permission and admin permission. All users can share coins and buy merchandise, teamleads can share team coins, admins can update users, teams and merchandise data and make refunds.

## Tech description
The app infrastructure consists of:
* **MySQL database** - It should be created and filled before deployment of the app. It stores data about:
    *  **App users** (your workspace members that are entered into the system), their info and permissions
    *  **Users and teams accounts** and their balances
    *  **Transfers** between users and between different accounts of one user
    *  **Avalaible merch items** (changes in merch items list are not written, db keeps only actual list of available items)
    *  **Merchandise purchases history**
    *  **MySQL Procedure monthly_transfer**
    *  **MySQL Event trigger_monthly_transfer**
* **Slack app** - You should create an app with several permissions (it can view members of a workspace, write and read messages in the chats it is added to). When you deploy the service, your app will have a home page with several command buttons (buttons visibility depend on the permissions of the user). When user clicks the buttons slack sends a request to the app. 
* **Google Drive Folder** Before deploying the service you should create a google drive folder with two docs that will be used as a part of YourCorpCoin interface to handle more complicated data. There should be a file with users and teams data (should contain all the initial users data and should be updated by the app only) and a file with merchandise and purchases data (is supposed to be used by YourCorpCoin admins to update merch items and keep track of the users purchases). You can see the example here: https://drive.google.com/drive/u/0/folders/1RmdJUItkQOpkYVbpFZ1yciVt_uUgVO9x

## Tech requirements
* The app should be run with **3.7.4 python**
* The app should be permanenty available for slack requests
* **MySQL DB** schema should be created (app was tested on 8.0.26 MySQL version) - `CREATE SCHEMA yourcorpcoin DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`
* <details>
        <summary><strong>MySQL Procedure monthly_transfer</strong> should be created in db after app launch (expand to view query)</summary>
        <code>
        CREATE PROCEDURE monthly_transfer() 
        BEGIN
        START TRANSACTION;
        set @current_datetime=UTC_TIMESTAMP();
        update accounts left join users using (user_id)
        set accounts.coins_for_share=coins_for_share+monthly_coins_for_share, free_use_coins=free_use_coins+100, accounts.updated_at=@current_datetime
         where account_type='user';
        update accounts left join teams using (team_id)
        set accounts.coins_for_share=coins_for_share+monthly_transfer, accounts.updated_at=@current_datetime
        where account_type='team';
        insert into external_transfers (sender_account_id,receiver_account_id,receiver_subaccount_type,transfer_type,coins_sent,created_at)
        (select 'tech' as sender_account_id, concat('user:',user_id) as receiver_account_id,
        'coins_for_share' as receiver_subaccount_type,'tech_scheduled' as transfer_type, 
        monthly_coins_for_share as coins_sent, @current_datetime as created_at
        from users)
        union all
        (select 'tech' as sender_account_id, concat('user:',user_id) as receiver_account_id,
        'free_use_coins' as receiver_subaccount_type,'tech_scheduled' as transfer_type, 
        100 as coins_sent, @current_datetime as created_at
        from users)
        union all
        (select 'tech' as sender_account_id, concat('team:',team_id) as receiver_account_id,
        'coins_for_share' as receiver_subaccount_type,'tech_scheduled' as transfer_type,
        monthly_transfer as coins_sent,@current_datetime as created_at from teams);
        COMMIT;
        END</code>
        </details>
* <details>
        <summary><strong>MySQL Event trigger_monthly_transfer</strong> should be created in db after app launch (expand to view query)</summary>
        <code>
        CREATE EVENT trigger_monthly_transfer
        ON SCHEDULE EVERY 1 MONTH
        STARTS '2022-12-01 00:30:00.000'
        ON COMPLETION NOT PRESERVE
        ENABLE
        DO call monthly_transfer()</code>
        </details>
* App consists of:
    * **app.py** - main script that receives slack requests (should run permanently)
    * **additional scripts** that are imported and used by app.py - all the scripts starting with "class\_" (main app classes), "func\_" (separate functions that run transactions and update db data) or "view\_" (render different screens that app shows to users)
    * **\_initial\_db\_fill.py** script that should be run before launch of app.py. It creates tables in DB and fills them with initial data from google spreadsheet files.
    * **{YOUR_FILE_NAME}.json** - file with google service account credentials (that have access to google spreadsheet files)
    * **requirements.txt** - file with required python libraries list. They can be installed with following command `pip3 install -r requirements.txt`

## Local variables
Script uses some local variables that should be created (unknown values or values that contain credentials are not specified):
* SERVICE_ACCOUNT_FILE_ADDRESS="{YOUR_FILE_NAME}.json"
* DB_HOST=
* DB_NAME=
* DB_USER=
* DB_PASSWRD=
* SLACK_BOT_TOKEN=
* SLACK_SIGNING_SECRET=
* SPREADSHEETS_USERS_FILE="{ID_OF_SPREADSHEETS_USERS_FILE}" #you can get it from the spreadsheet url (example doc id: 1gjtSXamJXt8OKtjssoyN7AfXKLnmnu99t4uWdl54TWU)
* SPREADSHEETS_MERCH_FILE="{ID_OF_SPREADSHEETS_MERCH_FILE}" #you can get it from the spreadsheet url (example doc id: 1gm8Y-CLm-IPGNdgKiK_RA5Vk30ivRMyNveQMjltTNHk)
* ERRORS_CHANNEL_ID="{ERRORS_SLACK_CHANNEL_ID}"
* DEVELOPERS_SLACK_MENTION="<@{DEV_SLACK_ID}>"


