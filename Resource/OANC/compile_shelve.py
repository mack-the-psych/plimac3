#If there is an existing db, it should be deleted before loading otherwise
#the frequency information will be invalid.

import sys

sys.path.append(r'../../Lib')

from ac_oanc_lemma_frequency import *

ac_load_oanc_shelve(r'ANC-all-lemma-04262014.csv', r'ANC-all-lemma-04262014.db')
