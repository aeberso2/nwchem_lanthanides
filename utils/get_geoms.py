import os, sys, string, re
import pandas as pd

Ln_list = [
    'LaF', 'PrF', 'NdF', 'EuF', 'GdF', 'TbF', 'DyF', 'HoF', 'ErF', 'TmF', 'YbF', 'LuF', 'LaO', 'CeO', 'PrO', 'NdO', 'SmO', 'EuO', 'GdO', 'TbO', 'DyO', 'HoO', 'ErO', 'TmO', 'YbO', 'LuO', 
    'LaF2', 'SmF2', 'EuF2', 'LaCl2', 'CeCl2', 'PrCl2', 'NdCl2', 'SmCl2', 'EuCl2', 'GdCl2', 'TbCl2', 'HoCl2', 'ErCl2',
    'LaF3', 'CeF3', 'PrF3', 'NdF3', 'GdF3', 'TbF3', 'DyF3', 'HoF3', 'ErF3', 'LuF3', 'LaCl3', 'CeCl3', 'PrCl3', 'NdCl3', 'GdCl3'
]

geom_list = []

for ln in Ln_list:
    geom_path = '{}/opt'.format(ln)
    if os.path.isdir(geom_path):
        os.chdir(geom_path)
    else: 
        print('No folder for {} found.'.format(ln))
        continue
    dir_contents = os.listdir()
    geom_file = '{}.geom'.format(ln)
    if os.path.isfile(geom_file):
        f = open(geom_file, 'r')
        geom_str = ''
        for line in f.readlines():
            geom_str += line
            if re.search('\s*^\d\s',line):
                print('geometry for file {} is not cleaned'.format(ln))
#         geom_str += f.readlines()
        geom_list.append(geom_str)
        f.close()
    else:
        print('No geometry found for {}. There will be a blank entry appended in its place.'.format(ln))
        geom_list.append('')
    os.chdir('../..')

geom_db = pd.Series(geom_list,index=Ln_list)
main_db = pd.HDFStore('input_gendb.h5','a')
main_db['geom_tpss'] = geom_db
main_db.close()
