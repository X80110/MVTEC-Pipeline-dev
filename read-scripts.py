import subprocess
import os
import pandas

this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)
os.chdir(this_dir)

try:
    result = subprocess.run(["Rscript","xavier_dataprep.R"], capture_output=True)
    print(result.stdout.decode())
except Exception: 
    print(result.stderr.decode())

