#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @file download_gaia_csv.py
# @author: wujiangu
# @date: 2024-04-15 17:44
# @description: download_gaia_csv

# TODO: download gaia csv by gaia_id

import csv
import multiprocessing
import random

from astroquery.gaia import Gaia
import numpy as np
import pandas as pd
import time


def get_data_from_csv(filepath):
    pf = pd.read_csv(filepath)
    gaia_id = (pf['id_gaia'].astype(str)).tolist()
    return gaia_id

def get_data_from_archiveSearch(SQL):

    Gaia.login(user='your_username', password='your_password')
    job = Gaia.launch_job_async(SQL)
    r = job.get_results()
    outputsID = [r[i][0] for i in range(len(r))]
    # outputsClass = [r[i][1] for i in range(len(r))]
    return outputsID


def process_data(data, id_list, _property, csv_id, savepath):
    cnt = 0
    begin = csv_id + 1
    end = csv_id + len(data)
    print("loading...")
    datalink = Gaia.load_data(data,
                              data_structure='COMBINED',
                              retrieval_type='XP_SAMPLED',
                              format='votable'
                              )
    outputs = [i for i in datalink[list(datalink.keys())[0]]]
    print(len(outputs))
    for table in outputs:

        array = table.array
        with open(f'{savepath}/{id_list[csv_id]}.csv', "w",
                  newline="",
                  encoding="utf-8") as csvfile:
            print(f"\rprocessing download {begin}~{end} [{cnt + 1}]/[{len(data)}]")
            writer = csv.writer(csvfile)
            if _property:
                writer.writerow(["wavelength", "flux"])
            for k in range(array.size):
                writer.writerow([array[k][0], array[k][1]])
        csv_id += 1
        cnt += 1


def search(id_list, batch_size,save_Spectrum_Path,_property ):
    index = 0
    csv_id = 0
    while index < len(id_list):
        if index + batch_size <= len(id_list):
            data = id_list[index:index + batch_size]
        else:
            data = id_list[index:len(id_list)]
        # process_data(data, id_list, _property, csv_id, save_Spectrum_Path) # for debugging
        pool.apply_async(process_data, args=(data, id_list, _property, csv_id,save_Spectrum_Path), error_callback=err_call_back)
        index += batch_size
        csv_id += batch_size
        time.sleep(10)


def err_call_back(err):
    print(f'error ---> :{str(err)}')

if __name__ == '__main__':
    """
    note: You need to make the following changes to gaia's core.py to enable multi-process downloads
        origin code:
        now = datetime.now(timezone.utc)
        now_formatted = now.strftime("%Y%m%d_%H%M%S")
        temp_dirname = "temp_" + now_formatted
        downloadname_formated = "download_" + now_formatted

        revised code:
        if retrieval_type is None:
            raise ValueError("Missing mandatory argument 'retrieval_type'")  # This row is available in version 4.6 and not for the 4.7 update

        random_number = random.randint(10 ** 7, 10 ** 8 - 1)
        now = datetime.now()
        now_formatted = now.strftime(f"%Y%m%d_%H%M%S_{random_number}")
        temp_dirname = "temp_" + now_formatted
        downloadname_formated = "download_" + now_formatted
    """
    # path
    gaiaID_csv_path = "your_gaiaID_csv_path"
    save_Spectrum_Path = "your_spectrum_save_path"
    # get id and label
    id_list = get_data_from_csv(gaiaID_csv_path)
    print(f"{len(id_list)} files are going to be downloaded ")
    # parameter
    batch_size = 2000  # max: 5000
    poolnum = 6
    # mutiprocess
    pool = multiprocessing.Pool(poolnum)
    search(id_list, batch_size,save_Spectrum_Path, _property=False)
    pool.close()
    pool.join()
    print()
    print("Finishing download successfully!")
