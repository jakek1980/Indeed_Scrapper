import requests
from bs4 import BeautifulSoup

def get_last_page(url):
        
  result = requests.get(url)
  result.raise_for_status()
  soup = BeautifulSoup(result.text, "lxml")

  pagination = soup.find("div", attrs = {"class" : "pagination"})

  pages = []

  if pagination is None:
      pages =['0']

  else:
      links = pagination.find_all("a")
      for link in links[0:-1]:
         pages.append(int(link.string))

  max_page = pages[-1]
  return max_page

def extract_job(html):
     
        title = html.find("h2", {"class" : "title"}).find("a")["title"]
        company = html.find("span", {"class" : "company"})
        
        if company:
            company_a = company.find("a")

            if company_a is not None:
                company = str(company_a.get_text())

            else:
                company = str(company.get_text())
            
        else:
            company = None

        company = company.strip()
        location = html.find("div", {"class" : "recJobLoc"})["data-rc-loc"]
        job_id = html["data-jk"]

        return {'title' : title,
        'company' : company,
        'location' : location,
        "link" : f"https://www.indeed.com/viewjob?jk=" + job_id
        }



def extract_jobs(last_page, url):

    jobs = []

    for page in last_page:

        print(f"Scrapping Indeed_page {page}")

        result = requests.get(f"{url}&start={page * 50}")
        result.raise_for_status()
        soup = BeautifulSoup(result.text, "lxml")

        results = soup.find_all("div", {"class" : 
        "jobsearch-SerpJobCard"
        })

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs(word):

    url = f"https://www.indeed.com/jobs?q={word}&l=Los+Angeles%2C+CA&limit=50&radius=25"
    last_page = get_last_page(url)

    jobs = extract_jobs(last_page, url)

    return jobs


    
