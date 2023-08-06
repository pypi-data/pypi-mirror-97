from libLHF.LHF import LHF
import sys
import os



# print(os.path.abspath("moreexceptions.py"))
print(os.getcwd())
pyLHF = LHF()
# sys.argv = ["-i", "twoCircles.csv"]
testrun = pyLHF.runPH3(sys.argv)
print(testrun.betti.death)
