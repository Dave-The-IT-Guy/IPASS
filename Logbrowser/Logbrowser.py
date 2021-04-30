#Name: Dave van der Leek (1777075)
#Class:
#Programname: OVPNLogbrowser
#Description: Een programma om OpenVPN logfiles uit te lezen
version = 0.1


##########Functions##########


#This functions shows the menu
def dvdl_show_menu():
    print("How may I assist you?\n"
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
    return


#Retrieve all data from the logfile and filter it
def dvdl_filter_logfile(**kwargs):
    #Retrieve the filtertype ("or" or "and")
    type = kwargs.get("type", "or")
    #Retrieve the first filter. If no filter was given then return all data
    filter1 = kwargs.get("filter1", "")
    #Retrieve the second filter. If no value has been assigned use this random string to prevent false-positives
    filter2 = kwargs.get("filter2", "jdehfbwjedshfbsdjhbfsjdbdfjseadbfjshbvfuerbvf!!!#$!#$#!$%^@54546546546532654dzfjdsbjhbfshjab")

    #Define list to store the result(s)
    result = []

    #Open the logfile
    with open("openvpn.log", "r") as logfile:
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

        #Return the result
        return (result)


##########Run at boot code##########


#TODO: Check if program is interactive or not
#TODO: Show program version/information
#TODO: Check if the logfile exists
dvdl_filter_logfile(type="or", filter1="TLS: Initial packet")