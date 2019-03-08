import ldap3
import json
import getpass

#need to add some custom DN features, but this should work for the bulk of ya 

#pip install ldap3 

def spn_lookup(address, dn, password):
	roastable = []
	x = 0
	server = ldap3.Server(address, get_info=ldap3.ALL)

	try: 
		conn = ldap3.Connection(server, dn, password, authentication=ldap3.NTLM, auto_bind=True)
		print('LDAP Bind Successful.')
		basedn = vars(conn.server.info)['other']['defaultNamingContext'][0]
		print ("The base search DN is: %s" % (basedn,))
		print ("Searching for roastable users...")

		conn.search(basedn,'(&(servicePrincipalName=*)(UserAccountControl:1.2.840.113556.1.4.803:=512)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(!(objectCategory=computer)))',  search_scope=ldap3.SUBTREE, attributes=[ldap3.ALL_ATTRIBUTES, ldap3.ALL_OPERATIONAL_ATTRIBUTES], paged_size=500)
		for entry in conn.entries:
			spn_account = json.loads(entry.entry_to_json())
			spn_account_DNs = spn_account['dn'].split(',')
			for attribute in spn_account_DNs:
				if attribute == "OU=Users" or attribute == "OU=users":
					roastable.append(spn_account['attributes']['cn'][0])
					x += 1

		if roastable != []:
			buf = "       "
			print ("\nFound %s potentially roastable users " % (x))
			print ("   Account CNs:")
			for user in roastable:
				print (buf + user)

	except ldap3.core.exceptions.LDAPBindError as e:
		print('LDAP Bind Failed: ', e) 

def main():
	address = input("server: ")
	domain = input("domain: ")
	username = input("username: ")
	password = getpass.getpass("password: ")
	spn_lookup(address, "%s\%s" % (domain, username), password)

if __name__ == '__main__':
	main()
