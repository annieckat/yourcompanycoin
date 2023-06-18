import pymysql
import pandas as pd

class DbData:
    
    def __init__(self,mysql_cn):
        self.cn=mysql_cn
        self.cn.ping(reconnect=True)

    def get_user_info(self,user_id):
        return(self.User(self,user_id))

    class User:
        def __init__(self,outer_self,user_id):
            self.outer_self=outer_self
            self.user_id=user_id

        def get_fuc_balance(self):
            fuc_balance=pd.read_sql(f"""select free_use_coins from accounts where user_id='{self.user_id}'""",con=self.outer_self.cn)['free_use_coins'][0]
            return(int(fuc_balance))

        def get_cfs_balance(self):
            cfs_balance=pd.read_sql(f"""select coins_for_share from accounts where user_id='{self.user_id}'""",con=self.outer_self.cn)['coins_for_share'][0]
            return(int(cfs_balance))
        
        def is_teamlead(self):
            is_teamlead=pd.read_sql(f"""select is_teamlead from users where user_id='{self.user_id}'""",con=self.outer_self.cn)['is_teamlead'][0]
            return(is_teamlead)

        def is_admin(self):
            is_admin=pd.read_sql(f"""select is_admin from users where user_id='{self.user_id}'""",con=self.outer_self.cn)['is_admin'][0]
            return(is_admin)

        def get_external_transfers(self):
            external_transfers=pd.read_sql(f"""select 
                (case when comment is not null then concat(created_at,type,amount,subtype,' (comment: ',comment,')') 
                else concat(created_at,type,amount,subtype) end) as transfer
                from
                (select 
                created_at,
                (case when sender_account_id='user:{self.user_id}' then ' :heavy_minus_sign: ' else ' :heavy_plus_sign: ' end) as type,
                (case 
                when sender_account_id='user:{self.user_id}' then concat('to: <@',replace(receiver_account_id,'user:',''),'>')
                when sender_account_id like 'user:%' then concat('from: <@',replace(sender_account_id,'user:',''),'>') 
                when sender_account_id like 'team:%' then 'from: Team'
                when transfer_type='tech_scheduled' and receiver_subaccount_type='free_use_coins' then 'from: Tech Scheduled (free-use)'
                when transfer_type='tech_scheduled' and receiver_subaccount_type='coins_for_share' then 'from: Tech Scheduled (for-share)'
                when transfer_type='refund' then 'from: Tech Refund'
                else concat('from: ',sender_account_id) end) as subtype,
                concat('*',coins_sent,'* :dollar: ') as amount,
                comment
                from external_transfers 
                where sender_account_id='user:{self.user_id}' or receiver_account_id='user:{self.user_id}') as q
                order by created_at desc limit 25""",con=self.outer_self.cn)
            external_transfers=['• '+transfer[1] for transfer in list(external_transfers.to_records())]
            return(external_transfers)

        def get_purchases(self):
            purchases=pd.read_sql(f"""
            select concat('*(',purchase_id,')* ',created_at,' :heavy_minus_sign: *',item_cost,'* :dollar: ',' for *',item_name,'*') as purchase
            from purchases
            where account_id='user:{self.user_id}'
            order by created_at desc limit 25
            """,con=self.outer_self.cn)
            purchases=['• '+purchase[1] for purchase in list(purchases.to_records())]
            return(purchases)

        def get_team_id(self):
            team_id=pd.read_sql(f"""select team_id from users where user_id='{self.user_id}'""",con=self.outer_self.cn)['team_id'][0]
            return(team_id)
        
        def get_monthly_coins_for_share(self):
            monthly_coins_for_share=pd.read_sql(f"""select monthly_coins_for_share from users where user_id='{self.user_id}'""",con=self.outer_self.cn)['monthly_coins_for_share'][0]
            return(monthly_coins_for_share)

    def get_users_list(self):
        users_list=list(pd.read_sql("""SELECT user_id FROM users where is_deleted=0""",con=self.cn)['user_id'])
        return(users_list)

    def get_admins_list(self):
        admins_list=list(pd.read_sql("""SELECT user_id FROM users where is_admin=1 and is_deleted=0""",con=self.cn)['user_id'])
        return(admins_list)

    def get_teams_list(self):
        teams_list=list(pd.read_sql("""SELECT team_id FROM teams where is_deleted=0""",con=self.cn)['team_id'])
        return(teams_list)

    def get_merch_items_df(self):
        merch_items_df=pd.read_sql("""SELECT * FROM items order by item_id""",con=self.cn)
        return(merch_items_df)

    def get_merch_item_cost(self,item_id):
        item_cost=pd.read_sql(f"""select item_cost from items where item_id={item_id}""",con=self.cn)['item_cost'][0]
        return(item_cost)

    def get_team_balance(self,team_id):
        team_balance=pd.read_sql(f"""select coins_for_share from accounts where team_id='{team_id}'""",con=self.cn)['coins_for_share'][0]
        return(int(team_balance))

    def get_team_transfers(self,team_id):
        external_transfers=pd.read_sql(f"""select 
                (case when comment is not null then concat(created_at,type,amount,subtype,' (comment: ',comment,')') 
                else concat(created_at,type,amount,subtype) end) as transfer
                from
                (select 
                created_at,
                (case when sender_account_id='team:{team_id}' then ' :heavy_minus_sign: ' else ' :heavy_plus_sign: ' end) as type,
                (case 
                when sender_account_id='team:{team_id}' then concat('to: <@',replace(receiver_account_id,'user:',''),'>')
                when sender_account_id like 'user:%' then concat('from: <@',replace(sender_account_id,'user:',''),'>') 
                when transfer_type='tech_scheduled' then 'from: Tech Scheduled'
                when transfer_type='tech_refund' then 'from: Tech Refund'
                else concat('from: ',sender_account_id) end) as subtype,
                concat('*',coins_sent,'* :dollar: ') as amount,
                comment
                from external_transfers 
                where sender_account_id='team:{team_id}' or receiver_account_id='team:{team_id}') as q
                order by created_at desc limit 25""",con=self.cn)
        external_transfers=['• '+transfer[1] for transfer in list(external_transfers.to_records())]
        return(external_transfers)

    def get_team_users_list(self,team_id):
        users_list=list(pd.read_sql(f"""SELECT user_id FROM users where team_id='{team_id}'""",con=self.cn)['user_id'])
        return(users_list)

    def get_team_teamleads_list(self,team_id):
        teamleads_list=list(pd.read_sql(f"""SELECT user_id FROM users where team_id='{team_id}' and is_teamlead = 1""",con=self.cn)['user_id'])
        return(teamleads_list)

    def get_team_monthly_transfer(self,team_id):
        monthly_transfer=pd.read_sql(f"""SELECT monthly_transfer FROM teams where team_id='{team_id}'""",con=self.cn)['monthly_transfer'][0]
        return(int(monthly_transfer))

    def get_all_purchases(self):
        purchases=pd.read_sql(f"""
        select concat('*(',purchase_id,')* ',created_at,' :heavy_minus_sign: *',item_cost,'* :dollar: ',' paid <@',replace(account_id,'user:',''),'> for *',item_name,'*') as purchase
        from purchases
        order by created_at desc limit 25
        """,con=self.cn)
        purchases=['• '+purchase[1] for purchase in list(purchases.to_records())]
        return(purchases)
