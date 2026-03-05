import os

print("Running data collection...")
os.system("python src/data_collect.py")

print("Running data cleaning...")
os.system("python src/data_clean.py")

print("Pipeline complete!")
