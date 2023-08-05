from pyjob.search import Search
import pytest


search = Search()

def test_api_key_set():
    assert search._API_KEY != ""

def test_api_key_error(monkeypatch):
    
    monkeypatch.delenv("REED_API_KEY")
    with pytest.raises(SystemExit):
        new_search = Search()   
                       
        
def test_default_location_distance():

    search.set_location_distance(-50) # Default of 10 should be used
    assert search._distance_from_location == 10

def test_set_location():
    
    search.set_location("London")
    
    assert search._location == "London"

def test_keyterms_set():
    
    terms = ['software engineer', 'devops', 'SRE']
    search.set_keyterms(terms)
    
    assert search._search_keyterms == terms

def test_keyterms_errors():
    
    terms = ''

    with pytest.raises(SystemExit):
        search.set_keyterms(terms)

def test_invalid_salary():
    
    min_salary_invalid = -50000
    max_salary_invalid = -90000
    
    with pytest.raises(SystemExit):
        search.set_salary_range(min=min_salary_invalid, max=0)
    
    with pytest.raises(SystemExit):
        search.set_salary_range(min=0, max=max_salary_invalid)
        
def test_invalid_job_type():
    
    invalid_type = "infinite_salary_type"
    
    with pytest.raises(SystemExit):
        search.set_job_type(invalid_type)

def test_successful_job_type():
    
    valid_type = "permanent"
    another_valid_type = "contract"
    
    search.set_job_type(valid_type)
    assert search._permanent ==  True
    
    search.set_job_type(another_valid_type)
    assert search._contract == True

def test_job_poster():
    
    poster_type = "recruiter"
    
    search.set_posted_by(poster_type)
    
    assert search._recruitment_agency_post == True
    
def test_invalid_job_poster():
    
    invalid_poster_type = "myself"
    
    with pytest.raises(SystemExit):
        search.set_posted_by(invalid_poster_type)

def test_graduate_roles():

    search.set_graduate_roles(True)
    
    assert search._graduate_suitable == True