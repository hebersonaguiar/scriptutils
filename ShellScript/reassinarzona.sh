#!/bin/bash

############################################################################
#Script Name	: reassinarZona.sh                                                                                           
#Description	: Script para reassinar zona DNS externo.                                                                                
#Args           : No Args                                                                                          
#Author       	: Rede Interna                                                
#Email         	: rede@mme.gov.br                                           
############################################################################

#VARIABLES

GREP=$( which grep )
CAT=$( which cat )
LS=$( which ls )
MV=$( which mv )
RM=$( which rm )
ECHO=$( which echo )
AWK=$( which awk )
DIR="/var/named/data"
FILE=""
SERIAL=$( $CAT $DIR/$FILE | $GREP -w Serial | $AWK '{print $1}' )
NOW=$(date +"%Y%m%d")
SED=$( which sed )
DNSSEC=$( which dnssec-signzone )
SERVICE=$( which service )
RNDC=$( which rndc )

$SED -i "s/$SERIAL/$NOW/g" $DIR/$FILE
$DNSSEC -S -z -o mme.gov.br $DIR/$FILE
$SERVICE named restart
$RNDC reload
