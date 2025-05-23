
import random
import json
import pandas as pd
from datetime import datetime, timedelta, time

# Configuratie
START_DATE = datetime(2025, 4, 28)
END_DATE = datetime(2025, 5, 5)
POWER_USAGE_WATT = 900
server_name = 'server_1337'
tables = list(range(1, 21))
negative_comments = ['Traag bezorgd', 'Koud eten', 'Verkeerde bestelling']
positive_comments = ['Uitstekende service', 'Lekker en snel', 'Geweldige ervaring']
all_comments = negative_comments + positive_comments

# Gedefinieerde storingen
ERROR_BLOCKS = [
    (datetime(2025, 5, 1), time(10, 13), time(11, 56), "E01", "POLLING ERROR"),
    (datetime(2025, 5, 5), time(9, 4), time(11, 13), "E02", "UNABLE TO CONNECT"),
    (datetime(2025, 5, 5), time(15, 56), time(18, 46), "E03", "Runtime error: Physical collision detected"),
]

def generate_birth_date(reference_date):
    if random.random() < 0.43:
        age = random.randint(18, 44)
    else:
        age = random.randint(45, 90)
    birth_date = reference_date - timedelta(days=age * 365 + random.randint(0, 364))
    return birth_date.strftime('%d-%m-%Y')

def is_in_error_block(date, dt):
    for err_date, start, end, _, _ in ERROR_BLOCKS:
        if date.date() == err_date.date() and start <= dt.time() <= end:
            return True
    return False

def generate_orders_for_day(date):
    orders = []
    order_id = 1
    for hour in range(9, 21):  # Van 09:00 tot 21:00
        num_orders = random.randint(8, 14)
        
        batch_orders = 0
        attempts = 0
        existing_trips = []
        while batch_orders < num_orders and attempts < 1000:
            group_size = 1
            if random.random() < 0.2:
                group_size = random.choice([2, 3])
            if batch_orders + group_size > num_orders:
                group_size = 1

            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            time_picked = datetime(date.year, date.month, date.day, hour, minute, second)
            if is_in_error_block(date, time_picked) or any(start <= time_picked <= end for (start, end) in existing_trips):
                attempts += 1
                continue
            if time_picked.time() > time(21, 30):
                attempts += 1
                continue

            delivery_delays = [timedelta(seconds=random.randint(30, 180)) for _ in range(group_size)]
            time_deliveries = [time_picked + d for d in delivery_delays]
            if any(t.time() > time(21, 30) for t in time_deliveries):
                attempts += 1
                continue

            trip_end = max(time_deliveries)
            existing_trips.append((time_picked, trip_end))
            for i in range(group_size):
                include_comment = random.random() < 0.10
                comment = random.choice(all_comments) if include_comment else ""
                rating = random.randint(1, 5) if comment in negative_comments else random.randint(6, 10)
                duration_sec = (time_deliveries[i] - time_picked).total_seconds()
                power_kwh = (duration_sec / 3600) * (POWER_USAGE_WATT / 1000)

                order = {
                    'Order_ID': f"{date.strftime('%Y%m%d')}-{str(order_id).zfill(3)}",
                    'Date': date.strftime('%d-%m-%Y'),
                    'Time_Picked': time_picked.strftime('%H:%M:%S'),
                    'Time_Delivery': time_deliveries[i].strftime('%H:%M:%S'),
                    'Server': server_name,
                    'Table': random.choice(tables),
                    'Rating': rating,
                    'Total_Amount': round(random.uniform(10, 100), 2),
                    'Birth_Date': generate_birth_date(date),
                    'Comment': comment,
                    'Power consumption': round(power_kwh, 3),
                    'Error_code': ""
                }

                orders.append(order)
                order_id += 1
                batch_orders += 1
    
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            time_picked = datetime(date.year, date.month, date.day, hour, minute, second)
            if is_in_error_block(date, time_picked) or any(start <= time_picked <= end for (start, end) in existing_trips):
                attempts += 1
                continue
            time_delivery = time_picked + timedelta(seconds=random.randint(30, 180))
            if time_delivery.time() > time(21, 30):
                attempts += 1
                continue

            include_comment = random.random() < 0.10
            comment = random.choice(all_comments) if include_comment else ""
            rating = random.randint(1, 5) if comment in negative_comments else random.randint(6, 10)
            duration_sec = (time_delivery - time_picked).total_seconds()
            power_kwh = (duration_sec / 3600) * (POWER_USAGE_WATT / 1000)

            order = {
                'Order_ID': f"{date.strftime('%Y%m%d')}-{str(order_id).zfill(3)}",
                'Date': date.strftime('%d-%m-%Y'),
                'Time_Picked': time_picked.strftime('%H:%M:%S'),
                'Time_Delivery': time_delivery.strftime('%H:%M:%S'),
                'Server': server_name,
                'Table': random.choice(tables),
                'Rating': rating,
                'Total_Amount': round(random.uniform(10, 100), 2),
                'Birth_Date': generate_birth_date(date),
                'Comment': comment,
                'Power consumption': round(power_kwh, 3),
                'Error_code': ""
            }

            orders.append(order)
            order_id += 1
    return orders

def generate_error_block(date, start_time, end_time, error_code, error_msg):
    orders = []
    start_dt = datetime.combine(date, start_time)
    end_dt = datetime.combine(date, end_time)
    duration_minutes = int((end_dt - start_dt).total_seconds() // 60)
    num_errors = duration_minutes // 4
    time_blocks = sorted([
        start_dt + timedelta(minutes=random.randint(0, duration_minutes)) 
        for _ in range(num_errors)
    ])

    for i, t_picked in enumerate(time_blocks):
        time_delivery = ""
        order = {
            'Order_ID': f"{date.strftime('%Y%m%d')}-ERR{str(i+1).zfill(3)}",
            'Date': date.strftime('%d-%m-%Y'),
            'Time_Picked': t_picked.strftime('%H:%M:%S'),
            'Time_Delivery': "",
            'Server': server_name,
            'Table': random.choice(tables),
            'Rating': "",
            'Total_Amount': round(random.uniform(10, 100), 2),
            'Birth_Date': generate_birth_date(date),
            'Comment': "",
            'Power consumption': "",
            'Error_code': f"{error_code}: {error_msg}"
        }
        orders.append(order)
    return orders

def generate_week_log_with_errors():
    weekly_orders = []
    current_date = START_DATE
    while current_date <= END_DATE:
        daily_orders = generate_orders_for_day(current_date)
        weekly_orders.extend(daily_orders)
        current_date += timedelta(days=1)

    for err_date, start, end, code, msg in ERROR_BLOCKS:
        error_orders = generate_error_block(err_date, start, end, code, msg)
        weekly_orders.extend(error_orders)

    all_orders_sorted = sorted(weekly_orders, key=lambda x: (x['Date'], x['Time_Picked']))

    with open("robot_restaurant_log_week_cleaned.json", "w", encoding='utf-8') as f:
        json.dump(all_orders_sorted, f, indent=4, ensure_ascii=False)

    df = pd.DataFrame(all_orders_sorted)
    df.to_excel("robot_restaurant_log_week_cleaned.xlsx", index=False)

if __name__ == "__main__":
    generate_week_log_with_errors()
