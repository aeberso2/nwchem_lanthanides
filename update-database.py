#!/mnt/home/aeberso2/miniconda3/bin/python
#!/mnt/home/thom1618/miniconda3/bin/python

import os, re, string
import sys, argparse
from numpy import *
import pandas as pd
top_direc = os.getcwd()

# this is for your reference
Ln_list = [
    'LaF', 'PrF', 'NdF', 'EuF', 'GdF', 'TbF', 'DyF', 'HoF', 'ErF', 'TmF', 'YbF', 'LuF', 'LaO', 'CeO', 'PrO', 'NdO', 'SmO', 'EuO', 'GdO', 'TbO', 'DyO', 'HoO', 'ErO', 'TmO', 'YbO', 'LuO', 
    'LaF2', 'SmF2', 'EuF2', 'LaCl2', 'CeCl2', 'PrCl2', 'NdCl2', 'SmCl2', 'EuCl2', 'GdCl2', 'TbCl2', 'HoCl2', 'ErCl2',
    'LaF3', 'CeF3', 'PrF3', 'NdF3', 'GdF3', 'TbF3', 'DyF3', 'HoF3', 'ErF3', 'LuF3', 'LaCl3', 'CeCl3', 'PrCl3', 'NdCl3', 'GdCl3'
]


def data_sync2():
    os.chdir('db_files')
    mult_info = pd.read_csv('multiplicity.csv', index_col=0)
    mult = mult_info.loc[:, 'Mult']
    os.chdir('..')

    maindb = pd.HDFStore('input_gendb.h5', 'a')
#     maindb['basis'] =  proto_basis_database
#     maindb['geom_init']  =  geom_db
    maindb['multiplicity'] = mult
    maindb.close()

# data_sync2()
