#'''CREATE SCHEMA yourcorpcoin DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'''
import os
import pygsheets
import numpy as np
import pandas as pd
import pymysql
import datetime
from class_services_connector import ServicesConnector

mysql_cn=ServicesConnector().mysql_connect()

def fill_db(mysql_cn):
    #VARIABLES AND FUNCTIONS
    CURRENT_TIMESTAMP=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    def stream_to_db(df,table_,insert_type):
        try:
            columns=str(df.columns.to_list()).replace("'","").replace("[","").replace("]","")
            columns_mapping=('%s, '*len(df.columns))[:-2]
            sql_insert =f'''{insert_type} INTO {ServicesConnector().DB_NAME}.{table_} ({columns})
                    VALUES ({columns_mapping})'''
            data_to_insert = [tuple(x) for x in df.values]
            mycursor.executemany(sql_insert, data_to_insert)
        except Exception as e:
            print(f'{insert_type} Error {table_}: '+str(e))

    #####CREATE CONNECTION WITH AUTOCOMMIT
    mycursor = mysql_cn.cursor()

    #DELETE TABLES
    mycursor.execute('''DROP TABLE IF EXISTS yourcorpcoin.purchases''')
    mycursor.execute('''DROP TABLE IF EXISTS yourcorpcoin.items''')
    mycursor.execute('''DROP TABLE IF EXISTS yourcorpcoin.internal_transfers''')
    mycursor.execute('''DROP TABLE IF EXISTS yourcorpcoin.external_transfers''')
    mycursor.execute('''DROP TABLE IF EXISTS yourcorpcoin.accounts''')
    mycursor.execute('''DROP TABLE IF EXISTS yourcorpcoin.users''')
    mycursor.execute('''DROP TABLE IF EXISTS yourcorpcoin.teams''')

    #CREATE TABLES
    create_teams_query='''
    CREATE TABLE yourcorpcoin.teams (
        team_id varchar(20) NOT NULL,
        monthly_transfer FLOAT NOT NULL,
    	created_at DATETIME NOT NULL,
    	updated_at DATETIME NOT NULL,
        is_deleted TINYINT DEFAULT 0 NOT NULL,
     CONSTRAINT NewTable_PK PRIMARY KEY (team_id)
    )
    ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4
    COLLATE=utf8mb4_unicode_ci
    '''
    create_users_query='''
    CREATE TABLE yourcorpcoin.users (
    	user_id varchar(30) NOT NULL,
    	user_name varchar(50) NULL,
    	team_id varchar(20) NOT NULL,
    	is_teamlead TINYINT DEFAULT 0 NOT NULL,
    	is_admin TINYINT DEFAULT 0 NOT NULL,
        monthly_coins_for_share INT DEFAULT 100 NOT NULL,
    	created_at DATETIME NOT NULL,
    	updated_at DATETIME NOT NULL,
        is_deleted TINYINT DEFAULT 0 NOT NULL,
    	CONSTRAINT users_PK PRIMARY KEY (user_id),
    	CONSTRAINT users_FK FOREIGN KEY (team_id) REFERENCES yourcorpcoin.teams(team_id)
    )
    ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4
    COLLATE=utf8mb4_unicode_ci
    '''
    create_accounts_query='''
    CREATE TABLE yourcorpcoin.accounts (
    	account_id varchar(50) NOT NULL,
    	account_type varchar(10) NOT NULL,
    	user_id varchar(30) NULL,
    	team_id varchar(20) NULL,
    	coins_for_share FLOAT NULL,
    	free_use_coins FLOAT NULL,
    	updated_at DATETIME NOT NULL,
    	CONSTRAINT accounts_PK PRIMARY KEY (account_id),
    	CONSTRAINT accounts_FK FOREIGN KEY (user_id) REFERENCES yourcorpcoin.users(user_id),
    	CONSTRAINT accounts_FK_1 FOREIGN KEY (team_id) REFERENCES yourcorpcoin.teams(team_id),
        CONSTRAINT cfs_null_or_positive CHECK ((coins_for_share>=0 or coins_for_share is null)),
        CONSTRAINT fuc_null_or_positive CHECK ((free_use_coins>=0 or free_use_coins is null))
    )
    ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4
    COLLATE=utf8mb4_unicode_ci
    '''

    create_external_transfers_query='''
    CREATE TABLE yourcorpcoin.external_transfers (
    	external_transfer_id INT auto_increment NOT NULL,
    	sender_account_id varchar(50) NOT NULL,
    	receiver_account_id varchar(50) NOT NULL,
        receiver_subaccount_type varchar(20) NOT NULL,
    	transfer_type varchar(20) NOT NULL,
    	coins_sent FLOAT NOT NULL,
    	created_at DATETIME NOT NULL,
    	comment varchar(200) NULL,
    	CONSTRAINT external_transfers_PK PRIMARY KEY (external_transfer_id),
    	CONSTRAINT external_transfers_FK FOREIGN KEY (sender_account_id) REFERENCES yourcorpcoin.accounts(account_id),
    	CONSTRAINT external_transfers_FK_1 FOREIGN KEY (receiver_account_id) REFERENCES yourcorpcoin.accounts(account_id)
    )
    ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4
    COLLATE=utf8mb4_unicode_ci;
    '''
    create_internal_transfers_query='''
    CREATE TABLE yourcorpcoin.internal_transfers (
    	internal_transfer_id INT auto_increment NOT NULL,
    	account_id varchar(50) NOT NULL,
    	coins_sent FLOAT NOT NULL,
    	created_at DATETIME NOT NULL,
    	CONSTRAINT internal_transfers_PK PRIMARY KEY (internal_transfer_id),
    	CONSTRAINT internal_transfers_FK FOREIGN KEY (account_id) REFERENCES yourcorpcoin.accounts(account_id)
    )
    ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4
    COLLATE=utf8mb4_unicode_ci;
    '''
    create_items_query='''
    CREATE TABLE yourcorpcoin.items (
    	item_id INT auto_increment NOT NULL,
    	item_name varchar(200) NOT NULL,
    	item_cost FLOAT NOT NULL,
    	CONSTRAINT items_PK PRIMARY KEY (item_id)
    )
    ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4
    COLLATE=utf8mb4_unicode_ci;
    '''
    create_purchases_query='''
    CREATE TABLE yourcorpcoin.purchases (
    	purchase_id INT auto_increment NOT NULL,
    	account_id varchar(50) NOT NULL,
    	item_cost FLOAT NOT NULL,
        item_name varchar(200) NOT NULL,
    	created_at DATETIME NOT NULL,
        status varchar(20) DEFAULT 'waiting' NOT NULL,
    	CONSTRAINT purchases_PK PRIMARY KEY (purchase_id),
    	CONSTRAINT purchases_FK FOREIGN KEY (account_id) REFERENCES yourcorpcoin.accounts(account_id)
    )
    ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4
    COLLATE=utf8mb4_unicode_ci;
    '''
    mycursor.execute(create_teams_query)
    mycursor.execute(create_users_query)
    mycursor.execute(create_accounts_query)
    mycursor.execute(create_external_transfers_query)
    mycursor.execute(create_internal_transfers_query)
    mycursor.execute(create_items_query)
    mycursor.execute(create_purchases_query)
    mysql_cn.commit()

    #FILL TEAMS AND USERS TABLES 
    gs_cn=ServicesConnector().gs_connect()

    sh = gs_cn.open_by_key(os.environ.get('SPREADSHEETS_USERS_FILE'))
    wk=sh.worksheet('title','teams')
    teams = wk.get_as_df(has_header=True)
    wk=sh.worksheet('title','users')
    users = wk.get_as_df(has_header=True)

    sh = gs_cn.open_by_key(os.environ.get('SPREADSHEETS_MERCH_FILE'))
    wk=sh.worksheet('title','items')
    items = wk.get_as_df(has_header=True)

    teams['created_at']=CURRENT_TIMESTAMP
    teams['updated_at']=CURRENT_TIMESTAMP
    users['created_at']=CURRENT_TIMESTAMP
    users['updated_at']=CURRENT_TIMESTAMP

    stream_to_db(teams,'teams','INSERT')
    stream_to_db(users,'users','INSERT')
    stream_to_db(items,'items','INSERT')

    #FILL ACCOUNTS AND EXTERNAL_TRANSFERS TABLES
    try:
        mycursor.execute('''
        set @current_datetime=UTC_TIMESTAMP()
        ''')
        mycursor.execute('''
        insert into accounts (account_id,account_type,user_id,team_id,coins_for_share,free_use_coins,updated_at)
        (select concat('user:',user_id) as account_id,'user' as account_type,user_id,null as team_id,
        monthly_coins_for_share as coins_for_share,100 as free_use_coins,@current_datetime as updated_at from users)
        union all
        (select concat('team:',team_id) as account_id,'team' as account_type,null as user_id,team_id,
        monthly_transfer as coins_for_share,null as free_use_coins,@current_datetime as updated_at from teams)
        union all
        (select 'tech' as account_id,'tech' as account_type,null as user_id,null as team_id,
        null as coins_for_share,null as free_use_coins,@current_datetime as updated_at)
        ''')
        mycursor.execute('''
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
        monthly_transfer as coins_sent,@current_datetime as created_at from teams)
        ''')
    except Exception as e:
        print(f'Create and fill accounts error: '+str(e))
        mysql_cn.rollback()
        mycursor.close()
        return('error')
    mysql_cn.commit()
    mycursor.close()
    print('Successfully finished initial db fill')
    return('success')

fill_db(mysql_cn)
mysql_cn.close()
