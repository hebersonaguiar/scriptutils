#!/bin/bash

COMMAND=$(  hostname | grep -c 'mme.gov.br' )
HOSTNAME=$( hostname )
RPM=$( which rpm )
GREP=$( which grep )
YUM=$( which yum )
RM=$( which rm )
ECHO=$( which echo )
SYSTEMCTL=$( which systemctl )
PACKAGE=$( $RPM -aq | $GREP 'puppet-agent' )
HOSTNAMECTL=$( which hostnamectl )

#COLORS
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

installPuppet(){

        $RPM -aq | $GREP 'puppet-agent' &> /dev/null

        if [ $? -eq 0 ]; then


            $ECHO -e "${GREEN}[  OK  ] ${NC} Puppet Agent is installed \n ${NC}"
            $ECHO -e "${GREEN}[  OK  ] ${NC} Removing Puppet Agent - Version: ${RED}( $PACKAGE )\n ${NC}"

            PUPPET=$( which puppet )

            $YUM remove -y $PACKAGE

            $ECHO -e "${RED}[  OK  ] ${NC} Removing instaled directory Puppet Agent\n"

            $RM -rf /etc/puppetlabs/

            $RM -rf /opt/puppetlabs/

            $ECHO -e "${GREEN}[  OK  ] ${NC} Instaling Puppet Agent \n"

            $YUM install -y puppet-agent

            $ECHO -e "${GREEN}[  OK  ] ${NC} Recreating file puppet.conf\n"
            > /etc/puppetlabs/puppet/puppet.conf
            $ECHO "[main]
        certname = $HOSTNAME.mme.gov.br
        server = srv043.mme.gov.br
        environment = production" > /etc/puppetlabs/puppet/puppet.conf

            PUPPET=$( which puppet )

            $ECHO -e "${GREEN}[  OK  ] ${NC} Executing puppet agent -t\n"

            $PUPPET agent -t

            $ECHO -e "${GREEN}[  OK  ] ${NC} Starting service puppet agent \n"

            $SYSTEMCTL start puppet
            $SYSTEMCTL enable puppet

            $ECHO -e "${GREEN}[  OK  ] ${NC} Removing job of crontab \n"

            > /var/spool/cron/root
        else


            $ECHO -e "${RED}[  OK  ] ${NC} Puppet Agent not is installed \n"
            $ECHO -e "${GREEN}[  OK  ] ${NC} Instaling Puppet Agent \n "

            $YUM install -y puppet-agent

            $ECHO -e "${GREEN}[  OK  ] ${NC} Recreating file puppet.conf \n"
            > /etc/puppetlabs/puppet/puppet.conf
            $ECHO "[main]
        certname = $HOSTNAME.mme.gov.br
        server = srv043.mme.gov.br
        environment = production" > /etc/puppetlabs/puppet/puppet.conf

            PUPPET=$( which puppet )

            $ECHO -e "${GREEN}[  OK  ] ${NC} Executing puppet agent -t\n"

            $PUPPET agent -t

            $ECHO -e "${GREEN}[  OK  ] ${NC} Starting service puppet agent \n"

            $SYSTEMCTL start puppet
            $SYSTEMCTL enable puppet

            $ECHO -e "${GREEN}[  OK  ] ${NC} Removing job of crontab \n"

            > /var/spool/cron/root
        fi
        exit 0
}

if [ $COMMAND -eq 0 ]; then
    echo $HOSTNAME
    echo "Wrong Hostname, Correcting"
    $HOSTNAMECTL set-hostname $HOSTNAME.mme.gov.br

    sleep 10

    installPuppet

else
    echo "Correct Hostname"
    echo $HOSTNAME

    sleep 5

    installPuppet
fi
exit 0
