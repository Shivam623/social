import urllib.request
import mysql.connector
import os
from datetime import datetime, date, timedelta
import sys
import csv
import telegram
from pytz import all_timezones
from dateutil import tz


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)


def time_zone_change():
    for zone in all_timezones:
        print(zone)
        # Asia/Kolkata

def convert_time_zone(from_zone, time_value):
    from_zone = tz.gettz(from_zone)
    to_zone = tz.gettz('Asia/Kolkata')
    time_value = datetime.strptime(str(time_value).replace('T',' ').strip('Z').split('+')[0].split('.')[0], '%Y-%m-%d %H:%M:%S')
    time_value = time_value.replace(tzinfo=from_zone)
    time_value = time_value.astimezone(to_zone)
    time_value = str(time_value).split('+')[0]
    return time_value


def news_api_key():
    return "72e45284f0b34bd9b2857ce324e88157"


def bot_token():
    return "459330012:AAHznymEYmBr1kWHYQz0AEYF05ULAJ977Jw"


def insert_or_update_or_delete(query):
    mydb = mysql.connector.connect(
        host="116.206.105.72",
        user="pythoqdx_shivam",
        passwd="Shyna@623",
        database="pythoqdx_Shynachat"
    )
    try:
        my_cursor = mydb.cursor()
        my_cursor.execute(query)
        mydb.commit()
    except Exception as e:
        print(e)
    finally:
        print("Query Performed")
        mydb.close()


def select_from_table(query):
    result = []
    my_db = mysql.connector.connect(
        host="116.206.105.72",
        user="pythoqdx_shivam",
        passwd="Shyna@623",
        database="pythoqdx_Shynachat"
    )
    try:
        my_cursor = my_db.cursor()
        my_cursor.execute(query)
        cursor = my_cursor.fetchall()
        if len(cursor) > 0:
            for row in cursor:
                result.append(row)
        else:
            result.append('Empty')
    except Exception as e:
        print("Exception is: \n", e)
        result = "Exception"
    finally:
        print("Query Performed")
        my_db.close()
        return result


def device_id():
    print("Returning Device ID")
    return 'Shyna_notification_device'


def get_time():
    now_time = datetime.now().time().__format__('%H:%M:%S')
    print("Returning", now_time)
    return now_time


def get_date():
    now_date = date.today()
    print("Returning", now_date)
    return now_date


def subtract_hour(from_time, how_many):
    from_time = str(from_time).split('.')[0]
    new_time = (datetime.strptime(str(from_time), '%H:%M:%S') - timedelta(hours=int(how_many))).time()
    print("Returning", new_time)
    return new_time


def subtract_date(from_date, how_many):
    new_date = datetime.strptime(str(from_date - timedelta(days=int(how_many))), '%Y-%m-%d')
    print("Returning", new_date)
    return new_date


def string_to_date(date_string):
    convert_date = datetime.strptime(str(date_string), '%Y-%m-%d')
    print("Returning", convert_date)
    return convert_date


def string_to_time(time_string):
    convert_time = datetime.strptime(str(time_string), '%H:%M:%S')
    print("Returning", convert_time)
    return convert_time


def add_notification(command, priority):
    query = "INSERT INTO notification_log (new_date, new_time, notification, priority, device_ID) VALUES ' \
                '('" + str(get_date()) + "', '" + str(get_time()) + "', '" + str(command) + "', '" + str(priority) + \
            "', '" + str(device_id()) + "')'"
    insert_or_update_or_delete(query=query)


def add_local_log(query, priority):
    # TODO: add log to local file and send it on email in case internet is not there
    # flow 10 add log into csv using panda
    result = "Adding notification"
    try:
        with open('notification_file.csv', mode='w') as notification_file:
            notification_writer = csv.writer(notification_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            notification_writer.writerow([str(get_date()), str(get_time()), str(query), str(priority), str(device_id())])
        result = "Notification added"
    except Exception as e:
        print(e)
        result = "Exception in Notification"
    finally:
        print(result)


def back_up_notification_log():
    # flow 9. Move old notification to new after each status change
    check = (last_speak_or_not()).lower()
    if check == 'change':
        query_1 = "Select * from notification_log"
        result_1 = select_from_table(query_1)
        for row in result_1:
            count = row[0]
            new_date = row[1]
            new_time = row[2]
            notification = row[3]
            priority = row[4]
            select_device_id = row[5]
            query_2 = "INSERT INTO old_notification_log (new_date, new_time, notification, priority, device_ID) VALUES ' \
                            '('" + str(new_date) + "', '" + str(new_time) + "', '" + str(notification) + "', '" + str(priority) + \
                      "', '" + str(select_device_id) + "')'"
            insert_or_update_or_delete(query_2)
            query_3 = "DELETE from notification_log where count =" + str(count)
            insert_or_update_or_delete(query_3)


def speak_or_not():
    #  Flow 5. it check what is the last status I send her. it is morning, silent, or sleep and return accordingly
    result = "awake"
    try:
        query = "SELECT greet_string FROM greeting order by count DESC limit 1;"
        cursor = select_from_table(query)
        if str(cursor).__contains__('Exception') or str(cursor).__contains__('Empty'):
            pass
        else:
            for row in cursor:
                greet_string = str(row[0])
                if len(greet_string) > 0:
                    if str(greet_string).lower() == 'morning':
                        result = 'awake'
                    if str(greet_string).lower() == 'silent':
                        result = 'silent'
                    if str(greet_string).lower() == 'sleep':
                        result = 'sleep'
                else:
                    result = 'awake'
    except Exception as e:
        print(e)
        result = "awake"
    finally:
        print(result)
        return result


def last_speak_or_not():
    # Flow 7. look for last two status and compare if they remain same or not and return accordingly
    result = 'no_change'
    try:
        query = "SELECT greet_string FROM greeting order by count DESC limit 2;"
        cursor = select_from_table(query)
        if str(cursor).__contains__('Exception') or str(cursor).__contains__('Empty'):
            result = 'change'
        else:
            for row in cursor:
                if row[0] == row[1]:
                    result = 'no_change'
                else:
                    result = 'change'
    except Exception as e:
        print(e)
        result = "no_change"
    finally:
        print(result)
        return result


def open_url():
    result = ""
    try:
        x = urllib.request.urlopen('https://www.google.com')
        response = x.read()
        if response == b'':
            result = "Fail"
        else:
            result = "Pass"
    except Exception as ex:
        result = "Fail"
    finally:
        print("Internet Connection", result)
        return result


def get_location():
    try:
        location_result = ''
        my_cmd = os.popen('termux-location').read()
        if str(my_cmd) != '':
            new_dict = eval(my_cmd)
            new_latitude = new_dict['latitude']
            new_longitude = new_dict['longitude']
            new_altitude = new_dict['altitude']
            new_accuracy = new_dict['accuracy']
            new_vertical_accuracy = new_dict['vertical_accuracy']
            new_bearing = new_dict['bearing']
            new_speed = new_dict['speed']
            new_elapsedMS = new_dict['elapsedMs']
            new_provider = new_dict['provider']
            new_date = str(date.today())
            new_time = str(datetime.now().strftime("%H:%M:%S"))
            query = "INSERT INTO shivam_device_location(new_date, new_time, new_latitude, new_longitude, new_altitude," \
                    "new_accuracy, new_vertical_accuracy, new_bearing, new_speed, new_elapsedMS, new_provider) VALUES " \
                    "('"+str(new_date) + "','"+ str(new_time) + "', '" + str(new_latitude)+ \
                    "', '" + str(new_longitude) + "', '" + str(new_altitude) + "', '"+ str(new_accuracy) + "', '" \
                    + str(new_vertical_accuracy) + "', '"+ str(new_bearing) + "', '" + str(new_speed) + "', '" \
                    + str(new_elapsedMS) + "','" + str(new_provider) + "')"
            insert_or_update_or_delete(query=query)
            location_result="Got Location"
        else:
            location_result="Empty location"
    except Exception as e:
        print(e)
        location_result = "Exception"
    finally:
        set_date_system()
        print(location_result)
        return str(datetime.now().strftime("%H:%M:%S"))


def set_date_system():
    query = "UPDATE last_run_check SET last_run = '"+str(get_date())+"' WHERE from_application='"+str(device_id())+"'"
    insert_or_update_or_delete(query)


def run_shivam_device_task(start, end):
    try:
        print("Checking task")
        task_list = []
        start = datetime.strptime(start, "%H:%M")
        end = datetime.strptime(end, "%H:%M:%S")
        mydb = mysql.connector.connect(
            host="116.206.105.72",
            user="pythoqdx_shivam",
            passwd="Shyna@623",
            database="pythoqdx_Shynachat"
        )
        mycursor = mydb.cursor()
        query = "SELECT task_name, task_time FROM shivam_device_task WHERE task_date = '"+str(get_date())+"'"
        mycursor.execute(query)
        cursor = mycursor.fetchall()
        for row in cursor:
            task_string = row[0]
            task_t = str(row[1])
            task_time = datetime.strptime(task_t, "%H:%M:%S")
            if start <= task_time <= end:
                task_list.append(task_string)
            else:
                pass
        task_list = list(dict.fromkeys(task_list))
        for item in task_list:
            if len(item) > 0:
                perform_commands(str(item))
            else:
                pass
    except Exception as e:
        print(e)
    finally:
        mydb.close()


def check_charge():
    try:
        dic_charge = perform_commands(command='termux-battery-status')
        charge = dic_charge['percentage']
        status = dic_charge['status']
        if int(charge) < 15 and str(status).lower() == 'discharging':
            perform_commands(command='termux-tts-speak "Hey! Shiv please plugin the charger. My battery is low"')
        elif int(charge) == 100 and str(status).lower() == 'charging':
            perform_commands(command='termux-tts-speak "Hey! Shiv please unplug the charger. My battery is full"')
        else:
            pass
    except Exception as e:
        print(e)


def update_check_charge():
    try:
        dic_charge = perform_commands('termux-battery-status')
        charge = dic_charge['percentage']
        plug_status = dic_charge['status']
        query = "INSERT INTO Battery_Status (new_time, new_date, device_id, plug_status, charge) VALUES('" \
                +str(get_time())+"','"+str(get_date())+"','"+str(device_id())+"','"+str(plug_status)+"','" \
                +str(charge)+"')"
        insert_or_update_or_delete(query=query)
    except Exception as e:
        print(e)


def check_wifi():
    wifi_status = ''
    try:
        wifi_info = os.popen('termux-wifi-connectioninfo').read()
        if str(wifi_info).__contains__('haridutt'):
            wifi_status = 'home'
            query = "INSERT INTO connection_check (connection_type, from_application, new_date, new_time) VALUES ('" \
                    + str(wifi_status) + "','" + str(device_id()) + "','" + str(get_date()) + "','" \
                    + str(get_time()) + "')"
            insert_or_update_or_delete(query)
        else:
            wifi_status = 'phone'
        query = "INSERT INTO connection_check (connection_type, from_application, new_date, new_time) VALUES ('" \
                +str(wifi_status)+"','"+str(device_id())+"','"+str(get_date())+"','"+str(get_time())+"')"
        insert_or_update_or_delete(query)
    except Exception as e:
        print(e)
    finally:
        return wifi_status


def change_in_wifi():
    count_phone = 0
    count_home = 0
    my_dict = {'phone': 0, 'home': 0}
    query = 'SELECT connection_type from connection_check order by count DESC limit 9'
    status_1=str(select_from_table(query)).replace("'",'').replace(")",'').replace("(",'').replace(",","").replace("[",'').replace("]",'').split(' ')
    my_dict = {i: status_1.count(i) for i in status_1}
    print(my_dict)
    if 2>count_phone-count_home > 0:
        perform_commands(command='termux-tts-speak "Hello! Shiv. Switching to phone data"')
    elif 2>count_home-count_phone > 0:
        perform_commands(command='termux-tts-speak "Hello! Shiv. Welcome back home"')
    else:
        pass


def perform_commands(command, priority=1):
    status = ""
    try:
        if str(command).__contains__('termux-tts-speak'):
            check = (speak_or_not()).lower()
            if str(check).__contains__('silent') and int(priority)==1:
                os.popen(command)
            elif str(check).__contains__('sleep') or (str(check).__contains__('silent') and int(priority)==0):
                add_notification(command, priority)
            else:
                os.popen(command)
        else:
            my_cmd = os.popen(command).read()
            status = eval(my_cmd)
    except Exception as e:
        print(e)
        status = "exception"
    finally:
        print(command,"Performed")
        return status


def shyna_chat():
    return "669082824"


def get_day_of_week():
    today_day = datetime.today().weekday()
    return str(today_day)


def master_telegram_chat_id():
    return "479223209"


def send_msg_to_master(message):
    token = bot_token()
    bot = telegram.Bot(token=token)
    try:
        speak_or_not_status = speak_or_not()
        if speak_or_not_status.__contains__('awake'):
            bot.send_message(chat_id=master_telegram_chat_id(), text=str(message))
    except Exception as e:
        print(e)
        bot.send_message(chat_id=master_telegram_chat_id(), text=str(e),timeout=20)
