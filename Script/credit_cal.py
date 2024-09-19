from .databaseClient import get_info_by_id
import numpy as np

def cal_credit_budget(customer_id, credit_score= None, show= False):
    info = get_info_by_id(customer_id)
    if credit_score is None: credit_score = info['credit_score']
    
    order_list = []
    for order in info['records'].values():
        order_list.append(order['amount'])
    mean_order = np.mean(order_list)
    
    # M = 0.3 + 1.7 * (credit_score - 300) / 550
    fac = 1.7 * (credit_score - 490) / 360
    fac = 0 if fac < 0 else fac
    M = 0.3 + fac
    
    credit_budget = mean_order * M
    if show: print(f'Mean order: {mean_order}, Credit Budget: {credit_budget}')
    
    return credit_budget
    
def cal_credit_terms(customer_id, credit_score= None, show= False):
    info = get_info_by_id(customer_id)
    if credit_score is None: credit_score = info['credit_score']
    
    credit_terms = 5 + 25 * (credit_score - 300) / 500
    if show: print(f'Credit Terms: {credit_terms} days')
    
    return credit_terms
    
def cal_credit_values(customer_id, credit_score= None, show= False):
    info = get_info_by_id(customer_id)
    if credit_score is None: credit_score = info['credit_score']
    
    order_list = []
    try:
        for order in info['records'].values():
            order_list.append(order['amount'])
        if len(order_list) == 0:
            mean_order = 10000
        else:
            mean_order = np.mean(order_list)
    except:
        mean_order = 10000
    
    fac = (credit_score - 490) / 360
    fac = 0 if fac < 0 else fac
    # print(fac, mean_order)
    
    credit_terms = 7 + 14 * fac
    
    M_credit_budget = 0.3 + 1.7 * fac
    credit_budget = mean_order * M_credit_budget

    if show: print(f'Credit Budget: {round(mean_order, 3)} -> {round(credit_budget, 3)}\nCredit Terms: {round(credit_terms, 3)}')
    
    return credit_budget, credit_terms
     
    
if __name__ == '__main__':
    set_credit_score = 620
    cal_credit_values('00001', set_credit_score, True)
    
