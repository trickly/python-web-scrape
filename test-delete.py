import os
def logLastWorkedOn(filePath, fileName, fileStage, indices):
    
    f = open (filePath+"log.txt", 'w')
    print ("writing")
    f.write(fileStage + "\r" + fileName+"\n")
    levels = '-'.join(str(x) for x in indices)
    f.write(levels)
    print (levels)
    f.close()

dlPth = os.path.join(os.getenv('USERPROFILE'), 'Downloads')
# destPth will just be a directory where I'll put all my (renamed) files in.
destPth = dlPth+"\\dhis3data\\"
logLastWorkedOn(destPth,"chimp-chomp-champ", "PRE", [32,2,4])