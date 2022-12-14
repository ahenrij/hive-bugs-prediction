"""Git logs parser.

This script aims at converting the input hive logs file into a 
csv file formatted as follow:

BugID,File
HIVE-26619,Jenkinsfile
...
HIVE-26471,standalone-metastore/metastore-server/src/main/java/org/apache/hadoop/hive/metastore/metrics/AcidMetricService.java
...

Author: Henri Aidasso <ahenrij@gmail.com>
"""
import re

input_file = "src/data/input/hive-git-logs.txt"
output_file = "src/data/output/hive-issues-files.csv"

with open(input_file, "r") as f:
    issue_id = None
    commit_id = None
    output_content = "CommitId,IssueId,Filename\n"
    
    for line in f:
        line = line.strip()
        # Capture new bug id
        if results := re.findall(" HIVE-\d+", line):
            issue_id = results[0][1:] # remove whitespace
            commit_id = line.split(" ")[0]
            continue
        # Add new line of "bugId,filename" for Java and C++ files
        if line.endswith((".java", ".cpp", ".h")):
            output_content += f"{commit_id},{issue_id},{line}\n"

    # write output file
    with open(output_file, "w") as of:
        of.write(output_content)

    print("Logs successfully parsed!")