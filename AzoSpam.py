import random, string

fileFirstnames = "first-names.txt"
firstnames = None

fileLastnames = "last-names.txt"
lastnames = None

fileEmails = "mail-domains.txt"
emails = None

glob_hostname = ""
glob_username = ""
glob_email = ""

def CreateHostname():	
	prefixes = ['WIN-', 'Dev-', 'SRV', '']
	rand_prefix = random.randint(0,3)
	
	min_length = 4
	max_length = 12
	
	actual_length = random.randint(min_length, max_length)
	
	x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(actual_length))
	
	global glob_hostname	
	glob_hostname = prefixes[rand_prefix] + x

def CreateUsername():
	with open(fileFirstnames) as fName:
		firstnames = fName.read().splitlines()
		
	with open(fileLastnames) as lName:
		lastnames = lName.read().splitlines()
		
	rand_firstname = random.randint(0, len(firstnames) - 1)
	rand_lastname = random.randint(0, len(lastnames) - 1)	
	
	rand_username_format = random.randint(0,2)
	
	global glob_username
	
	if rand_username_format == 0:
		glob_username = firstnames[rand_firstname] + "." + lastnames[rand_lastname]
	elif rand_username_format == 1:
		glob_username = firstnames[rand_firstname][0] + lastnames[rand_lastname]
	elif rand_username_format == 2:
		glob_username = lastnames[rand_lastname] + firstnames[rand_firstname][0]
	
def CreateMailAddress():
	with open(fileEmails) as fEmails:
		emails = fEmails.read().splitlines()
		
	global glob_email
	glob_email = glob_username + "@" + emails[random.randint(0, len(emails))]
	
CreateHostname()
CreateUsername()
CreateMailAddress()

print "Hostname: " + glob_hostname
print "Username: " + glob_username
print "Mail: " + glob_email
	