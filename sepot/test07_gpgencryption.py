import sys
from user_profile import user_profile
from filestat import filestat

profile = user_profile()
print profile.get_public_keys()
print profile.get_private_keys()


combolist1 = []

# for k in profile.private_keys:
#     combolist1.append("(Priv) %s"%k["uids"][0])

for k in profile.public_keys:
    combolist1.append("(Publ) %s"%k["uids"][0])

combolist1.sort()

if len(combolist1) > 0:
    i=-1
    for row in combolist1:
        i=i+1
        print "%i %s" %(i,row)
else:
    print("ERROR: No users GPG key(s) found. Please import or create GPG key and start program again.") 
    sys.exit(1)    

keyindextobeused = raw_input("Enter key number which should be used:  ")
print "you entered ", keyindextobeused


keyselected = combolist1[int(keyindextobeused)][7:]

print "Key: [%s] will be used. " % keyselected

#===============================================================================
# Encrypting files
#===============================================================================
filein="C:\\Temp\\source.txt"
fileout="C:\\Temp\\source.txt.gpg"

#open(filein, 'w').write('You need to Google Venn diagram.')



fcin = filestat(filein)
fcin.printinfo()

if fcin["is_gpgencrypted_flag"]:
#     with open(filein, 'rb') as f:
#         status = profile.gpg.encrypt_file(f, recipients=[keyselected], armor=True, output="%s.asc"%fileout)
#         status = profile.gpg.encrypt_file(f, recipients=[keyselected], output=fileout)
#     
#     print 'ok: ', status.ok
#     print 'status: ', status.status
    pass
else:
    with open(filein, 'rb') as f:
        status = profile.gpg.encrypt_file(f, recipients=[keyselected], armor=True, output="%s.asc"%fileout)
        status = profile.gpg.encrypt_file(f, recipients=[keyselected], output=fileout)
    
    print 'ok: ', status.ok
    print 'status: ', status.status


#===============================================================================
# Decrypting files
#===============================================================================
#filein="C:\\Temp\\source.txt.gpg"


