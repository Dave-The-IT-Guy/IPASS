#Name: Dave van der Leek (1777075)
#Class:
#Programname: OVPNLogbrowser
#Description: Een programma om OpenVPN logfiles uit te lezen
version = 0.1


##########Imports##########
import re #For regex
import os
import json

##########Functions##########


#This functions shows the menu
def dvdl_show_menu(logfile):
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
    dvdl_menu_handler(logfile, choice)

    #Give the user time to check the data
    input("Press return to continue...")


def dvdl_menu_handler(logfile, choice):
    #If one of the first 2 choices were selected then...
    if choice == "1" or choice == "2":
        #Let the user know the program is generating the requested info
        print("\nGenerating...\n")

        #Check which parameter the function needs and call the function
        if choice == "1":
            results = dvdl_top10_inlog(file=logfile, unsuccessful=True)
            # Show the title
            print(f"Top 10 unsuccessful connections:")
        else:
            results = dvdl_top10_inlog(file=logfile, unsuccessful=False)
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

    elif choice == "3":
        pass

    elif choice == "4":
        pass

    #If the user chose option 5 than...
    elif choice == "5":
        # Let the user know the program is generating the requested info
        print("\nGenerating...\n")

        #Call the right function...
        result = dvdl_non_ovpn_prot_counter(file=logfile)

        #And show the result
        print(f"{result} connection(s) weren't made with the OpenVPN protocol")

    elif choice == "6":
        results = dvdl_used_management_commands(logfile)

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

    elif choice == "7":
        #Ask which IP needs to be checked
        ip = input("Type an IP-address to check it: ")

        #Call the function
        results = dvdl_check_ip(logfile, ip)

        #If the IP is valid than show the results
        if results != None:
            #Show the result to the user
            print(f"\nChecked IP: {results[0]}\nSuccessful attempts: {results[1]}\nUnsuccessful attempts: {results[2]}\nTotal attempts: {results[3]}")

    elif choice == "8":
        dvdl_show_all_new_ips(logfile=logfile)

    elif choice == "9":
        pass

    elif choice == "10":
        pass

    elif choice == "11":
        exit()

    else:
        print("You selected an invalid choice. Please try again")


#Retrieve all data from the logfile and filter it
def dvdl_filter_logfile(file, **kwargs):
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
def dvdl_top10_inlog(file, unsuccessful):
    #If it needs to be an top 10 of unsuccessful attempts than...
    if unsuccessful:
        #Make a list of all unsuccessful attempts
        filtered = dvdl_filter_logfile(file, filter1="AUTH_FAILED")

    #If it needs to be an top 10 of successful attempts than...
    else:
        # Make a list of all successful attempts
        filtered = dvdl_filter_logfile(file, filter1="TLS: Initial packet")

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
def dvdl_non_ovpn_prot_counter(file):
    #Filter the logfile
    connections = dvdl_filter_logfile(file, filter1="Non-OpenVPN client protocol detected")

    #Since one entry is one hit, take the lenght of the list and return it (number)
    return len(connections)


#Collect all used management commands
def dvdl_used_management_commands(file):
    # Filter the logfile
    logdata = dvdl_filter_logfile(file, filter1="MANAGEMENT: CMD")

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
def dvdl_check_ip(file, ip):
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
    successful_attempts = len(dvdl_filter_logfile(file, type="and", filter1=ip, filter2="TLS: Initial packet"))
    # Get all unsuccessful attempts form the logfile
    unsuccessful_attempts = len(dvdl_filter_logfile(file, type="and", filter1=ip, filter2="AUTH_FAILED"))

    #If no IP was given then let the user know there was no filter applied
    if ip == "":
        ip = "All IP-addresses"

    #Return the result (list)
    return [ip, successful_attempts, unsuccessful_attempts, (successful_attempts + unsuccessful_attempts)]


#Show all the new IP addresses
def dvdl_show_all_new_ips(logfile, **kwargs):
    #Get the filelocation
    ipfile = kwargs.get("ipfile", "knowip.txt")

    #Grab all IP's from the logfile
    iplist = dvdl_filter_logfile(logfile)

    #Set the errormessage variable to true (shows errormessage if file is not found)
    fnf = True

    #Keep looping to give the user a chance to change the path of the file if the file could not be found
    while True:

        #If the file can be opend...
        if os.path.exists(ipfile):
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
                print("\nNo new IP-addresses found\n")

            #If new IP's where found...
            else:
                #Then tell the user
                print(f"\n{counter} new IP-address(es) found\n")

            #Stop the loop
            break

        #If the file cannot be opend...
        else:
            if fnf:
                print("\nCannot access knownip-file. Please make sure the file location and permissions are correct and try again\n")
            choice = input("Would you like to try again? [y/n]: ")

            #Try to ask the user for another logfile location
            try:
                if choice[0] == "y" or choice[0] == "Y":
                    #Ask for anoher location
                    ipfile = input("What is the location of the knownip-file: ")

                    #If the file cannot be found make sure to show the "file not found" message
                    fnf = True

                #If the user doesn't want to change te file...
                elif choice[0] == "n" or choice[0] == "N":
                    #Stop the loop
                    break

                #If the user didin't answer correctly...
                else:
                    #Let the except handle the rest
                    raise Exception

            # If the user didin't answer correctly...
            except:
                #Let them know
                print("\nPlease give a valid answer\n")
                #Make sure the "file not found" message is not shown again
                fnf = False


##########Run at boot code##########


#TODO: Check if program is interactive or not
#TODO: Show program version/information
#TODO: Check if the logfile exists

logfile = "openvpn.log"

while True:
    dvdl_show_menu(logfile)