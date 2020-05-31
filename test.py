import os,datetime,sys
sys.path.append("E:\云\OneDrive\code\python\cov19_dv")
sys.path.append("/home/ec2-user/cov19_dv/")
from django.shortcuts import render,HttpResponse
from django.contrib import messages
from django.http import HttpResponse, Http404, StreamingHttpResponse,FileResponse

from functions import system_varables,subscription_save,subscription_load,download_file,get_daily_increment_from_variables,chart_covid_themeRiver,chart_covid_daily_increasement


system_variables_path = "E:\云\OneDrive\code\python\cov19_dv\\"

# output_file_config = {
#     'covid_daily_increasement': {'file_name': "covid_daily_increasement.html_customized.html",
#                                  'output_path': system_variables_path + "\\Django - web\\templates\\", 'enable': True},
#     'covid_daily_update_themeRiver': {'file_name': "covid_daily_update_themeRiver_customized.html",
#                                       'output_path': system_variables_path + "\\Django - web\\templates\\", 'enable': True}
# }
#
# output_file_config = {
#     'covid_daily_increasement': {'file_name': "covid_daily_increasement.html_customized.html",
#                                  'output_path': system_variables_path + "\\Django - web\\templates\\", 'enable': True}
# }
#
#
# get_daily_increment_from_variables("2020_02_12", "2020_02_28",output_file_config)

#print('covid_daily_increasement' in output_file_config.keys())


output_file_config = {
    'covid_daily_update_themeRiver': {'file_name': "covid_daily_update_themeRiver_customized.html",
                                      'output_path': system_variables_path + "\\Django - web\\templates\\",
                                      'enable': True}
}

get_daily_increment_from_variables('2020_02_12', '2020_03_12', output_file_config)