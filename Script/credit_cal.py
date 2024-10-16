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
    
    order_per_month = {}
    for i_order, order in enumerate(info['records'].values()):
        if len(order_per_month) > 6:
            del order_per_month[month]
            break
        
        month = order['order_date'][1]
        if i_order == 0:
            current_month = month
        if current_month == month:
            continue
        
        try:
            order_per_month[month] += 1
        except:
            order_per_month[month] = 1
    
    n_per_month = round(np.mean([val for val in order_per_month.values()]), 0)
    if show: print(f'order: {order_per_month}, n: {n_per_month}')
    
    return credit_budget, n_per_month
    
def cal_credit_terms(customer_id, credit_score= None, show= False):
    info = get_info_by_id(customer_id)
    if credit_score is None: credit_score = info['credit_score']
    
    credit_terms = 5 + 25 * (credit_score - 300) / 500
    if show: print(f'Credit Terms: {credit_terms} days')
    
    return credit_terms
    
def cal_credit_values(customer_id, credit_score= None, cal_n= True, show= False):
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
    
    
    fac_terms = (credit_score - 670) / 370
    fac_terms = 0 if fac_terms > 0 else fac_terms
    credit_terms = 30 + 23 * fac_terms
    
    fac_budget = (credit_score - 490) / 360
    fac_budget = 0 if fac_budget < 0 else fac_budget
    M_credit_budget = 0.3 + 1.7 * fac_budget
    credit_budget = mean_order * M_credit_budget

    if show: print(f'fac_budget =>\tCredit Budget: {round(mean_order, 3)} -> {round(credit_budget, 3)}\nfac_terms =>\tCredit Terms: {round(credit_terms, 3)}')
    
    n_per_month = 0
    if cal_n:
        order_per_month = {}
        for i_order, order in enumerate(info['records'].values()):
            if len(order_per_month) > 6:
                del order_per_month[month]
                break
            
            month = order['order_date'][1]
            if i_order == 0:
                current_month = month
            if current_month == month:
                continue
            
            try:
                order_per_month[month] += 1
            except:
                order_per_month[month] = 1
        
        if len(order_per_month) == 0: n_per_month = 3
        else: n_per_month = round(np.mean([val for val in order_per_month.values()]), 0)
        if show: print(f'n_order => \tOrder: {order_per_month} -> n: {n_per_month}')
    
    return int(credit_budget), int(credit_terms), n_per_month
 
def budget_round(score):
    return int(round(score, -1 * (len(str(int(score)))-2)))
   
    
if __name__ == '__main__':
    set_credit_score = None
    budget, terms, n = cal_credit_values('00001', set_credit_score, False)
    
    print(f'Results: {budget * n} - {budget_round(budget * n)}')
    
