############################################################
#Name: Dave van der Leek (1777075)
#Class:
#Programname: OVPNLogbrowser
#Description: Een programma om OpenVPN logfiles uit te lezen
version = 0.1
############################################################

#Functions

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

#At boot code
#TODO: Check if program is interactive or not
#TODO: Check if the logfile exists
#TODO: Read entire log file and put it in a dictonairy?

dvdl_show_menu()