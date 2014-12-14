import logging

log = logging.getLogger('sepot')
log.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

filelog = logging.FileHandler('sepot.log')
filelog.setLevel(logging.INFO)
filelog.setFormatter(formatter)

log.addHandler(filelog)



cons = logging.StreamHandler()
cons.setLevel(logging.INFO)
log.addHandler(cons)

