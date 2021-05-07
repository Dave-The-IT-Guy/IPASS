# Name: Dave van der Leek (1777075)
# Class:
# Program: OVPNLogbrowser
# Description: Een programma om OpenVPN logfiles uit te lezen
version = 0.1


##########Imports##########
import re # For regex
import os
import argparse
from contextlib import suppress
import json


##########Arguments##########
parser = argparse.ArgumentParser(description="A program to browse and analyse OpenVPN logfiles", exit_on_error=True)
parser.add_argument("-c", "--config-location", help="path to the configuration file", default="", dest="configfile")
parser.add_argument("-d", "--top5-connection-days", help="show the top 5 of days with the most (un)successful connections", choices=["failed", "successful"], dest="top5")
parser.add_argument("-g", "--show-menu", help="when called the menu will be showed", action="store_true", dest="gui")
parser.add_argument("-i", "--check-ip", help="check one or more ip-addresses for attempted connection(s)", nargs="*", dest="checkip")
parser.add_argument("-k", "--knownipfile-location", help="path to the knownip file", default="knownip.txt", dest="knownip")
parser.add_argument("-l", "--logfile-location", help="path to the OpenVPN logfile", default="openvpn.log", dest="logfile")
parser.add_argument("-m", "--used-management-commands", help="show all used management commands", action="store_true", dest="management")
parser.add_argument("-n", "--new-ips", help="show all new IP-adresses", action="store_true", dest="shownip")
parser.add_argument("-p", "--non-openvpn-protocol", help="show how many connections weren't made with the OpenVPN protocol", action="store_true", dest="openvpnprot")
parser.add_argument("-s", "--save-output", help="determines if the output should be shown or written to a file", action="store_true", dest="printer")
parser.add_argument("-t", "--top10-connection-ips", help="show the top 10 (failed) connection attempts", choices=["failed", "successful"], dest="top10")
arguments = parser.parse_args()


##########Functions##########

# This functions shows the menu
def dvdl_show_menu(logfile):
    print("\nHow may I assist you?\n"
    "1.  Show me the top 10 IP's with the most unsuccessful connections\n"
    "2.  Show me the top 10 IP's with most successful connections\n"
    "3.  Show me the top 5 days with the most unsuccessful connections\n"
    "4.  Show me the top 5 days with the most successful connections\n"
    "5.  Show me how many connections weren't made with OpenVPN\n"
    "6.  Show me all used management commands\n"
    "7.  I want to check an IP-adres for attempted connection's\n"
    "8.  Show me all new IP-adresses\n"
    "9.  I want to create a new knownip file\n"
    "10. I want to create a new configuration file\n"
    "11. Show me all the program parameters\n"
    "12. Close program\n")
    # Ask which option needs to be selected
    choice = input("Make your choice: ")

    # Start the function that handles the menu
    dvdl_menu_handler(logfile, choice)

    # Give the user time to check the data
    input("Press return to continue...")


def dvdl_menu_handler(logfile, choice, **kwargs):

    ipfile = kwargs.get("ipfile", arguments.knownip)
    checkip = kwargs.get("checkip", arguments.checkip)

    # If no choice is valid this variable wll make sure an errormessage is shown
    error = True
    
    # Source: https://towardsdatascience.com/quick-python-tip-suppress-known-exception-without-try-except-a93ec34d3704
    with suppress(AttributeError):
        # If one of the first 2 choices were selected then...
        if choice == "1" or choice == "2" or choice.top10 == "failed" or choice.top10 == "successful":
            # Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False
            
            # Check if the output needs to be written to a file
            if not arguments.printer:
                # Let the user know the program is generating the requested info
                print("\nGenerating...\n")
            
            with suppress(AttributeError):
                # Check which parameter the function needs and call the function
                if choice == "1" or choice.top10 == "failed":
                    results = dvdl_top10_inlog(logfile, unsuccessful=True)

                    # Check if the output needs to be written to a file
                    if not arguments.printer:
                        # Show the title
                        print(f"Top 10 unsuccessful connections:")

                    # If the output needs to be in the file:
                    else:
                        # Open the result file
                        with open("result.txt", "a") as resultfile:
                            # And write the, otherwise printed, statement to the file
                            resultfile.write("\n\nTop 10 unsuccessful connections:")
                            
            with suppress(AttributeError):
                if choice == "2" or choice.top10 == "successful":
                    results = dvdl_top10_inlog(logfile, unsuccessful=False)
                    
                    # Check if the output needs to be written to a file
                    if not arguments.printer:
                        # Show the title
                        print(f"Top 10 successful connections:")

                    # If the output needs to be in the file:
                    else:
                        # Open the result file
                        with open("result.txt", "a") as resultfile:
                            # And write the, otherwise printed, statement to the file
                            resultfile.write("\n\nTop 10 successful connections:")
    
            # A counter to show the positions
            position = 0
    
            # Loop trough the results...
            for result in results:
                # Add one to count
                position += 1
    
                # Check if it needs to be try or try's
                word = "try's"
                if result[1] == 1:
                    word = "try"
                
                # Check if the outputs needs to be printed or not
                if not arguments.printer:
                    # And show it to the user
                    print(f"{position}: {result[0]} ({result[1]} {word})")
                    
                else:
                    # Open the result file
                    with open("result.txt", "a") as resultfile:
                        # And write the, otherwise printed, statement to the file
                        resultfile.write(f"\n{position}: {result[0]} ({result[1]} {word})")
                
    with suppress(AttributeError):
        if choice == "3" or choice == "4" or choice.top5 == "failed" or choice.top5 == "successful":
            # Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False

            # Check if the output needs to be written to a file
            if not arguments.printer:
                # Let the user know the program is generating the requested info
                print("\nGenerating...\n")
                print("option 3/4")

            # If the output needs to be in the file:
            else:
                # Open the result file
                with open("result.txt", "a") as resultfile:
                    # And write the, otherwise printed, statement to the file
                    resultfile.write("\n\noption 3/4")
            
            

    with suppress(AttributeError):
        # If the user chose option 5 than...
        if choice == "5" or choice.openvpnprot:
            # Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False

            # Check if the output needs to be written to a file
            if not arguments.printer:
                # Let the user know the program is generating the requested info
                print("\nGenerating...\n")
    
            # Call the right function...
            result = dvdl_non_ovpn_prot_counter(logfile)
            
            # Check if the output needs to be written to a file
            if not arguments.printer:
                # And show the result
                print(f"{result} connection(s) weren't made with the OpenVPN protocol")

            # If the result needs to be in the file...
            else:
                # Open the file
                with open("result.txt", "a") as resultfile:
                    # And write the, otherwise printed, statement to the file
                    resultfile.write(f"\n\n{result} connection(s) weren't made with the OpenVPN protocol")

    with suppress(AttributeError):
        if choice == "6" or choice.management:
            # Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False

            # Check if the output needs to be written to a file
            if not arguments.printer:
                # Let the user know the program is generating the requested info
                print("\nGenerating...\n")

            # If the output needs to be written to a file...
            else:
                # Open the file
                with open("result.txt", "a") as resultfile:
                    # Write a blank line to the file to make the file more readable
                    resultfile.write("\n")
            
            # Gat all used management commands
            results = dvdl_used_management_commands(logfile)
    
            # A counter to show the positions
            position = 0
    
            # Loop trough the results...
            for result in results:
                # Add one to count
                position += 1
    
                # Check if it needs to be time or times
                word = "times"
                if result[1] == 1:
                    word = "time"
                
                if not arguments.printer:
                    # And show it to the user
                    print(f"{position}: {result[0]} (used {result[1]} {word})")

                # If the output needs to be written to a file
                else:
                    # Open the file
                    with open("result.txt", "a") as resultfile:
                        # And write the, otherwise printed, statement to the file
                        resultfile.write(f"\n{position}: {result[0]} (used {result[1]} {word})")

    with suppress(AttributeError):
        if choice == "7" or choice.checkip:
            # Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False

        # If chosen by menu:
        if choice == "7" and not arguments.printer:
            # Ask which IP's needs to be checked
            checkip = input("Type one or more IP-address to check it (space seperated): ")

        # Check if the output needs to be written to a file
        if not arguments.printer:
            # Let the user know the program is generating the requested info
            print("\nGenerating...")
        
        if type(checkip) != list:
            # Make a list of all the given IP's
            checkip = checkip.split(" ")
        
        # Loop trough the IP's and...
        for ip in checkip:
            # Call the function
            results = dvdl_check_ip(logfile, ip)

            # If the IP is valid and the results need to be printed than show the results
            if results != None and not arguments.printer:
                # Show the result to the user
                print(f"\nChecked IP: {results[0]}\nSuccessful attempts: {results[1]}\nUnsuccessful attempts: {results[2]}\nTotal attempts: {results[3]}\n")

            # If the IP is valid and output needs to be written to a file...
            elif results != None:
                # Open the file
                with open("result.txt", "a") as resultfile:
                    # And write the, otherwise printed, statement to the file
                    resultfile.write(f"\n\nChecked IP: {results[0]}\nSuccessful attempts: {results[1]}\nUnsuccessful attempts: {results[2]}\nTotal attempts: {results[3]}")

    with suppress(AttributeError):
        if choice == "8" or choice.shownip:
            # Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False

            # Check if the output needs to be written to a file
            if not arguments.printer:
                # Let the user know the program is generating the requested info
                print("\nGenerating...\n")
            
            # Call the right function
            dvdl_show_all_new_ips(logfile, ipfile)
    
    with suppress(AttributeError):
        if choice == "9":
            # Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False
            
            # Let the user know the program is generating the requested info
            print("\nCreating...\n")
            
            with open("knownip.txt", "w") as file:
                file.write("48 65 74 20 51 57 45 52 54 59 20 74 6f 65 74 73 65 6e 62 6f 72 64 20 77 61 73 20 67 65 6d 61 61 6b 74 20 6f 6d 20 74 65 20 76 6f 6f 72 6b 6f 6d 65 6e 20 64 61 74 20 6c 65 74 74 65 72 73 74 61 6e 67 65 74 6a 65 73 20 67 69 6e 67 65 6e 20 62 6f 74 73 65 6e 20 65 6e 20 6b 6c 65 6d 20 6b 77 61 6d 65 6e 20 74 65 20 7a 69 74 74 65 6e 20 28 62 72 6f 6e 3a 20 57 69 6b 69 70 65 64 69 61 29")
    
    with suppress(AttributeError):
        if choice == "10":
            # Since a valid option was chosen the errormessage doesn't need to be displayed
            error = False

            # Create an empty dictionairy to store all the answers
            answers = {}

            # Let the user know what's going to happen
            print("\n\nYou are now presented with couple of questions to make sure the logfile fits your needs. You can (almost) always press return to skip a question. If you skip a question it will be answerd with no.\n")

            # Get the location of the logfile
            while True:
                # Ask the location of the logfile
                logfile = input("What is the location of the logfile: ")

                # If no answer was provided...
                if logfile == "":
                    # Aks the user to try again
                    print("\nThis question is unskippable. Please provide a valid answer\n")

                # If an answer was provided...
                else:
                    # Update the dictionairy
                    answers.update({"logfile": logfile})

                    # And stop the loop
                    break

            # Check if a top 10 needs to be added
            while True:
                # Ask if a top 10 needs to be added
                top10 = input("Do you want to show a top 10 of (un)successful connections [unsuccessful/successful/no]: ")

                # If the question was skipped or answerd with no...
                if top10 == "" or top10[0].lower() == "n":
                    # Then add the answer to the dictionairy
                    answers.update({"top10": "False"})

                    # And stop the loop
                    break

                # If the user wants a top 10 of successful connections...
                elif top10[0].lower() == "s":
                    # Then add the answer to the dictionairy
                    answers.update({"top10": "Successful"})

                    # And stop the loop
                    break

                # If the user wants a top 10 of unsuccessful connections...
                elif top10[0].lower() == "u":
                    # Then add the answer to the dictionairy
                    answers.update({"top10": "Unsuccessful"})

                    # And stop the loop
                    break

                # If no valid answer was provided...
                else:
                    # Let the user know
                    print("\nPlease provide a valid answer\n")

            # Check if a top 5 needs to be added
            while True:
                # Ask if a top 5 needs to be added
                top5 = input("Do you want to show a top 5 of days with the most (un)successful connections [unsuccessful/successful/no]: ")

                # If the question was skipped or answerd with no...
                if top5 == "" or top5[0].lower() == "n":
                    # Then add the answer to the dictionairy
                    answers.update({"top5": "False"})

                    # And stop the loop
                    break

                # If the user wants a top 5 of days with the most successful connections
                elif top5[0].lower() == "s":
                    # Then add the answer to the dictionairy
                    answers.update({"top5": "Successful"})

                    # And stop the loop
                    break

                # If the user wants a top 5 of days with the most unsuccessful connections
                elif top5[0].lower() == "u":
                    # Then add the answer to the dictionairy
                    answers.update({"top5": "Unsuccessful"})

                    # And stop the loop
                    break

                # If no valid answer was provided...
                else:
                    # Let the user know
                    print("\nPlease provide a valid answer\n")

            # Check if the connections that weren't made with ovpn need to be added
            while True:
                # Ask the user if the connections that weren't made with ovpn need to be added
                protocol = input("Do you want to show all the connections that weren't made with the OVPN protocol [yes/no]: ")

                # If the question was skipped or answerd with no...
                if protocol == "" or protocol[0].lower() == "n":
                    # Then add the answer to the dictionairy
                    answers.update({"non-ovpn-prot": "False"})

                    # And stop the loop
                    break

                # If the question was answerd with yes...
                elif protocol[0].lower() == "y":
                    # Then add the answer to the dictionairy
                    answers.update({"non-ovpn-prot": "True"})

                    # And stop the loop
                    break

                # If no valid answer was provided...
                else:
                    # Let the user know
                    print("\nPlease provide a valid answer\n")

            # Check if all used management commands need to added
            while True:
                # Ask if all used management commands need to be added
                management = input("Do you want to show all used management commands [yes/no]: ")

                # If the question was skipped or answerd with no...
                if management == "" or management[0].lower() == "n":
                    # Then add the answer to the dictionairy
                    answers.update({"man-coms": "False"})

                    # And stop the loop
                    break

                # If the question was answerd with yes...
                elif management[0].lower() == "y":
                    # Then add the answer to the dictionairy
                    answers.update({"man-coms": "True"})

                    # And stop the loop
                    break

                # If no valid answer was provided...
                else:
                    # Let the user know
                    print("\nPlease provide a valid answer\n")

            # Ask which IP's need to be checked
            checkip = input("Which IP's do you want to check (space seperated): ")

            # Is later used to check if the user skipped the question
            skipped = False

            # If no IP needs to be checked
            if checkip == "":
                # Makes sure the question is skipped
                skipped = True

            # If there are IP's to check...
            else:

                # Make a list of all IP's
                checkip = checkip.split(" ")

                # Create an empty list to store all IP)'s in
                ips = []
            
            # Try to get an IP from the string
            try:
                # Check if all IP -adresses are valid
                for ip in checkip:
                    # Regex to check if the IP is valid or if a * is provided
                    ip = re.findall(r"\b(?:(?:[0-9]{1,2}|[1]{1}[0-9]{2}|[2]{1}[0-5]{1}[0-9]{1}){1}[.]{1}){3}(?:[0-9]{1,2}|[1]{1}[0-9]{2}|[2]{1}[0-5]{1}[0-9]{1}){1}\b|^\*$", ip)[0]  # To test: https://regex101.com/

                    # If the IP is valid...
                    if ip != []:
                        # Add it to the list with IP's
                        ips.append(ip)
                # If some of the IP's are valid...
                if skipped and len(ips) > 0:
                    # Let the user know
                    print("\nSome of the provided IP's were invalid. The invalid IP's were skipped")

                    # Add the valid IP's to the dictionairy
                    answers.update({"check-ip": ips})

                # If none of the provided IP's are valid...
                elif len(ips) == 0:
                    # Let the user know
                    print("\nNone of the provided IP's were valid. The question is skipped")

                    # Then add the answer to the dictionairy
                    answers.update({"check-ip": "False"})

                # If all the IP's are valid
                else:
                    # Then add the answer to the dictionairy
                    answers.update({"check-ip": ips})

            # If the question is skipped
            except UnboundLocalError:
                # Then add the answer to the dictionairy
                answers.update({"check-ip": "False"})
            
            # If an invalid string was given...
            except IndexError:
                # Let the user know
                print("\nAn invalid answer as given. The question is skipped\n")

                # Then add the answer to the dictionairy
                answers.update({"check-ip": "False"})
                
            # Check if all new IP's need to be added
            while True:
                # Ask if all new IP's need to be added
                newip = input("Do you want to know all the new IP's [yes/no]: ")

                # If the question was skipped or answered with no...
                if newip == "" or newip[0].lower() == "n":
                    # Then add the answer to the dictionairy
                    answers.update({"new-ips": "False"})

                    # And stop the loop
                    break

                # If the question was answered with yes...
                elif newip[0].lower() == "y":
                    # Then add the answer to the dictionairy
                    answers.update({"new-ips": "True"})

                    # And ask the user the location of the knownip-file
                    knowip = input("What is the location of the knownip-file: ")

                    # Then add the answer to the dictionairy
                    answers.update({"knownip-file": knowip})

                    # And stop the loop
                    break

                # If no valid answer was provided...
                else:
                    # Let the user know
                    print("\nPlease provide a valid answer\n")

            # Source: https://www.geeksforgeeks.org/how-to-convert-python-dictionary-to-json/
            with open("config.json", "w") as configfile:
                json.dump(answers, configfile, indent=4)

            # Let the user know the program is generating the requested info
            print("\nGenerating...\n")

    if choice == "11":
        # Since a valid option was chosen the errormessage doesn't need to be displayed
        error = False

        # Shows all parameters
        print("\nParameters: -h, --help\n"
              "Action: Shows all parameters and it's info\n\n"
              "Parameters: -c {path}, --configfile {path}\n"
              "Action: Path to the configuration file\n\n"
              "Parameters: -d {unsuccessful, successful}, --top5-conncection-days {unsuccessful, successful}\n"
              "Action: Shows a top 5 of the days with the most (un)successful connections\n\n"
              "Parameters: -g, --show-menu\n"
              "Action: Shows the menu\n\n"
              "Parameters: -i {ip}, --check-ip {ip}\n"
              "Action: Checks one or more IP-addresses for attempted connections\n\n"
              "Parameters: -k {path}, --knownipfile-location {path}\n"
              "Action: Path to the knownip file\n\n"
              "Parameters: -l {path}, --logfile-location {path}\n"
              "Action: Path to the OpenVPN logfile\n\n"
              "Parameters: -m, --used-mamangement-commands\n"
              "Action: Shows all used management commands\n\n"
              "Parameters: -n, --new-ips\n"
              "Action: Shows all new IP-addresses\n\n"
              "Parameters: -p, --non-openvpn-protocol\n"
              "Action: Shows how many connections weren't made with the OpenVPN protocol\n\n"
              "Parameters: -s --save-output\n"
              "Action: Saves all output to the result.txt file\n\n"
              "Parameters: -t  {unsuccessful, successful}, --top10-connection-ips {unsuccessful, successful}\n"
              "Action: Shows a top 10 of the IP-adresses with the most (un)successful connections\n")

    if choice == "12":
        # Stop the program
        exit()

    if error:
        print("You selected an invalid choice. Please try again")


# Retrieve all data from the logfile and filter it
def dvdl_filter_logfile(file, **kwargs):
    # Check if the logfile is (still) at the right location
    file = dvdl_check_file_location(file, "OpenVPN-logfile")

    while True:
        # Check if the identifier is present
        with open(file, "r") as logfile:
            
            # Check if the file looks like a logfile
            if not re.findall(r"\d{4}(:\d{2}){2}-(\d{2}:){2}\d{2} \w{1,} openvpn\[\d{1,5}]:", logfile.readline()):
                
                # Comment here
                if not arguments.printer:
                    # If the identiefier isn't present let the user choose another file
                    print("This doesn't seem to be an OpenVPN-logfile. Please select another file")
                    file = dvdl_check_file_location("", "OpenVPN-logfile", fnf=False)

                # If the output needs to be written to the file...
                else:
                    # Open the file...
                    with open("result.txt", "a") as resultfile:
                        # And write the, otherwise printed, statement to the file
                        resultfile.write("\n\nThe submitted file doesn't seem to be an OpenVPN-logfile.\n\n")
                    exit()
                
            # If the identifier is present stop the loop
            else:
                break
    
    # Retrieve the filtertype ("or" or "and")
    type = kwargs.get("type", "or")
    # Retrieve the first filter. If no filter was given then return all data
    filter1 = kwargs.get("filter1", "")
    # Retrieve the second filter. If no value has been assigned use this random string to prevent false-positives
    filter2 = kwargs.get("filter2", "jdehfbwjedshfbsdjhbfsjdSDJVBSDVJBSVJHBDMANSJDBHVJASBHVbdfjseadbfjshbvfuerbvf!!!# $!# $# !$%^@54546546546532654dzfjdsbjhbfshjab")

    # Define list to store the result(s)
    result = []
    
    # Open the logfile
    with open(file, "r") as logfile:
        # If the filtertype is "or"...
        if type == "or":
            # Loop trough the file
            for logline in logfile:
                # If one of the filters is true than...
                if filter1 in logline or filter2 in logline:
                    result.append(logline)

        # If the filtertype is "and"...
        elif type == "and":
            # Loop trough the file
            for logline in logfile:
                # If both of the filters are true than...
                if filter1 in logline and filter2 in logline:
                    result.append(logline)

        # If anything other than "or" or "and" is used throw an error and stop the program
        else:
            print("Error in the filter function: Value of type variable isn't valid!")
            exit()

        # Return the result (list)
        return result


# This function makes a top 10 of the most (un)successful login attempts
def dvdl_top10_inlog(logfile, unsuccessful):
    # If it needs to be an top 10 of unsuccessful attempts than...
    if unsuccessful:
        # Make a list of all unsuccessful attempts
        filtered = dvdl_filter_logfile(logfile, filter1="AUTH_FAILED")

    # If it needs to be an top 10 of successful attempts than...
    else:
        # Make a list of all successful attempts
        filtered = dvdl_filter_logfile(logfile, filter1="TLS: Initial packet")

    # Make an empty dictionairy to count the IP-addresses
    counter = {}

    # Loop trough all filtered results
    for string in filtered:
        # Extract the IP-address from the string...
        ip = (re.findall(r"\b(?:[0-9]{1,3}\.){3}(?:[0-9]{1,3}){1}\b", string))[0] # To test: https://regex101.com/

        # If the IP is already in the dictionairy than add 1
        if ip in counter:
            i = counter.get(ip)
            i += 1
            counter.update({ip: i})

        # If the IP isn't in the dictionairy than add it
        else:
            counter.update({ip: 1})

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
    
    # If no results are available...
    if len(sorted_counter) == 0:
        result.append(["No results available", 0])
    
    # Try to fill the list with results
    with suppress(IndexError):
        # Create a top 10
        for i in range(0,10):
            # Append the results
            if i < len(sorted_counter):
                result.append([keys[i], values[i]])

    # Return the result (list)
    return result


# A function that determines how many connections weren't made with the OVPN protocol
def dvdl_non_ovpn_prot_counter(logfile):
    # Filter the logfile
    connections = dvdl_filter_logfile(logfile, filter1="Non-OpenVPN client protocol detected")

    # Since one entry is one hit, take the lenght of the list and return it (number)
    return len(connections)


# Collect all used management commands
def dvdl_used_management_commands(logfile):
    # Filter the logfile
    logdata = dvdl_filter_logfile(logfile, filter1="MANAGEMENT: CMD")

    # Make an empty dictionairy to count the management commands
    counter = {}

    for logline in logdata:
        # Extract the management command from the string...
        command = (re.findall(r"\'.*\'", logline))[0]  # To test: https://regex101.com/
        # Remove the ' characters from the string
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


# Check an IP-address for attempted connections
def dvdl_check_ip(logfile, ip):
    # If a star was given as IP than make it an empty string to filter succesfully
    if ip == "*":
        ip = ""
    # If the wildcard was not provided check if the IP is valid
    else:
        # Regex to check if the IP is valid
        ip = re.findall(r"\b(?:(?:[0-9]{1,2}|[1]{1}[0-9]{2}|[2]{1}[0-5]{1}[0-9]{1}){1}[.]{1}){3}(?:[0-9]{1,2}|[1]{1}[0-9]{2}|[2]{1}[0-5]{1}[0-9]{1}){1}\b", ip) # To test: https://regex101.com/

        # If the IP is not valid...
        if ip == [] and not arguments.printer:
            # Let the user know the IP was incorrect
            print("\nPlease provide a valid IP")
            # Since the IP was incorrect there's nothing to return
            return None

        # If the output needst to be written to the file
        elif ip == []:
            # Open the file
            with open("result.txt", "a") as resultfile:
                # And write the, otherwise printed, statement to the file
                resultfile.write("\n\nNo valid IP provided\n\n")
                
        # Revert the list to a single IP
        ip = ip[0]

    # Get all successful attempts form the logfile
    successful_attempts = len(dvdl_filter_logfile(logfile, type="and", filter1=ip, filter2="TLS: Initial packet"))
    # Get all unsuccessful attempts form the logfile
    unsuccessful_attempts = len(dvdl_filter_logfile(logfile, type="and", filter1=ip, filter2="AUTH_FAILED"))

    # If no IP was given then let the user know there was no filter applied
    if ip == "":
        ip = "All IP-addresses"

    # Return the result (list)
    return [ip, successful_attempts, unsuccessful_attempts, (successful_attempts + unsuccessful_attempts)]


# Show all the new IP addresses
def dvdl_show_all_new_ips(logfile, ipfile):

    # Check if the file is (still) at the right location
    ipfile = dvdl_check_file_location(ipfile, "knownip-file")

    # Value of the first line of the knownip file.
    identifier = "48 65 74 20 51 57 45 52 54 59 20 74 6f 65 74 73 65 6e 62 6f 72 64 20 77 61 73 20 67 65 6d 61 61 6b 74 20 6f 6d 20 74 65 20 76 6f 6f 72 6b 6f 6d 65 6e 20 64 61 74 20 6c 65 74 74 65 72 73 74 61 6e 67 65 74 6a 65 73 20 67 69 6e 67 65 6e 20 62 6f 74 73 65 6e 20 65 6e 20 6b 6c 65 6d 20 6b 77 61 6d 65 6e 20 74 65 20 7a 69 74 74 65 6e 20 28 62 72 6f 6e 3a 20 57 69 6b 69 70 65 64 69 61 29"
    
    while True:
        # Check if the identifier is present
        with open(ipfile, "r") as file:
            if not (file.readline()).strip() == identifier:
                
                if not arguments.printer:
                    # If the identiefier isn't present let the user choose another file
                    print("The identifier isn't correct. Please select another file")
                    ipfile = dvdl_check_file_location("", "knownip-file", fnf=False)

                # If the output needs to be written to a file
                else:
                    # Open the file
                    with open("result.txt", "a") as resultfile:
                        # And write the, otherwise printed, statement to the file
                        resultfile.write("\n\nThe identiefier of the knownipfile isn't correct\n\n")
            
            # If the identifier is present stop the loop
            else:
                break
    
    # Grab all IP's from the logfile
    iplist = dvdl_filter_logfile(logfile)

    # Keep track how many IP addresses are added
    counter = 0

    # Create an empty list for all IP's
    ips = []

    # Open the file with known IP's...
    with open(ipfile, "r") as knownips:
        
        # And add it to the list with the other IP's
        for ip in knownips:
            ips.append(ip.strip())

    # If the output needs to be written to a file...
    if arguments.printer:
        # Open the file
        with open("result.txt", "a") as resultfile:
            # And write the, otherwise printed, statement to the file
            resultfile.write("\n\nNew IP-addresses:")

    # Find all the IP's in the logfile
    for string in iplist:
        ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}(?:[0-9]{1,3}){1}\b", string)  # To test: https://regex101.com/

        # Sometimes the regex gives back an empty list.
        if ip == []:
            pass

        # If that isn't the case then get the IP
        else:
            ip = ip[0]

        # If the IP is not in the list with known IP's and not an empty string/list...
        if ip not in ips and ip != [] and ip != "":

            if not arguments.printer:
                # Show the IP to the user
                print(ip)

            # If the output needs to be written to a file...
            else:
                # Open the file
                with open("result.txt", "a") as resultfile:
                    # And write the, otherwise printed, statement to the file
                    resultfile.write(f"\n{ip}")
                
            # Add one to the new-IP counter
            counter += 1
            # Add the IP to the list with known IP's
            ips.append(ip)
    

    # Write all the (now) known IP's to the file
    with open(ipfile, "w") as knownips:
        knownips.write(identifier)
        for ip in ips:
            # Otherwise there will be an empty list at top of the file
            if ip != [] and ip != identifier:
                knownips.write(f"\n{ip}")

    # If no new IP's were detetected and the output needs to be printed...
    if counter == 0 and not arguments.printer:
        print("No new IP-addresses found")
    
    # If one new IP was found and the output needs to be printed...
    elif counter == 1 and not arguments.printer:
        print(f"{counter} new IP-address found")
    
    # If more then one IP was found and the output needs to be printed...
    elif counter >= 2 and not arguments.printer:
        print(f"{counter} new IP-addresses found")

    # If no new IP's were detetected and the output needs to be written to a file...
    elif counter == 0:
        # Open the file
        with open("result.txt", "a") as resultfile:
            # And write the, otherwise printed, statement to the file
            resultfile.write("\nNo new IP-addresses found")

    # If one new IP was found and the output needs to be written to a file...
    elif counter == 1:
        # Open the file
        with open("result.txt", "a") as resultfile:
            # And write the, otherwise printed, statement to the file
            resultfile.write(f"\n{counter} new IP-address found")

    # If more then one IP was found and the output needs to be written to a file...
    elif counter >= 2:
        # Open the file
        with open("result.txt", "a") as resultfile:
            # And write the, otherwise printed, statement to the file
            resultfile.write(f"\n{counter} new IP-addresses found")


def dvdl_check_file_location(file, filename, **kwargs):
    
    # Determines if the "file not found message should be shown (the first time)"
    fnf = kwargs.get("fnf", True)
    
    # Check of the file exists
    if os.path.exists(file):
        return file

    # If the file can't be found and the output needs to be written to a file...
    if not os.path.exists(file) and arguments.printer:
        # Open the file
        with open("result.txt", "a") as resultfile:
            # And write the, otherwise printed, statement to the file
            resultfile.write(f"\n\nCannot access {filename}\n\n")

        # Exit the program
        exit()
    
    # Keep the loop until the file is found or the user want to quit
    while True:
        # This statement determines if the "file not found" message should be displayed
        if fnf:
            print(f"\nCannot access {filename}. Please make sure the file location and permissions are correct and try again\n")

        # Ask the user if they would like to try again
        choice = input("Would you like to try again? [y/n]: ")

        # Try to ask the user for another file location
        try:
            if choice[0].lower() == "y":
                # Ask for anoher location
                file = input(f"What is the location of the {filename}: ")

                # Try the path
                if os.path.exists(file):
                    # If the file exists than stop the loop
                    break

                # If the path doesn't exist...
                else:
                    # If the file cannot be found make sure to show the "file not found" message
                    fnf = True

            # If the user doesn't want to change te file...
            elif choice[0].lower() == "n":
                # Stop the program
                print("\nOperatation canceled by user")
                exit()

            # If the user didin't answer correctly...
            else:
                # Let the except handle the rest
                raise IndexError

        # If the user didin't answer correctly...
        except IndexError:
            # Let them know
            print("\nPlease give a valid answer\n")
            # Make sure the "file not found" message is not shown again
            fnf = False

    return file


# Handles the configuration file
def dvdl_config_handler(configfile):

    # Open the configfile and convert it to an dictionairy
    with open(configfile, "r") as json_file:
        configdata = json.load(json_file)

    try:
        # Check the path of the logfile
        logfile = dvdl_check_file_location(configdata["logfile"], "OpenVPN-logfile")
    except KeyError:
        with open("result.txt", "a") as resultfile:
            resultfile.write("\n\nThe logfile entry from the configurationfile isn't present. Aborting program\n\n")
            exit()
    
    # Checks if the logfile is a valid logfile
    with open(logfile, "r") as file:
        # Check if the file looks like a logfile
        if not re.findall(r"\d{4}(:\d{2}){2}-(\d{2}:){2}\d{2} \w+ openvpn\[\d{1,5}]:", file.readline()):
                # Open the file
                with open("result.txt", "a") as resultfile:
                    # And write the, otherwise printed, statement to the file
                    resultfile.write("\n\nThe submitted file doesn't seem to be an OpenVPN-logfile. Aborting program\n\n")
                exit()

    # Check which functions need to be called
    with suppress(KeyError):
        if configdata["top10"].lower() == "unsuccessful":
            dvdl_menu_handler(logfile, "1")

        elif configdata["top10"].lower() == "successful":
            dvdl_menu_handler(logfile, "2")

    with suppress(KeyError):
        if configdata["top5"].lower() == "unsuccessful":
            dvdl_menu_handler(logfile, "3")

        elif configdata["top5"].lower() == "successful":
            dvdl_menu_handler(logfile, "4")

    with suppress(KeyError):
        if configdata["non-ovpn-prot"].lower() == "true":
            dvdl_menu_handler(logfile, "5")

    with suppress(KeyError):
        if configdata["man-coms"].lower() == "true":
            dvdl_menu_handler(logfile, "6")

    with suppress(KeyError):
        if type(configdata["check-ip"]) == list:
            dvdl_menu_handler(logfile, "7", checkip=configdata["check-ip"])

    with suppress(KeyError):
        if configdata["knownip-file"].lower() != "false" and configdata["new-ips"].lower() != "false":
            # Check if the knownip-file exists
            knownip = dvdl_check_file_location(configdata["knownip-file"], "knownip-file")
            dvdl_menu_handler(logfile, "8", ipfile=knownip)


##########Run at boot code##########

try:
    # If the program is started with the configfile
    if arguments.configfile != "":
        # Make sure all output gets redirected to a file
        arguments.printer = True
    
        # Call the function that handles the configfile
        dvdl_config_handler(arguments.configfile)
        
        # And stop the program
        exit()
    
    # Check if the logfile location is correct
    logfile = dvdl_check_file_location(arguments.logfile, "OpenVPN-logfile")
    
    # Check if the logfile is actually a logfile
    while True:
        # Check if the identifier is present
        with open(logfile, "r") as file:

            # Check if the file looks like a logfile
            if not re.findall(r"\d{4}(:\d{2}){2}-(\d{2}:){2}\d{2} \w+ openvpn\[\d{1,5}]:", file.readline()):

                # If the output needs to be printed...
                if not arguments.printer:
                    # If the identiefier isn't present let the user choose another file
                    print("This doesn't seem to be an OpenVPN-logfile. Please select another file")
                    file = dvdl_check_file_location("", "OpenVPN-logfile", fnf=False)

                # If the output needs to be written to a file...
                else:
                    # Open the file
                    with open("result.txt", "a") as resultfile:
                        # And write the, otherwise printed, statement to the file
                        resultfile.write("\n\nThe submitted file doesn't seem to be an OpenVPN-logfile.\n\n")
                    exit()

            # If the identifier is present stop the loop
            else:
                break

    # If the GUI needs to be showed
    if arguments.gui:
        # Show the file version
        print(f"Program version: {version}")

        # Start the menu loop
        while True:
            # Call the show menu function
            dvdl_show_menu(logfile)

    # If the GUI doesn't need to be showed and no configfile path was given
    elif arguments.configfile == "":
        dvdl_menu_handler(logfile, arguments)

# If the program is stopped by a keyboardinterrupt (crtl+c)...
except KeyboardInterrupt:
    # If the output needs to be printed...
    if not arguments.printer:
        # Print the message
        print("\n\nOperation cancelled by user")

    # If the output needs to be written to a file...
    else:
        # Open the file
        with open("result.txt", "a") as resultfile:
            # And write the, otherwise printed, statement to the file
            resultfile.write("\n\nOperation cancelled by user\n\n")

            # Write a breakline to the file to make it more organised
            resultfile.write("\n====================================================================================================\n")

    # And stop the program
    exit()

# To make the exit-statements in the code work without unnecissairy messages
except SystemExit:
    # If the output needs to be written to a file...
    if arguments.printer:
        # Open the file
        with open("result.txt", "a") as resultfile:
            # Write a breakline to the file to make it more organised
            resultfile.write("\n====================================================================================================\n")
    exit()

# If an unknown error ocured...
except:
    # If the output needs to be printed...
    if not arguments.printer:
        # Print the message
        print("\n\nSomething went wrong. Please try again later")

    # If the output needs to be written to a file...
    else:
        # Open the file
        with open("result.txt", "a") as resultfile:
            # And write the, otherwise printed, statement to the file
            resultfile.write("\n\nSomething went wrong\n\n")

            # Write a breakline to the file to make it more organised
            resultfile.write("\n====================================================================================================\n")
    exit()

# If the output needs to be written to a file...
if arguments.printer:
    # Open the file
    with open("result.txt", "a") as resultfile:
        # Write a breakline to the file to make it more organised
        resultfile.write("\n\n\n====================================================================================================\n")