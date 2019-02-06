import os
dlPth = os.path.join(os.getenv('USERPROFILE'), 'Downloads')
# destPth will just be a directory where I'll put all my (renamed) files in.
destPth = dlPth+"\\dhis2data\\"

#deprecated
def hasColdStore(txt):
    keywords = [" Cold Store"]
    if any(word in txt for word in keywords):
        return True
    else:
        return False


for f in os.listdir(destPth):
    if f.find(" Cold Store") > 0:
        os.rename(destPth+"\\" + f, destPth+"\\" + f.replace(" Cold Store", ""))
