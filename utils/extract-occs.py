#!/home/aeberso2/miniconda3/bin/python
#!/home/thom1618/miniconda3/bin/python
import pandas as pd
from numpy import *
import os, sys, re
import argparse 
# outfile =  'O2.triplet.dplots.out'

parser = argparse.ArgumentParser(description='''
experimental script: occupations finder 
''',
epilog='\n Usage:\n extract-occs.py -f LaF.tpss.rp.out\n')

parser.add_argument('-f', '--file', help="Output file to analyze", required=True)
# parser.add_argument('-r', '--vector_range', help="vector range (3,8)", required=True)
args = vars(parser.parse_args())

outfile = args['file'] 
# so_test = os.system('grep "Total SO-DFT" {}'.format(filename))
# if so_test != '':
#     raise Exception('Spin-orbit calculations detected, not yet supported by parser!')

filename = 'file.temp-occvals' 
os.system("grep 'Vector' {} > {}".format(outfile, filename))
os.system("sed -i 's/D/e/g' {}".format(filename))
os.system("sed -i 's/E=//g' {}".format(filename))
os.system("sed -i 's/Occ=//g' {}".format(filename))
os.system("sed -i 's/Symmetry=//g' {}".format(filename))
os.system("sed -i 's/Vector//g' {}".format(filename))


# os.system(r"grep 'S2' {}|awk '{{print$3,$6}}'| tail -n1 > temp_s2".format(outfile))
S2_val = os.system(r"grep 'S2' {} | awk '{{print$3}}'| tail -n1 > temp".format(outfile))
f = open('temp', 'r')
S2_c = float(f.readlines()[0])
f.close()

S2_exact = os.system(r"grep 'S2' {} | awk '{{print$6}}'| tail -n1 > temp".format(outfile))
f = open('temp', 'r')
S2_e = f.readlines()[0]
S2v = S2_e.split(')')
S2_e = float(S2v[0])
f.close()
os.system('rm -f temp')
print('\n{:^80}\n'.format('Vector analysis'))
Scontaim = S2_c/S2_e - 1
print('Spin contamination is {: .2%}'.format(S2_c/S2_e - 1))
if Scontaim < 0.05:
    print('This is OK')
elif 0.05 <= Scontaim < 0.15:
    print('This value is pushing it, it may or may not be OK')
elif 0.15 <= Scontaim < 0.4:
    print("Something likely isn't right with the spin")
elif Scontaim >= 0.4:
    print("Damn son, that's some high AF spin contaim. Probably not ok.")


occs = pd.read_csv(filename, sep='\s+', header=None,index_col=0)
# occs.columns = ['Vectors', 'Occupation', 'Energy', 'Symmetry']
os.system('rm -f {}'.format(filename))
if len(occs.iloc[0,:]) == 3:
    occs.columns = ['Occupation', 'Energy', 'Symmetry'] 
elif len(occs.iloc[0,:]) == 2:
    occs.columns = ['Occupation', 'Energy'] 

occs.index.name = "Vectors"
fvector = occs.index.max() 
# occs = occs.iloc[-1:-2*fvector:, :]
occs = occs.iloc[::-1, :] 
occs = occs.iloc[:2*fvector,:]
occs = occs.iloc[::-1, :] 


hsize = len(occs.index)//2 - 1
occ_alpha = occs.iloc[:hsize,:]
occ_beta = occs.iloc[hsize:,:]


full_occ_a = occ_alpha[occ_alpha.loc[:,'Occupation'] == 1.0]
full_occ_b = occ_beta[occ_beta.loc[:,'Occupation'] == 1.0]

mult = len(full_occ_a) - len(full_occ_b)
if mult > 1:
    print('There are {} unpaired electrons'.format(mult))
elif mult == 1:
    print('There is only 1 unpaired electron')
elif mult == 0:
    print('There are no unpaired electrons')
Nalpha = len(full_occ_a)
Nbeta = len(full_occ_b)

# screen_set = occ_alpha.iloc[Nalpha-1:Nalpha+7]
screen_set = occ_alpha.iloc[Nalpha-1:Nalpha+5]
HOMOS = occ_alpha.iloc[Nalpha-4:Nalpha]
HOMOS = HOMOS[::-1]

HOMO = screen_set.Energy.iloc[0]
# HOMO = HOMOS.iloc[0]
HOMOm1 = HOMOS.Energy.iloc[1]
HOMOm2 = HOMOS.Energy.iloc[2]
HOMOm3 = HOMOS.Energy.iloc[3]

print('\nFor the alpha vectors')
issues = 0 
for i in range(1, len(screen_set)):
    if screen_set.Energy.iloc[i] < screen_set.Energy.iloc[0]:
        issues += 1
        print('Vector {} is unoccupied and lower in energy than HOMO vector {}'.format(screen_set.index[i], screen_set.index[0]))
    if screen_set.Energy.iloc[i] < HOMOm1:
        issues += 1
        print('Vector {} is unoccupied and lower in energy than HOMO-1 vector {}'.format(screen_set.index[i], HOMOS.index[1]))
    if screen_set.Energy.iloc[i] < HOMOm2:
        issues += 1
        print('Vector {} is unoccupied and lower in energy than HOMO-2 vector {}'.format(screen_set.index[i], HOMOS.index[2]))
    if screen_set.Energy.iloc[i] < HOMOm3:
        issues += 1
        print('Vector {} is unoccupied and lower in energy than HOMO-3 vector {}'.format(screen_set.index[i], HOMOS.index[3]))
if issues == 0:
    print('No apparent issues found.')

print(occ_alpha.iloc[Nalpha-5:Nalpha+5])

print('')

# screen_set = occ_beta.iloc[Nbeta:Nbeta+7]
screen_set = occ_beta.iloc[Nbeta:Nbeta+5]
HOMOS = occ_beta.iloc[Nbeta-4:Nbeta]
HOMOS = HOMOS[::-1]

HOMO = screen_set.Energy.iloc[0]
HOMOm1 = HOMOS.Energy.iloc[1]
HOMOm2 = HOMOS.Energy.iloc[2]
# HOMOm3 = HOMOS.Energy.iloc[3]
print('\nFor the beta vectors')
issues = 0 
for i in range(1, len(screen_set)):
    if screen_set.Energy.iloc[i] < screen_set.Energy.iloc[0]:
        issues += 1
        print('Vector {} is unoccupied and lower in energy than HOMO vector {}'.format(screen_set.index[i], screen_set.index[0]))
    if screen_set.Energy.iloc[i] < HOMOm1:
        issues += 1
        print('Vector {} is unoccupied and lower in energy than HOMO-1 vector {}'.format(screen_set.index[i], HOMOS.index[1]))
    if screen_set.Energy.iloc[i] < HOMOm2:
        issues += 1
        print('Vector {} is unoccupied and lower in energy than HOMO-2 vector {}'.format(screen_set.index[i], HOMOS.index[2]))
if issues == 0:
    print('No apparent issues found')

print(occ_beta.iloc[Nbeta-5:Nbeta+5])

