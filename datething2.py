from bs4 import BeautifulSoup
import time, re, datetime

f = open("testdata2.txt", "r")
testdata = f.read()
f.close()

testdata_soup = BeautifulSoup(testdata, 'html.parser')
testdata_parsed_list = []

""" Use this for lists within <option> markup, like with Nimax """
"""
testdata_parsed_list = testdata_soup.get_text().split('\n')
"""
#
""" Use this for stuff hidden in <tr>s of performances with <td>s of date/time """
"""
for tr in testdata_soup.findAll('tr'):
	timeitem = []
	for td in tr.findAll('td'):
		try:
			timeitem.append(td.string.encode('ascii', 'ignore'))
		except:
			pass
	time_pmless = re.sub('[^0-9]',' ', timeitem[1])
	time_pmless = time_pmless.rstrip()
	testdata_parsed_list.append(timeitem[0] + " " + time_pmless)

"""
#
""" Use this for HTML with <li> items and "showing" classes, like with Spectrix """
"""
for li in testdata_soup.findAll('li', {'class':'showing'}):
	timeitem = []
	for i in li.findAll('time'):
		timeitem.append(i.string.encode('ascii', 'ignore'))
	testdata_parsed_list.append(timeitem[1] + " " + timeitem[0])
"""

testdata_parsed_list_dtobj = []
for i in testdata_parsed_list:
	i = re.sub('[^0-9a-zA-Z]+', ' ', i)
	i = re.sub(r"(?<=\d)(st|nd|rd|th)", ' ', i)
	dtobject = time.strptime(i, "%A %d %B %Y %H %M")
	testdata_parsed_list_dtobj.append(dtobject)
	# %A day (full) %a day (abbreviated)
	# %d date 
	# %b month (abreviated) %B month (full) 
	# %Y year %H hour %M min

testdata_parsed_list_asweeks = {}
for i in testdata_parsed_list_dtobj:
	weeknum = datetime.date(i[0], i[1], i[2]).isocalendar()[1]
	year = i[0]
	try:
		testdata_parsed_list_asweeks[(weeknum, year)]
	except KeyError:
		testdata_parsed_list_asweeks[(weeknum, year)] = [i]
	else:
		testdata_parsed_list_asweeks[(weeknum, year)].append(i)

def rtn_daytime(timeobj):
	""" Returns the day, hour and minute """
	return (timeobj[6], timeobj[3], timeobj[4])

def rtn_isoweek(timeobj):
	""" Return the ISO calender week and year """
	week = datetime.date(timeobj[0], timeobj[1], timeobj[2]).isocalendar()[1]
	return (week, timeobj[0])

testdata_parsed_list_asweeks_unique = {}

for weeks in testdata_parsed_list_asweeks.keys():
	""" This loops through every week in the schedule, which is a dict with the week as key, dates as list data """
	if not testdata_parsed_list_asweeks_unique:
		testdata_parsed_list_asweeks_unique[weeks] = (testdata_parsed_list_asweeks[weeks], [rtn_isoweek(testdata_parsed_list_asweeks[weeks][0])])
	else:
		uniqueweek_check = []
		uniqueweek_refs = []
		
		"""
		We loop through the unique weeks.
			We loop through the dates in the unique week.
				We loop through the dates in the week we're testing.
					If the test date doesn't match any of the unique week's dates
						We append "Y" to the uniqueweek_check list
						We append unique week dict key to the uniqueweek_refs list
					Else
						We append "N" to the uniqueweek_check list
						We append unique week dict key to the uniqueweek_refs list
		We expect to see either ALL Ys or a single N in uniqueweek_check. 
		For index, item in enumerate uniqueweek_check
			If item == "N":
				Add the test week to Uniqueweeks_refs[index]'s entry in the parsed unique dict
		If "N" not in uniqueweek_check
			Add the test week as a unique week
		"""
		
		for weeks_tested in testdata_parsed_list_asweeks_unique.keys():
			""" This loops through the weeks we know are unique """
			testagainst = []
			isunique = False
			for date_uniqueweek in testdata_parsed_list_asweeks_unique[weeks_tested][0]:
				""" This loops through the date/time performances in a particular unique week """
				testagainst.append(rtn_daytime(date_uniqueweek))
			for dates_testweek in testdata_parsed_list_asweeks[weeks]:
				""" This loops through the date/time performances in a week key in the un-unique (mundane?) dict """
				untested = rtn_daytime(dates_testweek)
				if untested not in testagainst:
					isunique = True
			
			if isunique == False:
				""" For sneaky weeks where there's just less performances """
				if len(testdata_parsed_list_asweeks[weeks]) != len(testdata_parsed_list_asweeks_unique[weeks_tested][0]):
					isunique = True
			
			if isunique == True:
				uniqueweek_check.append("Y")
				uniqueweek_refs.append(weeks_tested)
			else:
				uniqueweek_check.append("N")
				uniqueweek_refs.append(weeks_tested)
		
		nocount = 0
		for index, item in enumerate(uniqueweek_check):
			if item == "N":
				""" It's not unique. Add to whatever week it matches """
				nocount += 1
				curr_iso = rtn_isoweek(testdata_parsed_list_asweeks[weeks][0])
				testdata_parsed_list_asweeks_unique[uniqueweek_refs[index]][1].append(curr_iso)
		if nocount > 1:
			""" It's not unique but for some reason matches more than one unique week """
			print "Unique checker still not written right :/"
		
		if "N" not in uniqueweek_check:
			""" It's unique, adds it as such """
			testdata_parsed_list_asweeks_unique[weeks] = (testdata_parsed_list_asweeks[weeks], [rtn_isoweek(testdata_parsed_list_asweeks[weeks][0])])

	
def rtn_daterange(date, list):
	""" Takes a date and list, returns the date and the last concurrent date for it in the list """
	startindex = list.index(date)
	enddate = ""
	for i in list[startindex:]:
		currentindex = list.index(i)
		try:
			if list[currentindex][0] == (list[currentindex + 1][0] - 1):
				""" Dates are concurrent """
				pass
			elif list[currentindex][0] == 52 and list[currentindex + 1][0] != 1 and list[currentindex][1] == (list[currentindex + 1][1] - 1):
				""" Following indice's week is 1 if this is 52, and years are concurrent """
				pass
			else:
				enddate = i
				break
		except IndexError:
			enddate = i
			break
	return date, enddate

print ""
print "The following date ranges have the following performance schedule:"
print ""

for weeks in testdata_parsed_list_asweeks_unique.keys():
	weekdata = testdata_parsed_list_asweeks_unique[weeks][0]
	isoweekdata = sorted(testdata_parsed_list_asweeks_unique[weeks][1], key=lambda x: (x[1], x[0]))
	dateranges = []
	
	"""
	Define function that takes a date and list and loops through until is finds the last concurrent date
		Returns tuple of first and last week-year pairs
	Loop through list. Call funtion on first item, then each returned values second date until the last
	date is the same as the last date in the list
	"""
	
	dateranges.append(rtn_daterange(isoweekdata[0], isoweekdata))
	while dateranges[-1][1] != isoweekdata[-1]:
		nexttestindex = isoweekdata.index(dateranges[-1][1]) + 1
		dateranges.append(rtn_daterange(isoweekdata[nexttestindex], isoweekdata))
	
	for i in dateranges:
		firstdateraw = str(i[0][1]) + "-W" + str(i[0][0])
		firstdate = datetime.datetime.strptime(firstdateraw + '-1', "%Y-W%W-%w")
		firstdate = firstdate.strftime("%A %d/%m/%Y")
		
		lastdateraw = str(i[1][1]) + "-W" + str(i[1][0])
		lastdate = datetime.datetime.strptime(lastdateraw + '-0', "%Y-W%W-%w")
		lastdate = lastdate.strftime("%A %d/%m/%Y")
		
		print str(firstdate) + " - " + str(lastdate)
		
	performances = []
	for i in weekdata:
		week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
		rawday = i[6]
		mins = "00"
		if str(i[4]) == "0":
			mins = "00"
		else:
			mins = str(i[4])
		performances.append(str(week[rawday]) + " " + str(i[3]) + ":" + mins)

	for i in performances:
		print i
	print ""