import pandas as pd
import numpy as np
from Script.customerInfo import FinancialInfo, extract_fin_info, read_financial_file, user
import Script.databaseClient as db



def FICO_cal(all_fin_info, show = False):
    credit_mix_list = []
    amount_owe_list = []
    new_credit_list = []
    
    for i, fin_info in enumerate(all_fin_info):
    
        # Cal each parameter -- Credit Mix
        credit_mix_ratio = fin_info.current_assets / fin_info.total_liabilities
        debt_to_equity = 1 - (fin_info.total_liabilities / fin_info.shareholder_equity)
        debt_to_assets = 1 - (fin_info.total_liabilities / fin_info.total_assets)
        
        debt_to_equity = 1 if debt_to_equity > 1 else 0 if debt_to_equity < 0 else debt_to_equity
        debt_to_assets = 1 if debt_to_assets > 1 else 0 if debt_to_assets < 0 else debt_to_assets

        credit_mix = 0.6 * credit_mix_ratio + 0.2 * debt_to_equity + 0.2 * debt_to_assets
        credit_mix_list.append(credit_mix * 550 + 300)
        

        # Cal each parameter -- Amounts Owe
        debt_to_revenue = 1 - (fin_info.total_liabilities / fin_info.total_revenue)
        debt_to_currentAsset = 1 - (fin_info.total_liabilities / fin_info.current_assets)
        
        debt_to_revenue = 1 if debt_to_revenue > 1 else 0 if debt_to_revenue < 0 else debt_to_revenue
        debt_to_currentAsset = 1 if debt_to_currentAsset > 1 else 0 if debt_to_currentAsset < 0 else debt_to_currentAsset
        
        amount_owe = 0.4 * debt_to_equity + 0.3 * debt_to_assets + 0.2 * debt_to_revenue + 0.1 * debt_to_currentAsset
        amount_owe_list.append(amount_owe * 550 + 300)
        
        
        # Cal each parameter -- New Credit
        try:
            ratio_of_liabilities_difference = (all_fin_info[i].total_liabilities - all_fin_info[i-1].total_liabilities) / all_fin_info[i-1].total_liabilities
            new_credit_list.append((550 / (1 + np.exp(5 * ratio_of_liabilities_difference))) + 300)
        except:
            print('first of list')
            
            
        if show:
            print('\nIteration', i+1)
            print(f'>>>>>> Amounts Owe: {amount_owe_list[i]} -> {debt_to_revenue}, {debt_to_currentAsset}')
            print(f'>>>>>> Credit Mix: {credit_mix_list[i]} -> {credit_mix_ratio}, {debt_to_equity}, {debt_to_assets}')
            print(f'>>>>>> New Credit: {new_credit_list[i]} -> {ratio_of_liabilities_difference}')
            
            
    # print(amount_owe_list, credit_mix_list, new_credit_list)
    n_fin_info = len(amount_owe_list) - 1
    FICO = 0.6 * amount_owe_list[n_fin_info] + 0.2 * credit_mix_list[n_fin_info] + 0.2 * np.mean(new_credit_list)
    if show:
        print('\nFICO SCORE:', round(FICO, 3))
    return min(FICO, 850)
     
def register_new_user(customer_id, customer_type, fin_info, show= False):
    credit_score = FICO_cal(fin_info, show= show)
    print(credit_score)
    
    fin_info_list = []
    for info in fin_info:
        fin_info_list.append(info.FinancialInfo_to_DICT())
    
    new_user = {
        'customer_id': customer_id,
        'type': customer_type,
        'credit_score': credit_score,
        'credit_budget': 17000,
        'credit_terms': 15,
        'financial_info': fin_info_list,
        'record_summary': {'mean': None, 'std': None, 'n': None }, 
        'records': []
    }
    
    
    if show: print(f'{fin_info_list} \n>>>>>>>>>>>>>>>>>>\n{new_user}')
    db.add_new_user(new_user)
    
    
     
if __name__ == '__main__':
    doc_finan_position = read_financial_file(r"D:\KMITL\KMITL\Year 03 - 01\Prompt Engineer\Work\08_08_2024_Project\Data\Original Data\financial data\00194\Financial Position 00194.xlsx")
    doc_income_statement = read_financial_file(r"D:\KMITL\KMITL\Year 03 - 01\Prompt Engineer\Work\08_08_2024_Project\Data\Original Data\financial data\00194\Income Statement 00194.xlsx")
    
    fin_info = extract_fin_info(doc_finan_position, doc_income_statement)
    
    # FICO_cal(fin_info, show= True)
    register_new_user('TS0001', 'Tyre Shop', fin_info, True)
    
    

