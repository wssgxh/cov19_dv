import paramiko
def send_file_to_aws(file_path,destination):
    hostname = 'ec2-18-208-183-153.compute-1.amazonaws.com'
    myuser   = 'ec2-user'
    mySSHK   = "E:\\OneDrive\\admin\\FYP\\xinghefyp_studnet_account_converted.ppk"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname = hostname, username=myuser, key_filename=mySSHK)

    sftp = ssh.open_sftp()

    sftp.put(file_path, destination)

    # stdin, stdout, stderr = ssh.exec_command('ls')
    # print (stdout.readlines())
    ssh.close()
    print('file has been transferred to aws')

send_file_to_aws(r'E:\OneDrive\code\python\cov19_dv\Django - web\static\images\covid19_cases_by_China_province.gif','/home/ec2-user/cov19_dv/Django - web/static/images/covid19_cases_by_China_province.gif')