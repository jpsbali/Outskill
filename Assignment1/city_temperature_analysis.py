import numpy as np
from collections import Counter
from datetime import datetime

CSV_FILE = 'city_temperature.csv'

# Read CSV using numpy and parse dates and temps
# We'll build: dates (list of datetime), city_temps (dict of city -> np.array), months (list of YYYY-MM str)
def load_data(filename):
    with open(filename, 'r') as f:
        header = f.readline().strip().split(',')
        cities = header[1:]
        dates = []
        months = []
        city_temps = {city: [] for city in cities}
        for line in f:
            parts = line.strip().split(',')
            date = datetime.strptime(parts[0], '%d-%m-%Y')
            dates.append(date)
            months.append(date.strftime('%Y-%m'))
            for i, city in enumerate(cities):
                city_temps[city].append(float(parts[i+1]))
        for city in cities:
            city_temps[city] = np.array(city_temps[city])
        return dates, months, cities, city_temps

def max_temp_day(dates, cities, city_temps):
    result = {}
    for city in cities:
        idx = np.argmax(city_temps[city])
        result[city] = (dates[idx].strftime('%d-%m-%Y'), city_temps[city][idx])
    return result

def monthly_avg_temp(months, cities, city_temps):
    result = {city: {} for city in cities}
    unique_months = sorted(set(months))
    for city in cities:
        for month in unique_months:
            mask = np.array([m == month for m in months])
            avg = np.mean(city_temps[city][mask])
            result[city][month] = avg
    return result

def five_day_stretch_above_monthly_avg(dates, months, cities, city_temps):
    monthly_avgs = monthly_avg_temp(months, cities, city_temps)
    n = len(dates)
    result = {}
    for city in cities:
        count = 0
        temps = city_temps[city]
        for i in range(n - 4):
            window_months = months[i:i+5]
            window_temps = temps[i:i+5]
            month_counts = Counter(window_months)
            max_count = max(month_counts.values())
            # If tie, pick later month
            max_month = sorted([m for m, c in month_counts.items() if c == max_count])[-1]
            avg = monthly_avgs[city][max_month]
            if np.all(window_temps > avg):
                count += 1
        result[city] = count
    return result

if __name__ == '__main__':
    dates, months, cities, city_temps = load_data(CSV_FILE)
    print('Day of max temperature for each city:')
    for city, (date, temp) in max_temp_day(dates, cities, city_temps).items():
        print(f'{city}: {date} ({temp}°C)')
    print('\nMonthly average temperature for each city:')
    for city, months_dict in monthly_avg_temp(months, cities, city_temps).items():
        print(f'{city}:')
        for month, avg in months_dict.items():
            print(f'  {month}: {avg:.2f}°C')
    print('\nNumber of 5-day stretches above monthly average for each city:')
    for city, count in five_day_stretch_above_monthly_avg(dates, months, cities, city_temps).items():
        print(f'{city}: {count}')
