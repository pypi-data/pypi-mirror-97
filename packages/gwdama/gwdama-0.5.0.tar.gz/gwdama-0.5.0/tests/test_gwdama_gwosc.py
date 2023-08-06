# This file tests the reading capabilities
# using gwosc datasets

import os, sys
import numpy as np
import pandas as pd
from gwdama.io.gwdatamanager import GwDataManager

input_test_glitch_list = "glitch_sample_list_L1_O2.csv"

cwd = os.getcwd()
script_path = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]))

data_dir = os.path.join(os.path.dirname(script_path),'..',"data")

print("data dir is %s" % data_dir)
input_test_glitch_list = os.path.join(data_dir,input_test_glitch_list)
print("input file list is %s" % input_test_glitch_list)

in_df = pd.read_csv(input_test_glitch_list)
print(in_df)

ifo = np.unique(in_df["ifo"].values)[0]

# init gwdama
gwdama_manager_cvmfs = GwDataManager("test_glitch_gwosc_cvmfs")

for ii in range(len(in_df)):
    t0_gps = in_df.iloc[ii]["GPStime"]
    print("Testing %d (gps=%.4f)" % (ii,t0_gps))
    t1=t0_gps-1
    t2=t0_gps+1
    gwdama_manager_cvmfs.read_gwdata(t1, t2, m_data_source="gwosc-cvmfs", m_channel_name="ht", ifo='L1')

gwdama_manager_cvmfs.write_gwdama_dataset("test_glitch_gwosc_cvmfs_out.h5")