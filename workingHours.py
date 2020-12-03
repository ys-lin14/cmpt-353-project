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


