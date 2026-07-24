import os                                                   # Imports the "os" module for file detection and deletion.

if not os.path.exists('MasterFile.txt'):                    # Checks if a MasterFile already exists in the system.
    masterfile=open('MasterFile.txt','w+')                  # Creates a new blank Masterfile.
else:
    masterfile=open('MasterFile.txt','r+')


def master():
    'Creates, Opens and Deletes Database Files on Demand.'

    global masterfile                                       # Fetches the global masterfile variable to use inside the function.
    
    print("\nChoose an Option from the Master Menu:")
    print("1.Create a New File.")
    print("2.Open an Existing File.")
    print("3.Delete a File.")
    masterchoice = input("Choose an Option(1-3): ")
        
    if masterchoice == '1':
        filename = input("\nCreate File with the Name: ")
        masterfile.seek(0)
        lines=masterfile.readlines()
        
        if os.path.exists(f'{filename}.csv'):               # Checks if the file with this name already exists.
            print(f'\n"{filename}.csv" already Exists. Choose an Option:')
            print(f'\n1.Create a New File with a Similar Name: "_{filename}.csv"')
            print(f'2.Open the Original "{filename}.csv"')
            print(f'3.Empty the Original "{filename}.csv" and Start from Scratch.')
            print('>Or Enter Any Key to Go Back to the Master Menu.')
            choice=input('\nChoose an Option: ')
            
            if choice=='1':
                file=open(f'_{filename}.csv','w+')          # Creates a new blank file with a similar name.
                filename='_'+filename                       # Renames the file.
                lines.append(filename)                      # Adds the new file name to the list of database files.
                
                with open('MasterFile.txt','w+') as masterfile:
                    masterfile.writelines(lines)            # Writes the updated list of file names on a fresh Masterfile.
                    masterfile.write('\n')
                
                print(f'"{filename}.csv" Created and Opened Successfully!')
                return file, filename
            
            elif choice=='2':
                file=open(f'{filename}.csv','r+')
                print(f'"{filename}.csv" Opened Successfully!')
                return file, filename
            
            elif choice=='3':
                file=open(f'{filename}.csv','w+')
                primefile=open(f'{filename}(prime).txt','w+')
                primefile.close()                           # Creates a new primary key file with the original name.
                print(f'New, Empty "{filename}.csv" Created and Opened Successfully!')
                return file, filename
            
            else:
                file, filename=master()                     # Recursive call to the "master()" function.
                return file, filename
        
        else:
            file=open(f'{filename}.csv','w+')
            lines.append(filename)
            
            with open('MasterFile.txt','w+') as masterfile:
                masterfile.writelines(lines)                # Writes the updated list of file names on a fresh Masterfile.
                masterfile.write('\n')

            print(f'"{filename}.csv" Created and Opened Successfully!')
            return file, filename
        
    elif masterchoice == '2':
        masterfile.seek(0)
        lines=masterfile.readlines()
        
        while True:
            print('\nChoose a File to Open:')
            for l in lines:                                 # Displays the names of the existing database files.
                print(l,end='')
            
            print('>Or Enter "E" to Go Back to the Master Menu.')
            filename = input('\nEnter the File Name(Or "E"): ')
            
            if filename=='E' or filename=='e':
                break
            
            elif os.path.exists(f'{filename}.csv'):         # Check if the file exists.
                file=open(f'{filename}.csv','r+')
                print(f'"{filename}.csv" Opened Successfully!')
                return file,filename
            
            else:
                print(f'"{filename}.csv" Not Found.')
        
        file, filename=master()                             # Recursive call to the "master()" function.
        return file, filename

    elif masterchoice == '3':
        masterfile.seek(0)
        lines=masterfile.readlines()
        
        while True:
            print('\nChoose a File to Delete:')           
            for l in lines:                                 # Displays the names of the existing database files.
                print(l,end='')
            
            print('>Or Enter "E" or to Go Back to the Master Menu.')
            filename = input('\nEnter the File Name(Or "E"): ')
            
            if filename=='E' or filename=='e':
                break
            
            elif os.path.exists(f'{filename}.csv'):         # Check if the file exists.
                os.remove(f'{filename}.csv')                # Deletes the file from the system.
                os.remove(f'{filename}(prime).txt')         # Deletes the corresponding primary key file from the system.
                lines.remove(f'{filename}\n')
                
                with open('MasterFile.txt','w+') as masterfile:
                    masterfile.writelines(lines)            # Writes the updated list of file names on a fresh Masterfile.
                    masterfile.write('\n')

                print(f'"{filename}.csv" Deleted Successfully!')
                break
            
            else:
                print(f'"{filename}.csv" Not Found.')
        
        file, filename=master()                             # Recursive call to the "master()" function.
        return file, filename

    else:
        print("\nInvalid Input! Please Enter 1,2 or 3.")
        file, filename=master()                             # Recursive call to the "master()" function.
        return file, filename


def write_row(filename, list, n,e=0):
    'Takes the List as an Input and Writes it on the nth Line of the given File'
    
    file = open(f'{filename}.csv', 'r+')
    file.seek(n * 501)                                      # Points to the first byte of the nth line.
    line_len = 0

    for d in list:
        file.write(f'{d},')                                 # Writes the list element and a comma as the separator.
        line_len += (len(d) + 1)                            # Calculates the combined total width of all the fields/entries.
    
    file.write(' ' * (500 - line_len))                      # Uses space to overwrite/erase the previous entries.
    
    if e or not n:
        file.seek((n+1)*501-2)                              # The first line is a special case, and 'e' stands for exception.
    else:
        file.seek((n+1)*501-1)
    
    file.write('\n')                                        # Completes the row entry by moving to next line.
    file.close()
    pass


def removefield(filename,i):
    'Takes the Field Number, i, and Removes that Field from the given File'
    
    file = open(f'{filename}.csv', 'r')
    lines=file.readlines()
    file.close()
    line_num=0                                              # Initializes the line number count.
    
    for l in lines:
        entries=l.split(',')                                # Uses comma to split a string into a list of multiple substrings.
        entries.pop()                                       # Removes the last element, which is always '\n'.
        delta=i-len(entries)+1                              # Calculates the number of times to fill the rest of the record.
        
        for n in range(delta):
            entries.append('-')                             # Fills the record with '-' if any field is empty.
        
        entries.remove(entries[i])                          # Removes all the data under the field, with the field number i.
        write_row(filename,entries,line_num)                # Writes the updated records on same lines of the database file.
        line_num+=1                                         # Increments the line number to help the 'write_row()' function.
    
    print('Field Removed!')
    pass


def display_file(filename):
    'Reads the Contents of the given File and Displays them in the Terminal.'
    
    file = open(f'{filename}.csv', 'r')
    data = file.readlines()
    column_widths=[]                                        # Initializes a list which stores max width of each column.
    
    for d in data:
        content = d.split(',')                              # Uses comma to split a string into a list of multiple substrings.
        content.pop()                                       # Removes the last element, which is always '\n'.
        
        if len(column_widths)==0:                           # Checks if the column widths list is empty.
            for c in content:
                column_widths.append(0)                     # Fills the column widths list with zeroes if empty.
        
        for i in range(len(content)):                       # Iterates over the indices of the list.
            if len(content[i])>column_widths[i]:            # Checks if the this width is the greatest for its column.
                column_widths[i]=len(content[i])            # Updates the column widths if the above condition is true
    
    for d in data:
        content = d.split(',')                              # Uses comma to split a string into a list of multiple substrings.
        content.pop()                                       # Removes the last element, which is always '\n'.
        n=0                                                 # Initializes the index counter.
        for c in content:
            print(f' {c:^{column_widths[n]}} ',end='|')     # Displays each element in terminal with proper formatting.
            n+=1                                            # Increments the index counter.
        print()                                             # Moves the pointer to the next line in the terminal.
    file.close()
    pass


def check_unique(fieldname,lines,prompt):
    'Checks if the Data Entry into the Primary Key Field is Unique or not.'
    
    while True:
        entry = input(prompt)
                    
        if fieldname==primekey:                             # Checks if the field being entered is the primary key or not.
            for l in lines:
                entries = l.split(',')                      # Splits the line string, returning entries as individual strings.
                            
                if entries[prime_index]==entry:             # Checks if the new entry is unique or not.
                    print(f'\nThe "{fieldname}" Field already contains the Value "{entry}"!')
                    print(f'The "{fieldname}" Field is the Primary Key so All Values in it Must be Unique.')
                    break
            else:
                break
        else:
            break
    return entry



print('\n\nWelcome to The DataBase Manager!')
file, filename=master()
masterfile.close()
fields = file.readline()                                    # Reads the first line and returns the field names as a string.
file.close()
fields = fields.split(',')                                  # Splits the string, returning field names as individual strings.
fields.pop()                                                # Removes the last element, which is always '\n'.

with open(f'{filename}(prime).txt','a+') as primefile:      # Creates a file to hold information about the primary key.
    primefile.seek(0)
    primekey=primefile.readline()
    
    if primekey=='':
        primekey_set=0                                      # Raises a flag to demand a primary key, if not found in the file.
    else:
        prime_index=fields.index(primekey)                  # Retrieves the field number of the primary key field.
        primekey_set=1                                      # Raises a flag that the primary key is already decided, if found.

while True:
    print('\nChoose an Option:')
    print('1.Add a New Field')
    print('2.Remove a Field')
    print('3.Add a New Record')
    print('4.View a Record')
    print('5.Display all Records')
    print('6.End Program')
    option = input('Select 1-6: ')
    
    if option == '1':
        newfield = input('\nEnter Field Name: ')
        fields.append(f'{newfield}')                        # Adds the new field to the list of fields.
        write_row(filename, fields, 0)                      # Writes the new field onto the top of the database file.
        print('Field Added!')
    
    elif option == '2':
        while True:
            fieldname = input('\nRemove Field: ')
            
            if fieldname in fields:                         # Checks if the field entered exists in the current database.
                break
            else:
                print(f'"{fieldname}" Field Not Found.')
        
        field_index=fields.index(fieldname)                 # Finds the index of the specified field in the list and returns it.
        
        if fieldname==primekey:                             # Checks if the field to be removed is the primary key or not.
            print(f'The "{fieldname}" Field is the Primary Key. Removing it may Break some DataBase Functions.')
            confirmation=input('Are you Sure you want to Remove this Field? (Y/N): ')
            
            if confirmation=='Y' or confirmation=='y':
                fields.remove(f'{fieldname}')               # Removes the specified field from the list of fields.
                primekey_set=0                              # Raises a flag to demand a primary key.
                primefile=open(f'{filename}(prime).txt','w+')
                primefile.close()                           # Empties the primary key file.
                removefield(filename,field_index)           # Removes the field and all its contents from the database file.
        
        else:
            fields.remove(f'{fieldname}')                   # Removes the specified field from the list of fields.
            removefield(filename,field_index)               # Removes the field and all its contents from the database file.
    
    elif option == '3':
        file = open(f'{filename}.csv', 'r+')
        lines=file.readlines()
        file.close()
        
        if primekey_set:                                    # Checks if the primary key is already decided or not.
            records = []
            total_lines = len(lines)
            print()
            
            for f in fields:
                prompt=(f'Enter {f}: ')
                data=check_unique(f,lines,prompt)
                records.append(data)                        # Adds the new record to the list of the records.
            
            write_row(filename, records, total_lines)       # Writes the new record on the last line of the database file.
            print('Record Added!')
        
        else:
            while True:
                primekey=input('\nChoose and Enter a Field as the Primary Key: ')
                
                if primekey in fields:                      # Checks if the desired primary key is an existing field or not.
                    prime_index=fields.index(primekey)      # Determines the index number of the primary key field.
                    primefile=open(f'{filename}(prime).txt','r+')
                    primefile.write(primekey)               # Save the name of the primary key on a separate text file.
                    primefile.close
                    primekey_set=1                          # Raises the flag that the primary key has been chosen.
                    print('Success! Primary Key Set.')
                    break
                
                else:
                    print(f'"{primekey}" Field Not Found.')
    
    elif option=='4':
        file=open(f'{filename}.csv', 'r+')
        lines=file.readlines()
        file.close()
        prime_rec_found=0                                   # Initiates a flag that tells if the primary record has been found.
        
        while not prime_rec_found:                          # Keeps the loop going until the primary record has been found.
            prime_rec=input(f'\nEnter {primekey}: ')
            line_num=0                                      # Initializes a line counter.
            
            for l in lines:
                entries=l.split(',')                        # Uses comma to split a string into a list of multiple substrings.
                entries.pop()                               # Removes the last element, which is always '\n'.
                
                if prime_rec==entries[prime_index]:         # Checks if the primary record called is in the primary key field.
                    view=entries                            # Stores the record data as a separate variable.
                    prime_rec_found=1                       # Indicates that the primary record has been found.
                    break
                line_num+=1                                 # Increments the line counter to help the 'write_row()' function.
            
            else:
                print(f'"{prime_rec}" Not Found.')
        
        for i in range(len(view)):
            print(f'{fields[i]}: {view[i]}')                # Displays the record contents in an appropriate format.
        
        print('\nChoose an Option:')
        print('1.Edit the Record')
        print('2.Remove the Record')
        print('Or Enter Any Value to Go Back.')
        choice=input('Enter your Choice: ')
        
        if choice=='1':
            while True:
                fieldname=input('\nEnter a Field: ')
                
                if fieldname in fields:                     # Checks if the field entered exists in the current database.
                    break
                else:
                    print(f'"{fieldname}" Field Not Found.')
            
            field_index=fields.index(fieldname)             # Finds the index of the specified field in the list and returns it.
            delta=field_index-len(view)+1                   # Calculates the number of times to fill the rest of the record.
            
            for n in range(delta):
                view.append('-')                            # Fills the record with '-' if any field is empty.
            
            prompt='Set New Value: '
            view[field_index]=check_unique(fieldname,lines,prompt)
            write_row(filename,view,line_num,1)             # Writes the edited record on the same line of the database file.
            print('Success! New Value Set.')
        
        elif choice=='2':
            lines.remove(lines[line_num])                   # Removes the record on the specified line of the database file.
            print('Record Removed!')
            file=open(f'{filename}.csv', 'w+')              # Wipes teh database file clean for the re-entry of all records.
            file.close()
            
            line_num=0                                      # Initializes a line counter.
            for l in lines:
                entries=l.split(',')                        # Uses comma to split a string into a list of multiple substrings.
                entries.pop()                               # Removes the last element, which is always '\n'.
                delta=len(fields)-len(entries)              # Calculates the number of times to fill the rest of the record.
                
                for n in range(delta):
                    entries.append('-')                     # Fills the record with '-' if any field is empty.
                
                write_row(filename,entries,line_num)        # Writes the records on the same respective lines of the file.
                line_num+=1                                 # Increments the line counter to help the 'write_row()' function.
    
    elif option=='5':
        print()
        display_file(filename)                              # Calls the function to display the database in the terminal.
    
    elif option == '6':
        print('\nProgram Ended!')                           # Ends the program.
        break
