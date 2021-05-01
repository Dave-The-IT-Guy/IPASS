#Name: Dave van der Leek (1777075)
#Class:
#Programname: OVPNLogbrowser
#Description: Een programma om OpenVPN logfiles uit te lezen
version = 0.1


##########Imports##########
import re #For regex


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

    #If one of the first choices were selected then...
    if choice == "1" or choice == "2":
        #Let the user know the program is generating the requested info
        print("\nGenerating...\n")

        #Check which parameter the function needs and call the function
        if choice == "1":
            results = dvdl_top10_inlog(file="openvpn.log", unsuccessful=False)
        else:
            results = dvdl_top10_inlog(file="openvpn.log", unsuccessful=True)

        #A counter to show the positions
        position = 0

        #Loop trough the results...
        for result in results:
            #Add one to count
            position += 1

            #And show it to the user
            print(f"{position}: {result[0]} ({result[1]} try's)")

    elif choice == "3":
        pass

    elif choice == "4":
        pass

    elif choice == "5":
        pass

    elif choice == "6":
        pass

    elif choice == "7":
        pass

    elif choice == "8":
        pass

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
        ip = (re.findall(r"\b(?:[0-9]{0,3}\.){3}(?:[0-9]{1,3})", string))[0] #To test: https://regex101.com/

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


##########Run at boot code##########


#TODO: Check if program is interactive or not
#TODO: Show program version/information
#TODO: Check if the logfile exists
while True:
    dvdl_show_menu()