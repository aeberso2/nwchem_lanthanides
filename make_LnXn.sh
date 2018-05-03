#!/bin/bash



compounds='LaF PrF NdF EuF GdF TbF DyF HoF ErF TmF YbF LuF LaO CeO PrO NdO SmO EuO GdO TbO DyO HoO ErO TmO YbO LuO LaF2 SmF2 EuF2 LaCl2 CeCl2 PrCl2 NdCl2 SmCl2 EuCl2 GdCl2 TbCl2 HoCl2 ErCl2 LaF3 CeF3 PrF3 NdF3 GdF3 TbF3 DyF3 HoF3 ErF3 LuF3 LaCl3 CeCl3 PrCl3 NdCl3 GdCl3'
atoms='La Ce Pr Nd Sm Eu Gd Tb Dy Er Tm Ho Yb Lu'


for i in $atoms
    do
      gen_nwchem_input.py -c ${i} -d both -b SEG
#      gen_nwchem_input.py -c ${i} -d soft -b SEG -opt y
#      gen_nwchem_input.py -c ${i} -d both -b ANO -opt n
#      gen_nwchem_input.py -c ${i} -d both -b DK3 -opt n
    done

        
