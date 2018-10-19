#!/bin/bash

# this launches the actual energy search 
# now its just one script, yay!

# Etype => what type of energy
#Etype='DFT'
#Etype='SO-DFT'
BDIR=$1
Etype=$2

#func="tpss m06l"

if [[ $# == 0  ]]; then
    echo "enter a directory and etype to get"
    exit 1
fi

if [[ $Etype == 'DFT' ]]; then 
    Etype='DFT'
elif [[ $Etype == 'SO-DFT' ]]; then  
    Etype='SO-DFT'
else
    echo "unrecognized etype"
    exit 2
fi 

#if [[ $search_dir == 'so_opt' ]]; then
#    exten='sopt'

# which functional to collect energies from 
#FUNC='b3lyp'
#FUNC='tpss'
FUNC='svwn pbe tpss m06l b3lyp'
#FUNC=$1

LnXn='LaF PrF NdF EuF GdF TbF DyF HoF ErF TmF YbF 
      LuF LaO CeO PrO NdO SmO EuO GdO TbO DyO HoO 
      ErO TmO YbO LuO LaF2 SmF2 EuF2 LaCl2 CeCl2 
      PrCl2 NdCl2 SmCl2 EuCl2 GdCl2 TbCl2 HoCl2 
      ErCl2 LaF3 CeF3 PrF3 NdF3 GdF3 TbF3 DyF3 
      HoF3 ErF3 LuF3 LaCl3 CeCl3 PrCl3 NdCl3 GdCl3'

atoms='La Ce Pr Nd Sm Eu Gd Tb Dy Ho Er Tm Yb Lu'
haloxides='O F O2 F2 Cl2'

workdir=`pwd`
for i in $LnXn
    do 
        Fvals=$i
        for f in $FUNC; do 
            # execute grep "Total DFT"/"Total SO-DFT" from any out file for the current functional in the directory we want 
            # list only the last entry found. 
            aval=`find ./${i}/${BDIR} -name *.${f}.*.out -execdir grep "Total $Etype" '{}' \; | tail -n1`
            # pipe (send output of command) to awk and print the 5th column
            # this result is set to the variable Fval
            Fval=`echo $aval | awk '{print$5}'`
            # if the Fval is nothing then the calculation was not done or errored out very early on 
            # likely due to a input error any diis/opt failure still will print the energy out
            if [[ -z $Fval ]]; then 
#                Fval=''
                Fvals="$Fvals,$Fval"
            # if Fval is the = sign, then go get the sixth column instead, this will be the value we need 
            elif [[ $Fval == '=' ]]; then
                Fval2=`echo $aval | awk '{print$6}' | tail -n1`
#                echo "$Fval2"
                Fvals="$Fvals,$Fval2"
            # print out the values found
            else
#                Fval="${Fval}"
                Fvals="$Fvals,$Fval"
            fi 
        done 
        # we are done print out the column line
        echo "$Fvals,"
done 

