from datetime import datetime
from urllib import request
from bs4 import BeautifulSoup

# Grabs SP 500 table from CBOE "Total options data"
def getLatest():
    system_time = str(datetime.now().time()).split(":")
    system_day = int(datetime.today().weekday())

    CBOE_options_page = BeautifulSoup(request.urlopen("http://www.cboe.com/data/intradayvol.aspx"), "html.parser")
    table = CBOE_options_page.find_all("table")
    table = table[5] # SP 500 table

    table_data = table.findAll('tr')
    table = [] # table = {}
    for row in table_data[1:]:
        row = str(row.text).split('\n')

        time = row[1]
        time_of_day = time.split(' ')[1]
        hour = time.split(' ')[0].split(':')[0]
        minute = time.split(' ')[0].split(':')[1]

        calls = row[2]
        puts = row[3]
        total = row[4]

        # Convert to military time
        if("PM" in time_of_day and int(hour) != 12):
            time = str(int(hour[0])+12)+":"+minute
        else:
            time = str(int(hour))+":"+minute

		# Determine market status
        status = ["open","success"]
        if(system_day > 4 or int(system_time[0]) < 9 or int(system_time[0]) >= 16):
        	status = ["closed","danger"]

		# Add all non-null data to table
        if(calls != '\xa0' and puts != '\xa0'):
            ratio = float(int(puts) / int(calls))
            calls_centage = float(int(calls) / int(total))*100
            puts_centage = float(int(puts) / int(total))*100

            table.append({"time":time,"calls":int(calls), "puts":int(puts),"total":int(total),"call_centage":float(calls_centage),"put_centage":float(puts_centage),"ratio":float(ratio),"status":status})

    return table[-1] # Get latest data

# Returns array of all SP 500 table rows from CBOE
def getAll():
    system_time = str(datetime.now().time()).split(":")
    system_day = int(datetime.today().weekday())

    CBOE_options_page = BeautifulSoup(request.urlopen("http://www.cboe.com/data/intradayvol.aspx"), "html.parser")
    table = CBOE_options_page.find_all("table")
    table = table[5] # SP 500 table

    table_data = table.findAll('tr')
    table = [] # table = {}
    for row in table_data[1:]:
        row = str(row.text).split('\n')

        time = row[1]
        time_of_day = time.split(' ')[1]
        hour = time.split(' ')[0].split(':')[0]
        minute = time.split(' ')[0].split(':')[1]

        calls = row[2]
        puts = row[3]
        total = row[4]

        # Convert to military time
        if("PM" in time_of_day and int(hour) != 12):
            time = str(int(hour[0])+12)+":"+minute
        else:
            time = str(int(hour))+":"+minute

		# Determine market status
        status = ["open","success"]
        if(system_day > 4 or int(system_time[0]) < 9 or int(system_time[0]) >= 16):
        	status = ["closed","danger"]

		# Add all non-null data to table
        if(calls != '\xa0' and puts != '\xa0'):
            ratio = float(int(puts) / int(calls))
            calls_centage = float(int(calls) / int(total))*100
            puts_centage = float(int(puts) / int(total))*100

            table.append({"time":time,"calls":int(calls), "puts":int(puts),"total":int(total),"call_centage":float(calls_centage),"put_centage":float(puts_centage),"ratio":float(ratio),"status":status})

    return table # Get latest data
