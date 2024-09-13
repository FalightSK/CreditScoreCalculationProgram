import pandas as pd
import os
import numpy as np
import datetime
import Script.databaseClient as db
from Script.customerInfo import order, extract_fin_info, read_financial_file, PaymentInfo
from currentCustomer import cal_FICO_current, cal_final_FICO_score


# def set_date(dmy):
#     return (dmy[2], dmy[1], dmy[0])
    


doc = pd.read_excel(r"D:\KMITL\KMITL\Year 03 - 01\Prompt Engineer\Work\08_08_2024_Project\Data\Original Data\Merged_Transaction_Data_with_Customer_Type.xlsx")
doc.fillna('UNKNOWN', inplace= True)
# doc2 = pd.read_excel()

############ Upload data structure
def upload_data_struct():
    prev_id = ''
    prev_cus_id = ''
    users = {}
    for i, row in enumerate(doc.iloc()):
        local_data = order.copy()
        if row['Transaction Status'] != 'สำเร็จ' or row['Transaction Value'] in [0, 'UNKNOWN']:
            continue
        
        trans_id = row['Transaction ID']
        customer_id = row['Customer ID']
        
        if customer_id != prev_cus_id:
            prev_cus_id = customer_id
            
            users[customer_id] = {
                'customer_id': customer_id,
                'type': row['Type Of Customer'],
                'credit_score': None,
                'credit_budget': 17000,
                'credit_terms': 15,
                'financial_info': [],
                'record_summary': {
                    'mean': None,
                    'std': None,
                    'n': None
                }, 
                'records': {}
            }
            
        if trans_id != prev_id:
            print(trans_id)
            prev_id = trans_id
            local_data['ID'] = trans_id
            local_data['amount'] = row['Transaction Value']
            
            local_data['order_date'] = [int(j) for j in row['Transaction Date'].split('/')]
            # print(local_data['order_date'])
            
            try:
                local_data['paid_date'] = [int(j) for j in row['Payment Date'].split()[0].split('/')]
            except:
                local_data['paid_date'] = None
            
            local_stat = row['Payment Status']
            if local_stat == 'ชำระครบ':
                local_stat = 'FULL'
            elif local_stat == 'ชำระบางส่วน':
                local_stat = 'PARTIAL'
            elif local_stat == 'รอการชำระเงิน':
                local_stat = 'OVERDUE'
            else:
                continue
            local_data['stat'] = local_stat
            
            local_method = row['Payment Method'] 
            local_data['method'] = 'CASH' if local_method == 'เงินสด' else 'IN_STORE' if local_method == 'หน้าร้าน' else 'CREDIT_CARD' if local_method == "รอตัด" or local_method == "เครื่องรูดบัตร" else 'OTHERS'
            
            users[customer_id]['records'][trans_id] = local_data
        

    users = dict(sorted(users.items()))
    database = {
        'history': users,
        'summary': None
    }        

    db.save(database)


############ Upload record summary
def upload_record_sum():
    database = db.read()['history']

    type_shop_list = {}

    for key, val in database.items():
        value_list = []
        # print(key)
        
        for order_id, order in val['records'].items():
            # print(order)
            if order['stat'] == 'FULL': value_list.append(order['amount'])
            
            if val['type'] in type_shop_list:
                type_shop_list[val['type']].append(order['amount'])
            else:
                type_shop_list[val['type']] = [order['amount']]
        
        if len(value_list) == 0:
            database[key]['record_summary'] = {
                'mean': None,
                'std': None,
                'n': 0
            }
        else:   
            database[key]['record_summary'] = {
                'mean': np.mean(value_list),
                'std': np.std(value_list),
                'n': len(value_list)
            }

    new_database = {
        'history': database,
        'summary': {}
    }        

    # print(type_shop_list)
    for key, val in type_shop_list.items():
        new_database['summary'][key] = {
            'mean': np.mean(val),
            'std': np.std(val),
            'n': len(val)
        }
        
    print(new_database['summary'])

    db.save(new_database)


############ Upload financial record
def upload_fin_record():
    database = db.read()['history']

    path = r'D:\KMITL\KMITL\Year 03 - 01\Prompt Engineer\Work\08_08_2024_Project\Data\Original Data\financial data'
    for dir in os.listdir(path):
        target = os.path.join(path, dir)
        try:
            doc1 = read_financial_file(os.path.join(target, f'Financial Position {dir}.xlsx'))
            doc2 = read_financial_file(os.path.join(target, f'Income Statement {dir}.xlsx'))
        except:
            print(dir)
        
        # print(doc1)
        if dir not in database:
            print(dir)
            continue
        
        data = extract_fin_info(doc1, doc2)
        database[dir]['financial_info'] = []
        for datum in data:
            database[dir]['financial_info'].append({
                'total_assets': datum.total_assets,
                'current_assets': datum.current_assets,
                'total_liabilities': datum.total_liabilities,
                'total_revenue': datum.total_revenue,
                'shareholder_equity': datum.shareholder_equity
            })
        print(database[dir]['financial_info'])

    print('\n\n', database)
    new_database = {
        'history': database,
        'summary': db.read()['summary']
    }        

    db.save(new_database)


############ Upload credit_history_criteria
def upload_cred_criteria():
    database = db.read()

    new_database = {
        'history': database['history'],
        'summary': database['summary'],
        'credit_history_criteria': {
            'Fleet': [25000, 6],
            'Garage': [4000, 2],
            'Tyre Shop': [47000, 4],
            'Used Car Dealer': [22000, 6]
        }
    }    

    db.save(new_database)


############ Update credit score
def upload_local_credit_score():
    database = db.read()
    
    ## update specific person
    # for i_order, order in enumerate(database['history']['50083']['records']):
        
    #     requested_budget = order['amount']
    #     payment_info = PaymentInfo()
    #     payment_info.JSON_to_PaymentInfo(order)
    #     # payment_info.show()
    #     FICO = round(cal_FICO_current('50083', payment_info, requested_budget, set_n= i_order+1, show= False), 3)
    #     database['history']['50083']['records'][i_order]['local_credit_score'] = FICO
    #     print(f'({i_order} - {FICO})', end=' ')
    
    
    for user, val in database['history'].items():
        print('\n', val['customer_id'])

        n_record = len(val['records'])
        for i_order, (order_id, order) in enumerate(val['records'].items()):
            requested_budget = order['amount']
            payment_info = PaymentInfo()
            payment_info.JSON_to_PaymentInfo(order)
            
            
            FICO, FICO_info = cal_FICO_current(user, payment_info, requested_budget, set_n= n_record-i_order, show= False)
            FICO = round(FICO, 3)
            database['history'][user]['records'][order_id]['local_credit_score'] = FICO
            database['history'][user]['records'][order_id]['local_credit_score_info'] = FICO_info
            print(f'({n_record-i_order} - {FICO})', end=' ')
            
        

        # print(database['history'][user])


    print('----------- DONE -----------')
    new_database = {
        'history': database['history'],
        'summary': database['summary'],
        'credit_history_criteria': database['credit_history_criteria']
        }  
    # print(database['history']['50083']['records'])
    db.save(new_database)

def upload_credit_score():
    database = db.read()
    
    for user, val in database['history'].items():
        # print(user)
        score = cal_final_FICO_score(user)
        
        if score == 300:
           score = cal_final_FICO_score(user, cal_duration= 10e9) 
        print(f'{user} - {score}')
        
        database['history'][user]['credit_score'] = score

    new_database = {
        'history': database['history'],
        'summary': database['summary'],
        'credit_history_criteria': database['credit_history_criteria']
        }  
    # print(database['history']['50083']['records'])
    db.save(new_database)
   
   
    
if __name__ == '__main__':
    # upload_data_struct()
    # upload_record_sum()
    # upload_fin_record()
    # upload_cred_criteria()
    upload_local_credit_score()
    # upload_credit_score()
    
    pass