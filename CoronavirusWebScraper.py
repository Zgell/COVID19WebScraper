import tkinter as tk
from datetime import date, datetime
from math import ceil, log
from time import sleep

import requests
from bs4 import BeautifulSoup

global cases_number
cases_number = 0

death_number = 0
recovered = 0
prev_cases = 0
prev_deaths = 0
prev_recovered = 0

print("Loading...")
print("")

root = tk.Tk()
BGCOLOR = '#%02x%02x%02x' % (30, 30, 30)
root.title('Coronavirus Live Statistics')
root.configure(background = BGCOLOR)
title = tk.Label(root, text="Coronavirus Statistics", font = "Arial 32 bold underline", fg = "white", bg = BGCOLOR)
title.pack(padx = 20, pady = 10)

def prev_cases(pc):
    prev_cases.previous_cases = pc

def prev_deaths(pd):
    prev_deaths.previous_deaths = pd

def prev_recovered(pr):
    prev_recovered.previous_recovered = pr

prev_cases.previous_cases = ""
prev_deaths.previous_deaths = ""
prev_recovered.previous_recovered = ""

label_time = tk.Label(root, text = "Time: " + datetime.now().strftime("%H:%M:%S") + " " + date.today().strftime("%m/%d/%Y"), font = "Arial 16", fg = "white", bg = BGCOLOR)
label_time.pack()
label_total_cases = tk.Label(root, text = "Total Cases Worldwide: Loading...", font = "Arial 16", fg = "white", bg = BGCOLOR)
label_total_cases.pack()
label_total_deaths = tk.Label(root, text = "Total Deaths Worldwide: Loading...", font = "Arial 16", fg = "white", bg = BGCOLOR)
label_total_deaths.pack()
label_total_recovered = tk.Label(root, text = "Total Recovered Worldwide: Loading...", font = "Arial 16", fg = "white", bg = BGCOLOR)
label_total_recovered.pack()
label_active_cases = tk.Label(root, text = "Active Cases: Loading...", font = "Arial 16", fg = "white", bg = BGCOLOR)
label_active_cases.pack()
label_closed_cases = tk.Label(root, text = "Closed Cases: Loading...", font = "Arial 16", fg = "white", bg = BGCOLOR)
label_closed_cases.pack()
label_net_mortality = tk.Label(root, text = "Net Mortality of Closed Cases: Loading...", font = "Arial 16", fg = "white", bg = BGCOLOR)
label_net_mortality.pack()

def check_stats():
    page = requests.get('https://www.worldometers.info/coronavirus/')
    soup = BeautifulSoup(page.content, 'html.parser')
    mcw = soup.find_all(id='maincounter-wrap')
    
    # Total Coronavirus Cases
    cases = mcw[0].find(class_='maincounter-number').get_text()
    cases = cases.strip('\n')
    cases = cases.strip(' ')
    #prev_cases = cases_number
    prev_cases.previous_cases = label_total_cases['text'].replace(',','')
    cases_number = int(cases.replace(',',''))

    # Total Coronavirus Deaths
    deaths = mcw[1].find(class_='maincounter-number').get_text()
    deaths = deaths.strip('\n')
    deaths = deaths.strip(' ')
    #prev_deaths = death_number
    death_number = int(deaths.replace(',', ''))

    # Total Recovered
    rec = mcw[2].find(class_='maincounter-number').get_text()
    rec = rec.strip('\n')
    rec = rec.strip(' ')
    #prev_recovered = recovered
    recovered = int(rec.replace(',', ''))

    # All Closed Cases (THERE ARE MORE THAN ONE OF THESE!!!)
    panel = soup.find_all(class_ = "panel_front")
    active_cases = panel[0].find(class_ = "number-table-main").get_text()
    closed_cases = panel[1].find(class_ = "number-table-main").get_text()
    mortality = 100 * death_number / (int(closed_cases.replace(',','')))

    # Get the Change in Cases, Deaths, Recovered, etc.
    # if (prev_cases != 0) and (cases_number - prev_cases) != 0:
    #     delta_cases = "("
    #     if (cases_number - prev_cases) > 0:
    #         delta_cases += "+"
    #     elif (cases_number - prev_cases) < 0:
    #         delta_cases += "-"
    #     delta_cases += (str(cases_number - prev_cases) + ")")
    # else:
    #     delta_cases = ""

    # if (prev_deaths != 0) and (death_number - prev_deaths) != 0:
    #     delta_deaths = "("
    #     if (death_number - prev_deaths) > 0:
    #         delta_deaths += "+"
    #     elif (death_number - prev_deaths) < 0:
    #         delta_deaths += "-"
    #     delta_deaths += (str(death_number - prev_deaths) + ")")
    # else:
    #     delta_deaths = ""

    # if (prev_recovered != 0) and (recovered - prev_recovered) != 0:
    #     delta_rec = "("
    #     if (recovered - prev_recovered) > 0:
    #         delta_rec += "+"
    #     elif (recovered - prev_recovered) < 0:
    #         delta_rec += "-"
    #     delta_rec += (str(recovered - prev_recovered) + ")")
    # else:
    #     delta_rec = ""

    # Display the Results
    if 1 == 1: #(cases_number - prev_cases) != 0 or (death_number - prev_deaths) != 0 or (recovered - prev_recovered) != 0:
        JCONST = 14 # A justification constant for keeping info tidy
        #print(current_date + " " + current_time)
        label_time.config(text = "Time: " + datetime.now().strftime("%H:%M:%S") + " " + date.today().strftime("%m/%d/%Y"))
        print("Total Cases Worldwide: " + cases.rjust(JCONST)) #+ delta_cases.rjust(10)
        label_total_cases.config(text = "Total Cases Worldwide: " + cases)
        print("Total Deaths:          " + deaths.rjust(JCONST)) #+ delta_deaths.rjust(10)
        label_total_deaths.config(text = "Total Deaths Worldwide: " + deaths)
        print("Total Recovered:       " + rec.rjust(JCONST)) #+ delta_rec.rjust(10)
        label_total_recovered.config(text = "Total Recovered Worldwide: " + rec)
        print("Active Cases:          " + active_cases.rjust(JCONST))
        label_active_cases.config(text = "Active Cases: " + active_cases)
        print("Closed Cases:          " + closed_cases.rjust(JCONST))
        label_closed_cases.config(text = "Closed Cases: " + closed_cases)
        mortality = round(1000*mortality)/1000 #Rounds off digits so that there's 3 digits past decimal
        print("Net Mortality:         " + str(mortality).rjust(JCONST) + "%")
        label_net_mortality.config(text = "Net Mortality of Closed Cases: " + str(mortality) + "%")
        print(" ")

    root.after(4000, check_stats)

check_stats()

root.mainloop()
