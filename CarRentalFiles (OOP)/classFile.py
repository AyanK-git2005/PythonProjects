
class File:

    def __init__(self,name):
        self.name=name                                              # Assigns a name to the file


    def readit(self):
        'Reads the contents of a list-containing text file and returns it as a list.'

        with open(self.name+'.txt','r+') as file:
            contents=file.read()                                    # Reads the contents of the text file
        return eval(contents)                                       # Returns the contents as a list


    def update(self,data):
        'Adds a new row containing data (a list) to a text file containing a list.'
        lines=self.readit()

        with open(self.name+'.txt','w+') as file:
            lines.append(data)                                      # Rewrites the updated list in an empty file
            lines.sort()                                            # Sorts the list in an ascending order
            file.write(str(lines))


    def shortlist(self,ID):
        'Removes a row with the specified ID, from a text file containing a list.'
        lines=self.readit()

        for i in range(len(lines)):
            if lines[i][0]==ID:                                     # Checks the ID from first column
                del lines[i]                                        # Deletes the row of specified ID
                
                with open(self.name+'.txt','w+') as file:
                    lines.sort()                                    # Sorts the list in an ascending order
                    file.write(str(lines))
                break


    def display(self,column=16,filter=','):
        """Displays the contents of a text file containing a list, in a proper 
        format. If specified, the function only displays those rows that contains 
        the specified filter in the specified column."""

        content=self.readit()
        column_width=[]
        print()

        for c in range(len(content[0])):
            column_width.append(0)                                  # Initializes the width of each column

        for m in range(len(content)):
            for n in range(len(content[m])):

                if len(content[m][n])>column_width[n]:
                    if column==16 or filter==',':
                        column_width[n]=len(content[m][n])          # Determines the max width of a column

                    elif content[m][column]==filter or m==0:
                        column_width[n]=len(content[m][n])          # Determines the max width of a column

        for i in range(len(content)):
            if column==16 or filter==',':

                for j in range(len(content[i])):
                    print(f'{content[i][j]:^{column_width[j]}}',end=' | ')
                print()                                             # Displays the list in a proper format

            elif content[i][column]==filter or i==0:

                for j in range(len(content[i])):
                    print(f'{content[i][j]:^{column_width[j]}}',end=' | ')
                print()                                             # Displays the list in a proper format
