#If there is an existing db, it should be deleted before loading otherwise
#the frequency information will be invalid.

import sys

sys.path.append(r'../../Lib')

from ac_oanc_lemma_frequency import *

ac_load_oanc_shelve(r'BCCWJ_frequencylist-FrqGE3.csv', r'BCCWJ_frequencylist-FrqGE3.db', 'Jp')
