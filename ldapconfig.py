CHROOTPW = """
dn: olcDatabase={0}config,cn=config
changetype: modify
add: olcRootPW
olcRootPW: SSHA_KEY
"""

CHDOMAIN="""
dn: olcDatabase={1}monitor,cn=config
changetype: modify
replace: olcAccess
olcAccess: {0}to * by dn.base="gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth"
  read by dn.base="cn=admin,dc=mlogcn,dc=inn" read by * none

dn: olcDatabase={2}hdb,cn=config
changetype: modify
replace: olcSuffix
olcSuffix: dc=mlogcn,dc=inn

dn: olcDatabase={2}hdb,cn=config
changetype: modify
replace: olcRootDN
olcRootDN: cn=admin,dc=mlogcn,dc=inn

dn: olcDatabase={2}hdb,cn=config
changetype: modify
add: olcRootPW
olcRootPW: SSHA_KEY

dn: olcDatabase={2}hdb,cn=config
changetype: modify
add: olcAccess
olcAccess: {0}to attrs=userPassword,shadowLastChange by
  dn="cn=admin,dc=mlogcn,dc=inn" write by anonymous auth by self write by * none
olcAccess: {1}to dn.base="" by * read
olcAccess: {2}to * by dn="cn=admin,dc=mlogcn,dc=inn" write by * read
"""

ETC_KRB5="""
[logging]
   default = FILE:/var/log/krb5libs.log
   kdc = FILE:/var/log/krb5kdc.log
   admin_server = FILE:/var/log/kadmind.log

  [libdefaults]
   dns_lookup_realm = false
   ticket_lifetime = 24h
   renew_lifetime = 7d
   forwardable = true
   rdns = false
   default_realm = MLOGCN.INN

  [realms]
   MLOGCN.INN = {
    kdc = KDC_SERVER
    admin_server = KDC_SERVER
    default_domain = mlogcn.inn
    database_module = openldap_ldapconf
   }

  [domain_realm]
   .mlogcn.inn = MLOGCN.INN
   mlogcn.inn = MLOGCN.INN

  [dbmodules]
   openldap_ldapconf = {
    db_library = kldap
    ldap_kdc_dn = "cn=admin,dc=mlogcn,dc=inn"

    # this object needs to have read rights on
    # the realm container, principal container and realm sub-trees
    ldap_kadmind_dn = "cn=admin,dc=mlogcn,dc=inn"

    # this object needs to have read and write rights on
    # the realm container, principal container and realm sub-trees
    ldap_service_password_file = /etc/krb5kdc/service.keyfile
    ldap_kerberos_container_dn = cn=container,dc=mlogcn,dc=inn
    ldap_servers = ldap://KDC_SERVER
    ldap_conns_per_server = 5
  }
"""

KERBEROS="""
dn: cn=kerberos,cn=schema,cn=config
objectClass: olcSchemaConfig
cn: kerberos
olcAttributeTypes: {0}( 2.16.840.1.113719.1.301.4.1.1 NAME 'krbPrincipalName
 ' EQUALITY caseExactIA5Match SUBSTR caseExactSubstringsMatch SYNTAX 1.3.6.1
 .4.1.1466.115.121.1.26 )
olcAttributeTypes: {1}( 1.2.840.113554.1.4.1.6.1 NAME 'krbCanonicalName' EQU
 ALITY caseExactIA5Match SUBSTR caseExactSubstringsMatch SYNTAX 1.3.6.1.4.1.
 1466.115.121.1.26 SINGLE-VALUE )
olcAttributeTypes: {2}( 2.16.840.1.113719.1.301.4.3.1 NAME 'krbPrincipalType
 ' EQUALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )
olcAttributeTypes: {3}( 2.16.840.1.113719.1.301.4.5.1 NAME 'krbUPEnabled' DE
 SC 'Boolean' SYNTAX 1.3.6.1.4.1.1466.115.121.1.7 SINGLE-VALUE )
olcAttributeTypes: {4}( 2.16.840.1.113719.1.301.4.6.1 NAME 'krbPrincipalExpi
 ration' EQUALITY generalizedTimeMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.24
 SINGLE-VALUE )
olcAttributeTypes: {5}( 2.16.840.1.113719.1.301.4.8.1 NAME 'krbTicketFlags'
 EQUALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )
olcAttributeTypes: {6}( 2.16.840.1.113719.1.301.4.9.1 NAME 'krbMaxTicketLife
 ' EQUALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )
olcAttributeTypes: {7}( 2.16.840.1.113719.1.301.4.10.1 NAME 'krbMaxRenewable
 Age' EQUALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALU
 E )
olcAttributeTypes: {8}( 2.16.840.1.113719.1.301.4.14.1 NAME 'krbRealmReferen
 ces' EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.12 )
olcAttributeTypes: {9}( 2.16.840.1.113719.1.301.4.15.1 NAME 'krbLdapServers'
  EQUALITY caseIgnoreMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )
olcAttributeTypes: {10}( 2.16.840.1.113719.1.301.4.17.1 NAME 'krbKdcServers'
  EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.12 )
olcAttributeTypes: {11}( 2.16.840.1.113719.1.301.4.18.1 NAME 'krbPwdServers'
  EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.12 )
olcAttributeTypes: {12}( 2.16.840.1.113719.1.301.4.24.1 NAME 'krbHostServer'
  EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
olcAttributeTypes: {13}( 2.16.840.1.113719.1.301.4.25.1 NAME 'krbSearchScope
 ' EQUALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )
olcAttributeTypes: {14}( 2.16.840.1.113719.1.301.4.26.1 NAME 'krbPrincipalRe
 ferences' EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1
 .12 )
olcAttributeTypes: {15}( 2.16.840.1.113719.1.301.4.28.1 NAME 'krbPrincNaming
 Attr' EQUALITY caseIgnoreMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 SINGLE-
 VALUE )
olcAttributeTypes: {16}( 2.16.840.1.113719.1.301.4.29.1 NAME 'krbAdmServers'
  EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.12 )
olcAttributeTypes: {17}( 2.16.840.1.113719.1.301.4.30.1 NAME 'krbMaxPwdLife'
  EQUALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )
olcAttributeTypes: {18}( 2.16.840.1.113719.1.301.4.31.1 NAME 'krbMinPwdLife'
  EQUALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )
olcAttributeTypes: {19}( 2.16.840.1.113719.1.301.4.32.1 NAME 'krbPwdMinDiffC
 hars' EQUALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VAL
 UE )
olcAttributeTypes: {20}( 2.16.840.1.113719.1.301.4.33.1 NAME 'krbPwdMinLengt
 h' EQUALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE
 )
olcAttributeTypes: {21}( 2.16.840.1.113719.1.301.4.34.1 NAME 'krbPwdHistoryL
 ength' EQUALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VA
 LUE )
olcAttributeTypes: {22}( 1.3.6.1.4.1.5322.21.2.1 NAME 'krbPwdMaxFailure' EQU
 ALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )
olcAttributeTypes: {23}( 1.3.6.1.4.1.5322.21.2.2 NAME 'krbPwdFailureCountInt
 erval' EQUALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VA
 LUE )
olcAttributeTypes: {24}( 1.3.6.1.4.1.5322.21.2.3 NAME 'krbPwdLockoutDuration
 ' EQUALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )
olcAttributeTypes: {25}( 1.2.840.113554.1.4.1.6.2 NAME 'krbPwdAttributes' EQ
 UALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )
olcAttributeTypes: {26}( 1.2.840.113554.1.4.1.6.3 NAME 'krbPwdMaxLife' EQUAL
 ITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )
olcAttributeTypes: {27}( 1.2.840.113554.1.4.1.6.4 NAME 'krbPwdMaxRenewableLi
 fe' EQUALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE
  )
olcAttributeTypes: {28}( 1.2.840.113554.1.4.1.6.5 NAME 'krbPwdAllowedKeysalt
 s' EQUALITY caseIgnoreIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 SINGLE-
 VALUE )
olcAttributeTypes: {29}( 2.16.840.1.113719.1.301.4.36.1 NAME 'krbPwdPolicyRe
 ference' EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.
 12 SINGLE-VALUE )
olcAttributeTypes: {30}( 2.16.840.1.113719.1.301.4.37.1 NAME 'krbPasswordExp
 iration' EQUALITY generalizedTimeMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.24
  SINGLE-VALUE )
olcAttributeTypes: {31}( 2.16.840.1.113719.1.301.4.39.1 NAME 'krbPrincipalKe
 y' EQUALITY octetStringMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.40 )
olcAttributeTypes: {32}( 2.16.840.1.113719.1.301.4.40.1 NAME 'krbTicketPolic
 yReference' EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121
 .1.12 SINGLE-VALUE )
olcAttributeTypes: {33}( 2.16.840.1.113719.1.301.4.41.1 NAME 'krbSubTrees' E
 QUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.12 )
olcAttributeTypes: {34}( 2.16.840.1.113719.1.301.4.42.1 NAME 'krbDefaultEncS
 altTypes' EQUALITY caseIgnoreMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )
olcAttributeTypes: {35}( 2.16.840.1.113719.1.301.4.43.1 NAME 'krbSupportedEn
 cSaltTypes' EQUALITY caseIgnoreMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )
olcAttributeTypes: {36}( 2.16.840.1.113719.1.301.4.44.1 NAME 'krbPwdHistory'
  EQUALITY octetStringMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.40 )
olcAttributeTypes: {37}( 2.16.840.1.113719.1.301.4.45.1 NAME 'krbLastPwdChan
 ge' EQUALITY generalizedTimeMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.24 SING
 LE-VALUE )
olcAttributeTypes: {38}( 1.3.6.1.4.1.5322.21.2.5 NAME 'krbLastAdminUnlock' E
 QUALITY generalizedTimeMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.24 SINGLE-VA
 LUE )
olcAttributeTypes: {39}( 2.16.840.1.113719.1.301.4.46.1 NAME 'krbMKey' EQUAL
 ITY octetStringMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.40 )
olcAttributeTypes: {40}( 2.16.840.1.113719.1.301.4.47.1 NAME 'krbPrincipalAl
 iases' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )
olcAttributeTypes: {41}( 2.16.840.1.113719.1.301.4.48.1 NAME 'krbLastSuccess
 fulAuth' EQUALITY generalizedTimeMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.24
  SINGLE-VALUE )
olcAttributeTypes: {42}( 2.16.840.1.113719.1.301.4.49.1 NAME 'krbLastFailedA
 uth' EQUALITY generalizedTimeMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.24 SIN
 GLE-VALUE )
olcAttributeTypes: {43}( 2.16.840.1.113719.1.301.4.50.1 NAME 'krbLoginFailed
 Count' EQUALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VA
 LUE )
olcAttributeTypes: {44}( 2.16.840.1.113719.1.301.4.51.1 NAME 'krbExtraData'
 EQUALITY octetStringMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.40 )
olcAttributeTypes: {45}( 2.16.840.1.113719.1.301.4.52.1 NAME 'krbObjectRefer
 ences' EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.12
  )
olcAttributeTypes: {46}( 2.16.840.1.113719.1.301.4.53.1 NAME 'krbPrincContai
 nerRef' EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.1
 2 )
olcAttributeTypes: {47}( 1.3.6.1.4.1.5322.21.2.4 NAME 'krbAllowedToDelegateT
 o' EQUALITY caseExactIA5Match SUBSTR caseExactSubstringsMatch SYNTAX 1.3.6.
 1.4.1.1466.115.121.1.26 )
olcObjectClasses: {0}( 2.16.840.1.113719.1.301.6.1.1 NAME 'krbContainer' SUP
  top STRUCTURAL MUST cn )
olcObjectClasses: {1}( 2.16.840.1.113719.1.301.6.2.1 NAME 'krbRealmContainer
 ' SUP top STRUCTURAL MUST cn MAY ( krbMKey $ krbUPEnabled $ krbSubTrees $ k
 rbSearchScope $ krbLdapServers $ krbSupportedEncSaltTypes $ krbDefaultEncSa
 ltTypes $ krbTicketPolicyReference $ krbKdcServers $ krbPwdServers $ krbAdm
 Servers $ krbPrincNamingAttr $ krbPwdPolicyReference $ krbPrincContainerRef
  ) )
olcObjectClasses: {2}( 2.16.840.1.113719.1.301.6.3.1 NAME 'krbService' SUP t
 op ABSTRACT MUST cn MAY ( krbHostServer $ krbRealmReferences ) )
olcObjectClasses: {3}( 2.16.840.1.113719.1.301.6.4.1 NAME 'krbKdcService' SU
 P krbService STRUCTURAL )
olcObjectClasses: {4}( 2.16.840.1.113719.1.301.6.5.1 NAME 'krbPwdService' SU
 P krbService STRUCTURAL )
olcObjectClasses: {5}( 2.16.840.1.113719.1.301.6.8.1 NAME 'krbPrincipalAux'
 SUP top AUXILIARY MAY ( krbPrincipalName $ krbCanonicalName $ krbUPEnabled
 $ krbPrincipalKey $ krbTicketPolicyReference $ krbPrincipalExpiration $ krb
 PasswordExpiration $ krbPwdPolicyReference $ krbPrincipalType $ krbPwdHisto
 ry $ krbLastPwdChange $ krbLastAdminUnlock $ krbPrincipalAliases $ krbLastS
 uccessfulAuth $ krbLastFailedAuth $ krbLoginFailedCount $ krbExtraData $ kr
 bAllowedToDelegateTo ) )
olcObjectClasses: {6}( 2.16.840.1.113719.1.301.6.9.1 NAME 'krbPrincipal' SUP
  top STRUCTURAL MUST krbPrincipalName MAY krbObjectReferences )
olcObjectClasses: {7}( 2.16.840.1.113719.1.301.6.11.1 NAME 'krbPrincRefAux'
 SUP top AUXILIARY MAY krbPrincipalReferences )
olcObjectClasses: {8}( 2.16.840.1.113719.1.301.6.13.1 NAME 'krbAdmService' S
 UP krbService STRUCTURAL )
olcObjectClasses: {9}( 2.16.840.1.113719.1.301.6.14.1 NAME 'krbPwdPolicy' SU
 P top STRUCTURAL MUST cn MAY ( krbMaxPwdLife $ krbMinPwdLife $ krbPwdMinDif
 fChars $ krbPwdMinLength $ krbPwdHistoryLength $ krbPwdMaxFailure $ krbPwdF
 ailureCountInterval $ krbPwdLockoutDuration $ krbPwdAttributes $ krbPwdMaxL
 ife $ krbPwdMaxRenewableLife $ krbPwdAllowedKeysalts ) )
olcObjectClasses: {10}( 2.16.840.1.113719.1.301.6.16.1 NAME 'krbTicketPolicy
 Aux' SUP top AUXILIARY MAY ( krbTicketFlags $ krbMaxTicketLife $ krbMaxRene
 wableAge ) )
olcObjectClasses: {11}( 2.16.840.1.113719.1.301.6.17.1 NAME 'krbTicketPolicy
 ' SUP top STRUCTURAL MUST cn )
"""