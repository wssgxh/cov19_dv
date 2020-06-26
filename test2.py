import pandas as pd
import bar_chart_race as bcr

import time
import datetime

#<img style="width:100%;" src="static/images/COVID-19_cases_by_China_province.gif" align="middle" />

start = datetime.datetime.now()

index_dict = {'covid19_tutorial': 'date',
                  'covid19': 'date',
                  'urban_pop': 'year',
                  'baseball': None}
# print(index_dict)

index_col = index_dict["covid19"]
parse_dates = [index_col] if index_col else None
print(index_col)
#abc = pd.read_csv("covid19_tutorial.csv", index_col=index_col, parse_dates=parse_dates)
abc = pd.read_csv("china_covid19.csv", index_col=index_col, parse_dates=parse_dates)


df = pd.read_csv("china_covid19.csv", index_col=index_col, parse_dates=parse_dates)
bcr.bar_chart_race(
    df=df,
    filename='covid19_cases_by_China_province.gif',

    title='COVID-19 cases by China province')


end = datetime.datetime.now()

print((end - start).seconds)