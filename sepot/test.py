
from files import files
from filestat import filestat
import sys
 

## Testing files in Run Arguments Configuration 
# C:\Temp\radio C:\Temp\bookmarks.html C:\lukaz\_DOCS\_SEC\sifrovane_verze_03.03\pas\Lukas-Pas-02.jpg.gpg

testingfiles = sys.argv[1:]    

## Non existing file test:
#testingfiles.append('C:\\nofile.txt')

selection = files(output_directory="C:\\Temp\\sepot_out", 
                  dir_archive_format="ZIP", 
                  gpg_key="lukaz@centrum.cz", 
                  use_ascii_armor=True)

for f in testingfiles:
    selection.add(filestat(f))
    print "-------------------------------------"
    

print "\n"*2
    
for item in selection.flist:
    print item.printinfo()
    print "\n"*2
