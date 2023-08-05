import os
import sys
import requests
import time
from loguru import logger

class Search(object):
    """The 'Search' class is for conducting searches to the Reed Jobseeker API.
    Options that you do not wish to include can simply remain unset.
    The API documentation can be found here: https://www.reed.co.uk/developers/jobseeker

    Args:
        object (object): Base class, this is optional.

    Raises:
        requests.HTTPError: Errors on the requests made to the Reed API will raise this exception.

    Returns:
        class: Instance of the Search class when instansiated.
    """
    
    _API_KEY = None
    _SEARCH_URL = "https://www.reed.co.uk/api/1.0/search?"
    _LOG_LEVEL = None

        
    _search_keyterms = None
    _employer_id = None # Set ID for jobs by a specific employer, e.g. BAE Systems is 413757. This is best to glean from a particular job posting.
    _employer_profile_id = None # Reed API is not very clear around this, even responses usually contain 'None', generally avoid. Added for completeness.
    _location = None
    _distance_from_location = 10 # Default in miles
    _result_amount = 100 # Default and upper limit according to Reed API.
    _results_to_skip = 0
    _minimum_salary = 0
    _maximum_salary = 0
    _permanent = None
    _temporary = None
    _contract = None
    _recruitment_agency_post = None
    _employer_direct_post = None
    _graduate_suitable = None
    _total_results = 0
    _full_time_hours = None
    _part_time_hours = None
    _session = requests.Session()
    
    results = {}
    
    def __init__(self):
        """
        Constructor function for class setup. This ensures the API key is within the environment, updates authorisation to the API, and sets the logging level.
        """
        
        self._API_KEY = os.getenv("REED_API_KEY")
        if self._API_KEY is None:
            logger.info("REED_API_KEY is not set, exiting...")
            sys.exit(1)
            
        self._session.auth = (self._API_KEY, '') # Password is left blank according to Reed API docs.
        
        # Reset logger for ability to specify custom level.
        logger.remove()
        self._LOG_LEVEL = os.getenv("PYJOB_LEVEL")
        if self._LOG_LEVEL is None:
            logger.add(sys.stderr, level="INFO")

        else:
            logger.add(sys.stderr, level=self._LOG_LEVEL.upper())

    def set_max_results(self, value: int):
        """Set the maximum number of results to return from the API request.

        Args:
            value (int): The number of results to return, must be between 0 and 100.
        """
        
        if value > 0 and value <= 100:
            self._result_amount = value
        else:
            logger.info("Max results must be between 0 and 100.")
            exit()

    def set_graduate_roles(self, grad: bool):
        """Set whether the results should be considered suitable for university graduates.

        Args:
            grad (bool): Results should be graduate roles or not.
        """
        
        self._graduate_suitable = grad
        
    def set_employer_id(self, id: str):
        """The employer ID for job postings. It is recommended to retrieve this first from a posting by the employer.

        Args:
            id (str): The employer ID.
        """
        
        self._employer_id = id
    
    def set_employer_profile_id(self, id: str):
        """The employer profile ID for job postings. 
        Note: It is recommended to avoid using this, a lot of the Reed API responses also return 'None' for this,
        as it requires an employer to have set up a profile; this is included for completeness.

        Args:
            id (str): The employer profile ID.
        """
        
        self._employer_profile_id = id
        
    def set_keyterms(self, keyterms: list):
        """The terms to use for the search criteria, typically a job title, such as software engineer.

        Args:
            keyterms (list): A number of terms to use for the search, e.g. ['software engineer', 'Python']
        """
        
        if len(keyterms) != 0:
            
            if len(keyterms) == 1:
                logger.debug("Singular term: {}", keyterms[0])
                self._search_keyterms = keyterms[0]
            else:
                logger.debug("Multiple terms: {}", keyterms)
                self._search_keyterms = []
                for keyword in keyterms:
                    self._search_keyterms.append(keyword)
        else:
            logger.info("Key terms must be populated for a search.")
            sys.exit(1)


            
    def set_location(self, location: str):
        """The location of the job posting.

        Args:
            location (str): The job location, such as London.
        """

        if location is None:
            return
        logger.info("NOTE: The REED API seems to display job adverts that are also promoted/sponsored outside of your specified location.")
        time.sleep(2)
        self._location = location.replace(" ", "+")
    
    def set_location_distance(self, distance: int):
        """Set the distance, in miles, from a location that jobs can be near to.
        For example, '25' miles from London. 

        Args:
            distance (int): Number of miles away from a location to include in the search.
        """
        
        if distance >= 0:
            self._distance_from_location = distance
            logger.debug("Distance from location set to {}", self._distance_from_location)
        else:
            logger.info("Cannot have a distance lower than 0, using default of 10.")
            self._distance_from_location = 10
    

    
    def set_salary_range(self, min=0, max=0):
        """Set the minimum and maximum salary for the job search.
        These can be left unset to include jobs in all ranges.

        Args:
            min (int, optional): The lowest amount you are willing to accept. Defaults to 0.
            max (int, optional): The highest amount to cap out the job searches for. Defaults to 0.
        """
        
        if min < 0 or max < 0:
            logger.info("Salary must be between greater than 0.")
            sys.exit(1)
            
        if min >= 0:
            self._minimum_salary = min
        
        if max >= 0:
            self._maximum_salary = max
            
        logger.debug("Maximum salary: {}, Minimum salary: {}", self._maximum_salary, self._minimum_salary)

    
    def set_posted_by(self, poster: str):
        """Set who the job advert was posted by, either a recruitment agency or the employer directly.

        Args:
            poster (str): Who posted the job to Reed.
        """
        
        if poster is None:
            return
        elif poster.lower() == "employer":
            self._employer_direct_post = True
        elif poster.lower() == "recruiter":
            self._recruitment_agency_post = True
        else:
            logger.info("Available values are 'employer' and 'recruiter' for job postings.")
            sys.exit(1)
        
    
    def set_job_type(self, job_type: str):
        """The type of job length that you are looking for.

        Args:
            job_type (str): The job type you are looking for, most commonly this will either be 'permanent' or 'contract'.
        """
        
        if job_type is None:
            return
        elif job_type.lower() == "permanent":
            self._permanent = True
        elif job_type.lower() == "temporary":
            self._temporary = True    
        elif job_type.lower() == "contract":
            self._contract = True
        else:
            logger.info("Available job types are 'permanent', 'contract', and 'temporary'.")
            sys.exit(1)
        
    def set_work_type(self, work_type: str):
        """The work pattern in colloquial terms.
        Accepted values are 'ft' and 'pt', equating to 'full-time' and 'part-time' respectively.

        Args:
            work_type (str): Type of working pattern.
        """
        
        if work_type is None:
            return
        elif work_type.lower() == "ft":
            self._full_time_hours = True
        elif work_type.lower() == "pt":
            self._part_time_hours = True
        else:
            logger.info("Work type must be either 'ft' or 'pt', denoting either full time or part-time working hours.")
            sys.exit(1)  
        
    
    def _build_url(self):
        """Used internally to build the full URL with the required criteria that is sent to the Reed API in order to return particular results.

        Returns:
            str: The full URL containing the various criteria that has been set with the various functions.
        """
        
        url = self._SEARCH_URL
        
        
        if self._search_keyterms is None:
            logger.debug("No search keyterms are set.")
        elif isinstance(self._search_keyterms, str):
            sanitised_kw = self._search_keyterms.replace(" ", "+")
            url += f"&Keywords={sanitised_kw}"
        else:
            url += f"&Keywords="
            for keyword in self._search_keyterms:
                sanitised_kw = keyword.replace(" ", "+")
                keyword.replace
                url += f"{sanitised_kw}%20"
  
        if self._location is None:
            logger.debug("No location set.")
        else:
            logger.debug("Location set to {}", self._location)
            url += f"&Location={self._location}"
        
        if self._maximum_salary > 0:
            logger.debug("Maximum salary set to {}", self._maximum_salary)
            url += f"&maximumSalary={self._maximum_salary}"
        
        elif self._minimum_salary > 0:
            logger.debug("Minimum salary set to {}", self._minimum_salary)
            url += f"&minimumSalary={self._minimum_salary}"
        
        if self._result_amount > 0:
            logger.debug("Results to display set to {}", self._result_amount)
            url += f"&resultsToTake={self._result_amount}"
        
        if self._permanent is not None:
            url += f"&permanent={self._permanent}"
            
        elif self._contract is not None:
            url += f"&contract={self._permanent}"
            
        elif self._temporary is not None:
            url += f"&temp={self._temporary}"
        
        if self._full_time_hours is not None:
            url += f"&fullTime={self._full_time_hours}"
        elif self._part_time_hours is not None:
            url += f"&partTime={self._part_time_hours}"
        
        if self._graduate_suitable is not None:
            url += f"&graduate={self._graduate_suitable}"
        
        if self._employer_direct_post is not None:
            url += f"&postedByDirectEmployer={self._employer_direct_post}"
        elif self._recruitment_agency_post is not None:
            url += f"&postedByRecruitmentAgency={self._recruitment_agency_post}"
        
        if self._employer_id is not None:
            url += f"&employerId={self._employer_id}"
        
        if self._employer_profile_id is not None:
            url += f"&employerProfileId={self._employer_profile_id}"
                    
        logger.debug("Built url: {}", url)
        return url
     
    def search(self):
        """Conduct a search against the Reed API, it is recommend to use the various 'set_<attribute>' functions prior
        to this, in order to filter the results that are returned.

        Raises:
            requests.HTTPError: If there is an error with the returned response from the API, this will be raised.
        """
        
        URL = self._build_url()
        try:
            resp = self._session.get(URL)
            resp.raise_for_status()
            self.results = resp.json()['results']
            self._total_results = resp.json()['totalResults']
            
            return self.results
        
        except requests.HTTPError as err:
            logger.info("There was an error performing the request: {}", err)
            raise requests.HTTPError
            
    def get_total_results(self):
        """After conducting a search, you can get the total number of results for particular criteria. 
        This is typically useful when viewing the total number of results from particular key term combinations in a certain location.

        Returns:
            int: Number of results for the most recently searched criteria.
        """
        
        if len(self.results) == 0:
            logger.info("You must conduct a search with results before retrieving the total.")
            sys.exit(1)
        else:
            return self._total_results