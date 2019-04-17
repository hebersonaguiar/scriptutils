#!/bin/bash

############################################################################
#Script Name	: retorno.sh                                                                                           
#Description	: Script for get files to FTP Banco do Brasil to Saped                                                                                
#Args           : No Args                                                                                          
#Author       	: Heberson Rocha Aguiar                                                
#Email         	: heberson.aguiar@hepta.com.br                                           
############################################################################

#VARIABLES

LFTP=$( which lftp )
GREP=$( which grep )
CAT=$( which cat )
LS=$( which ls )
MV=$( which mv )
RM=$( which rm )
ECHO=$( which echo )
AWK=$( which awk )
DIR="/srv/ftp-bb-retorno"
USERNAME=""
PASSWORD=""
IPFTP=""

#COLORS
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


#CHECK IF FTP RETORNO IS EMPTY

$LFTP -e "ls retorno; bye" -u $USERNAME:$PASSWORD $IPFTP > /srv/result

ISEMPTY=$( $CAT /srv/result | $GREP -w 'total' | $AWK '{print $2}' )


if [ "$ISEMPTY" -eq "0" ]; then
	$ECHO -e "${GREEN}[  OK  ] ${NC} Retorno is Empty ${NC}"
else
    $ECHO -e "${GREEN}[  OK  ] ${NC} Retorno is not Empty \n ${NC}"
    $ECHO -e "${GREEN}[  OK  ] ${NC} Get files to ftp retorno \n ${NC}"
    $LFTP -e "mirror --verbose --use-pget-n=8 -c --verbose retorno $DIR ; bye" -u $USERNAME:$PASSWORD $IPFTP
fi

