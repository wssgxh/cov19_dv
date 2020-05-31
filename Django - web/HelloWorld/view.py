import os,datetime,sys
sys.path.append("E:\云\OneDrive\code\python\cov19_dv")
sys.path.append("/home/ec2-user/cov19_dv/")
from django.shortcuts import render,HttpResponse
from django.contrib import messages
from django.http import HttpResponse, Http404, StreamingHttpResponse,FileResponse

from functions import system_varables,subscription_save,subscription_load,download_file,get_daily_increment_from_variables,chart_covid_themeRiver,chart_covid_daily_increasement

system_variables_path = "E:\云\OneDrive\code\python\cov19_dv\\"

def system_varables():

    #system_variables_path = "E:\云\OneDrive\code\python\cov19_dv\\"

    variables = dict()
    with open(system_variables_path + 'variables.txt', "r", encoding='utf-8') as read_file:
        for line in read_file:
            item = line.split("=")
            variables[str(item[0])] = str(item[1]).replace("\n","")
    print(variables)
    return variables

def days_of_cov_19():
    now_str = datetime.datetime.now().strftime('%Y-%m-%d')
    now = datetime.datetime.strptime(now_str, "%Y-%m-%d")
    future = datetime.datetime.strptime("2020-01-30", "%Y-%m-%d")
    return  -(future - now).days


def covid_daily_increasement(request):
    return render(request, 'covid_daily_increasement.html')

def china_map(request):
   ## return render(request, 'China_Map.html')
   return render(request, 'China_Map.html')

def covid_daily_update_themeRiver(request):
    return render(request, 'covid_daily_update_themeRiver.html')

def index(request):

    context = {}
    context['days_of_cov_19'] = days_of_cov_19()

    if  request.method == 'POST' and  request.POST.get('email')  :
        email = request.POST.get('email')

        if  subscription_save("None",email,"Daily") is True:
            return HttpResponse("Your Email address has been saved")

    if  request.method == 'POST' and  request.POST.get('source_data_from_date') and  request.POST.get('source_data_to_date') :

        From_date = request.POST.get('source_data_from_date')
        To_date = request.POST.get('source_data_to_date')

        try:
            datetime.datetime.strptime(From_date, '%Y-%m-%d')
            datetime.datetime.strptime(To_date, '%Y-%m-%d')
        except ValueError:
            return HttpResponse("Incorrect data format, should be YYYY-MM-DD")

        if From_date>= To_date:return HttpResponse("Incorrect data Range, From > To")

        file_list = download_file(str(From_date),str(To_date))

        #file = open('../' + file_list[0][1], 'rb')

        file = open(file_list, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=' + 'file.zip'

        return response

    if request.method == 'POST' and request.POST.get('increasement_from_date') and request.POST.get('increasement_to_date'):

        From_date = str(request.POST.get('increasement_from_date')).replace("-","_")
        To_date = str(request.POST.get('increasement_to_date')).replace("-","_")

        try:
            datetime.datetime.strptime(From_date, '%Y_%m_%d')
            datetime.datetime.strptime(To_date, '%Y_%m_%d')
        except ValueError:
            return HttpResponse("Incorrect data format, it should be YYYY-MM-DD")
        try:

            ''' 
             file_name : file is the output file name (output_path + file_name)
             enable : True = file will created , false = file will not be created  
             '''
            output_file_config = {
                'covid_daily_increasement': {'file_name': "covid_daily_increasement.html_customized.html",
                                             'output_path': system_variables_path + "\\Django - web\\templates\\",
                                             'enable': True}
            }

            get_daily_increment_from_variables(From_date,To_date,output_file_config)
            return render(request , 'covid_daily_increasement.html_customized.html')

        except IndexError:
            return HttpResponse("No Data")

    if request.method == 'POST' and request.POST.get('themeRiver_from_date') and request.POST.get('themeRiver_to_date'):

        From_date = str(request.POST.get('themeRiver_from_date')).replace("-","_")
        To_date = str(request.POST.get('themeRiver_to_date')).replace("-","_")

        try:
            datetime.datetime.strptime(From_date, '%Y_%m_%d')
            datetime.datetime.strptime(To_date, '%Y_%m_%d')
        except ValueError:
            return HttpResponse("Incorrect data format, it should be YYYY-MM-DD")
        try:

            ''' 
             file_name : file is the output file name (output_path + file_name)
             enable : True = file will created , false = file will not be created  
             '''
            output_file_config = {
                'covid_daily_update_themeRiver': {'file_name': "covid_daily_update_themeRiver_customized.html",
                                                      'output_path': system_variables_path + "\\Django - web\\templates\\", 'enable': True}
                }


            get_daily_increment_from_variables(From_date,To_date,output_file_config)
            return render(request , 'covid_daily_update_themeRiver_customized.html')

        except IndexError:
            return HttpResponse("No Data")




    return render(request, 'index.html',context)

def admin(request):
    os.chdir(os.path.dirname(os.getcwd()))
    os.system("python3 main.py")
    return HttpResponse("source data has been refreshed")

def read_log(request):

    txt = []
    sys_varables = system_varables()
    with open(system_variables_path + 'log.txt', "r", encoding='utf-8') as read_file:
        for line in read_file:
            txt.append(line + "<br>")
    return HttpResponse(txt)

def page_covid_daily_increasement_customized():
    return render(request, 'covid_daily_increasement.html_customized.html')

def covid_daily_update_themeRiver_customized():
    return render(request, 'covid_daily_update_themeRiver_customized.html')


# def subscription_list(request):
#
#     lines = subscription_load()
#
#     name = []
#     email_address =[]
#     frequency = []
#
#     for line in lines:
#         line = line.split(',')
#         name.append(line[0])
#         email_address.append((line[1]))
#         frequency.append((line[2]).replace("\n", ""))
#
#         html= {}
#         html['html'] =  "<tr><td>row 1, cell 1</td><td>row 1, cell 2</td></tr>"
#
#     return render(request, 'table.html',html)



if __name__ == '__main__':

    get_daily_increment_from_variables("2020_02_12", "2020_02_28","../../source_data/Tencent_news")
