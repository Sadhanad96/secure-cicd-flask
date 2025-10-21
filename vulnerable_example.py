# vulnerable_example.py
import os
password = "hardcodedpassword123"  # insecure: example for demo
def run_cmd(cmd):
    os.system(cmd)  # bandit should flag this
