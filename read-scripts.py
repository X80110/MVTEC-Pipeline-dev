import subprocess
import os

this_file = os.path.abspath(__file__)
this_dir = os.path.dirnaame(this_file)
os.chdir(this_dir)

result = subprocess.run(["Rscript", ])