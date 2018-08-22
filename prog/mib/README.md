installer les outils snmp
télécharger (wget) le MIB de ACME (ACME-MIB.txt) dans /usr/share/snmp/mibs
à la ligne 9 il dit avoir besoin de SNMPv2-SMI, donc il faut le télécharger (https://opensource.apple.com/source/net_snmp/net_snmp-7/net-snmp/mibs/SNMPv2-SMI.txt?txt) dans /usr/share/snmp/mibs
`snmptranslate -m ACME-MIB -IR -Onf {OID}`
où {OID} est un identifiant, comme pid, descr ou contact
On a par exemple
`snmptranslate -m ACME-MIB -IR -Onf processEntry.pid`
qui donne
`.iso.org.dod.internet.private.enterprises.ACME.processTable.processEntry.pid`
`snmptranslate -m ACME-MIB -Tp -OS`
affiche le tree