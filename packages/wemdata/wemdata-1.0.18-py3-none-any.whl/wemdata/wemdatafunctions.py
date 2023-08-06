#!/usr/bin/env python
# coding: utf-8

# # Overview
# This note book contains the function to scrape data from the AEMO data webpage. The scarpped data is stored in a dataframe. <br/>
# Each sections contains:
# * the title of the dataset
# * the link the dataset is in
# * the function for scrapping data from the dataset
# 

# In[1]:


import csv
import requests
import pandas as pd

domainstr='http://data.wa.aemo.com.au/datafiles/'


# # Commissioning test
# http://data.wa.aemo.com.au/#commissioning-test

# In[2]:


def comm_test(year):
  
    tempstr = 'commissioning-test/commissioning-test-summary-' + str(year) + '.csv'
    CSV_URL = domainstr + tempstr
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')

    return df1


# # Load forecast
# http://data.wa.aemo.com.au/#load-forecast

# In[3]:


def load_forecast():
    tempstr = 'load-forecast/load-forecast.csv'
    CSV_URL = domainstr + tempstr   
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # Extended load forecast
# http://data.wa.aemo.com.au/#extended-load-forecast

# In[4]:


def extended_load_forecast():
  
    tempstr = 'extended-load-forecast/extended-load-forecast.csv'
    CSV_URL = domainstr + tempstr    
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # Historical load forecast
# http://data.wa.aemo.com.au/#historical-load-forecast

# In[5]:


def hist_load_forecast(year):  
    
    tempstr = 'historical-load-forecast/historical-load-forecast-' + str(year) + '.csv'
    CSV_URL = domainstr + tempstr 
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # NCS dispatch
# http://data.wa.aemo.com.au/#ncs-dispatch-information

# In[6]:


def ncs_dispatch():    
    tempstr = 'ncs-dispatch-information/ncs-dispatch-information.csv'
    CSV_URL = domainstr + tempstr    
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # NON BALANCING DISPATCH MERIT ORDER
# http://data.wa.aemo.com.au/#non-balancing-dispatch-merit-order

# In[7]:


def non_bal_dmo(year, month):  
    
    monthstr = str(year) + '-' + str(month).zfill(2)       
    tempstr = 'non-balancing-dispatch-merit-order/nbdmo-' + monthstr + '.csv'
    CSV_URL = domainstr + tempstr 
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # Demand side program prices
# http://data.wa.aemo.com.au/#dsp-decrease-price

# In[8]:


def dsm_prices(year):
       
    tempstr = 'dsp-decrease-price/dsp-decrease-price-' + str(year) + '.csv'
    CSV_URL = domainstr + tempstr 
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # Operational measurements
# http://data.wa.aemo.com.au/#operational-measurements

# In[9]:


def ops_measurements(year):             
    tempstr = 'operational-measurements/operational-measurements-' + str(year) + '.csv'
    CSV_URL = domainstr + tempstr 
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # Facility SCADA
# http://data.wa.aemo.com.au/#facility-scada

# In[10]:


def facility_scada(year, month):  

    
    monthstr = str(year) + '-' + str(month).zfill(2)       
    tempstr = 'facility-scada/facility-scada-' + monthstr + '.csv'
    CSV_URL = domainstr + tempstr 
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # Load summary
# http://data.wa.aemo.com.au/#load-summary

# In[11]:


def load_summary(year):             
    tempstr = 'load-summary/load-summary-' + str(year) + '.csv'
    CSV_URL = domainstr + tempstr 
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # LFAS summary
# http://data.wa.aemo.com.au/#lfas-summary

# In[12]:


def lfas_summary(year):
       
    tempstr = 'lfas-summary/lfas-summary-' + str(year) + '.csv'
    CSV_URL = domainstr + tempstr
   
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1=df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # LFAS SUBMISSIONS
# http://data.wa.aemo.com.au/#lfas-submissions

# In[13]:


def lfas_submissions(year):
       
    tempstr = 'lfas-submissions/lfas-submissions-' + str(year) + '.csv'
    CSV_URL = domainstr + tempstr
   
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1=df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # Outages
# http://data.wa.aemo.com.au/#outages

# In[14]:


def outages(year):
       
    tempstr = 'outages/outages-' + str(year) + '.csv'
    CSV_URL = domainstr + tempstr
   
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1=df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # IRCR ratios
# http://data.wa.aemo.com.au/#ircr-ratios

# In[15]:


def ircr_ratios():    
    tempstr = 'ircr-ratios/ircr-ratios.csv'
    CSV_URL = domainstr + tempstr    
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # Peak trading intervals
# http://data.wa.aemo.com.au/#peak-intervals

# In[16]:


def peak_trading_intervals():    
    tempstr = 'peak-intervals/peak-intervals.csv'
    CSV_URL = domainstr + tempstr    
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # Real time outages
# http://data.wa.aemo.com.au/#realtime-outages

# In[17]:


def real_time_outages():    
    tempstr = 'realtime-outages/realtime-outages.csv'
    CSV_URL = domainstr + tempstr    
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        try:
            decoded_content = download.content.decode('utf-8')
        except:    
            decoded_content = download.content.decode('cp1252')
        
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # Refund exempt planned outages count
# http://data.wa.aemo.com.au/#repo-count

# In[18]:


def repo_count():    
    tempstr = 'repo-count/repo-count.csv'
    CSV_URL = domainstr + tempstr    
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # Balancing Market summary
# http://data.wa.aemo.com.au/#balancing-summary

# In[19]:


def balancing_summary(year):
       
    tempstr = 'balancing-summary/balancing-summary-' + str(year) + '.csv'
    CSV_URL = domainstr + tempstr
   
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1=df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # Effective Balancing Submission
# http://data.wa.aemo.com.au/#effective-balancing-submission

# In[20]:


def balancing_submissions(year, month):  

    
    monthstr = str(year) + '-' + str(month).zfill(2)       
    tempstr = 'effective-balancing-submission/effective-balancing-submission-' + monthstr + '.csv'
    CSV_URL = domainstr + tempstr 
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # STEM summary
# http://data.wa.aemo.com.au/#stem-summary

# In[21]:


def STEM_summary(year):
       
    tempstr = 'stem-summary/stem-summary-' + str(year) + '.csv'
    CSV_URL = domainstr + tempstr
   
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1=df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # STEM participant activity
# http://data.wa.aemo.com.au/#stem-participant-activity

# In[22]:


def STEM_participant_activity(year, month):  

    
    monthstr = str(year) + '-' + str(month).zfill(2)       
    tempstr = 'stem-participant-activity/stem-participant-activity-' + monthstr + '.csv'
    CSV_URL = domainstr + tempstr 
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # STEM bids and offers
# http://data.wa.aemo.com.au/#stem-bids-and-offers

# In[23]:


def STEM_bids_and_offers(year, month):  

    
    monthstr = str(year) + '-' + str(month).zfill(2)       
    tempstr = 'stem-bids-and-offers/stem-bids-and-offers-' + monthstr + '.csv'
    CSV_URL = domainstr + tempstr 
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # STEM facilities declarations
# http://data.wa.aemo.com.au/#stem-facility-declarations

# In[24]:


def STEM_facilities_declarations(year, month):  

    
    monthstr = str(year) + '-' + str(month).zfill(2)       
    tempstr = 'stem-facility-declarations/stem-facility-declarations-' + monthstr + '.csv'
    CSV_URL = domainstr + tempstr 
    
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1 =df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# # Total sent out generation
# http://data.wa.aemo.com.au/#tt30gen

# In[25]:


def total_sent_out_gen(year):
       
    tempstr = 'tt30gen/tt30gen-' + str(year) + '.csv'
    CSV_URL = domainstr + tempstr
   
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    df = pd.DataFrame(my_list)
    df.columns=my_list[0]
    df1 = df[df.index != 0]
    df1=df1.drop(columns='Extracted At')
    df1 = df1.apply(pd.to_numeric, errors='ignore')
    return df1


# In[ ]:




