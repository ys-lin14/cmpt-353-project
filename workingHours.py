# CMPT353-Computational Data Science | Professor Greg Baker | Fall 2020
# Course Project - Working Hours of Amenities
###################################################################
# Start with importing few python libraies for the desired computations
import sys
import numpy as np
import pandas as pd
from pprint import pprint


daysOfweek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
workingHours_tem = {"Monday": None, "Tuesday": None, "Wednesday": None, "Thursday": None, "Friday": None, "Saturday": None, "Sunday": None}

'''
input: Name of a weekday
output: The associated index to the weekday
''' 
def dayToindex(day):
    index = daysOfweek.index(day)
    return index

'''
input: time component which would be inform of 'Hour:Mins'
output: compute the number of hours in a given period of working hours
'''
def computeHours(timecomponent):
    
    min_hr = 60
    hr_day = 24
    
    # Few corner cases to note down: 
    # 1) The lenght of time component is negative: Probably erros in entering the data
    # 2 & 3) The store is closed: were encoded as 'off' or 'closed' in the dataset 
    if len(timecomponent) <= 0 or timecomponent == 'off' or timecomponent == 'closed':
        return 0.0
    
    # Split the time component over ','
    timePeriod = timecomponent.split(',')
    
    sign = 1 # As a flag 
    for i in timePeriod:
        # Split the time component over ','
        lst = i.split('-')
        if len(lst) == 2:
            start, end = lst
        elif len(lst) == 1:
            start = lst[0]
            if '+' in start:
                start = start.replace('+', '')
                start_H, start_M = [int(x) for x in start.split(':')]
                return (hr_day * min_hr - hr_day * start_H - start_M) / min_hr
            else:
                return 0.0
        
        try:
            start_H, start_M = [int(x) for x in start.split(':')]
            end_H, end_M = [int(x) for x in end.split(':')]
        except Exception as e:
            return 0.0
        
        start_min = start_H * min_hr + start_M
        end_min = end_H * min_hr + end_M
        
        if end_min < start_min:
            end_min += hr_day * min_hr
                
        total_minutes = end_min - start_min
        working_hour = total_minutes / min_hr
        
        return working_hour

# Compute the working hour
def working_hour_computer(s):
    if '24/7' in s:
        working_hour = workingHours_tem.copy()
        for key in working_hour:
            working_hour[key] = 24.0
        return working_hour
    s = s.replace('; ', ';')
    s = s.replace(', ', ',')
    lst = [x.strip() for x in (s.split(';') if ';' in s else s.split(','))]
    working_hour = workingHours_tem.copy()
    for i in lst:
        segs = i.split(' ')
        segs[0] = segs[0].replace(',', '-')
        days = segs[0].split('-')
        if days[0] == 'PH':
            continue
        elif len(days) > 1 and days[1] == 'PH':
            days[1] = days[0]
        if days[0] not in daysOfweek or days[-1] not in daysOfweek:
            h = computeHours(segs[0])
            for key in working_hour:
                working_hour[key] = h
            return working_hour
        start, end = dayToindex(days[0]), dayToindex(days[-1]) + 1
        end += len(daysOfweek) if end < start else 0
        for idx in range(start, end + 1):
            if len(segs) > 1:
                segs[1] = segs[1].replace('+', '')
                working_hour[daysOfweek[idx % len(daysOfweek)]] = computeHours(segs[1])
            else:
                working_hour[daysOfweek[idx % len(daysOfweek)]] = computeHours("")
    for key in working_hour:
        if working_hour[key] == None:
            working_hour[key] = 0.0
    return working_hour

def main():
    input_file = sys.argv[1]
    data = pd.read_json(input_file, lines = True)
    # print(data)


    #Compute working hours of food amenities
    food = data[data['amenity'].str.contains("restaurant|food|cafe|pub|bar|ice_cream|food_court|bbq|bistro") & ~data['amenity'].str.contains("disused")]
    food = food.dropna()
    food = food[food.apply(lambda x: 'opening_hours' in x['tags'], axis = 1)]

    food['opening_hours'] = food.apply(lambda x: working_hour_computer(x['tags']['opening_hours']), axis = 1)

    food['opening_hours_per_week'] = food.apply(lambda x: sum([x['opening_hours'][day] for day in daysOfweek]), axis = 1)
    food = food[[
        'lat', 
        'lon', 
        'amenity', 
        'tags', 
        'opening_hours', 
        'opening_hours_per_week'
    ]]
    food = food[food['opening_hours_per_week'] >= 10.0]
    food = food.reset_index(drop = True)
    print(food)

    food.to_json("working_hours.json", orient = 'records', lines = True)



if __name__ == '__main__':
    main()
