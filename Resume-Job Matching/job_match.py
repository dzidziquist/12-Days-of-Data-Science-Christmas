import pandas as pd
import docx2txt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


cv = CountVectorizer()


#matching scraped jobs with resume 
class MatchJobs:
    def job_matching(self,resume, company_name,job, job_description, location):
        companies = []
        Match = []
        job_desc = []
        locations = []
        for i, j, k,l in zip(company_name,job, job_description,location):
            text = [resume, i]
            count_matrix = cv.fit_transform(text)
            matchPercentage = round(cosine_similarity(count_matrix)[0][1] * 100, 2)
            companies.append(i)
            Match.append(matchPercentage)
            job_desc.append(k)
            locations.append(l)


            jobs = pd.DataFrame()
            jobs['Company'] = companies
            jobs['Job Description'] = job_desc
            jobs['Location'] = locations
            jobs['Matching Percentages'] = Match
        return jobs