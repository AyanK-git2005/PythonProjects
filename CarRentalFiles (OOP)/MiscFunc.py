
def updateID(index):
    'Retrieves and increments the ID stored at the specified index'

    with open('IDfile.txt','r+') as file:
        IDs=eval(file.read())                   # Retrieves contents of the file and converts it into a list
        IDs[index]+=1                           # Increments the tally of the ID at the specified index

    with open('IDfile.txt','w+') as file:
        file.write(str(IDs))                    # Writes the updated IDs into the an empty text file
    return IDs[index]                           # Returns the ID at the specified index
