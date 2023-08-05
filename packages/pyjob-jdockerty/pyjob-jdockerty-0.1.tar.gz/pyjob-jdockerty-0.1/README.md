# PyJob

PyJob is an abstraction around the [Reed](https://reed.co.uk) API for job searching.

After providing an API key you can interact with the API for finding jobs that have been posted to Reed, either by companies or agencies, as well as the various other functionality that they provide.

You can:
* **Search** for jobs
* Find **details** of particular jobs using their IDs, this is used to grab an *extended* description of the job.

## Installation

    pip install pyjob-jdockerty

## TODO

* ~~Finish **Search** class for API interaction.~~
* Add CI pipeline.
* Add custom exceptions for raising errors, currently just exiting on error and printing a log message with `sys.exit`. Instead will raise exception and move the current logging message to the raised exception.
* ~~Build out a **Detail** class for finding more information around a job with the ID. [Response is similar, just with extended description, using this for now.~~
* ~~Create CLI wrapper for this API for job searches on the command line.~~
