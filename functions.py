import time, datetime
import os, platform
import json,zipfile
from pyecharts import Line
from pyecharts import ThemeRiver, Page
from shutil import copyfile

# https://www.jianshu.com/p/e9dcfa2d7d65
# https://www.jianshu.com/p/c596d353a69e?utm_source=oschina-app


system_variables_path = "E:\云\OneDrive\code\python\cov19_dv\\"
#system_variables_path = "/home/ec2-user/cov19_dv/"

def system_varables():
    variables = {}
    with open(system_variables_path + 'variables.txt', "r", encoding='utf-8') as read_file:
        for line in read_file:
            item = line.split("=")
            variables[str(item[0])] = str(item[1]).replace("\n", "")
    # print(variables)
    return variables


system_varables = system_varables()


def log(LogID, time, LogMessage):
    LogTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    LogMessage = LogMessage
    LogID = "[" + LogID + "]"
    log = LogTime + LogID + ',' + LogMessage

    if (os.path.isfile("log.txt")) == False:
        f = open("log.txt", mode='w', encoding="utf-8")
        f.write(str(log))
    else:
        with open('log.txt', 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(log + '\n' + content)


sys = platform.system()
if sys == "Windows":
    pass
elif sys == "Linux":
    os.chdir(system_variables_path)


# def copy_result_to_django():
#     copyfile("./covid_daily_increasement.html", "./Django - web/templates/covid_daily_increasement.html")
#     copyfile("./China Map.html", "./Django - web/templates/China Map.html")
#     copyfile("./covid_daily_update_themeRiver.html", "./Django - web/templates/covid_daily_update_themeRiver.html")


def chart_covid_daily_increasement(output_file_config,result_date, result_increasement, result_confirmed):

    line = Line("daily confirmed cases on " +   str(result_date[1]) + " to " + str(result_date[-1]), width=1000, height=600)

    attr = result_date
    line.add('daily confirmed cases', attr, result_increasement, is_fill=True, line_opacity=0.2, area_opacity=0.4,
             is_smooth=True, legend_pos='40%')
    line.add("total confirmed case ", attr, result_confirmed, is_fill=True, line_opacity=0.2, area_opacity=0.4,
             legend_pos="70%")

    line.render(output_file_config["covid_daily_increasement"]["output_path"] + output_file_config["covid_daily_increasement"]["file_name"])
    log("0041", None, "chart_cov_daily_increasement Saved")


def chart_covid_themeRiver(output_file_config,file_counter, result_date, result_confirm, result_suspect, result_dead, result_heal):

    block = []
    result = []
    cov_item = ['result_confirm', 'result_suspect', 'result_dead', 'result_heal']
    loop_counter = 0

    for file in range(0, file_counter):

        for item in (result_confirm[file], result_suspect[file], result_dead[file], result_heal[file]):
            block.append(result_date[file].replace('_', '/'))
            block.append(item)
            block.append(cov_item[loop_counter])

            result.append(block)
            block = []
            loop_counter = loop_counter + 1

        loop_counter = 0
    log("0051", None, "theme river chart Saved")
    # print(result)

    sys = platform.system()
    if sys == "Windows":
        souce_data_path = (os.getcwd() + "\source_data\Tencent_news\\" + str(
            time.strftime("%Y_%m_%d", time.localtime())) + ".txt")
    elif sys == "Linux":

        souce_data_path = (os.getcwd() + "/source_data/Tencent_news/" + str(
            time.strftime("%Y_%m_%d", time.localtime())) + ".txt")

    page = Page()
    #chart = ThemeRiver("CoV_daily_update_themeRiver @ " + (time.ctime(os.stat(souce_data_path).st_mtime)), width=1000, height=600)

    chart = ThemeRiver("COVID daily update themeRiver @ " + str(result_date[1]) + " to " + str(result_date[-1]), width=1000,height=600)


    chart.add(cov_item, result, is_label_show=True, legend_pos='70%')
    page.add(chart)

    page.render(output_file_config["covid_daily_update_themeRiver"]["output_path"] + output_file_config["covid_daily_update_themeRiver"]["file_name"])


def get_daily_increment():

    # dirpath = "source_data/Tencent_news"
    #
    # sys = platform.system()
    # if sys == "Windows":
    #     dirpath = "source_data\Tencent_news"
    # elif sys == "Linux":
    #     dirpath = "source_data/Tencent_news"

    file_counter = 0

    result_date = []
    result_confirm = []
    result_increasement = []
    result_suspect = []
    result_dead = []
    result_heal = []

    # variables for calculating daily increasement
    before = 0
    after = 0

    for root, dirs, files in os.walk(system_variables_path+"source_data\Tencent_news"):

        files.sort()
        print(files)

        for file in files:

            #print (file.replace('.txt',''))

            if '.txt' not in os.path.join(root, file): continue
            result_date.append(str(file.replace('.txt', '')))
            with open(os.path.join(root, file), "r", encoding='utf-8') as f:
                data = json.loads(f.read())

                result_confirm.append(data['chinaTotal']['confirm'])
                result_suspect.append(data['chinaTotal']['suspect'])
                result_dead.append(data['chinaTotal']['dead'])
                result_heal.append(data['chinaTotal']['heal'])
                file_counter = file_counter + 1

                if file_counter == 1:
                    after = 0
                    result_increasement.append(0)
                    before = data['chinaTotal']['confirm']
                else:
                    after = data['chinaTotal']['confirm']
                    result_increasement.append(after - before)
                    before = after

    log("0061", None, "Get daily new data")

    #print(result_date,result_increasement,result_confirm)

    output_file_config = {
        'covid_daily_increasement': {'file_name': "covid_daily_increasement.html",
                                     'output_path': system_variables_path + "\\Django - web\\templates\\", 'enable': True},
        'covid_daily_update_themeRiver': {'file_name': "covid_daily_update_themeRiver.html",
                                          'output_path': system_variables_path + "\\Django - web\\templates\\", 'enable': True}
    }

    chart_covid_daily_increasement(output_file_config,result_date, result_increasement, result_confirm)
    chart_covid_themeRiver(output_file_config,file_counter, result_date, result_confirm, result_suspect, result_dead, result_heal)

def get_daily_increment_from_variables(from_date,to_date,output_file_config):


    # sys = platform.system()
    # if sys == "Windows":
    #     dirpath = "source_data\Tencent_news"
    # elif sys == "Linux":
    #     dirpath = "source_data/Tencent_news"

    file_counter = 0

    result_date = []
    result_confirm = []
    result_increasement = []
    result_suspect = []
    result_dead = []
    result_heal = []

    # variables for calculating daily increasement
    before = 0
    after = 0



    for root, dirs, files in os.walk(system_variables_path):

        files.sort()
        #print("files:",files)

        for file in files:



            if '.txt' not in os.path.join(root, file): continue
            if file.replace('.txt','') < from_date or file.replace('.txt','') > to_date :continue

            result_date.append(str(file.replace('.txt', '')))
            #print(file.replace('.txt', ''))


            with open(os.path.join(root, file), "r", encoding='utf-8') as f:
                data = json.loads(f.read())

                result_confirm.append(data['chinaTotal']['confirm'])
                result_suspect.append(data['chinaTotal']['suspect'])
                result_dead.append(data['chinaTotal']['dead'])
                result_heal.append(data['chinaTotal']['heal'])
                file_counter = file_counter + 1

                if file_counter == 1:
                    after = 0
                    result_increasement.append(0)
                    before = data['chinaTotal']['confirm']
                else:
                    after = data['chinaTotal']['confirm']
                    result_increasement.append(after - before)
                    before = after


    #print(result_date)

    if ('covid_daily_increasement' in output_file_config.keys()):
        print('^ 1')
        if  output_file_config["covid_daily_increasement"]["enable"] == True :
            chart_covid_daily_increasement(output_file_config,result_date, result_increasement, result_confirm)

    if ('covid_daily_update_themeRiver' in output_file_config.keys()):
        print('^ 2')
        if  output_file_config["covid_daily_update_themeRiver"]["enable"] == True :
            chart_covid_themeRiver(output_file_config,file_counter, result_date, result_confirm, result_suspect, result_dead, result_heal)


def subscription_save(name,email,frequency):

    if (os.path.isfile(system_variables_path + "source_data/subscription_list.txt")) == False:
        f = open(system_variables_path + "source_data/subscription_list.txt", mode='w', encoding="utf-8")
        print("subscription_list.txt not existed -> file created")

    log = name + "," + email + "," + frequency
    with open(system_variables_path + 'source_data/subscription_list.txt', 'r+') as f:
        content = f.read()

        if content.count(email) >= 1:
            print('Error:email already exitsed')
            #log('0070', None, "Error:email already exitsed")

        else:
            f.seek(0, 0)
            f.write(log + '\n' + content)
            print('subscription content saved')
            #log('0081', None, "subscription content saved")

    return True

def subscription_load():

    if (os.path.isfile(system_variables_path + "source_data/subscription_list.txt")) == False:
        if (os.path.isfile(system_variables_path + "source_data/subscription_list.txt")) == False:
            f = open(system_variables_path + "source_data/subscription_list.txt", mode='w', encoding="utf-8")
            print("subscription_list.txt not existed -> file created")



    with open(system_variables_path + "source_data/subscription_list.txt", 'r+') as f:
        lines = f.readlines()

    result = []
    for line in lines:
        result.append(line.replace("\n", ""))
    return result

def download_file(from_date,to_date):



    from_date = from_date.replace('-','_')
    to_date = to_date.replace('-','_')

    #print('input is :',from_date, to_date)

    dirpath = "source_data/Tencent_news"

    sys = platform.system()
    if sys == "Windows":
        dirpath = 'source_data\Tencent_news\\'
        beginner = '..\\'

    elif sys == "Linux":
        dirpath = "source_data/Tencent_news/"
        beginner = '..//'

    result = []
    temp_dirpath = ''
    temp = []

    if  os.path.exists("..//" + dirpath):

        temp_dirpath = ("..//" + dirpath)

        print(1)

    elif os.path.exists("..\\" + dirpath):

        temp_dirpath = os.walk("..\\" + dirpath)
        print('2')
    else:
        temp_dirpath = dirpath
        print('3')

    if os.path.exists(temp_dirpath + 'file.zip'): os.remove(temp_dirpath + 'file.zip')

    #for root, dirs, files in os.walk("..\\" + dirpath):

    create_zip_file = zipfile.ZipFile(temp_dirpath + 'file.zip', mode='a', compression=zipfile.ZIP_DEFLATED)


    for root, dirs, files in os.walk(temp_dirpath):

        files.sort()
        #print(files)

        for file in files:

            if file > from_date and file < to_date:

                #print(file)

                temp.append(file)
                temp.append(temp_dirpath + file)
                result.append(temp)
                temp = []

                create_zip_file.write(temp_dirpath + file , file, zipfile.ZIP_DEFLATED)

        create_zip_file.close()

    print("fiel zipped :" , result)

    return temp_dirpath + 'file.zip'

def send_email(subject,body,receiver_email):


    # message = """\
    # Subject: Hi there
    #
    # This message is sent from Python."""
    # send_email("wssgxh@gmail.com",message)
    import email, smtplib, ssl

    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    #subject = "COVID 19 Daily Notification"
    #body = "The status of today is ........................"
    sender_email = "covid19dailynotification"
    #receiver_email = "wssgxh@gmail.com"
    password = "Wssgxh12"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "document.pdf"  # In same directory as script

    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


if __name__ == '__main__':


    '''
    Daily Tasks
    
    '''
	# create charts
    get_daily_increment()

    #copy_result_to_django()

    # send e-mail based on subscription list
    # for each_item in subscription_load():
    #     reciveder_address = each_item.split(",")[1]
    #     send_email("COVID 19 Daily Notification", "The status of today is ........................", reciveder_address)
    #     print(reciveder_address, " in subscription list has been sent ")

    '''
    Test
    
    '''
    #data = get_daily_increment()
    #subscription_save("xinghe","shanggu123anxinghe@gmail.com","daily")
    #print(subscription_load())
    #download_file('2020-02-10','2020-02-18')
