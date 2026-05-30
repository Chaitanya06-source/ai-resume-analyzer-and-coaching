import os
import subprocess
import sys

# Change to project directory
os.chdir(r"C:\Users\sanam\resume_analyzer_coaching_system")

# Run Streamlit
subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])