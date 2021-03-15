import paramiko
import getpass

def check_pwd(address, port, usr, pwd):
    try:
        client = paramiko.client.SSHClient()
        client.load_system_host_keys() # this loads any local ssh keys
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(address, port=port, username=usr, password=pwd)
        client.close()
        return True
    except:
        return False

def sftp(address, port, usr, pwd, fname):
    try:
        print("sftp port " + port + " of " + usr + "@" + address + ", transferring : " +
                     fname)
        client = paramiko.client.SSHClient()
        client.load_system_host_keys() # this loads any local ssh keys
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(address, port=port, username=usr, password=pwd)
        sftp = client.open_sftp() # type SFTPClient
        print(sftp.put(fname, fname)) #src, dest path/filename
        client.close()
    except IOError:
        print(".. host " + address + " is not up or some other error occured")
        return "host not up", "host not up"

authenticated = False
pwd = ''
while not authenticated:
    pwd = getpass.getpass(prompt='sftp password: ')
    authenticated = check_pwd("8.tcp.ngrok.io", "17387", "snc", pwd)
    if not authenticated:
        print('authentication failed. try again')
    else:
        print('authenticated.')
sftp("8.tcp.ngrok.io", "17387", "snc", pwd, "ex.txt")
