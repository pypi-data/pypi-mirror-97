from pyjob.search import Search
from pyjob.details import Details
import click
import sys
import os

@click.group()
def cli():
    pass

@cli.command()
@click.option('--term', '-t', required=True, type=str, multiple=True, help='One or more key terms to use for the search, quote the string if using spaces.')
@click.option('--location', '-l', default=None, type=str, help='Location of the job search, e.g. London.')
@click.option('--max-results', '-r', default=100, type=int, help='The maximum number of results to return for the search.')
@click.option('--max-salary', '-max', default=0, type=int, help="Maximum salary for the job search.")
@click.option('--min-salary', '-min', default=0, type=int, help='Minimum salary you are willing to accept for the search.')
@click.option('--distance', '-d', default=10, type=int, help='Distance, in miles, from the specified location to include jobs from.')
@click.option('--posted-by', '-p', default=None, type=str, help='Who the job advert was posted by, either "recruiter" or "employer".')
@click.option('--job-type', '-j', default=None, type=str, help="Job type for the search, e.g. contract.")
@click.option('--work-type', '-w', default=None, type=str, help='Working pattern shorthand, e.g. "ft" means full-time.')
@click.option('--graduate', default=False, is_flag=True, help='Whether jobs shown are suitable for graduates.')
@click.option('--extended', default=False, is_flag=True, help='Get the details of the job to provide an extended description.')
@click.option('--debug', default=False, is_flag=True, help="Set debug mode on, equivalent to 'debug' logging level.")
def search(term, location, max_results, max_salary, min_salary, distance, posted_by, job_type, work_type, graduate, extended, debug):
    
    s = None
    if debug:
        os.environ['PYJOB_LEVEL'] = "DEBUG"
        
    s = Search()
    
    search_terms = list(term)
    s.set_keyterms(search_terms)
    s.set_location(location)
    s.set_max_results(max_results)
    s.set_salary_range(min=min_salary, max=max_salary)
    s.set_location_distance(distance)
    s.set_posted_by(posted_by)
    s.set_job_type(job_type)
    s.set_work_type(work_type)
    
    if graduate:
        click.echo("Showing jobs that are graduate suitable.")
        s.set_graduate_roles(graduate)
    

    results = s.search()
    
    if extended:
        d = Details()
        click.echo("Retrieving extended descriptions...")
        extended_desc = d.get_details(results)

        for item, ext_desc in zip(results,extended_desc):
            item.update({"extendedDescription": ext_desc})

        
    _pretty_output(results, extended)        

def _pretty_output(job_search_results, show_extended):

    for job in job_search_results:
        job_text = f"""
Title: {job['jobTitle']}
Company: {job['employerName']}
Location: {job['locationName']}
Minimum Salary: {job['minimumSalary']}
Maximum Salary: {job['maximumSalary']}
Job Posted: {job['date']}
Job Expiry: {job['expirationDate']}
URL: {job['jobUrl']}
Total Applicants: {job['applications']}"""

        if show_extended:
            job_text += f"""
Description: {job['extendedDescription']}"""
        else:
            job_text += f"""
Description: {job['jobDescription']}"""    
    
        click.echo(click.style(job_text, bold=True, fg='blue'))