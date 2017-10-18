from bs4 import BeautifulSoup
import unittest
import requests
import csv
#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their
##requirements, and what you need to understand.
## Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########

# Write your code for Part 0 here.
part_0_url = "http://newmantaylor.com/gallery.html"
part_0_data = requests.get(part_0_url).text
soup = BeautifulSoup(part_0_data, 'html.parser')
images = soup.find_all('img')

for image in images:
	print(str(image.get('alt', 'No alternative text provided!')))


######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except,
# but if you prefer to build up the code to do this scraping and caching yourself, that is OK.

try:
	nps_gov_data = open("nps_gov_data.html", "r").read()
except:
	nps_gov_data = requests.get("https://www.nps.gov/index.htm").text
	f = open("nps_gov_data.html","w")
	f.write(nps_gov_data)
	f.close()

# Get individual states' data...

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure
# that the rest of the program can access.
# TRY:
# To open and read all 3 of the files

# Note from README - start w/ BS object of gov't data
govt_data = BeautifulSoup(nps_gov_data, 'html.parser')
li = govt_data.find('ul', {'class':'dropdown-menu SearchBar-keywordSearch'}).find_all('a')
# Fetches data from cached soup instance of govt root url data
states = ['michigan', 'california', 'arkansas'] 
# States of interest to problem - keep these lower case to match to file names
# Try & Except clause - should be easy to just add a state on the fly, per README

for each_state in li:
    state = each_state.text
    if state in states:
        state_href = "http://www.nps.gov"+str(each_state.get('href'))
        fname = str(state)+"_data.html"
        print(state_href)
        try:
            state_data = open(fname, 'r').read()
        except:
            state_data = requests.get(state_href).text
            fn = open(fname, 'w')
            fn.write(state_data)
            fn.close()

# But if you can't, EXCEPT:

# Create a BeautifulSoup instance of main page data
# Access the unordered list with the states' dropdown

# Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method

# Use a list comprehension or accumulation to get all of the 'href' attributes of the 'a' tag objects in each li,
# instead of the full li objects

# Filter the list of relative URLs you just got to include only the 3 you want: AR's, CA's, MI's
# , using the accumulator pattern & conditional statements

# Create 3 URLs to access data from by appending those 3 href values to the main part of the NPS url.
# Save each URL in a variable.


## To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site.
# e.g. Maine parks URL is "http://www.nps.gov/state/me/index.htm",
# Michigan's is "http://www.nps.gov/state/mi/index.htm" --
# so if you compare that to the values in those href attributes you just got... how can you build the full URLs?


# Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause!
# Otherwise, all this code will run every time you run the program!)
# And then, write each set of data to a file so this won't have to run again.

michigan_data = open('michigan_data.html', 'r').read()
michigan_bs = BeautifulSoup(michigan_data, 'html.parser')
arkansas_data = open('arkansas_data.html', 'r').read()
arkansas_bs = BeautifulSoup(arkansas_data, 'html.parser')
california_data = open('california_data.html', 'r').read()
california_bs = BeautifulSoup(california_data, 'html.parser')

def get_each_states_parks(soup_object):
    list_of_parks = soup_object.find('ul', {'id':'list_parks'}).find_all('li', {'class':'clearfix'})
    return list_of_parks

######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation!
# So, of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state
# , but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park.
# However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition,
# you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions
# -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...

## Define your class NationalSite here:

## Recommendation: to test the class, at various points
## , uncomment the following code and invoke some of the methods
## / check out the instance variables of the test instance saved in the variable sample_inst:

class NationalSite(object):
	def __init__(self, each_park):
		self.location = each_park.find('div', {'class':'col-md-9 col-sm-9 col-xs-12 table-cell list_left'}).find('h4').get_text().strip() or "None"
		self.name = each_park.find('div', {'class':'col-md-9 col-sm-9 col-xs-12 table-cell list_left'}).find('h3').get_text().strip() or "None"
		self.type = each_park.find('div', {'class':'col-md-9 col-sm-9 col-xs-12 table-cell list_left'}).find('h2').get_text().strip() or "None"
		self.description = each_park.find('div', {'class':'col-md-9 col-sm-9 col-xs-12 table-cell list_left'}).find('p').get_text().strip() or ''
		self.url = str(each_park.find('div', {'class':'col-md-12 col-sm-12 noPadding stateListLinks'}).find_all('a')[1]['href'].strip())

	def __str__(self):
		return "{} | {}".format(self.name, self.location)

	def get_mailing_address(self):
		try:
			basic_info_url = self.url
			# fetch from this url to get address
			basic_info_resp = requests.get(basic_info_url).text
			# print(basic_info_url)
			sp = BeautifulSoup(basic_info_resp, 'html.parser')
			addressFull = sp.find('div', {'itemprop':'address'})
			streetAddress = addressFull.find('span', {'itemprop':'streetAddress'}).text.strip()
			localityAddress = addressFull.find('span', {'itemprop':'addressLocality'}).text.strip()
			stateAddress = addressFull.find('span', {'itemprop':'addressRegion'}).text.strip()
			codeAddress = addressFull.find('span', {'itemprop':'postalCode'}).text.strip()

			addressString = streetAddress.replace('\n','')+'/'+localityAddress.replace('\n','')
			+'/'+stateAddress.replace('\n','')+'/'+codeAddress.replace('\n','')
			return addressString
		except:
			addressString = ''
			return addressString

	def __contains__(self, additional_input):
		if additional_input in self.name:
			return True
		else:
			return False

###### TESTS #######
# f = open("sample_html_of_park.html",'r')
# soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
# sample_inst = NationalSite(soup_park_inst)
# print(sample_inst.name)
# print(sample_inst.url)
# print(sample_inst.location)
# f.close()

# list_of_michigan_parks = get_each_states_parks(michigan_bs)
# third_mich_park = list_of_michigan_parks[2]
# try1 = NationalSite(third_mich_park)
# print(try1)
# print("ABOVE IS TRY 1")

# fff = open('sample_html_of_park.html', 'r').read()
# ffff = BeautifulSoup(fff, 'html.parser')
# try2 = NationalSite(ffff)
# print(try2)
###### TESTS END #####
######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.

arkansas_list_of_parks = get_each_states_parks(arkansas_bs)
# print(len(arkansas_list_of_parks))
michigan_list_of_parks = get_each_states_parks(michigan_bs)
# print(len(michigan_list_of_parks))
california_list_of_parks = get_each_states_parks(california_bs)
# print(len(california_list_of_parks))

## sum of all the lengths of each list should = the number of rows in all of the CSV files! 
michigan_natl_sites = []
for park in michigan_list_of_parks:
	park_sp = NationalSite(park)
	michigan_natl_sites.append(park_sp)

arkansas_natl_sites = []
for park in arkansas_list_of_parks:
	park_sp = NationalSite(park)
	arkansas_natl_sites.append(park_sp)

california_natl_sites = []
for park in california_list_of_parks:
	park_sp = NationalSite(park)
	california_natl_sites.append(park_sp)

##Code to help you test these out:
# for p in california_natl_sites:
# 	print(p)
# for a in arkansas_natl_sites:
# 	print(a)
# for m in michigan_natl_sites:
# 	print(m)

# print(len(california_natl_sites)+len(arkansas_natl_sites)+len(michigan_natl_sites))

######### PART 4 #########

fieldnames = ['Name', 'Location', 'Type', 'Address', 'Description']

with open('arkansas.csv','w', newline='') as f:
	w = csv.writer(f, delimiter='|', quotechar='"')
	w.writerow(fieldnames)
	for site in arkansas_natl_sites:
		addr = site.get_mailing_address()
		addr.replace('\n','') #Just in case
		w.writerow([site.name.replace('\n',''), site.location.replace('\n',''), site.type.replace('\n',''), addr, site.description.replace('\n','')])

with open('michigan.csv','w', newline='') as f:
	w = csv.writer(f, delimiter='|', quotechar='"')
	w.writerow(fieldnames)
	for site in michigan_natl_sites:
		addr = site.get_mailing_address()
		addr.replace('\n','') #Just in case
		w.writerow([site.name.replace('\n',''), site.location.replace('\n',''), site.type.replace('\n',''), addr, site.description.replace('\n','')])

with open('california.csv','w', newline='') as f:
	w = csv.writer(f, delimiter='|', quotechar='"')
	w.writerow(fieldnames)
	for site in california_natl_sites:
		addr = site.get_mailing_address()
		addr.replace('\n','') #Just in case
		w.writerow([site.name.replace('\n',''), site.location.replace('\n',''), site.type.replace('\n',''), addr, site.description.replace('\n','')])

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run --
# so it's a good idea to test any methods/functions you write with just a little bit of data,
# so running the program will take less time!

## Also remember that IF you have None values that may occur,
# you might run into some problems and have to debug for where you need to put in some None value / error handling!
