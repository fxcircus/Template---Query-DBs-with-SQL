import os
from datetime import date
import mysql.connector
import subprocess
import credentials
import sys

# -------------------------------------------------
# Import ENV vars from credentials file
# -------------------------------------------------
db_list = credentials.DBList()
db_url = credentials.db_url
db_name = credentials.db_name
db_username = credentials.db_username
db_password = credentials.db_password

# -------------------------
# Get query_param from user
# -------------------------
query_param = input("Enter parameter for search:\n")
text_to_match = "add base case here"

# Optional - change DB based on input
if text_to_match in query_param:
    pass
elif "use db2" in query_param:
    db_url = db_list.db2
else:
    sys.exit(f"Invalid data: {query_param}\t!!! exiting script !!!") # Edge case - handling invalid input


print(f"Collecting data for: {query_param}\tfrom: {db_url}")

# ---------------------------------------------------------
# Run DB query with user input param (change to your needs)
# ---------------------------------------------------------
db_query= f"SELECT * FROM {query_param}'"

db = mysql.connector.connect(
	    host=db_url,
	    user=db_username,
	    password=db_password,
	    database=db_name
)
db_cursor = db.cursor()
db_cursor.execute(db_query)
db_results = db_cursor.fetchall() # returned results from DB
# print(db_results) # print results for testing

# -------------------------------------------------
# Build table with results
# (Converts results from a list to a string)
# -------------------------------------------------
results_str = ""
for row in db_results:
    formatted_row = '\t'.join(str(v) for v in row)
    results_str = results_str + formatted_row + '\n'

# -------------------------------------------------
# Create new folder and local results file
# -------------------------------------------------
curr_time = date.today()
folder_name = f"{curr_time}" 
file_name = query_param

# Create folder structure:
if not os.path.exists("output"):
    os.makedirs("output")
os.chdir("output")
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
os.chdir(folder_name)
output_folder = os.getcwd()

# Create file, write results, open in folder:
f = open(f"{file_name}.txt", "a")
f.write(results_str)
f.close()
subprocess.Popen(["open", output_folder])