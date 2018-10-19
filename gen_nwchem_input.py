#!/mnt/home/thom1618/miniconda3/bin/python
#!/mnt/home/aeberso2/miniconda3/bin/python

# this code generates nwchem input files 
# it was made as a convience, though it may not be perfect
#
import os, re, string
import sys, argparse
from numpy import *
import pandas as pd
top_direc = os.getcwd()

# direc = 'Lanthanides-Mark2/transfer_codes'
direc = 'Lanthanides'
# home_path = '/mnt/home/{}/'.format(os.getlogin()) + direc + '/nwchem_lanthanides/'
home_path = '/mnt/home/{}/'.format(os.getlogin())+'/nwchem_lanthanides/'

# this is for your reference
Ln_list = [
    'LaF', 'PrF', 'NdF', 'EuF', 'GdF', 'TbF', 'DyF', 'HoF', 'ErF', 'TmF', 'YbF', 'LuF', 'LaO', 'CeO', 'PrO', 'NdO', 'SmO', 
    'EuO', 'GdO', 'TbO', 'DyO', 'HoO', 'ErO', 'TmO', 'YbO', 'LuO', 'LaF2', 'SmF2', 'EuF2', 'LaCl2', 'CeCl2', 'PrCl2', 'NdCl2', 
    'SmCl2', 'EuCl2', 'GdCl2', 'TbCl2', 'HoCl2', 'ErCl2', 'LaF3', 'CeF3', 'PrF3', 'NdF3', 'GdF3', 'TbF3', 'DyF3', 'HoF3', 'ErF3', 
    'LuF3', 'LaCl3', 'CeCl3', 'PrCl3', 'NdCl3', 'GdCl3'
]

# This routine fetches the basis set information
def get_basis(atom, basis_set):
    
    os.chdir(home_path + '/basis_v2')
    basis_db = open('{}.dat'.format(basis_set), 'r')
    contents = basis_db.readlines()
    BASIS = []
    BASIS = ''
    can_proceed = False
    
    for i in range(0, len(contents)):
        if '# {} '.format(atom) in contents[i]:
            start_pos = i 
            can_proceed = True
            break
            
    if can_proceed == True:        
        BASIS += contents[start_pos]
        for j in range(start_pos + 1, len(contents)):
            if '# ' not in contents[j]:
                BASIS += contents[j]
                continue
            else:
                break

    elif can_proceed == False:
        basis_db.close()
#         os.chdir('..')
        os.chdir(top_direc)
        raise Exception('No {} basis entry  for {}!!! Aborting.'.format(basis_set, atom)) 
        
    basis_db.close()
#     os.chdir('..')
    os.chdir(top_direc)
    return BASIS

def get_the_geom(func, cmp, current_dir):
    # excised geom subroutine 
    # this regex term will find any match of an uppercase letter and if followed by a lowercase
    # letter includes that in the match, if not, it doesn't. Or it will match any digit
    # [A-Z] -> anything in this set, 
    # [a-z]* -> anything in this set 0 to infinite times
    # | -> or
    # \d+ -> matches any digit 1 or more times
    # So this will distinguish I from Ir, O from Os, etc, 
    sub_list = re.findall(r'[A-Z][a-z]*|\d+', cmp)
    
    # if only one match is found, that means only a single atom was entered
    # else, it means multiple atom strings, and/or digits were entered
    # that is why the digit was appended in case something like Th2 was entered
    if len(sub_list) == 1:
        GEO = 'zmatrix\n{}\nend\n'.format(cmp)
        elem_list = sub_list
        # halt if user is trying to optimize an atom 
        if optimize == 'y':
            raise Exception('Atoms do not require optimization')

    else:
        # now we don't care about digits, just find all entries of chemical elements
        elem_list = re.findall(r'[A-Z][a-z]*', cmp)

        os.chdir(top_direc)
        geom_file = pd.read_hdf('input_gendb.h5', 'geom_{}'.format(func))
        os.chdir(current_dir)

        # halt if geometry is not in the index 
        if cmp not in geom_file.index:
            raise Exception('No geometry entry found for {}'.format(cmp))

        GEO = geom_file[cmp]
    return GEO 

def init_params():
    # These elements require a pseudopotential - not inclusive list, just includes the atoms we work with.    
    rel_set = array(['Br', 'I', 'Hf', 'Ta','W','Re','Os','Ir','Pt','Au','Hg',
                     'Ac','Th','U','Pa','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No','Lr',
                     'La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu'])

    # functional prefix master list, includes general needed functionals 
    functionals_master = ['svwn',
                          'bp86',
                          'blyp',
                          'pw91',
                          'pbe', 
                          'tpss',
                          'm06l',
                          'pbe0',
                          'b3lyp',
                          'bhlyp',
                          'b3p86',
                          'b97-1',
                          'mpw1k',
                          'x3lyp',
                          'tpssh',
                          'm06',
                          'm06.2x',
                          'm11',
                          'camb3lyp',
                          'b2plyp'
                         ]

    # functional prefix key, order must match above or your file names will be off
    xckey_ms = ['xc slater vwn_5', 
                'xc becke88 perdew86', 
                'xc becke88 lyp', 
                'xc xperdew91 perdew91', 
                'xc xpbe96 cpbe96', 
                'xc xtpss03 ctpss03', 
                'xc m06-l', 
                'xc pbe0', 
                'xc b3lyp', 
                'xc bhlyp',
                'xc vwn_1_rpa perdew86 nonlocal 0.81 HFexch 0.20 slater 0.80 becke88 nonlocal 0.72', 
                'xc becke97-1', 
                'xc mpw1k',  
                'xc vwn_1_rpa 0.129 lyp 0.871 hfexch 0.218 slater 0.782 becke88 nonlocal 0.542 xperdew91 nonlocal 0.167', 
                'xc xctpssh', 
                'xc m06', 
                'xc m06-2x',  
                'xc m11', 
                'xc xcamb88 1.00 lyp 0.81 vwn_5 0.19 hfexch 1.00 \n cam 0.33 cam_alpha 0.19 cam_beta 0.46 \n direct', 
                'xc HFexch 0.53 becke88 0.47 lyp 0.73 mp2 0.27 \n dftmp2 \n direct'
               ]

    # store functional keywords to a dictionary for reference
    temp_frame = pd.Series(xckey_ms, index=functionals_master)
    xckey = temp_frame.to_dict()  
    return xckey, rel_set

def gen_nw_recp_dft_inputv2(input_set, 
                          rel_basis, 
                          dft_direc='dft',
                          optimize='n',
                          level='WB',
                          init_guess='atomic',
                          input_func=['tpss','m06l','b3lyp','svwn','pbe'],
                          Nbas_keys='',
#                           geom_read='tpss'
                          ):
#                                    Nbas_keys=['','T']):
    '''
    This program will generate a set of DFT functional inputs that run in NWChem
        
    Function arguments
        required:
            input_set: the molecule you are making inputs for, -
            rel_basis:  the basis set for the heavy atoms
                      'ANO': for the atomic natural orbitals Stuttgart generated basis sets
                      'SEG': for the Segmented Stuttgart generated basis sets
                      'AE': for the all-electron peterson cc-pVTZ-DK3 basis sets
                      '97': for the 1997 RSC Stuttgart generated basis set -> please don't use unless
                            there is a valid reason\n
        optional arguments:
            dft_direc: 'dft', 'sodft', 'both', default='dft'
            optimize: 'n', 'y' ; default='n'
            SG: 'ANO', 'SEG', 'AE' ; default='SEG'
            level: 'WB', 'DF' ; default='WB' <- this is hardcoded for the Ln species
            Nbas_keys: '-aug' ; default='' 
        
        To Do:
            make options for memory specifications
            make further options for optimizations
            a lot else 
    
    '''
    
    xckey, rel_set = init_params()
    # hard coded set of functionals built in for generator
     
#     functionals = ['svwn', 'bp86', 'blyp', 'pw91', 'pbe', 'tpss',
#                    'm06l', 'pbe0', 'b3lyp', 'bhlyp', 'b3p86', 'b97-1',
#                    'x3lyp', 'tpssh']
    
    functionals = input_func

#     functionals = ['tpss', 'm06l']
#     functionals = ['pbe', 'b3lyp']
    
    workdir = top_direc
    cmp = input_set
    # get multiplicities
    os.chdir(home_path)
    mult_data = pd.read_hdf('input_gendb.h5', 'multiplicity')
    os.chdir(top_direc)
    # if no multiplicity found, ask for one
    if cmp not in mult_data.index:
        print('No multiplicity value found for {}'.format(cmp))
        M = str(input('Enter in a multiplicty to use: '))
    else:
        M = str(int(mult_data[cmp]))
        
    if optimize == None:
        optimize = 'n'
        
    sub_list = re.findall(r'[A-Z][a-z]*|\d+', cmp)
        
    if len(sub_list) == 1:
        elem_list = sub_list

    else:
        elem_list = re.findall(r'[A-Z][a-z]*', cmp)

    # if CC was a flag, use the cc-pVTZ-PP basis set
    # if no the flag was either SEG or ANO, anything else will error out in later searches
    if rel_basis == 'CC':
        basis_ecp_exten = 'cc-pVTZ-PP'
        SG = 'cc-pvtz'
    
    else:
        SG = rel_basis
        basis_ecp_exten = '{}_ECPscM{}'.format(SG, level)
        
    non_rel_basis  = '{}cc-pVTZ'.format(Nbas_keys)
    ecp_exten = 'ECPscM{}'.format(level)
    soecp_exten = 'ECPscM{}-SO'.format(level)
    
    BASIS = []
    ECP = []
    SO = []
        
    # for each atom in the element list check is it an atom that needs an recp
    # then assign basis set accordingly 
    for atom in elem_list:
        if atom in rel_set:
            ECP_req = 'Yes'
            # special case for Br and I, they always need the cc-pVTZ-PP and DF recp
            if atom == 'Br' or atom == 'I':
                basis_ext = 'cc-pVTZ-PP'
                ecp_exten = 'ECPscMDF'
                soecp_exten = 'ECPscMDF-SO'
            else: 
                basis_ext = basis_ecp_exten

            BASIS.append(get_basis(atom, basis_ext))
            ECP.append(get_basis(atom, ecp_exten))
            SO.append(get_basis(atom, soecp_exten))

        elif atom not in rel_set:
            BASIS.append(get_basis(atom, non_rel_basis))

    # create a folder to put all inputs in
    # I usually lower the case 'cause I don't like constantly using the shift key to 
    # get into the folders, but others feel differently so its standard by default
#         new_dir = '{}/{}'.format(cmp.lower())
    new_dir = '{}'.format(cmp)
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

#     vec
    # not optimizing, set these options
    if optimize == 'n':
        card = 'energy'
        func_span = range(0, len(functionals))
        if dft_direc == 'both':
            DFT_DIRECS = []
            DFT_DIRECS.append('task dft energy')
            DFT_DIRECS.append('task sodft energy')
            exten = []
            exten.append('rp')
            exten.append('so')
            if init_guess != 'atomic':
                vec_input = '{}.{}.{}.movecs'.format(cmp, init_guess, exten[0])

#         elif dft_direc == 'sodft':
#             card = 'spin-orbit opt+freq'
#             exten = ['sopt']
        else:
            DFT_DIRECS = ['task {} energy'.format(dft_direc)]
            if dft_direc == 'sodft':
                exten = ['so']
                if init_guess != 'atomic':
                    vec_input = '{}.{}.m{}.f.movecs'.format(cmp, init_guess, str(M))
            elif dft_direc == 'dft':
                exten = ['rp']

                if init_guess != 'atomic':
                    vec_input = '{}.{}.{}.movecs'.format(cmp, init_guess, exten[0])

        new_dir2 = '{}/{}'.format(cmp, rel_basis)
        # if this directory doesn't exist make it
        if not os.path.isdir(new_dir2):
            os.mkdir(new_dir2)
        # change to new directory 
        os.chdir(new_dir2) 
        
    # optimize flags
    elif optimize == 'y':
        if dft_direc == 'dft':
            card = 'opt+freq'
            exten = ['m' + str(M)]

        elif dft_direc == 'sodft':
            card = 'spin-orbit opt+freq'
            exten = ['sopt']
        if init_guess != 'atomic':
            vec_input = '{}.{}.m{}.f.movecs'.format(cmp, init_guess, M)

        # optimizing dft and sodft in one input is a bad idea 
        if dft_direc == 'both':
            raise Exception('Optimizations are currently limited to one directive block')
        func_span = range(0, len(functionals))
        DFT_DIRECS = ['task {} optimize \ntask {} freq\n'.format(dft_direc, dft_direc)]

        if dft_direc == 'sodft':
            new_dir2 = '{}/so_opt'.format(cmp)
        else:
            new_dir2 = '{}/opt'.format(cmp)
        if not os.path.isdir(new_dir2):
            os.mkdir(new_dir2)         
        os.chdir(new_dir2) 

    #------------------------- Main Generator Routine ------------------------#
    # this writes the file, first it creates the header card
    # then adds geometry, basis and recps, task directives
    # does this for each functional in the func_span
    for i in func_span:
        Main_file = []
        file_out = open('{}.{}.{}.nw'.format(cmp, functionals[i], exten[0]), 'w', newline='\n')
        Main_file.append('start {}.{}.{}\n'.format(cmp, functionals[i], exten[0]))
        Main_file.append('title "{} {} {} basis {}"\n'.format(cmp, functionals[i], SG, card)) 
        Main_file.append('memory 500 mw\necho\n\n')
        
        Main_file.append('geometry\n')
        GEO = get_the_geom(functionals[i], cmp, os.getcwd())
        Main_file.append(GEO)

        Main_file.append('end\n')
        Main_file.append('\n\nbasis spherical\n')
        for j in range(0, len(BASIS)):
            Main_file.append(BASIS[j])
        Main_file.append('end\n\n')    
        
        if ECP_req == 'Yes':
            Main_file.append('ecp\n')
            for k in range(0, len(ECP)):
                Main_file.append(ECP[k])
            Main_file.append('end\n\n')

            Main_file.append('so\n')
            for s in range(0, len(SO)):
                Main_file.append(SO[s])
            Main_file.append('end\n')

        for j in range(0,len(DFT_DIRECS)):
#             Main_file.append('\ndft\n')
            Main_file.append('\ndft\n mult {}\n'.format(M))
            Main_file.append(' odft\n {}\n'.format(xckey[functionals[i]]))
            if j == 0:
                if init_guess == 'atomic':
                    inp_arg = 'atomic'
                else:
                    inp_arg = vec_input
                out_arg = '{}.{}.{}.movecs'.format(cmp, functionals[i], exten[j])
                Main_file.append(' vectors input {} output {}\n'.format(inp_arg, out_arg))

            else:
                inp_arg = '{}.{}.{}.movecs'.format(cmp, functionals[i], exten[j-1])
                out_arg = '{}.{}.{}.movecs'.format(cmp, functionals[i], exten[j])
                Main_file.append(' vectors input {} output {}\n'.format(inp_arg, out_arg))
                                 
            Main_file.append(' maxiter 200\nend\n\n') 
            # if first pass, then add line to generate nbo file 
            if j == 0 and exten[0] != 'sopt' and exten[0] != 'so':
                Main_file.append('property\n nbofile\nend\n\n')
#                 Main_file.append('property\n moldenfile\nmolden_norm nwchem\nend\n')
                Main_file.append('{}\ntask dft property\n'.format(DFT_DIRECS[j]))
            else:
                Main_file.append('{}'.format(DFT_DIRECS[j]))
            
        for k in range(0, len(Main_file)):
            file_out.write(str(Main_file[k]))
            
        file_out.close()
    # we're done, change back to the working directory if we haven't already 
    if os.getcwd() != top_direc:
        os.chdir(workdir)


parser = argparse.ArgumentParser(description='''
Hi! I generate nwchem input files for dft/so-dft calculations on the f-elements.''',
epilog='\n Usage: [insert-name].py -c LaF3 -b ANO -d sodft -o y \n')

parser.add_argument('-c', '--compound', help="Name of compound", required=True)
parser.add_argument('-b', '--relbasis', help="basis type: SEG, ANO, AE", required=False)
parser.add_argument('-iv', '--initvecs', help="functional to use as initial vectors, else uses atomic guess", required=False)
parser.add_argument('-o', '--optimize', help="do an optimization+freq", required=False)
parser.add_argument('-d', '--dft_task', help="task directive for: dft sodft both, default=dft", required=False)
parser.add_argument('-fs', '--infuncs', help="list of functionals to operate on, seperated by commas. svwn,b3lyp,m06l", required=False)
# parser.add_argument('-g','--geom', help='selects starting geom file (initial,tpss,...), default=tpss', required=False)
# parser.add_argument('-e', '--ecptype',     help="ECP type WB", required=False)
# parser.add_argument('-aug', '--augmented', help="augmented ligand set?", required=False)
# parser.add_argument('-rl', '--relativistic', help='type of rel calculation (rp, ae)', required=False)

args = vars(parser.parse_args())

compnd = args['compound']
# rel_basis = args['relbasis']

if args['relbasis']:
    rel_basis = args['relbasis']
else:
    rel_basis = 'SEG'

if args['optimize']:
    optimize = 'y'
else:
    optimize = 'n'
    
if args['dft_task']:
    dft_direc = args['dft_task']
else:
    dft_direc = 'dft'

# if args['geom']:
#     geom_read = args['geom']
# else:
#     geom_read = 'tpss'

if args['initvecs']:
    init_guess = args['initvecs']
else:
    init_guess = 'atomic'

if args['infuncs']:
    func_str = str(args['infuncs'])
    input_func = re.split(',', func_str)
else:
    input_func = ['tpss', 'm06l', 'b3lyp', 'svwn', 'pbe']


def gen_nw_DKH_dft_input(input_set, dft_direc='both',init_guess='atomic', optimize='n', Nbas_keys=['','T'], geom_read='tpss'):
    '''
    this program generates a set of DFT functional inputs that run in NWChem

    this routine is designed for DK3 all-electron calculations, maybe I'll implement zora, if for some reason
    someone gets stuck doing a benchmark for those.

    Function arguments
    required:
        input_set: the molecule you are making
    optional arguments:
        dft_direc= 'dft', 'sodft', 'both', default='both'
        optimize= 'n', 'y' ; default='n'
        Nbas_keys[0] = '-aug' ; default=''
        Nbas_keys[1] = 'T','Q','D' ; default='T'
        Note, I've only downloaded the T-zeta sets, so if you want to use others, go download them. 

    To Do:
        make options for memory specifications
    '''

    xckey, rel_set = init_params()
    
    # hard coded set of functionals built in for generator
    
    # lucas
#     functionals = ['tpss', 'm06l']
#     functionals = ['svwn', 'pbe', 'b3lyp']
#     functionals = ['tpss']
    # emily
    functionals = ['pbe', 'b3lyp']

#    functionals = ['svwn', 'pbe', 'tpss', 'm06l', 'b3lyp']
#    functionals = ['tpss', 'm06l']  
    
    workdir = top_direc
    cmp = input_set
    # get multiplicities
    mult_data = pd.read_hdf('input_gendb.h5', 'multiplicity')

    # if no multiplicity found, ask for one
    if cmp not in mult_data.index:
        print('No multiplicity value found for {}'.format(cmp))
        M = str(input('Enter in a multiplicty to use: '))
    else:
        M = str(int(mult_data[cmp]))
        
    if optimize == None:
        optimize = 'n'

    sub_list = re.findall(r'[A-Z][a-z]*|\d+', cmp)
        
    if len(sub_list) == 1:
        elem_list = sub_list

    else:
        elem_list = re.findall(r'[A-Z][a-z]*', cmp)
        
        

#### differences 
    basis_ext = '{}cc-pV{}Z-DK'.format(Nbas_keys[0], Nbas_keys[1])

    BASIS = []

    for atom in elem_list:
        BASIS.append(get_basis(atom, basis_ext))
        BASIS.append('\n')

#     vec_input = ['atomic']
    if optimize == 'n':
        card = 'energy'
        func_span = range(0, len(functionals))
        if dft_direc == 'both':
            DFT_DIRECS = []
            DFT_DIRECS.append('task dft energy')
            DFT_DIRECS.append('task sodft energy')
            exten = []
            exten.append('ae')
            exten.append('so')
#             vec_input.append('')
        else:
            DFT_DIRECS = ['task {} energy'.format(dft_direc)]
            exten = ['ae']

        if init_guess != 'atomic':
            vec_input = '{}.{}.{}.movecs'.format(cmp, init_guess, exten[0])

        new_dir = '{}'.format(cmp)
        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)
        new_dir = '{}/DKH'.format(cmp)
        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)
        os.chdir(new_dir)

    elif optimize == 'y':
        raise Exception("Let's hold off on optimizing in the all-electron basis sets for now.")

#------------------------- Main Generator Routine ------------------------#

    for i in func_span:
        Main_file = []
        file_out = open('{}.{}.{}.nw'.format(cmp,functionals[i],exten[0]), 'w', newline='\n')
        Main_file.append('start {}.{}.{}\n'.format(cmp, functionals[i], exten[0]))
        Main_file.append('title "{} {} ae DK-basis {}"\n'.format(cmp, functionals[i], card))
        Main_file.append('memory total 6000 stack 2000 mb\necho\n\n')

        Main_file.append('geometry\n')
        GEO = get_the_geom(functionals[i], cmp, os.getcwd())
        Main_file.append(GEO)
        Main_file.append('end\n')
        Main_file.append('\n\nbasis spherical\n')
        for j in range(0, len(BASIS)):
            Main_file.append(BASIS[j])
        Main_file.append('end\n\n')    


        Main_file.append('\nrelativistic\n douglas-kroll DK3Full\nend')
        for j in range(0, len(DFT_DIRECS)):

            Main_file.append('\n\ndft\n')
            Main_file.append(' mult {}\n'.format(M))
            Main_file.append(' odft\n {}\n'.format(xckey[functionals[i]]))

            if j == 0:
                if init_guess == 'atomic':
                    inp_arg = 'atomic'
                else:
                    inp_arg = vec_input
                out_arg = '{}.{}.{}.movecs'.format(cmp, functionals[i], exten[j])
                Main_file.append(' vectors input {} output {}\n'.format(inp_arg, out_arg))

            else:
                inp_arg = '{}.{}.{}.movecs'.format(cmp, functionals[i], exten[j-1])
                out_arg = '{}.{}.{}.movecs'.format(cmp, functionals[i], exten[j])
                Main_file.append(' vectors input {} output {}\n'.format(inp_arg, out_arg))
                                 
            Main_file.append(' maxiter 200\nend\n\n') 
            # if first pass, then add line to generate nbo file 
            # nevermind, nbo does not support h functions (lazy fucks), and guess
            # what the AE basis sets have? H functions! So, can't do this. 
#             if j == 0 and exten[0] != 'sopt':
#                 Main_file.append('property\n nbofile\nend\n\n')
# #                 Main_file.append('property\n moldenfile\nmolden_norm nwchem\nend\n')
#                 Main_file.append('{}\ntask dft property\n'.format(DFT_DIRECS[j]))
#             else:
#                 Main_file.append('{}'.format(DFT_DIRECS[j]))
            Main_file.append('{}'.format(DFT_DIRECS[j]))


        for k in range(0, len(Main_file)):
            file_out.write(str(Main_file[k]))

        file_out.close()
    if os.getcwd() != top_direc:
        os.chdir(workdir)

if args['relbasis'] == 'AE' or args['relbasis'] == 'DKH' or args['relbasis'] == 'DK':
    gen_nw_DKH_dft_input(compnd, dft_direc=dft_direc, init_guess=init_guess, optimize='n', Nbas_keys=['','T'])
else: 
#     gen_nw_recp_dft_inputv2(compnd, rel_basis, dft_direc=dft_direc, init_guess=init_guess, optimize=optimize, level='WB', Nbas_keys='', geom_read=geom_read)
    gen_nw_recp_dft_inputv2(compnd, rel_basis, dft_direc=dft_direc, init_guess=init_guess, input_func=input_func, optimize=optimize, level='WB', Nbas_keys='')
