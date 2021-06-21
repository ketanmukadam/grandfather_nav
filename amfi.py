import requests
import datetime
import os
import logging
import re
import pandas as pd
from io import StringIO

######### AMFI URL ##########
amfi_url = "https://www.amfiindia.com/spages/NAVAll_31Jan2018.txt?t=18062021062831"
fname = "gfnav.txt"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " 
           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 " 
           "Safari/537.36"}

def get_url_data(url):
    try:
        logging.info(url)
        rsp = requests.get(url, headers=headers)
        rsp.raise_for_status()
        logging.debug(rsp)
        return rsp
    except:
        logging.error("GET error - %s", url)
        return None

def download_info():
    if not os.path.isfile(fname) :
        logging.info("File %s not found .. downloading\n", fname)
        rsp = get_url_data(amfi_url)
        if rsp.ok : 
            with open(fname, "w") as f:
                f.write(rsp.text)
    else :
    	logging.info("File %s found\n", fname)

def read_info():
    if not os.path.isfile(fname) :
        download_info()
    with open(fname, "r") as f:
        return f.read()

def read_info_in_df(rsp) :
    logging.info("reading %s entries into dataframe", len(rsp.splitlines()))
    logging.info("reading into dataframe...")
    df = pd.read_csv(StringIO(rsp), sep=";")
    logging.info("Dropping lines not having NAVs...")
    df.dropna(subset = ["Date"], inplace=True) # Drop top level headings
    logging.info("Merging ISIN columns ...")
    df['ISIN'] = df['ISIN Div Payout/ ISIN Growth'] + ',' + df['ISIN Div Reinvestment']
    df.drop(['ISIN Div Payout/ ISIN Growth', 'ISIN Div Reinvestment'], axis=1, inplace=True)
    # Rename to NAV 
    df.rename({'Net Asset Value': 'NAV'}, axis=1, inplace=True)
    logging.info("Readjust the index sequentially...")
    df.reset_index(drop=True)
    # Move ISIN column to second place
    df.insert(1, "ISIN", df.pop('ISIN'))
    logging.info("cleaned up %s", df.to_string())
    return df

def search_isin(isin):
    logging.info("passed isin %s", isin)
    df = read_info_in_df(read_info())
    logging.info("searching isin %s", df.to_string())
    nav = df[df['ISIN'].str.contains(isin, na=False)][['ISIN', 'NAV']]
    print(nav.to_string(index=False))

def get_gf_nav(rsp):
    logging.info("04 Rsp has %s entries", len(rsp.splitlines()))
    for line in rsp.splitlines() :
        if re.match(r'[^0-9].*', str(line)) is None:
            sline = line.split(";")
            print(sline[3], "=>", sline[4])

def get_mf_schemes(rsp, mf_name):
    mf_schemes = set()
    logging.info("03 Rsp has %s entries", len(rsp.splitlines()))
    mf_name = mf_name.replace("Mutual Fund", '')
    for line in rsp.splitlines() :
        if re.match(r'[^0-9].*', str(line.rstrip())) is None:
            if mf_name in str(line.rstrip()):
                mf_schemes.add(line)
    return mf_schemes

def get_mf_names(rsp):
    mf_names = set()
    logging.info("02 Rsp has %s entries", len(rsp.splitlines()))
    for line in rsp.splitlines() :
        if re.match(r'[^0-9].*', str(line.rstrip())) :
            #print ("**", line)
            if re.match(r'^.*Mutual Fund$', str(line)) :
                mf_names.add(line)
    return mf_names

def get_mf_types(rsp):
    mf_types = set()
    logging.info("01 Rsp has %s entries", len(rsp.splitlines()))
    for line in rsp.splitlines() :
        if re.match(r'[^0-9].*', str(line.rstrip())) :
            if re.match(r'^.*Schemes.*$', str(line)) :
                mf_types.add(line)
    return mf_types

def getinfo(args):
    if args.mf_names:
        logging.info("Printing MF Names\n")
        mfnames = get_mf_names(read_info())
        [print(mf) for mf in sorted(mfnames)]
        exit(0)
    if args.mf_types:
        logging.info("Printing Scheme Types\n")
        mftypes = get_mf_types(read_info())
        [print(mf) for mf in sorted(mftypes)]
        exit(0)
    if args.download:
        download_info()
        logging.info("Grandfathered NAVs downloaded\n")
        exit(0)
    if not args.isin and not args.mf_name:
        logging.error("Neither ISIN nor MF_Name provided\n")
        print ("Neither ISIN nor MF_Name provided\n")
        exit(1)
    if args.isin :
        logging.info("ISIN %s searched\n", args.isin)
        search_isin(args.isin) 
        exit(0)
    if args.mf_name :
        logging.info("MF Name %s\n", args.mf_name)
        mfschemes = get_mf_schemes(read_info(), args.mf_name)
        if not mfschemes : 
            logging.error("No schemes found %s\n", args.mf_name)
            print ("No schemes found for - ", args.mf_name)
        else :
            [print(mf) for mf in sorted(mfschemes)]
