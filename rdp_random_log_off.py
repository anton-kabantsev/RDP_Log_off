import random, subprocess, sys, time, datetime, os.path

def logging(log_message):
    log_name = sys.path[1]+'\\'+str(datetime.date.today())+'.txt'
    if os.path.exists(log_name):
        log = open(log_name,"a")
    else:
        log = open(log_name, "w")
    log.write(str(datetime.datetime.now()) +' '+log_message + '\n')
    log.close()

def spaces_deletion(str):
    string = ''
    ind = 0
    for i in str.split():
        if ind > 0:
            string = string +' '+i.strip()
        else:
            string = string + i.strip()
        ind = ind +1
    return string

def str_parse(str, user_list):
    output = str.split('   ')
    for i in output:
        session_str = spaces_deletion(i)
        if session_str.find('rdp')==0:
            user_list.append(session_str)

def console(command,split=True):
    try:
        result = subprocess.check_output(command)
        if split:
            return result.decode('cp866').split("\n")
        else:
            return result.decode('cp866')
    except:
        logging('script error')

    return ('error')

def get_rdp_sessions():
    command = [sys.path[1]+'\\'+'quser.exe']
    output = console(command)
    user_list = []
    ind = 0
    while ind != len(output):
        str_parse(output[ind],user_list)
        ind = ind +1
    return user_list

def service_st_st():
    command = ['sc','query','Spooler']
    output = console(command)
    logging(spaces_deletion(output[3]))
    if output[3].find('RUNNING')>0:
        command = ['sc', 'stop', 'Spooler']
        try:
            console(command)
            logging('service stopped')
        except:
            logging("service wasn't stop")
    else:
        command = ['sc', 'start', 'Spooler']
        try:
            console(command)
            logging('service started')
        except:
            logging("service wasn't start")

def main_func():
    logging("logging started")
    #ind = 0
    while True:
        session_list = get_rdp_sessions()
        logging(str(session_list))
        if len(session_list)>0:
            command = ['reset','session',random.choice(session_list)]
            logging(str(command))
            #console(command)
            time.sleep(2)#60*10)
            service_st_st()
        #ind = ind +1
        #logging('index = '+str(ind))
        #if ind == 100:
        #    break
        time.sleep(2)#60*60*2)

main_func()