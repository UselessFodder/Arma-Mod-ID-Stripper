"""
Arma 3 Mod ID Stripper by UselessFodder
Description: This code will search through a generated Arma 3 modlist hrml file
    and pull out every Steam Mod ID. Then, it will format it into a server param
    launcher format as such: "@[modid]; @[modid];"
    
Input: User entered filename
Return: Printout of param IDs

"""
#imports
import sys

def checkFile(fileLoc):
    """
        Function to open a modfile and check for the text 
            <!--Created by Arma 3 Launcher: https://arma3.com-->
            which denotes the file is a modlist and not a different
            kind of file
        Parameters: html file name[str]
        Return: confirm file is a modlist [bool]
    """
    
    #define array to pull first three lines to check file
    some_lines = []
    
    #define text to search for
    key_text = "<!--Created by Arma 3 Launcher: https://arma3.com-->"
    
    #catch exceptions and return false
    try:
        #open file and create new reader
        with open(fileLoc,'r') as file:
            #read three lines
            for x in [0,1,2]:
                some_lines.append(file.readline())

            #***DEBUG    print(some_lines)

        #look for key_text in line 3 to prove it is a modlist
        if key_text in some_lines[2]:
            return True
        else:
            return False
    except:
        return False

def getModIDs(fileLoc):
    """
        Function that takes in a previously verified Arma 3 modlist and outputs
            an array of Steam mod IDs to be formatted into a startup param list
        Parameters: html file name[str]
        Return: mod ids [array]
    """
    #define return array
    mod_ids = []
    
    #define text we will look for
    key_Text = "?id="
    
    #open file and create new reader
    with open(fileLoc,'r') as file:
        #read all lines
        all_lines = file.readlines()
    
    #loop to scan through all lines
    for x in all_lines:
        #check if the start of a mod ID is in this line
        if key_Text in x:
            #get start of id
            id_start = x.find('?id=')
            #get end of id
            id_end = x.find('\"',id_start)
            #get mod id which starts at +4 after ?id=
            new_mod = x[id_start + 4:id_end]
            #store in array to return
            mod_ids.append(new_mod)
        
    #send finished array out
    return mod_ids

def formatModIDs(all_mods):
    """
        Function that takes in a previously stripped set of mod ids and outputs
            them in the correct format for an arma 3 server start parameter line
        Parameters: array of mod id's from getModIDs
        Return: string with all mod ids correctly formatted
    """
    #define final return array
    formatted_mods = ""
    
    #loop through all mods
    for x in all_mods:
        #attach proper format around entry
        formatted_mods = formatted_mods + "@" + x + ";"
    
    #return completed string
    return formatted_mods

#define loop exit variable
isModlist = False

#hold user in file selection until a good file is chosen
while(True):
    print()
    #get modlist file name
    modlist = input('Please enter exact name of modlist including the .html: ')

    #check file to ensure it is a modlist
    isModlist = checkFile(modlist)
    #***DEBUG print(isModlist)
    
    #exit loop if file is good
    if isModlist:
        break
    
    #if we get here, inform the user the files was not good
    print("File name incorrect. Please check spelling and ensure you put the .html!")

#strip mod ids
all_mods = getModIDs(modlist)
#***DEBUG all_mods = getModIDs('example.html')

#***DEBUG print(f'Array is {all_mods}')

forrmatted_mods = formatModIDs(all_mods)

print()
print('Your Server Mod param line is:')
print(f'{forrmatted_mods}')
print()
end = input("------------- END PROGRAM -------------")