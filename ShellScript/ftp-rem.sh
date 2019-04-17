#!/bin/bash

############################################################################
#Script Name	: remessa.sh                                                                                           
#Description	: Script for send files to FTP Banco do Brasil from Saped                                                                                
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
DIR="/srv/ftp-bb-remessa"
DIRBACKUP="/srv/ftp-bb-backup"
USERNAME=""
PASSWORD=""
IPFTP=""

#COLORS
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

if [ "$($LS -A $DIR)" ]; then
     $ECHO -e "${GREEN}[  OK  ] ${NC} Take action $DIR is not Empty \n ${NC}"
     $ECHO -e "${GREEN}[  OK  ] ${NC} Send files to ftp remessa \n ${NC}"
     $LFTP -e "mput -O remessa $DIR/*; bye" -u $USERNAME:$PASSWORD $IPFTP
     $ECHO -e "${GREEN}[  OK  ] ${NC} \n Move files from remessa to backup \n ${NC}"
     $MV $DIR/* $DIRBACKUP
     # $ECHO -e "${RED}[  OK  ] ${NC} Delete file from remessa \n ${NC}"
     # $RM -rf $DIR/*
else
    $ECHO -e "${GREEN}[  OK  ] ${NC} $DIR is Empty ${NC}"
fi
