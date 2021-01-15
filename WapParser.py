#!/usr/bin/python3

'''
This script opens a downloaded json file from the WiFi Pineapple.
The file contains information from a recon scan.
The script parses the json file, removes duplicate SSIDs,
and outputs the number of APs, Associated Clients,
the channel numbers used, the AP security encryption used, 
and the number of unassociated clients used.
'''

import json
import sys

def main():
    
    if len(sys.argv) <= 1:
        sys.stdout.write("\t-::: ap-parser.py :::-\n")
        sys.stdout.write("# Returns parsed data from a wifi pineapple generated json file.\n")
        sys.stdout.write("\nUsage: %s [pineapple json file]\n" % (sys.argv[0]))
        sys.stdout.flush()
        exit(0)
    
    #Set variabales for capture fields     
    accessPoints = set()
    associatedClients = set()
    apChannels = set()
    apSecurity = set()
    openSecurity = set()
    apSecurityType = set()
    unassociatedClients = set()
    
    #load json capture
    pineapple_capture = sys.argv[1]
    with open(pineapple_capture) as f:
        data = json.loads(f.read())
        
        ap = data['1']['aps']
        
        for point in ap:
            
            accessPoints.add(point)
            apChannels.add(ap[point]['channel'])
            
            for client in ap[point]['clients']:
                associatedClients.add(client)
                
            if ap[point]['encryption'] != 'Open':
                apSecurity.add(point)
                apSecurityType.add(ap[point]['encryption'])
                
            if ap[point]['encryption'] == 'Open':
                openSecurity.add(point)
        
        for UAC in data['1']['unassociatedClients']:
            unassociatedClients.add(UAC)
            
    print("The number of Access Points is:", len(accessPoints))
    print("The number of Associated Clients is:", len(associatedClients))
    print("The channels used by the Access Points are:", sorted(apChannels))
    print("There are", len(apSecurity), "Access Points employing security.")
    print("There are", len(openSecurity), "Access Points set to Open.\n" )
    print("The types of security used are:")
    
    for types in sorted(apSecurityType):
        print("- " + types)
    
    print()
    print("The number of Unassociated Clients detected is:", len(unassociatedClients))

if __name__ == "__main__":
    main()
