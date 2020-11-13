import csv

def save_to_file(jobs):
    file = open("jobs.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["TITLE", "COMPANY", "LOCATION", "LINK"])
    
    for job in jobs:
        writer.writerow(job.values())
    
    return