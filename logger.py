import logging

log = logging.getLogger('sepot')
log.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Log messages to file
filelog = logging.FileHandler('sepot.log')
filelog.setLevel(logging.INFO)
filelog.setFormatter(formatter)
log.addHandler(filelog)

# Log messages to console 
cons = logging.StreamHandler()
cons.setLevel(logging.INFO)
log.addHandler(cons)

