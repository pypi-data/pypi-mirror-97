from pyjob.search import Search
from loguru import logger
import sys
import time

class Details(Search):
    
    _DETAILS_URL = "https://www.reed.co.uk/api/1.0/jobs/"
    
    details = []
    
    def __init__(self):
        Search.__init__(self)
    
    def get_extended_description(self, jobId: str):
        resp = self._session.get(f"{self._DETAILS_URL}/{jobId}").json()
        time.sleep(1) # Rate-limiting avoidance on continually getting job details.
        extended_desc = resp['jobDescription']
        
        return extended_desc
        
    def get_details(self, jobs: dict):
        
        if len(jobs) == 0:
            logger.info("Amount of search results cannot be 0.")
            sys.exit(1)
        
        for job in jobs:
            self.details.append(self.get_extended_description(job['jobId']))
        
        return self.details
