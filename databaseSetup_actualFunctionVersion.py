import pandas as pd
import os
import numpy as np
import datetime
import Script.databaseClient as db
from Script.customerInfo import order, extract_fin_info, read_financial_file, PaymentInfo, read_order_file, extract_order_info
from currentCustomer import cal_FICO_current, cal_final_FICO_score, add_list_new_order
from newCustomer import register_new_user
from Script.credit_cal import cal_credit_values


doc = pd.read_excel(r"D:\KMITL\KMITL\Year 03 - 01\Prompt Engineer\Work\08_08_2024_Project\Data\Original Data\Merged_Transaction_Data_with_Customer_Type.xlsx")
doc.fillna('UNKNOWN', inplace= True)
# doc2 = pd.read_excel()

############ Register users
def upload_data_struct():
    new_database = {
        'history': {},
        "summary": {
            "Tyre Shop": {
                "mean": 12185.232171581769,
                "std": 14943.382533063737,
                "n": 1865
                },
            "UNKNOWN": {
                "mean": 10061.668687615527,
                "std": 16816.10607392258,
                "n": 541
                },
            "Fleet": {
                "mean": 4227.359375,
                "std": 4421.592877456563,
                "n": 320
                },
            "Garage": {
                "mean": 2185.0390625,
                "std": 4064.090241451538,
                "n": 128
                },
            "Used Car Dealer": {
                "mean": 3788.823529411765,
                "std": 3254.595632880376,
                "n": 34
                }
            },
        "credit_history_criteria": {
            "Fleet": [25000, 6],
            "Garage": [4000, 2],
            "Tyre Shop": [47000, 4],
            "Used Car Dealer": [22000, 6]
            }
        }  
    # print(database['history']['50083']['records'])
    db.save(new_database)
    
    prev_cus_id = ''
    users = {}
    for i, row in enumerate(doc.iloc()):
        local_data = order.copy()
        if row['Transaction Status'] != 'สำเร็จ' or row['Transaction Value'] in [0, 'UNKNOWN']:
            continue
        
        customer_id = row['Customer ID']
        
        if customer_id != prev_cus_id:
            prev_cus_id = customer_id
            
            register_new_user(customer_id, row['Type Of Customer'], None)
            
            

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
        'summary': db.read()['summary'],
        'credit_history_criteria': db.read()['credit_history_criteria']
    }        

    db.save(new_database)



############ Upload record summary
def upload_record_sum(path= r"D:\KMITL\KMITL\Year 03 - 01\Prompt Engineer\Work\08_08_2024_Project\Data\Original Data\raw_data_original.xlsx"):
    database = db.read()['history']
    order_list = extract_order_info(read_order_file(path))
    # print(order_list.head())
    add_list_new_order(order_list, True)


if __name__ == '__main__':
    time_start = datetime.datetime.now()
    
    upload_data_struct()
    upload_fin_record()
    upload_record_sum(r"D:\KMITL\KMITL\Year 03 - 01\Prompt Engineer\Work\08_08_2024_Project\Data\Original Data\sale jan-aug 2024 for update.xlsx")

    time_end = datetime.datetime.now()
    
    print(f'>>>>>>>>>>>> Total Process Time {str(time_end - time_start).split(".")[0]}')
    
    pass