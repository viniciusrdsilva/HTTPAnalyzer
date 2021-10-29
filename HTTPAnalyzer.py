import requests
import argparse
import os,sys
import subprocess
from concurrent.futures import ThreadPoolExecutor

#VARIAVEIS
list_of_urls = []
output = ""
outputBool = False

#FUNÇÕES
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    ##UNDERLINE = '\033[4m'

def welcome():
    print(bcolors.OKCYAN + "-----------------------------------------------------------------------" + bcolors.ENDC)
    print(bcolors.OKCYAN + "| This program is an analyzer to find HTTP site with misconfiguration |" + bcolors.ENDC)
    print(bcolors.OKCYAN + "-----------------------------------------------------------------------" + bcolors.ENDC)
    print(bcolors.OKCYAN + "|" + bcolors.OKBLUE + "                   Create By Wh0aMn1c0 and Th3Br41n                  " + bcolors.OKCYAN + "|"  + bcolors.ENDC)
    print(bcolors.OKCYAN + "----------------------------------------------------------------------" + bcolors.ENDC)

def run():
    print(bcolors.WARNING + "Starting the status code scan" + bcolors.ENDC)

def get_url(url):
    return requests.get("http://"+url, allow_redirects=False).status_code

def report(site):
    status_code = get_url(site)
    if(status_code == 301):
        print(bcolors.OKBLUE + site + " ["  + str(status_code) + "] " + bcolors.OKGREEN + " - IT'S OK!" + bcolors.ENDC)
    else:
        print(bcolors.OKBLUE + site + " [" + str(status_code) + "] " + bcolors.BOLD + bcolors.FAIL + " - PLEASE VERIFY ME!" + bcolors.ENDC)

def runFile(path):
    if(os.path.exists(path)):
        with open(path) as f:
            lines = f.readlines()
        for lU in lines:
            list_of_urls.append((lU).rstrip())
    else:
        print("File not found: "+path)
        print("Try the full path")
        sys.exit(1)

def saveToOutput(text):

    if(outputBool):
        f = open(output, "a")
        f.write(text+"\n")
        f.close()


#PARSE PARA UDO DE ARGUMENTOS
parser = argparse.ArgumentParser(prog='CheckStatus', conflict_handler='resolve')
parser.add_argument('-u', help='Simple url')
parser.add_argument('-uL', help='List url')
parser.add_argument('-o', help='Output file')
args = parser.parse_args()
output = args.o

#EXECUÇÃO DO COMANDO EM SI EM MULTITHREAD
if(args.o):
    output = args.o
    outputBool = True
    print("Writing on "+args.o)
if(args.u):
    welcome()
    run()
    report(args.u)

elif(args.uL):
    welcome()
    #LISTANDO DOMINIOS
    domain = args.uL
    print(bcolors.WARNING + "Listing subdomains using google." + bcolors.ENDC)
    print(bcolors.WARNING + "This process may take a while. " + bcolors.ENDC)
    process = subprocess.run(['sublist3r', '-d', domain, '-o', 'domains'], stdout=open(os.devnull, 'wb'))

    run()
    runFile('domains')
    with ThreadPoolExecutor(max_workers=20) as pool:
        response_list = list(pool.map(report,list_of_urls))