

'''
Created on Oct 24, 2014

@author: lukaz@centrum.cz
'''
from argparse import RawTextHelpFormatter
import argparse
import os
from pkg_resources import require
import sys

from logger import log
import user_profile
#log.error("adsasd")

#
# Arguments parsing
#
parser=argparse.ArgumentParser(description='sepot.py', formatter_class=RawTextHelpFormatter)

parser_group = parser.add_mutually_exclusive_group()

parser_group.add_argument("-d","--decrypt",
                          help="Decryption mode.\n(If not set then this will be set automatically depending on the file type)\n\n",
                          action="store_true"
                          )
parser_group.add_argument("-e","--encrypt",
                          help="Encryption mode.\n(If not set then this will be set automatically depending on the file type)\n\n\n",
                          action="store_true"
                          )


parser.add_argument("-s","--shred-source",
                          help="Shred input files/directories.\n\n",
                          action="store_true"
                          )

parser.add_argument("-o","--output-dir",
                     help="Output files can optionaly be saved to specified directory.\n(If not set this will be asked interactively)\n\n",
                     action="store_true")

parser.add_argument("-v", "--verbose\n\n", 
                    action="store_true")

parser.add_argument("FILE",
                    help="Single or multiple files/directories to process delimited by space\n\n",
                    nargs="+"
                    )

args=parser.parse_args()






# Python version check
if (sys.version_info > (3, 0)):
    log.info("Python version {0}.{1}.{2} program is started.".format(sys.version_info.major,sys.version_info.minor,sys.version_info.micro)  )
else:
    log.warning("ABORTED - Python version {0}.{1}.{2} but at least version 3.0 is required. ".format(sys.version_info.major,sys.version_info.minor,sys.version_info.micro)  )
    exit(1)


def Main():
    # Log arguments
    log.info(args)
    log.info("called with arguments: {0}".format(args))
    log.info('testlog')
    exit(0)
    
if __name__ == '__main__':
    Main()