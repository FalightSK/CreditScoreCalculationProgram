from openai import OpenAI
from .databaseClient import get_info_by_id, update_explanation
import os

### Setup
client = OpenAI(
    api_key= 'sk-uIQkiWnCuvZwmI49MliRQL5FPCtmn9P1MYdjUIrV6M74xyl2',
    base_url= 'https://api.opentyphoon.ai/v1'
)



### Utilities function
def read_system_file(filename):
    path = os.path.join(os.getcwd(), f'Script\\{filename}.txt')
    system_content = ''
    with open(path, 'r', encoding= 'utf-8') as file:
        system_content = file.read()
    return system_content

def read_customer_info(customer_id, new_FICO= None, request_budget= None):
    info = get_info_by_id(customer_id)
    if new_FICO is not None:
        info['credit_score'] = new_FICO
        msg = f"ลูกค่าหมายเลข {info['customer_id']} เป็นลูกค้าชนิด {info['type']} มี credit score ใหม่ที่คำนวณจาก requested budget อยู่ที่ {new_FICO} โดยมี requested budget เป็น {request_budget}"
    else:
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
    
    msg += "ลูกค้ามีรายการสั่งซื้อทั้งหมดมีดังนี้ ซึ่งถูกเขียนในรูปแบบนี้ (รายการสั่งซื้อ, การสั่งซื้อ, วันที่สั่งซื้อ, สถานะการสั่งซื้อ)"
    for i_record, record in enumerate(info['records'].values()):
        
        msg += f"({record['ID']}, {record['amount']}, {'/'.join(str(k) for k in record['order_date'])}, "
        
        if record['stat'] == 'FULL':
            paid_date = '/'.join(str(k) for k in record['paid_date'])
            msg += f"ชำระครบวันที่ {paid_date} ชำระโดยใช้ {record['method']}),"
        elif record['stat'] == 'PARTIAL':
            paid_date = '/'.join(str(k) for k in record['paid_date'])
            msg += f"ชำระบางส่วนวันที่ {paid_date} ชำระโดยใช้ {record['method']}),"
        else:
            msg += f"ยังคงค้างชำระ),"
    
    return msg
 
def get_explanation(customer_id, index= 0, new_FICO= None, request_budget= None):
    user_type = ['current_customer', 'new_customer', 'request_budget']
    prompt = read_customer_info(customer_id, new_FICO= new_FICO, request_budget= request_budget)
    system_content = read_system_file(f'typhoon_system_{user_type[index]}')
    # prompt = "ลูกค่าหมายเลข 00001 เป็นลูกค้าชนิด Tyre Shop มี credit score อยู่ที่ 754 ลูกค้าไม่มีข้อมูลทางธุรกิจ (financial information) ลูกค้ามีรายการสั่งซื้อทั้งหมดมีดังนี้ 1) การสั้่งซื้อที่ SO-202406700 มียอดการสั่งซื้ออยู่ที่ 2360.0 สั่งซื้อวันที่ 28/6/2024 ชำระครบวันที่ 28/6/2024 ชำระโดยใช้ CASH 2) การสั้่งซื้อที่ SO-202406659 มียอดการสั่งซื้ออยู่ที่ 17700.0 สั่งซื้อวันที่ 26/6/2024 ชำระครบวันที่ 27/6/2024 ชำระโดยใช้ OTHERS 3) การสั้่งซื้อที่ SO-202406648 มียอดการสั่งซื้ออยู่ที่ 6360.0 สั่งซื้อวันที่ 26/6/2024 ชำระครบวันที่ 26/6/2024 ชำระโดยใช้ OTHERS 4) การสั้่งซื้อที่ SO-202406629 มียอดการสั่งซื้ออยู่ที่ 10040.0 สั่งซื้อวันที่ 25/6/2024 ชำระครบวันที่ 26/6/2024 ชำระโดยใช้ OTHERS 5) การสั้่งซื้อที่ SO-202406578 มียอดการสั่งซื้ออยู่ที่ 9108.0 สั่งซื้อวันที่ 24/6/2024 ชำระครบวันที่ 24/6/2024 ชำระโดยใช้ OTHERS 6) การสั้่งซื้อที่ SO-202406463 มียอดการสั่งซื้ออยู่ที่ 4554.0 สั่งซื้อวันที่ 19/6/2024 ชำระครบวันที่ 21/6/2024 ชำระโดยใช้ OTHERS 7) การสั้่งซื้อที่ SO-202406405 มียอดการสั่งซื้ออยู่ที่ 4640.0 สั่งซื้อวันที่ 17/6/2024 ชำระครบวันที่ 17/6/2024 ชำระโดยใช้ OTHERS 8) การสั้่งซื้อที่ SO-202406347 มียอดการสั่งซื้ออยู่ที่ 3140.0 สั่งซื้อวันที่ 14/6/2024 ชำระครบวันที่ 15/6/2024 ชำระโดยใช้ OTHERS 9) การสั้่งซื้อที่ SO-202406242 มียอดการสั่งซื้ออยู่ที่ 9108.0 สั่งซื้อวันที่ 10/6/2024 ชำระครบวันที่ 12/6/2024 ชำระโดยใช้ OTHERS 10) การสั้่งซื้อที่ SO-202406078 มียอดการสั่งซื้ออยู่ที่ 4640.0 สั่งซื้อวันที่ 4/6/2024 ชำระครบวันที่ 4/6/2024 ชำระโดยใช้ CASH 11) การสั้่งซื้อที่ SO-202406042 มียอดการสั่งซื้ออยู่ที่ 9720.0 สั่งซื้อวันที่ 2/6/2024 ชำระครบวันที่ 2/6/2024 ชำระโดยใช้ CASH 12) การสั้่งซื้อที่ SO-202405786 มียอดการสั่งซื้ออยู่ที่ 9735.0 สั่งซื้อวันที่ 27/5/2024 ชำระครบวันที่ 28/5/2024 ชำระโดยใช้ OTHERS 13) การสั้่งซื้อที่ SO-202405715 มียอดการสั่งซื้ออยู่ที่ 6160.0 สั่งซื้อวันที่ 25/5/2024 ชำระครบวันที่ 25/5/2024 ชำระโดยใช้ OTHERS 14) การสั้่งซื้อที่ SO-202405710 มียอดการสั่งซื้ออยู่ที่ 2700.0 สั่งซื้อวันที่ 24/5/2024 ชำระครบวันที่ 24/5/2024 ชำระโดยใช้ CASH 15) การสั้่งซื้อที่ SO-202405671 มียอดการสั่งซื้ออยู่ที่ 12160.0 สั่งซื้อวันที่ 23/5/2024 ชำระครบวันที่ 23/5/2024 ชำระโดยใช้ CASH 16) การสั้่งซื้อที่ SO-202405370 มียอดการสั่งซื้ออยู่ที่ 5800.0 สั่งซื้อวันที่ 13/5/2024 ชำระครบวันที่ 13/5/2024 ชำระโดยใช้ CASH 17) การสั้่งซื้อที่ SO-202405312 มียอดการสั่งซื้ออยู่ที่ 4350.0 สั่งซื้อวันที่ 11/5/2024 ชำระครบวันที่ 11/5/2024 ชำระโดยใช้ CASH 18) การสั้่งซื้อที่ SO-202405256 มียอดการสั่งซื้ออยู่ที่ 4640.0 สั่งซื้อวันที่ 8/5/2024 ชำระครบวันที่ 9/5/2024 ชำระโดยใช้ CASH 19) การสั้่งซื้อที่ SO-202405147 มียอดการสั่งซื้ออยู่ที่ 9200.0 สั่งซื้อวันที่ 5/5/2024 ชำระครบวันที่ 6/5/2024 ชำระโดยใช้ CASH 20) การสั้่งซื้อที่ SO-202405045 มียอดการสั่งซื้ออยู่ที่ 4640.0 สั่งซื้อวันที่ 2/5/2024 ชำระครบวันที่ 3/5/2024 ชำระโดยใช้ OTHERS 21) การสั้่งซื้อที่ SO-202404845 มียอดการสั่งซื้ออยู่ที่ 11200.0 สั่งซื้อวันที่ 30/4/2024 ชำระครบวันที่ 2/5/2024 ชำระโดยใช้ OTHERS 22) การสั้่งซื้อที่ SO-202404797 มียอดการสั่งซื้ออยู่ที่ 6740.0 สั่งซื้อวันที่ 29/4/2024 ชำระครบวันที่ 30/4/2024 ชำระโดยใช้ CASH 23) การสั้่งซื้อที่ SO-202404789 มียอดการสั่งซื้ออยู่ที่ 6880.0 สั่งซื้อวันที่ 29/4/2024 ชำระครบวันที่ 30/4/2024 ชำระโดยใช้ CASH 24) การสั้่งซื้อที่ SO-202404736 มียอดการสั่งซื้ออยู่ที่ 4640.0 สั่งซื้อวันที่ 27/4/2024 ชำระครบวันที่ 27/4/2024 ชำระโดยใช้ CASH 25) การสั้่งซื้อที่ SO-202404710 มียอดการสั่งซื้ออยู่ที่ 3600.0 สั่งซื้อวันที่ 26/4/2024 ชำระครบวันที่ 26/4/2024 ชำระโดยใช้ OTHERS 26) การสั้่งซื้อที่ SO-202404562 มียอดการสั่งซื้ออยู่ที่ 17700.0 สั่งซื้อวันที่ 22/4/2024 ชำระครบวันที่ 22/4/2024 ชำระโดยใช้ OTHERS 27) การสั้่งซื้อที่ SO-202404424 มียอดการสั่งซื้ออยู่ที่ 7520.0 สั่งซื้อวันที่ 17/4/2024 ชำระครบวันที่ 18/4/2024 ชำระโดยใช้ OTHERS 28) การสั้่งซื้อที่ SO-202404346 มียอดการสั่งซื้ออยู่ที่ 3440.0 สั่งซื้อวันที่ 11/4/2024 ชำระครบวันที่ 12/4/2024 ชำระโดยใช้ OTHERS 29) การสั้่งซื้อที่ SO-202404317 มียอดการสั่งซื้ออยู่ที่ 15040.0 สั่งซื้อวันที่ 10/4/2024 ชำระครบวันที่ 10/4/2024 ชำระโดยใช้ CASH 30) การสั้่งซื้อที่ SO-202404286 มียอดการสั่งซื้ออยู่ที่ 3140.0 สั่งซื้อวันที่ 9/4/2024 ชำระครบวันที่ 9/4/2024 ชำระโดยใช้ CASH 31) การสั้่งซื้อที่ SO-202404273 มียอดการสั่งซื้ออยู่ที่ 4640.0 สั่งซื้อวันที่ 8/4/2024 ชำระครบวันที่ 9/4/2024 ชำระโดยใช้ CASH 32) การสั้่งซื้อที่ SO-202404127 มียอดการสั่งซื้ออยู่ที่ 4720.0 สั่งซื้อวันที่ 4/4/2024 ชำระครบวันที่ 4/4/2024 ชำระโดยใช้ CASH 33) การสั้่งซื้อที่ SO-202404085 มียอดการสั่งซื้ออยู่ที่ 18640.0 สั่งซื้อวันที่ 3/4/2024 ชำระครบวันที่ 3/4/2024 ชำระโดยใช้ CASH 34) การสั้่งซื้อที่ SO-202403774 มียอดการสั่งซื้ออยู่ที่ 9240.0 สั่งซื้อวันที่ 27/3/2024 ชำระครบวันที่ 1/4/2024 ชำระโดยใช้ OTHERS 35) การสั้่งซื้อที่ SO-202403685 มียอดการสั่งซื้ออยู่ที่ 1570.0 สั่งซื้อวันที่ 25/3/2024 ชำระครบวันที่ 25/3/2024 ชำระโดยใช้ CASH 36) การสั้่งซื้อที่ SO-202403615 มียอดการสั่งซื้ออยู่ที่ 10280.0 สั่งซื้อวันที่ 22/3/2024 ชำระครบวันที่ 25/3/2024 ชำระโดยใช้ CASH 37) การสั้่งซื้อที่ SO-202403586 มียอดการสั่งซื้ออยู่ที่ 3800.0 สั่งซื้อวันที่ 21/3/2024 ชำระครบวันที่ 21/3/2024 ชำระโดยใช้ OTHERS 38) การสั้่งซื้อที่ SO-202403500 มียอดการสั่งซื้ออยู่ที่ 12680.0 สั่งซื้อวันที่ 19/3/2024 ชำระครบวันที่ 19/3/2024 ชำระโดยใช้ OTHERS 39) การสั้่งซื้อที่ SO-202403356 มียอดการสั่งซื้ออยู่ที่ 2120.0 สั่งซื้อวันที่ 13/3/2024 ชำระครบวันที่ 13/3/2024 ชำระโดยใช้ CASH 40) การสั้่งซื้อที่ SO-202403331 มียอดการสั่งซื้ออยู่ที่ 9240.0 สั่งซื้อวันที่ 12/3/2024 ชำระครบวันที่ 12/3/2024 ชำระโดยใช้ OTHERS 41) การสั้่งซื้อที่ SO-202403309 มียอดการสั่งซื้ออยู่ที่ 7800.0 สั่งซื้อวันที่ 12/3/2024 ชำระครบวันที่ 12/3/2024 ชำระโดยใช้ OTHERS 42) การสั้่งซื้อที่ SO-202403217 มียอดการสั่งซื้ออยู่ที่ 150.0 สั่งซื้อวันที่ 8/3/2024 ชำระครบวันที่ 8/3/2024 ชำระโดยใช้ CASH 43) การสั้่งซื้อที่ SO-202403215 มียอดการสั่งซื้ออยู่ที่ 13040.0 สั่งซื้อวันที่ 8/3/2024 ชำระครบวันที่ 8/3/2024 ชำระโดยใช้ CASH 44) การสั้่งซื้อที่ SO-202403006 มียอดการสั่งซื้ออยู่ที่ 2900.0 สั่งซื้อวันที่ 1/3/2024 ชำระครบวันที่ 1/3/2024 ชำระโดยใช้ CASH 45) การสั้่งซื้อที่ SO-202402615 มียอดการสั่งซื้ออยู่ที่ 10040.0 สั่งซื้อวันที่ 26/2/2024 ชำระครบวันที่ 27/2/2024 ชำระโดยใช้ OTHERS 46) การสั้่งซื้อที่ SO-202402464 มียอดการสั่งซื้ออยู่ที่ 10280.0 สั่งซื้อวันที่ 19/2/2024 ชำระครบวันที่ 19/2/2024 ชำระโดยใช้ OTHERS 47) การสั้่งซื้อที่ SO-202402377 มียอดการสั่งซื้ออยู่ที่ 2900.0 สั่งซื้อวันที่ 15/2/2024 ชำระครบวันที่ 16/2/2024 ชำระโดยใช้ CASH 48) การสั้่งซื้อที่ SO-202402315 มียอดการสั่งซื้ออยู่ที่ 7000.0 สั่งซื้อวันที่ 13/2/2024 ชำระครบวันที่ 13/2/2024 ชำระโดยใช้ OTHERS 49) การสั้่งซื้อที่ SO-202402268 มียอดการสั่งซื้ออยู่ที่ 6200.0 สั่งซื้อวันที่ 12/2/2024 ชำระครบวันที่ 13/2/2024 ชำระโดยใช้ OTHERS 50) การสั้่งซื้อที่ SO-202402179 มียอดการสั่งซื้ออยู่ที่ 8918.0 สั่งซื้อวันที่ 8/2/2024 ชำระครบวันที่ 8/2/2024 ชำระโดยใช้ OTHERS 51) การสั้่งซื้อที่ SO-202402148 มียอดการสั่งซื้ออยู่ที่ 4880.0 สั่งซื้อวันที่ 7/2/2024 ชำระครบวันที่ 7/2/2024 ชำระโดยใช้ CASH 52) การสั้่งซื้อที่ SO-202402140 มียอดการสั่งซื้ออยู่ที่ 5200.0 สั่งซื้อวันที่ 6/2/2024 ชำระครบวันที่ 6/2/2024 ชำระโดยใช้ CASH 53) การสั้่งซื้อที่ SO-202402100 มียอดการสั่งซื้ออยู่ที่ 10040.0 สั่งซื้อวันที่ 5/2/2024 ชำระครบวันที่ 6/2/2024 ชำระโดยใช้ OTHERS 54) การสั้่งซื้อที่ SO-202401807 มียอดการสั่งซื้ออยู่ที่ 9200.0 สั่งซื้อวันที่ 31/1/2024 ชำระครบวันที่ 31/1/2024 ชำระโดยใช้ CASH 55) การสั้่งซื้อที่ SO-202401772 มียอดการสั่งซื้ออยู่ที่ 4550.0 สั่งซื้อวันที่ 30/1/2024 ชำระครบวันที่ 30/1/2024 ชำระโดยใช้ CASH 56) การสั้่งซื้อที่ SO-202401730 มียอดการสั่งซื้ออยู่ที่ 7600.0 สั่งซื้อวันที่ 28/1/2024 ชำระครบวันที่ 29/1/2024 ชำระโดยใช้ CASH 57) การสั้่งซื้อที่ SO-202401705 มียอดการสั่งซื้ออยู่ที่ 4800.0 สั่งซื้อวันที่ 27/1/2024 ชำระครบวันที่ 29/1/2024 ชำระโดยใช้ OTHERS 58) การสั้่งซื้อที่ SO-202401703 มียอดการสั่งซื้ออยู่ที่ 1200.0 สั่งซื้อวันที่ 27/1/2024 ชำระครบวันที่ 29/1/2024 ชำระโดยใช้ OTHERS 59) การสั้่งซื้อที่ SO-202401702 มียอดการสั่งซื้ออยู่ที่ 11200.0 สั่งซื้อวันที่ 27/1/2024 ชำระครบวันที่ 29/1/2024 ชำระโดยใช้ OTHERS 60) การสั้่งซื้อที่ SO-202401639 มียอดการสั่งซื้ออยู่ที่ 2060.0 สั่งซื้อวันที่ 25/1/2024 ชำระครบวันที่ 25/1/2024 ชำระโดยใช้ CASH 61) การสั้่งซื้อที่ SO-202401615 มียอดการสั่งซื้ออยู่ที่ 10220.0 สั่งซื้อวันที่ 24/1/2024 ชำระครบวันที่ 24/1/2024 ชำระโดยใช้ CASH 62) การสั้่งซื้อที่ SO-202401578 มียอดการสั่งซื้ออยู่ที่ 14240.0 สั่งซื้อวันที่ 23/1/2024 ชำระครบวันที่ 23/1/2024 ชำระโดยใช้ CASH 63) การสั้่งซื้อที่ SO-202401485 มียอดการสั่งซื้ออยู่ที่ 11320.0 สั่งซื้อวันที่ 19/1/2024 ชำระครบวันที่ 20/1/2024 ชำระโดยใช้ OTHERS 64) การสั้่งซื้อที่ SO-202401454 มียอดการสั่งซื้ออยู่ที่ 8200.0 สั่งซื้อวันที่ 18/1/2024 ชำระครบวันที่ 19/1/2024 ชำระโดยใช้ OTHERS 65) การสั้่งซื้อที่ SO-202401353 มียอดการสั่งซื้ออยู่ที่ 4240.0 สั่งซื้อวันที่ 15/1/2024 ชำระครบวันที่ 15/1/2024 ชำระโดยใช้ OTHERS 66) การสั้่งซื้อที่ SO-202401237 มียอดการสั่งซื้ออยู่ที่ 4960.0 สั่งซื้อวันที่ 10/1/2024 ชำระครบวันที่ 10/1/2024 ชำระโดยใช้ OTHERS 67) การสั้่งซื้อที่ SO-202401077 มียอดการสั่งซื้ออยู่ที่ 10750.0 สั่งซื้อวันที่ 5/1/2024 ชำระครบวันที่ 5/1/2024 ชำระโดยใช้ CASH 68) การสั้่งซื้อที่ SO-202401027 มียอดการสั่งซื้ออยู่ที่ 7400.0 สั่งซื้อวันที่ 4/1/2024 ชำระครบวันที่ 5/1/2024 ชำระโดยใช้ OTHERS 69) การสั้่งซื้อที่ SO-202401012 มียอดการสั่งซื้ออยู่ที่ 22850.0 สั่งซื้อวันที่ 4/1/2024 ชำระครบวันที่ 5/1/2024 ชำระโดยใช้ OTHERS "
    
    chat_completion = client.chat.completions.create(
        model="typhoon-v1.5x-70b-instruct",
        messages=[
            {'role': 'system', 'content': system_content},
            {"role": "user", "content": prompt}],
        temperature= 0.05,
        top_p= 0.9,
    )
    # print(chat_completion.choices[0].message.content)
    explanation = chat_completion.choices[0].message.content
    print(new_FICO)
    if new_FICO is None:
        update_explanation(customer_id, explanation)
    return explanation

if __name__ == '__main__':
    custom_ID = '00001'
    # print(get_explanation(custom_ID, index= 0))
    # print(read_customer_info(custom_ID))
    
