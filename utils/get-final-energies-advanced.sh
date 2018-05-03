#!/bin/bash

# this launches the actual energy search 
# now its just one script, yay!
# this took like three hours so 
Etype='DFT'
FUNC='tpss'
BDIR='SEG'

command_usage()
{
   echo ' '
   echo 'Hi! This script gets energys for you: '
      echo ' '
      echo '   get_the_energies [dft/sodft]   -f the functional'
      echo '                                  -d the directory name (opt,seg,ano,dkh,so_opt)'
      echo '   '
      echo ' example: parse_energies dft -f tpss -d SEG  ' 
      echo '   '
   exit
}

if [ $# -eq 0 ] || [ ${1} == -h ] || [ ${1} == --help ]; then
   command_usage
   # else the energy type is taken as the first argument given. 
else
   Etype=${1}
   shift
   while [ "$1" != "" ]; do
       case $1 in
           -d | --type )     shift  
                             BDIR=${1}
                             ;;
           -f | --func )     shift  
                             FUNC=${1}
                             ;;
           -h  | --help )    command_usage
                             exit
                             ;;
           * )               echo 
                             echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                             echo "* You put something in wrong, (${1}) isn't an option *"
                             echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                             echo 
                             exit 1
       esac
       shift
   done
fi 

#Fval='DFT'

Etype=`echo $Etype | awk '{print toupper($0)}'`
if [[ $Etype == SODFT ]]; then 
    Etype='SO-DFT'
fi 

LnXn='LaF PrF NdF EuF GdF TbF DyF HoF ErF TmF YbF 
      LuF LaO CeO PrO NdO SmO EuO GdO TbO DyO HoO 
      ErO TmO YbO LuO LaF2 SmF2 EuF2 LaCl2 CeCl2 
      PrCl2 NdCl2 SmCl2 EuCl2 GdCl2 TbCl2 HoCl2 
      ErCl2 LaF3 CeF3 PrF3 NdF3 GdF3 TbF3 DyF3 
      HoF3 ErF3 LuF3 LaCl3 CeCl3 PrCl3 NdCl3 GdCl3'

#LnXn='LaF3'

atoms='La Ce Pr Nd Sm Eu Gd Tb Dy Ho Er Tm Yb Lu'
workdir=`pwd`

for i in $LnXn
do 
    aval=`find ./${i}/${BDIR} -name *.${FUNC}.*.out -execdir grep "Total $Etype" '{}' \;`
    Fval=`echo $aval | awk '{print$5}' | tail -n1`
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

