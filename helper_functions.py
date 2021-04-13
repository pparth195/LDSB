
import re
from datetime import datetime


#  FOR LOYALIST WATER BILLS

def get_numbers(s):
    return float(re.search(r"\d{1,}\.\d{1,}", s).group())

def get_loy_water_consuption(text):
    
    try:
        temp_consuption = re.compile(r'Consumption:\s\d{1,}\.\d{1,}')
        consuption =  get_numbers(temp_consuption.search(text).group())
    except:
        try:
            temp_consuption = re.compile(r'Consumption: —\s\d{1,}\.\d{1,}')
            consuption =  get_numbers(temp_consuption.search(text).group())
        except:
            return "Consuption not found!"
        
    return consuption

def get_loy_period(text):
    bill_from_pattern = re.compile(r'Bill From: \d{2}\-\w{3}\-\d{4}')
    bill_to_pattern = re.compile(r'Bill To: \d{2}\-\w{3}\-\d{4}')
    
    try:
        bill_from = bill_from_pattern.search(text).group()
        bill_to = bill_to_pattern.search(text).group()
    except:
        return "Billing period not found!"
    
    bill_from = re.search(r"\d{2}\-\w{3}\-\d{4}", bill_from).group()
    bill_to = re.search(r"\d{2}\-\w{3}\-\d{4}", bill_to).group()
    
    from_date = datetime.strptime(bill_from, '%d-%b-%Y').strftime('%Y-%m-%d')
    to_date = datetime.strptime(bill_to, '%d-%b-%Y').strftime('%Y-%m-%d')
    
    return {"from" : from_date, "to": to_date}
    
def get_loy_amount(text):
    try:
        mid_amount = re.search(r"Current Levy \d{1,}\.\d{1,}", text).group()
        amount = float(get_numbers(mid_amount))
    except:
        try:
            mid_amount = re.search(r"Current Levy \d{1,}\,\d{1,}\.\d{1,}", text).group()
            amount = re.search(r"\d{1,}\,\d{1,}\.\d{1,}", mid_amount).group()
            amount = float(amount.replace(',',''))
        except:
            return "Bill Amount Not Found!"
    return amount    

def get_loyalist_data(text):
    period = get_loy_period(text)
    return {
        "From": period["from"],
        "To": period["to"],
        "consumption": get_loy_water_consuption(text),
        "amount": get_loy_amount(text)
    }

# FOR GREATER NAPANEE

def get_napanee_amount(text):
    try:
        mid_amount = re.search(r"Balance: \$\d{1,}\.\d{1,}", text).group()
        amount = float(get_numbers(mid_amount))
    except:
        try:
            mid_amount = re.search(r"Balance: \$\d{1,}\,\d{1,}\.\d{1,}", text).group()
            amount = re.search(r"\d{1,}\,\d{1,}\.\d{1,}", mid_amount).group()
            amount = float(amount.replace(',',''))
        except:
            return "Bill Amount Not Found!"
    return amount

def get_napanee_consumption(text):
    try:
        con = float(re.search(r"\d{4}\/\d{2}\/\d{2}\s\d{1,}\s\d{1,}", text).group().split(" ")[2])
        return con
    except:
        return "Consumption not found!"

def get_napanee_period(text):
    
    # try:
    period = re.compile(r"\d{4}\/\d{2}\/\d{2}")
    matches = period.finditer(text)

    dates = [i.group() for i in matches]
#     All dates from text in datetime format.
    dates = [datetime.strptime(i, '%Y/%m/%d') for i in dates]

    for i in enumerate(dates):
#         finding difference between two dates.
#         First pair of date with Non zero difference would be our period. 
        d = i[1] - dates[i[0]+1]

        if d.days != 0:
            return {
                "end" : i[1].strftime('%Y-%m-%d'),
                "start" : dates[i[0]+1].strftime('%Y-%m-%d')
            }
    # except:
    #     return {
    #                 "end" : "Billing period not found!",
    #                 "start" : "Billing period not found!"
    #             }

    
def get_napanee_data(text):
    period = get_napanee_period(text)
    return {
        "amount" : get_napanee_amount(text),
        "consumption" : get_napanee_consumption(text),
        "start" : period["start"],
        "end" : period["end"]
    }



# FOR UTILITIES KINGSTON 

def get_mached_str_list(p, t):
    result = []
    matches = p.finditer(t)
    result = [match.group() for match in matches]
    
    return result

def get_water_price(p, t):
    price = p.search(t).group()
    price = float(re.search(r"\d{1,}\.\d{1,}", price).group())
    return price
 
def get_sewer_price(p, t):
    price = p.search(t).group()
    price = float(re.search(r"\d{1,}\.\d{1,}", price).group())
    return price

def get_billing_period(p, t):
    raw_period = p.search(t).group()
    temp = raw_period.split("to")
    s_date = temp[0].strip()
    e_date = temp[1].strip()
    
    s_date = datetime.strptime(s_date, '%b %d, %Y')
    e_date = datetime.strptime(e_date, '%b %d, %Y')
    
    s_date = s_date.strftime('%Y-%m-%d')
    e_date = e_date.strftime('%Y-%m-%d')
    
    return (s_date, e_date)
    
def get_water_usage(p, t):
    temp_l = get_mached_str_list(p, t)
    r = []
    for i in temp_l:
        r.append(float(re.search(r"\d{1,}\.\d{1,}", i).group()))
    return min(r)

def get_data_from_txt(txt):
    water_price_pattern = re.compile(r'eens\s\$\s\d{1,}\.\d{1,}')
    sewer_price_pattern = re.compile(r'eee\s\$\s\d{1,}\.\d{1,}')
    billing_period_pattern = re.compile(r'\w{3}\s\d{2}\,\s\d{4}\sto\s\w{3}\s\d{2}\,\s\d{4}')
    water_usage_pattern = re.compile(r"\d{1,}\.\d{1,}\sm3")
    
    return {
    "water_price" : get_water_price(water_price_pattern, txt),
    "sewer_price" : get_sewer_price(sewer_price_pattern, txt),
    "billing_period" : get_billing_period(billing_period_pattern, txt),
    "water_usage" : get_water_usage(water_usage_pattern, txt)
    }
    