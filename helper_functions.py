
import re
from datetime import datetime


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
    