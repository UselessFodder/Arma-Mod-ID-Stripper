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
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Mod Lists", "*.html")])
    
    is_acceptable = checkFile(file_path)
    
    if is_acceptable:
        mods = getModIDs(file_path)
        
        global mod_IDs
        mod_IDs = formatModIDs(mods)
        
        #update label
        update_results(mod_IDs)
        
        #enable copy button
        execute_button["state"] = "normal"
    else:
        messagebox.showerror("Error", "Mod List cannot be read.\n"
            +"Please confirm this is a correct mod list file.")

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

def update_results(new_text):
    result_label.config(text=new_text)

def copy_text(*args):
    if mod_IDs != "":
        root.clipboard_clear()
        root.clipboard_append(mod_IDs)
        
        messagebox.showinfo("Copy Successful","Mod IDs successfully copied to clipboard")
        #new_result = mod_IDs + "\n\n Mod IDs copied to the clipboard!"
        
        #result_label.config(text = new_result)

#variable to hold current list of modIDs
mod_IDs = ""

#Start GUI
 
#define main window
root = tk.Tk()
root.title("Arma 3 Mod ID Stripper")
root_frame = tk.Frame(root)
#root_frame.grid(row=0, column=0, padx=10, pady=10)

#define viewing window
result_frame = tk.Frame(root_frame, width=150,height=200)
result_frame.grid(row=0, column=0)
result_label = tk.Label(root_frame,
                        # bg="lightgray",
                        relief="sunken",
                        state="normal",
                        text="Mod ID list will appear here.",
                        anchor='n',
                        wraplength=300,
                        width = 50,
                        height= 30,
                        padx=10,
                        pady=10)
#result_label.pack(pady=5)
result_label.grid(row=0,column=0, rowspan=3, padx=5, pady=5)
result_label.bind('<Button-1>', copy_text)

#define frame for buttons
button_frame = tk.Frame(root_frame, width=50, height=200)
button_frame.grid(row=0,column=1,padx=5)

#define buttons for window
open_button = tk.Button(button_frame, text="Open File", width = 20, command=open_file)
open_button.grid(row=0, column=0, pady=5)
#open_button.pack(pady=5)
execute_button = tk.Button(button_frame, text="Copy IDs", width = 20, command=copy_text, state="disabled")
execute_button.grid(row=1, column=0, pady=5)

close_button = tk.Button(button_frame, text="Close", width = 20, command=root.destroy)
close_button.grid(row=2, column=0, pady=5)

#push buttons up
button_push_frame1 = tk.Frame(root_frame, width=50, height=100)
button_push_frame1.grid(row=1,column=1,pady=5)
button_push_frame2 = tk.Frame(root_frame, width=50, height=100)
button_push_frame2.grid(row=2,column=1,pady=5)

#result_frame.pack()
#button_frame.pack()
root_frame.pack()
#root_frame.pack_propagate(0)
root.mainloop() 
 
#define loop exit variable
#isModlist = False
#
#hold user in file selection until a good file is chosen
# while(True):
#     print()
#     #get modlist file name
#     modlist = input('Please enter exact name of modlist including the .html: ')
# 
#     #check file to ensure it is a modlist
#     isModlist = checkFile(modlist)
#     #***DEBUG print(isModlist)
#     
#     #exit loop if file is good
#     if isModlist:
#         break
# 
#     #check if exit is typed
#     if modlist.lower() == "exit":
#         #if so, quit program
#         sys.exit(0)
#     
#     #if we get here, inform the user the files was not good
#     print("File name incorrect. Please check spelling and ensure you put the .html!")
#     print("Type 'exit' to quit")
# 
# #strip mod ids
# all_mods = getModIDs(modlist)
# #***DEBUG all_mods = getModIDs('example.html')
# 
# #***DEBUG print(f'Array is {all_mods}')
# 
# forrmatted_mods = formatModIDs(all_mods)
# 
# print()
# print('Your Server Mod param line is:')
# print(f'{forrmatted_mods}')
# print()
# end = input("------------- END PROGRAM -------------")