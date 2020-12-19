
import bs4, requests
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import time
import string
import os
import tkinter as tk

window = tk.Tk()

frame_a = tk.Frame()
frame_b = tk.Frame()

query = "python"
location = "Manchester"

indeedlink = f"https://www.indeed.co.uk/jobs?q={query}&l={location}&radius=15"

recruitlist = []
companylist = []
rolelist=[]
titlelist = []
pricelist =[]
summarylist = []
reedcompanylist = []
reedrolelist=[]


def indeedfind(link):
	filelist = open('\recruitnamelist.txt','r')
	namelist = []
	for x in filelist:
		clean = x.strip()
		namelist.append(clean)

	res=requests.get(link)
	res.raise_for_status
	soup =bs4.BeautifulSoup(res.text, 'html.parser')
	for found in soup.find_all('span', 'company'):
		if found:
			entry = found.text
			entryclean = entry.strip()
			if entryclean in namelist:
				companylist.append(f"***RECRUITMENT COMPANY--{entryclean}")
			else:
				companylist.append(entryclean)

	for found2 in soup.find_all('h2', 'title'):
		if found2:
			role = found2.text
			roleclean = role.strip()
			rolelist.append(roleclean)

	for found3 in soup.find_all ('div', 'summary'):
		if found3:
			summary = found3.text
			summarylist.append(summary)
			
def reedfind(link):
	namelist2 = []
	filelist = open('\recruitnamelist.txt','r')
	for x in filelist:
		clean = x.strip()
		namelist2.append(clean)
	namelist = []
	res=requests.get(link)
	res.raise_for_status
	soup =bs4.BeautifulSoup(res.text, 'html.parser')
	for found in soup.find_all('div', 'posted-by'):
		if found:
			condensed = found.find('a','gtmJobListingPostedBy')
			found2 = condensed.text
			foundend = found2.strip()
			if foundend in namelist2:
				reedcompanylist.append(f"{foundend}<------*RECRUITMENT COMPANY*------->")
					#recruitlist.append(foundsnip.text)
			else:
				reedcompanylist.append(foundend)
		for found in soup.find_all('h3', 'title'):
			if found:
				reedrolelist.append(found.text)

foundreedlinks = []

def reedscrape():
	for x in range(1, 5):
		reedfind(f"https://www.reed.co.uk/jobs/{query}-jobs-in-{location}?pageno={x}")
	for entry in range (len(reedcompanylist)):
		if "RECRUITER" in reedcompanylist[entry]:
			pass
		else:
			#print("---------Reed-----------")
			foundreedlinks.append(f"COMPANY:{reedcompanylist[entry]}")
			return(f" ROLE:{reedrolelist[entry]}")


foundindeedlinks = []


def indeedscrape():
	urlamount = ['0','10','20','30','40','40','60','70','80', '90','100']
	for x in urlamount:
		indeedfind(f"https://www.indeed.co.uk/jobs?q={query}&l={location}&radius=15&start={x}")
		for x in range(len(companylist)):
			#return("----------------")
			foundindeedlinks.append(f"POSTED BY: {companylist[x]}")
			return(f" Found: {companylist[x]}")

indeedscrape()
reedscrape()

def indeedlabel():
	text_box = tk.Text(frame_a, width=60, height=50)
	for item in companylist:
		if "RECRUITER" in item:
			pass
		else:
			text_box.insert(tk.END, item + '\n')
			text_box.pack()

def reedlabel():
	text_box = tk.Text(frame_b, width=60, height=50)
	for item in reedcompanylist:
		if "RECRUITER" in item:
			pass
		else:
			text_box.insert(tk.END, item + '\n')
			text_box.pack()
			

text_boxa = tk.Button(master =frame_a, text = "Indeed", command = indeedlabel)
text_boxa.pack()
text_boxb = tk.Button(master =frame_b, text = "Reed")
text_boxb.pack()

indeedlabel()
reedlabel()

frame_a.pack(fill=tk.X, side=tk.LEFT) 
frame_b.pack(fill=tk.X, side=tk.RIGHT)

window.mainloop()

