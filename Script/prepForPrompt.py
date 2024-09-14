import Script.databaseClient as db
import numpy as np

data = db.read()['history']
msg = ''

def prep_dataset():
    for user_i, user in enumerate(data.values()):
        credit_score = user['credit_score']
        
        order_amount = []
        for order in user['records'].values():
            order_amount.append(order['amount'])

        msg += f'{credit_score} | {np.mean(order_amount)} | {len(order_amount)}\n'

    with open('prompt.txt', 'w') as file:
        file.write(msg)

    data_list = data.values()

def read_customer_info(customer_id):
    info = data[customer_id]
    msg = f"ลูกค่าหมายเลข {info['customer_id']} เป็นลูกค้าชนิด {info['type']} มี credit score อยู่ที่ {info['credit_score']}"
    
    if len(info['financial_info']) != 0:
        msg+= ' มีข้อมูลทางธุรกิจ (financial information) ดังนี้ '
        for i_info, fin_info in enumerate(info['financial_info']):
            if i_info == 0:
                msg += 'ปีนี้ มี'
            if i_info == len(info['financial_info']) - 1:
                msg += f'และ {i_info} ปีก่อน มี'
            else:
                msg += f'{i_info} ปีก่อน มี'
                
            msg += f" total assets อยู่ที่ {fin_info['total_assets']}, current assets อยู่ที่ {fin_info['current_assets']}, total liabilities อยู่ที่ {fin_info['total_liabilities']}, total revenue อยู่ที่ {fin_info['total_revenue']}, และ shareholder's equity อยู่ที่ {fin_info['shareholder_equity']}; "
    else:
        msg+= ' ลูกค้าไม่มีข้อมูลทางธุรกิจ (financial information) '
    
    msg += "ลูกค้ามีรายการสั่งซื้อทั้งหมดมีดังนี้ "
    for i_record, record in enumerate(info['records'].values()):
        
        msg += f"{i_record+1}) การสั้่งซื้อที่ {record['ID']} มียอดการสั่งซื้ออยู่ที่ {record['amount']} สั่งซื้อวันที่ {'/'.join(str(k) for k in record['order_date'])} "
        
        if record['stat'] == 'FULL':
            paid_date = '/'.join(str(k) for k in record['paid_date'])
            msg += f"ชำระครบวันที่ {paid_date} ชำระโดยใช้ {record['method']} "
        elif record['stat'] == 'PARTIAL':
            paid_date = '/'.join(str(k) for k in record['paid_date'])
            msg += f"ชำระบางส่วนวันที่ {paid_date} ชำระโดยใช้ {record['method']} "
        else:
            msg += f"ยังคงค้างชำระ "
    
    print(msg)
    with open('prompt.txt', 'w', encoding= 'utf-8') as file:
        file.write(msg) 
    
    
if __name__ == '__main__':
    read_customer_info('00001')
    
    
       
        
