#Name: Dave van der Leek (1777075)
#Class:
#Programname: OVPNLogbrowser
#Description: Een programma om OpenVPN logfiles uit te lezen
from dis import code_info

version = 0.1


##########Imports##########
import re #For regex
import os
import argparse
from contextlib import suppress
import json


##########Arguments##########
parser = argparse.ArgumentParser(description="A program to browse and analyse OpenVPN logfiles", exit_on_error=True)
parser.add_argument("-c", "--config-location", help="path to the configuration file", default="config.json", dest="configfile")
parser.add_argument("-d", "--top5-connection-days", help="show the top 5 of days with the most (un)successful connections", choices=["failed", "successful"], dest="top5")
parser.add_argument("-g", "--show-menu", help="when called the menu will be showed", action="store_true", dest="gui")
parser.add_argument("-i", "--check-ip", help="check one or more ip-addresses for attempted connection(s)", nargs="*", dest="checkip")
parser.add_argument("-k", "--knownipfile-location", help="path to the knownip file", default="knownip.txt", dest="knownip")
parser.add_argument("-l", "--logfile-location", help="path to the OpenVPN logfile", default="openvpn.log", dest="logfile")
parser.add_argument("-m", "--used-management-commands", help="show all used management commando's", action="store_true", dest="management")
parser.add_argument("-n", "--new-ips", help="show all new IP-adresses", action="store_true", dest="shownip")
parser.add_argument("-p", "--non-openvpn-protocol", help="show how many connections weren't made with the OpenVPN protocol", action="store_true", dest="openvpnprot")
parser.add_argument("-t", "--top10-connection-ips", help="show the top 10 (failed) connection attempts", choices=["failed", "successful"], dest="top10")
arguments = parser.parse_args()


##########Functions##########

#This functions shows the menu
def dvdl_show_menu():
    print("\nHow may I assist you?\n"
    "1.  Show me the top 10 IP's with the most unsuccessful connections\n"
    "2.  Show me the top 10 IP's with most successful connections\n"
    "3.  Show me the top 5 days with the most unsuccessful connections\n"
    "4.  Show me the top 5 days with the most successful connections\n"
    "5.  Show me how many connections weren't made with OpenVPN\n"
    "6.  Show me all used management commando's\n"
    "7.  I want to check an IP-adres for attempted connection's\n"
    "8.  Show me all new IP-adresses\n"
    "9.  I want to create a new configuration file\n"
    "10. Show me all the program parameters\n"
    "11. Close program\n")
    #Ask which option needs to be selected
    choice = input("Make your choice: ")

    #Start the function that handles the menu
    dvdl_menu_handler(choice)

    #Give the user time to check the data
    input("Press return to continue...")


def dvdl_menu_handler(choice):
    
    #If no choice is valid this variable wll make sure an errormessage is shown
    error = True
    
    #Source: https://towardsdatascience.com/quick-python-tip-suppress-known-exception-without-try-except-a93ec34d3704
    with suppress(AttributeError):
        #If one of the first 2 choices were selected then...
        if choice == "1" or choice == "2" or choice.top10 == "failed" or choice.top10 == "successful":
            #Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False
            
            #Let the user know the program is generating the requested info
            print("\nGenerating...\n")
            
            with suppress(AttributeError):
                #Check which parameter the function needs and call the function
                if choice == "1" or choice.top10 == "failed":
                    results = dvdl_top10_inlog(unsuccessful=True)
                    # Show the title
                    print(f"Top 10 unsuccessful connections:")

            with suppress(AttributeError):
                if choice == "2" or choice.top10 == "successful":
                    results = dvdl_top10_inlog(unsuccessful=False)
                    # Show the title
                    print(f"Top 10 successful connections:")
    
            #A counter to show the positions
            position = 0
    
            #Loop trough the results...
            for result in results:
                #Add one to count
                position += 1
    
                #Check if it needs to be try or try's
                word = "try's"
                if result[1] == 1:
                    word = "try"
    
                #And show it to the user
                print(f"{position}: {result[0]} ({result[1]} {word})")
                
    with suppress(AttributeError):
        if choice == "3" or choice == "4" or choice.top5 == "failed" or choice.top5 == "successful":
            #Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False
            
            # Let the user know the program is generating the requested info
            print("\nGenerating...\n")
            print("option 3/4")

    with suppress(AttributeError):
        #If the user chose option 5 than...
        if choice == "5" or choice.openvpnprot:
            #Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False
            
            # Let the user know the program is generating the requested info
            print("\nGenerating...\n")
    
            #Call the right function...
            result = dvdl_non_ovpn_prot_counter()
    
            #And show the result
            print(f"{result} connection(s) weren't made with the OpenVPN protocol")

    with suppress(AttributeError):
        if choice == "6" or choice.management:
            #Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False
            
            # Let the user know the program is generating the requested info
            print("\nGenerating...\n")
            
            #Gat all used management commands
            results = dvdl_used_management_commands()
    
            # A counter to show the positions
            position = 0
    
            # Loop trough the results...
            for result in results:
                # Add one to count
                position += 1
    
                #Check if it needs to be time or times
                word = "times"
                if result[1] == 1:
                    word = "time"
    
                #And show it to the user
                print(f"{position}: {result[0]} (used {result[1]} {word})")

    with suppress(AttributeError):
        if choice == "7" or choice.checkip:
            #Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False
            
            # Let the user know the program is generating the requested info
            print("\nGenerating...\n")
            
            
            #If chosen by menu:
            if choice == "7":
                #Ask which IP needs to be checked
                ip = input("Type an IP-address to check it: ")
                #Call the function
                results = dvdl_check_ip(ip)
                #If the IP is valid than show the results
                if results != None:
                    #Show the result to the user
                    print(f"\nChecked IP: {results[0]}\nSuccessful attempts: {results[1]}\nUnsuccessful attempts: {results[2]}\nTotal attempts: {results[3]}\n")
                
            #If chosen with parameters:
            else:
                #Loop trough all given IP's
                for ip in choice.checkip:
                    # Call the function
                    results = dvdl_check_ip(ip)
                    # If the IP is valid than show the results
                    if results != None:
                        # Show the result to the user
                        print(f"\nChecked IP: {results[0]}\nSuccessful attempts: {results[1]}\nUnsuccessful attempts: {results[2]}\nTotal attempts: {results[3]}\n")

    with suppress(AttributeError):
        if choice == "8" or choice.shownip:
            #Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False
            
            # Let the user know the program is generating the requested info
            print("\nGenerating...\n")
            
            #Call the right function
            dvdl_show_all_new_ips()

    with suppress(AttributeError):
        if choice == "9":
            #Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False
            
            # Let the user know the program is generating the requested info
            print("\nGenerating...\n")
            pass

    with suppress(AttributeError):
        if choice == "10":
            #Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False
            
            # Let the user know the program is generating the requested info
            print("\nGenerating...\n")
            pass

        if choice == "11":
            #Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False
            
            exit()
    
        if error:
            print("You selected an invalid choice. Please try again")


#Retrieve all data from the logfile and filter it
def dvdl_filter_logfile(file=arguments.logfile, **kwargs):
    #Check if the logfile is (still) at the right location
    file = dvdl_check_file_location(file)
    
    #Retrieve the filtertype ("or" or "and")
    type = kwargs.get("type", "or")
    #Retrieve the first filter. If no filter was given then return all data
    filter1 = kwargs.get("filter1", "")
    #Retrieve the second filter. If no value has been assigned use this random string to prevent false-positives
    filter2 = kwargs.get("filter2", "jdehfbwjedshfbsdjhbfsjdbdfjseadbfjshbvfuerbvf!!!#$!#$#!$%^@54546546546532654dzfjdsbjhbfshjab")

    #Define list to store the result(s)
    result = []

    #Open the logfile
    with open(file, "r") as logfile:
        #If the filtertype is "or"...
        if type == "or":
            #Loop trough the file
            for logline in logfile:
                #If one of the filters is true than...
                if filter1 in logline or filter2 in logline:
                    result.append(logline)

        #If the filtertype is "and"...
        elif type == "and":
            #Loop trough the file
            for logline in logfile:
                #If both of the filters are true than...
                if filter1 in logline and filter2 in logline:
                    result.append(logline)

        #If anything other than "or" or "and" is used throw an error and stop the program
        else:
            print("Error in the filter function: Value of type variable isn't valid!")
            exit()

        #Return the result (list)
        return result


#This function makes a top 10 of the most (un)successful login attempts
def dvdl_top10_inlog(unsuccessful):
    #If it needs to be an top 10 of unsuccessful attempts than...
    if unsuccessful:
        #Make a list of all unsuccessful attempts
        filtered = dvdl_filter_logfile(filter1="AUTH_FAILED")

    #If it needs to be an top 10 of successful attempts than...
    else:
        # Make a list of all successful attempts
        filtered = dvdl_filter_logfile(filter1="TLS: Initial packet")

    #Make an empty dictionairy to count the IP-addresses
    counter = {}

    #Loop trough all filtered results
    for string in filtered:
        #Extract the IP-address from the string...
        ip = (re.findall(r"\b(?:[0-9]{1,3}\.){3}(?:[0-9]{1,3}){1}\b", string))[0] #To test: https://regex101.com/

        #If the IP is already in the dictionairy than add 1
        if ip in counter:
            i = counter.get(ip)
            i += 1
            counter.update({ip: i})

        # If the IP isn't in the dictionairy than add it
        else:
            counter.update({ip: 1})

    #Source: https://stackabuse.com/how-to-sort-dictionary-by-value-in-python/
    
    #Create an empty dictionairy to store the sorted values in
    sorted_counter = {}

    #Create an list with only sorted values
    sorted_counter_values = sorted(counter, key=counter.get, reverse=True)
    
    #Find the right key by the value
    for item in sorted_counter_values:
        sorted_counter[item] = counter[item]

    #Create an empty list to store the result
    result = []

    #Grab all keys from the dictionairy and put them in a list
    keys = list(sorted_counter.keys())
    # Grab all values from the dictionairy and put them in a list
    values = list(sorted_counter.values())

    #Create a top 10
    for i in range(0,10):
        result.append([keys[i], values[i]])

    #Return the result (list)
    return result


#A function that determines how many connections weren't made with the OVPN protocol
def dvdl_non_ovpn_prot_counter():
    #Filter the logfile
    connections = dvdl_filter_logfile(filter1="Non-OpenVPN client protocol detected")

    #Since one entry is one hit, take the lenght of the list and return it (number)
    return len(connections)


#Collect all used management commands
def dvdl_used_management_commands():
    # Filter the logfile
    logdata = dvdl_filter_logfile(filter1="MANAGEMENT: CMD")

    # Make an empty dictionairy to count the management commands
    counter = {}

    for logline in logdata:
        # Extract the management command from the string...
        command = (re.findall(r"\'.*\'", logline))[0]  # To test: https://regex101.com/
        #Remove the ' characters from the string
        command = command.replace("\'", "")


        # If the command is already in the dictionairy than add 1
        if command in counter:
            i = counter.get(command)
            i += 1
            counter.update({command: i})

        # If the command isn't in the dictionairy than add it
        else:
            counter.update({command: 1})

    # Source: https://stackabuse.com/how-to-sort-dictionary-by-value-in-python/

    # Create an empty dictionairy to store the sorted values in
    sorted_counter = {}

    # Create an list with only sorted values
    sorted_counter_values = sorted(counter, key=counter.get, reverse=True)

    # Find the right key by the value
    for item in sorted_counter_values:
        sorted_counter[item] = counter[item]

    # Create an empty list to store the result
    result = []

    # Grab all keys from the dictionairy and put them in a list
    keys = list(sorted_counter.keys())
    # Grab all values from the dictionairy and put them in a list
    values = list(sorted_counter.values())

    # Create a top 10
    for i in range(0, len(counter)):
        result.append([keys[i], values[i]])

    # Return the result (list)
    return result


#Check an IP-address for attempted connections
def dvdl_check_ip(ip):
    #If a star was given as IP than make it an empty string to filter succesfully
    if ip == "*":
        ip = ""
    #If the wildcard was not provided check if the IP is valid
    else:
        #Regex to check if the IP is valid
        ip = re.findall(r"\b(?:(?:[0-9]{1,2}|[1]{1}[0-9]{2}|[2]{1}[0-5]{1}[0-9]{1}){1}[\.]{1}){3}(?:[0-9]{1,2}|[1]{1}[0-9]{2}|[2]{1}[0-5]{1}[0-9]{1}){1}\b", ip) # To test: https://regex101.com/

        #If the IP is not valid...
        if ip == []:
            #Let the user know the IP was incorrect
            print("Please provide a valid IP")
            #Since the IP was incorrect there's nothing to return
            return None

        #Revert the list to a single IP
        ip = ip[0]

    # Get all successful attempts form the logfile
    successful_attempts = len(dvdl_filter_logfile(type="and", filter1=ip, filter2="TLS: Initial packet"))
    # Get all unsuccessful attempts form the logfile
    unsuccessful_attempts = len(dvdl_filter_logfile(type="and", filter1=ip, filter2="AUTH_FAILED"))

    #If no IP was given then let the user know there was no filter applied
    if ip == "":
        ip = "All IP-addresses"

    #Return the result (list)
    return [ip, successful_attempts, unsuccessful_attempts, (successful_attempts + unsuccessful_attempts)]


#Show all the new IP addresses
def dvdl_show_all_new_ips(ipfile=arguments.knownip):
    
    ipfile = dvdl_check_file_location(ipfile)
    
    #Grab all IP's from the logfile
    iplist = dvdl_filter_logfile()

    #Keep track how many IP addresses are added
    counter = 0

    #Create an empty list for all IP's
    ips = []

    #Open the file with known IP's...
    with open(ipfile, "r") as knownips:

        #And add it to the list with the other IP's
        for ip in knownips:
            ips.append(ip.strip())

    #Find all the IP's in the logfile
    for string in iplist:
        ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}(?:[0-9]{1,3}){1}\b", string)  # To test: https://regex101.com/

        #Sometimes the regex gives back an empty list.
        if ip == []:
            pass

        #Get the IP
        else:
            ip = ip[0]

        #If the IP is not in the list with known IP's and not an empty string/list...
        if ip not in ips and ip != [] and ip != "":
            #Show the IP to the user
            print(ip)
            #Add one to the new-IP counter
            counter += 1
            #Add the IP to the list with known IP's
            ips.append(ip)

    #Write all the (now) known IP's to the file
    with open(ipfile, "w") as knownips:
        for ip in ips:
            #Otherwise there will be an empty list at top of the file
            if ip != []:
                knownips.write(f"{ip}\n")

    #If no new IP's were detetected...
    if counter == 0:
        #Then tell the user
        print("No new IP-addresses found")

    #If new IP's where found...
    else:
        #Then tell the user
        if counter == 1:
            print(f"{counter} new IP-address found")
        else:
            print(f"{counter} new IP-addresses found")

def dvdl_check_file_location(file):
    if os.path.exists(file):
        return file
                                                                                            ##########COMMENTAAR PLAATSES!!!###########
    fnf = True
    while True:
        # This statement determines if the "file not found" message should be displayed
        if fnf:
            print("\nCannot access file. Please make sure the file location and permissions are correct and try again\n")

        # Ask the user if they would like to try again
        choice = input("Would you like to try again? [y/n]: ")

        # Try to ask the user for another file location
        try:
            if choice[0] == "y" or choice[0] == "Y":
                # Ask for anoher location
                file = input("What is the location of the file: ")

                # Try the path
                if os.path.exists(file):
                    # If the file exists than stop the loop
                    break

                # If the path doesn't exist...
                else:
                    # If the file cannot be found make sure to show the "file not found" message
                    fnf = True

            # If the user doesn't want to change te file...
            elif choice[0] == "n" or choice[0] == "N":
                # Stop the loop
                return ""

            # If the user didin't answer correctly...
            else:
                # Let the except handle the rest
                raise Exception

        # If the user didin't answer correctly...
        except:
            # Let them know
            print("\nPlease give a valid answer\n")
            # Make sure the "file not found" message is not shown again
            fnf = False

    return file


##########Run at boot code##########

if arguments.gui:
    while True:
        dvdl_show_menu()
else:
    dvdl_menu_handler(arguments)

#TODO: Finish file params
#TODO: Show program version/information