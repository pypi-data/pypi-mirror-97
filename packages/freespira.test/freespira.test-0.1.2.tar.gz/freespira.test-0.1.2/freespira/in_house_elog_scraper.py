"""
Scrapes Freespiradata for elogs from a given patient id and parses them into txt and csv files
"""

import os
import shutil
import sys
from os import path
import pandas as pd
import matplotlib.pyplot as plt

from selenium import webdriver
import secrets

print('test')
header = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38," \
         "39,40,41,42,43 \n "

# import chrome driver and open fsd
driver = webdriver.Chrome(executable_path="Drivers/chromedriver.exe")
driver.get('https://freespiradata.net/scripts/login.php')

# input username and password
user_field = driver.find_element_by_xpath("//input[@name='user']")
user_field.send_keys(secrets.username)
pass_field = driver.find_element_by_xpath("//input[@name='pass']")
pass_field.send_keys(secrets.password)
submit_button = driver.find_element_by_xpath("//input[@type='submit']")
submit_button.click()

# go to specific patient
go_to_pat_link = driver.find_element_by_link_text('Go to Patient')
go_to_pat_link.click()
pat_id_field = driver.find_element_by_xpath("//input[@name='patient_id']")
patient_id = sys.argv[1]
pat_id_field.send_keys(patient_id)
desired_sensor = sys.argv[2]
if patient_id == '21002':
    table_num = '4'
else:
    table_num = '5'

# go to sessions
session_data_button = driver.find_element_by_xpath("//input[@value='Session Data']")
session_data_button.click()

# find the right table
table = driver.find_element_by_xpath("/html/body/table[" + table_num + "]")

# step through the rows in the table
sensor_count = 0
row_num = -1

rows = table.find_elements_by_xpath(".//tr/td[2]")
"""
for row in table.find_elements_by_xpath(".//tr"):
    row_num += 1
    num = 0
    table = driver.find_element_by_xpath("/html/body/table[5]")
    row = table.find_elements_by_xpath(".//tr")[row_num]
    for cell in row.find_elements_by_xpath(".//td"):
        if num == 1:
            sensor_num = cell.get_attribute("innerText")
            print(type(sensor_num))
            if sensor_num == desired_sensor:
                sensor_count += 1
            num = 0
            break
        print(sensor_count)
        num += 1
"""
sensor_num_rows = []
for row in rows:
    sensor_num_rows.append(row.get_attribute("innerText"))
indexes = [len(sensor_num_rows) - 1 - sensor_num_rows[::-1].index(desired_sensor)]

del sensor_num_rows[indexes[0]]
indexes.insert(0, len(sensor_num_rows) - 1 - sensor_num_rows[::-1].index(desired_sensor))
print(indexes)

row_num = -1
table = driver.find_element_by_xpath("/html/body/table[" + table_num + "]")
new_rows = [table.find_element_by_xpath(".//tr[" + str(indexes[0]) + "]"),
            table.find_element_by_xpath(".//tr[" + str(indexes[1]) + "]")]
# print(new_rows)

for row in new_rows:
    row_num += 1
    # print(row_num)

    num = 0
    unlock = 0
    table = driver.find_element_by_xpath("/html/body/table[" + table_num + "]")
    new_rows = [table.find_element_by_xpath(".//tr[" + str(indexes[0] + 1) + "]"),
                table.find_element_by_xpath(".//tr[" + str(indexes[1] + 1) + "]")]
    row = new_rows[row_num]
    for cell in row.find_elements_by_xpath(".//td"):
        if num == 5:
            if 'success' in cell.get_attribute("innerText"):
                unlock = 1
                status_str = "CalSuccess"
            if 'failure' in cell.get_attribute("innerText"):
                unlock = 1
                status_str = "CalFail"
        # open link in last column
        if num == 7 and unlock == 1:
            # get elog as string

            e_log_link = cell.find_element_by_xpath(".//a")
            e_log_link.click()
            e_log_str = driver.find_element_by_xpath(".//pre").get_attribute("innerText")

            # get sensor id
            index_of_sensor = e_log_str.find("sensor_id")
            index_of_new_line = e_log_str.find("\n", index_of_sensor)
            sensor_str = e_log_str[index_of_sensor: index_of_new_line]
            sensor_str = ''.join(i for i in sensor_str if i.isdigit())

            # get mu id
            index_of_mu = e_log_str.find("mu_id")
            index_of_new_line = e_log_str.find("\n", index_of_mu)
            mu_str = e_log_str[index_of_mu: index_of_new_line]
            mu_str = ''.join(i for i in mu_str if i.isdigit())
            if not mu_str:
                print('no mu id')

            # get date
            date_str = e_log_str[0: 10]

            # get time
            time_str = e_log_str[11: 19]
            time_str = time_str.replace(':', '')

            file_name = patient_id + "_" + sensor_str + "_" + mu_str + "_" + date_str + "_" + time_str + "_" + status_str + ".txt"
            # Check if "Outputs" path exists
            if os.path.isdir("Outputs/") == False:
                # Create all the dierctories in the given path
                os.makedirs("Outputs/")

            # Check if "Outputs/patient_id" path exists
            if os.path.isdir("Outputs/" + patient_id + "/") == False:
                # Create all the dierctories in the given path
                os.makedirs("Outputs/" + patient_id + "/")

            # Check if "Outputs/patient_id/TXT" path exists
            if os.path.isdir("Outputs/" + patient_id + "/TXT/") == False:
                # Create all the dierctories in the given path
                os.makedirs("Outputs/" + patient_id + "/TXT/")

                # Check if "Outputs/patient_id/CSV" path exists
            if os.path.isdir("Outputs/" + patient_id + "/CSV/") == False:
                # Create all the dierctories in the given path
                os.makedirs("Outputs/" + patient_id + "/CSV/")

            if path.exists("Outputs/" + file_name):
                driver.back()
                print("Log is duplicate")
                break

            file_object = open("Outputs/" + patient_id + "/" + file_name, "w+")
            file_object.write(e_log_str)
            print('created_log')
            driver.back()
            break
        num += 1

for filename in os.listdir("Outputs/" + patient_id + "/"):
    if patient_id in filename:
        filename = filename[:-4]
        # print(filename)
        with open("Outputs/" + patient_id + "/" + filename + '.txt') as file:
            data = file.read().replace(' ', ',')
            data = data.replace('\t', ',')
            data = data.replace('=', ',')
            data = data.replace(';', ',')

        if path.exists("Outputs/" + patient_id + "/CSV/" + filename + 'LONG.csv'):
            print("CSV already created for the log " + filename)
        else:
            file_object = open("Outputs/" + patient_id + "/CSV/" + filename + 'LONG.csv', "w+")
            csvdata = header + data
            file_object.write(csvdata)
            print('CSV created for log ' + filename)

    file_object.close()
    if filename == 'CSV' or filename == 'TXT' or filename == "Graphs":
        continue
    sourcePath = "Outputs/" + patient_id + "/" + filename + '.txt'
    dstDir = "Outputs/" + patient_id + "/TXT/"
    print('moving from ' + sourcePath + " to " + dstDir)
    if path.exists(dstDir + "/" + filename + ".txt"):
        print("Text file already in TXT folder for this elog")
    else:
        shutil.move(sourcePath, dstDir)

print('closing browser')
driver.close()

# getting rid of extra txt files that are saved as duplicates
for filename in os.listdir("Outputs/" + patient_id + "/"):
    if ".txt" in filename:
        os.remove("Outputs/" + patient_id + "/" + filename)

# trimming csv to only include until cal success or fail: need to make it graph only this
for filename in os.listdir("Outputs/" + patient_id + "/CSV"):
    if 'LONG.csv' in filename:
        if not path.exists("Outputs/" + patient_id + "/CSV" + filename[:-8] + ".csv"):
            short_filename = filename[:-8] + ".csv"
            file_object = open("Outputs/" + patient_id + "/CSV/" + short_filename, "w+")
            with open("Outputs/" + patient_id + "/CSV/" + filename) as file:
                csv_str = file.read()
                if "fs3e_cal_success" in csv_str:
                    index_of_end_cal = csv_str.rindex('fs3e_cal_success')
                elif "fs3e_cal_fail" in csv_str:
                    index_of_end_cal = csv_str.rindex('fs3e_cal_fail')
                else:
                    print("\n*****THIS LOG DOESN'T CONTAIN EITHER 'fs3e_cal_fail' OR 'fs3e_cal_success'******")
                    print(filename)
                    print("\n")
                    file_object.close()
                    os.remove("Outputs/" + patient_id + "/CSV/" + short_filename)
                    continue
                index_of_end = csv_str.index('\n', index_of_end_cal)
                csv_str = csv_str[0:index_of_end]
                file_object.write(csv_str)

# Added from JJ's script to create graphs
patient_id = sys.argv[1]
for csvfilename in os.listdir("Outputs/" + patient_id + "/CSV/"):
    if "LONG" in csvfilename:
        continue
    if desired_sensor not in csvfilename:
        continue
    # Read .csv file into pandas dataframe
    orig_filename = csvfilename
    csvfilename = "Outputs/" + patient_id + "/CSV/" + csvfilename
    # print(csvfilename)
    df = pd.read_csv(csvfilename)
    # print(df['6'])

    # Extract voltage data
    df_LEDA = df[df['5'] == 'LEDA']
    df_Voltage = df_LEDA[['2', '6']].reset_index()

    # Extract temperature and humidity data
    df_TEMP = df[df['7'] == 'TEMP'].reset_index()
    df_TH = df_TEMP[['2', '8', '10']]

    # Extract pressure data
    df_OPR = df[df['37'] == 'OPR'].reset_index()
    df_Pressure = df_OPR[['2', '38']]

    # Extract pump current data
    df_PC = df[df['11'] == 'PC'].reset_index()
    df_Pump = df_PC[['2', '12']]

    # Extract cal success data
    df_CAL = df[df['5'] == 'CHAN'].reset_index()

    # extract non average temp humid and pressure
    df_CAL_NON_AVE = df[df['3'] == 'fs3e_cal_success'].reset_index()

    # Extract cal fail data
    df_CALF = df[df['4'] == 'FS3CALFAIL'].reset_index()

    # Extract patient and sensor information
    df_PID = df[df['3'] == 'patient_id'].reset_index()
    df_SID = df[df['3'] == 'sensor_id'].reset_index()
    df_MID = df[df['3'] == 'fs3_mu_id'].reset_index()

    # Select temperature values corresponding to char values

    # print(df_Voltage['6'])
    index = df_Voltage['6'].astype(float).ne(0).idxmax()

    if index == 0:
        index = 1

    t6T = float(df_TH.loc[index - 1, '8'])
    sixTChar = round(((0.000797 * t6T * t6T) + (-0.120327 * t6T) + 4.500059), 3)

    trT = float(df_TH.loc[index + 1, '8'])
    roomTChar = round((-0.008796 * trT) + 0.541048, 3)

    # Graph extracted data
    fig, ax1 = plt.subplots(figsize=(10, 8))
    ax2 = ax1.twinx()

    ax2.plot(df_Voltage['2'], df_Voltage['6'].astype(float), color='blue', label='ChA Voltage (V)')
    ax1.plot(df_TH['2'], df_TH['8'].astype(float), color='red', label='Temperature (C)')
    ax1.plot(df_TH['2'], df_TH['10'].astype(float), color='green', label='Humidity (%)')
    ax1.plot(df_Pressure['2'], df_Pressure['38'].astype(float) * 0.0393701, color='purple', label='Pressure (inHg)')
    ax1.plot(df_Pump['2'], df_Pump['12'].astype(float), color='orange', label='Pump Current (mA)')

    # Scale axes
    ax2.set(ylim=(0, 3.5))
    ax1.set(ylim=(0, 100))

    # Set legend locations
    ax2.legend(loc='upper left')
    ax1.legend(loc='upper right')

    # Set and adjust axes labels
    ax1.set_ylabel('Voltage', labelpad=30, fontsize=16)
    ax2.set_ylabel('Temperature, Humidity, Pressure & Pump Current', labelpad=30, fontsize=16)

    # Remove dates from each axis
    ax1.axes.xaxis.set_visible(False)
    ax2.axes.xaxis.set_visible(False)

    # Switch cursor axis
    ax1.yaxis.set_ticks_position("right")
    ax2.yaxis.set_ticks_position("left")

    # Create relevant data table
    data = [[sixTChar, roomTChar, round(df_TH['8'].astype(float).mean(), 3), round(df_TH['10'].astype(float).mean(), 3)
                , round(df_Pressure['38'].astype(float).mean(), 3)]]

    columns = ["SixTChar (V)", "RoomAirTChar (V)", "Temperature Ave (C)", "Humidity Ave (%)", "Pressure Ave (mmHg)"]

    table = ax1.table(cellText=data, colLabels=columns, loc="bottom", bbox=[0.0, -0.15, 1, 0.1])
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Create success cal data table
    if not df_CAL.empty:
        # print("nicks computer has a ghost in it xxxxxxxxxxxxxxx")
        # print(df_CAL_NON_AVE)
        data2 = [[df_CAL.loc[0, '10'], df_CAL.loc[0, '12'], df_CAL.loc[0, '14'],df_CAL.loc[0, '16']]]

        columns2 = ["ChA Current (uA)", "ChA Gain", "ChA Offset (mV)", "ChA Previous CO2 (%CO2)"]

        table2 = ax1.table(cellText=data2, colLabels=columns2, loc="bottom", bbox=[0.0, -0.30, 1, 0.1])
        table2.auto_set_font_size(False)
        table2.set_fontsize(10)

        data4 = [[df_CAL.loc[0, '8'], df_CAL.loc[0, '20'], df_CAL.loc[0, '18']]]

        columns4 = ["Temperature at Cal", "Humidity at Cal", "Pressure at Cal"]

        table4 = ax1.table(cellText=data4, colLabels=columns4, loc="bottom", bbox=[0.0, -0.45, 1, 0.1])
        table4.auto_set_font_size(False)
        table4.set_fontsize(10)
    else:
        # print('nicks computer definitely has a ghost in ityyyyyyyyyyyyyyy')
        data3 = [[df_CALF.loc[0, '8'], df_CALF.loc[0, '16'], df_CALF.loc[0, '18']]]

        columns3 = ["ChA Previous CO2 (%CO2)", "Temperature at Cal", "Humidity at Cal"]

        table3 = ax1.table(cellText=data3, colLabels=columns3, loc="bottom", bbox=[0.0, -0.30, 1, 0.1])
        table3.auto_set_font_size(False)
        table3.set_fontsize(10)



    # Set title to elog ID information
    plt.title('ID:' + df_PID.loc[0, '4'] + '_SN:' + df_SID.loc[0, '4'] + '_MU:' + df_MID.loc[0, '4'], fontsize=20)
    plt.tight_layout(pad=1)

    plt.show()

    if not os.path.isdir("Outputs/" + patient_id + "/Graphs/"):
        os.makedirs("Outputs/" + patient_id + "/Graphs/")

    '''print(csvfilename)
    print(orig_filename)'''
    fig.savefig("Outputs/" + patient_id + "/Graphs/" + orig_filename[0:-4] + '.png')
