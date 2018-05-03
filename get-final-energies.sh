#!/bin/bash

# this launches the actual energy search 
# now its just one script, yay!
# this took like three hours so 
Etype='DFT'
#Etype='SO-DFT'
FUNC='tpss'
#FUNC='m06l'
BDIR='SEG'
#BDIR='ANO'

LnXn='LaF PrF NdF EuF GdF TbF DyF HoF ErF TmF YbF 
      LuF LaO CeO PrO NdO SmO EuO GdO TbO DyO HoO 
      ErO TmO YbO LuO LaF2 SmF2 EuF2 LaCl2 CeCl2 
      PrCl2 NdCl2 SmCl2 EuCl2 GdCl2 TbCl2 HoCl2 
      ErCl2 LaF3 CeF3 PrF3 NdF3 GdF3 TbF3 DyF3 
      HoF3 ErF3 LuF3 LaCl3 CeCl3 PrCl3 NdCl3 GdCl3'

atoms='La Ce Pr Nd Sm Eu Gd Tb Dy Ho Er Tm Yb Lu'

workdir=`pwd`
for i in $LnXn
do 
    # execute grep "Total DFT"/"Total SO-DFT" from any out file for the current functional in the directory we want 
    aval=`find ./${i}/${BDIR} -name *.${FUNC}.*.out -execdir grep "Total $Etype" '{}' \;`
    # pipe (send output of command) to awk and print the 5th column, pipe again and list only the last result
    # this result is set to the variable Fval
    Fval=`echo $aval | awk '{print$5}' | tail -n1`
        # if the Fval is nothing then the calculation was not done or errored out very early on 
        # likely due to a input error any diis/opt failure still will print the energy out
        if [[ -z $Fval ]]; then 
            echo "" 
        # if Fval is the = sign, then go get the sixth column instead, this will be the value we need 
        elif [[ $Fval == '=' ]]; then
            Fval2=`echo $aval | awk '{print$6}' | tail -n1`
            echo "$Fval2"
        # print out the values found
        else
            echo "$Fval"
        fi 
done 

