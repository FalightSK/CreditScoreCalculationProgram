import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import datetime
import Script.databaseClient as db
from Script.customerInfo import PaymentInfo

 

if __name__ == '__main__':
    # _in = input('Enter Customer ID: ')
    customer_id = '00156'
    # customer_id = '00033'
    
    customer_info = db.get_info_by_id(customer_id)
    
    monthly_order = {}
    n_monthly_order = {}
    total_order = []
    customer_behavior = {}
    payment_behavior = {'Late': 0, 'Ontime': 0}
    for order in customer_info['records'].values():
        payment = PaymentInfo()
        payment.JSON_to_PaymentInfo(order)
        
        
        try: 
            monthly_order[str(payment.order_date.strftime("%b"))] += payment.amount
            n_monthly_order[str(payment.order_date.strftime("%b"))] += 1
        except: 
            monthly_order[str(payment.order_date.strftime("%b"))] = payment.amount
            n_monthly_order[str(payment.order_date.strftime("%b"))] = 1
        
        total_order.append(order['amount'])
        
        try: customer_behavior[order['stat']] += 1
        except: customer_behavior[order['stat']] = 1
        
        if order['stat'] == 'FULL':
            val = (payment.paid_date - payment.order_date).days - customer_info['credit_terms']
            if val > 0:
                payment_behavior['Late'] += 1
            else:
                payment_behavior['Ontime'] += 1
        
        
        
    print(f'Mean: {np.mean(total_order)}\nPayment Status: {customer_behavior}\nPayment Behavior: {payment_behavior}')
    

    fig, axes = plt.subplots(1, 2, figsize= (8, 4))
    
    fig.suptitle('Six Latest Months Order Records')
    
    axes[0].bar(monthly_order.keys(), monthly_order.values())
    axes[0].set_xlabel('Months')
    axes[0].set_ylabel('Values of Order')
    # axes[0].set_title('Six Latest Months Order Records')
    
    axes[1].bar(n_monthly_order.keys(), n_monthly_order.values())
    axes[1].set_xlabel('Months')
    axes[1].set_ylabel('Number of Order')
    # axes[1].set_ylim(0, 6)

    # Show the plot
    plt.show()
    
    
    pass