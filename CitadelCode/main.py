import json
import urllib.request

# API Key
TOKEN = '680419b0a91f14e780af14daaed5a8da02a12a9bb7b4f513b8f2430d9a2e3dc3'
API = "https://api.sec-api.io?token=" + TOKEN

# Define the filter parameters
filtr = "formType:\"4\" AND formType:(NOT \"N-4\") AND formType:(NOT \"4/A\") AND filedAt:[2019-07-01 TO 2019-08-01]"
payload = {
  "query": {"query_string": {"query": filtr}},
  "from": "0",
  "size": "1000",
  "sort": [{"filedAt": {"order": "desc"}}]
}

# format your payload to JSON bytes
jsondata = json.dumps(payload)
jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes

# instantiate the request
req = urllib.request.Request(API)

# set the correct HTTP header: Content-Type = application/json
req.add_header('Content-Type', 'application/json; charset=utf-8')
# set the correct length of your request
req.add_header('Content-Length', len(jsondataasbytes))

# send the request to the API
response = urllib.request.urlopen(req, jsondataasbytes)

# read the response
res_body = response.read()
# transform the response into JSON
filings = json.loads(res_body.decode("utf-8"))

# print JSON
print(filings)

print(json.dumps(filings, indent=2))
print(filings['total'])


def compress_filings(filings):
    store = {}
    compressed_filings = []
    for filing in filings:
        filedAt = filing['filedAt']
        if filedAt in store and store[filedAt] < 5:
            compressed_filings.append(filing)
            store[filedAt] += 1
        elif filedAt not in store:
            compressed_filings.append(filing)
            store[filedAt] = 1
    return compressed_filings


filings = compress_filings(filings['filings'])

import xml.etree.ElementTree as ET
import re
import time


# Download the XML version of the filing. If it fails wait for 5, 10, 15, ... seconds and try again.
def download_xml(url, tries=1):
    try:
        response = urllib.request.urlopen(url)
    except:
        print('Something went wrong. Wait for 5 seconds and try again.', tries)
        if tries < 5:
            time.sleep(5 * tries)
            download_xml(url, tries + 1)
    else:
        # decode the response into a string
        data = response.read().decode('utf-8')
        # set up the regular expression extractoer in order to get the relevant part of the filing
        matcher = re.compile('<\?xml.*ownershipDocument>', flags=re.MULTILINE | re.DOTALL)
        matches = matcher.search(data)
        # the first matching group is the extracted XML of interest
        xml = matches.group(0)
        # instantiate the XML object
        root = ET.fromstring(xml)
        print(url)
        return root

    # Calculate the total transaction amount in $ of a giving form 4 in XML


def calculate_transaction_amount(xml):
    total = 0

    if xml is None:
        return total

    nonDerivativeTransactions = xml.findall("./nonDerivativeTable/nonDerivativeTransaction")

    for t in nonDerivativeTransactions:
        # D for disposed or A for acquired
        action = t.find('./transactionAmounts/transactionAcquiredDisposedCode/value').text
        # number of shares disposed/acquired
        shares = t.find('./transactionAmounts/transactionShares/value').text
        # price
        priceRaw = t.find('./transactionAmounts/transactionPricePerShare/value')
        price = 0 if priceRaw is None else priceRaw.text
        # set prefix to -1 if derivatives were disposed. set prefix to 1 if derivates were acquired.
        prefix = -1 if action == 'D' else 1
        # calculate transaction amount in $
        amount = prefix * float(shares) * float(price)
        total += amount

    return round(total, 2)


# Download the XML for each filing
# Calculate the total transaction amount per filing
# Save the calculate transaction value to the filing dict with key 'nonDerivativeTransactions'
def add_non_derivative_transaction_amounts():
    for filing in filings:
        url = filing['linkToTxt']
        xml = download_xml(url)
        nonDerivativeTransactions = calculate_transaction_amount(xml)
        filing['nonDerivativeTransactions'] = nonDerivativeTransactions


# Running the function prints the URL of each filing fetched
add_non_derivative_transaction_amounts()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pandas.io.json import json_normalize
filings = json_normalize(filings)
filings

def getBins (filings):
    bins = {}
    for index, row in filings.iterrows():
        filedAt = row['filedAt']
        nonDerivativeTransactions = row['nonDerivativeTransactions']
        value = bins[filedAt] + nonDerivativeTransactions if filedAt in bins else nonDerivativeTransactions
        bins[filedAt] = round(value, 2)
    return bins
bins = getBins(filings)
bins

# Set size of figure
plt.rcParams['figure.figsize'] = [15, 10]

# Prettify y axis: 2000000 to $2M
def millions(x, pos):
    return '${:,.0f}M'.format(x*1e-6)

fig, ax = plt.subplots()
# Define bar plot
ax.bar(range(len(bins)), list(bins.values()), align='center')
ax.grid(True)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(millions))
# Prettify x axis
fig.autofmt_xdate()
# Set x axis values
plt.xticks(range(len(bins)), list(bins.keys()))
plt.show()
