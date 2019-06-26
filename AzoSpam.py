import random, string

fileFirstnames = "first-names.txt"

fileLastnames = "last-names.txt"

fileEmails = "mail-domains.txt"

glob_hostname = ""
glob_username = ""
glob_email = ""
glob_guid = ""
glob_windowsversion = []

''' 
Version codes taken from https://docs.microsoft.com/en-us/windows/desktop/sysinfo/operating-system-version
For the sake of simplicity I did not add Windows XP 64 Bit since it has another version code than 32 bit version
and the processor architecture is generated elsewhere in this script and has to fit the version code to not be suspicous
'''
def create_windsversion():
    versions = [["Windows 10", "10.0"],
                ["Windows Server 2019", "10.0"],
                ["Windows Server 2016", "10.0"],
                ["Windows 8.1", "6.3"],
                ["Windows Server 2012 R2", "6.3"],
                ["Windows 8", "6.2"],
                ["Windows Server 2012", "6.2"],
                ["Windows 7", "6.1"],
                ["Windows Server 2008 R2", "6.1"],
                ["Windows Server 2008", "6.0"],
                ["Windows Vista", "6.0"],
                ["Windows Server 2003 R2", "5.2"],
                ["Windows Server 2003", "5.2"],
                ["Windows XP", "5.1"]]

    global glob_windowsversion
    glob_windowsversion = versions[random.randint(0, len(versions) - 1)]
    return glob_windowsversion


''' Here we generate our pseudo random Guid which will later be used to post the report to the panel'''
def create_guid():
    # Sample: 3BF5F2C-1343A2EC-6F2D975A-27E28A13-6E1212342
    # The different parts have different lengths which are defined here:
    part_lengths = [7,8,8,8,8,9]
    guid = ""

    for length in part_lengths:
        x = ''.join(random.choice("ABCDEFGH0123456789") for n in range(length))

        # Only add the dash if it is NOT the last part of the Guid:
        if length != 9:
            guid = guid + x + "-"
        else:
            guid = guid + x

    global glob_guid
    glob_guid = guid
    return glob_guid


def create_hostname():
    prefixes = ['WIN-', 'Dev-', 'SRV', '']
    rand_prefix = random.randint(0,3)

    min_length = 4
    max_length = 12

    actual_length = random.randint(min_length, max_length)

    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(actual_length))

    global glob_hostname
    glob_hostname = prefixes[rand_prefix] + x
    return glob_hostname


def create_username():
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
    return glob_username


def create_mailaddress():
    with open(fileEmails) as fEmails:
        emails = fEmails.read().splitlines()

    global glob_email
    glob_email = glob_username + "@" + emails[random.randint(0, len(emails))]
    return glob_email


create_hostname()
create_username()
create_mailaddress()
create_guid()
create_windsversion()

print "Hostname: " + glob_hostname
print "Username: " + glob_username
print "Mail: " + glob_email
print "Guid: " + glob_guid
print "Windows Version: " + glob_windowsversion[0]
print "Windows Version Code: " + glob_windowsversion[1]
