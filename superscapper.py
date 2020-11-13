from flask import Flask, render_template, request, redirect, send_file
from selenium import webdriver
from indeed_so import get_jobs
from exporter import save_to_file
import time

app = Flask("SuperScrapper")

db = {}

@app.route("/")

def home():
  return render_template("h1.html")

@app.route("/report")

def report():
      
  word = request.args.get("word")
   
  if word:
    word = word.lower()
    jobs_in_db = db.get(word)
     
    if jobs_in_db:
      jobs = jobs_in_db
     
    else:
      jobs  = get_jobs(word)
      db[word] = jobs
        
 
  else:
     return redirect("/")

  return render_template("report.html",
    searchingBy = word,
    resultsNumber=len(jobs),
    jobs = jobs
  )

@app.route("/export")
def export():
  
  try:
    word = request.args.get("word")
    if not word:
      raise Exception()

    word  = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    
    save_to_file(jobs)
    return send_file("jobs.csv", as_attachment=True)
  
  except:
    return redirect("/")
 



app.run(host="0.0.0.0")
