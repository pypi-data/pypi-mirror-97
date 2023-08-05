# PyJob

PyJob is an abstraction around the [Reed](https://reed.co.uk) API for job searching.

After providing an API key you can interact with the API for finding jobs that have been posted to Reed, either by companies or agencies, as well as the various other functionality that they provide.

You can:
* **Search** for jobs
* Find **details** of particular jobs using their IDs, this is used to grab an *extended* description of the job.

## Installation

    pip install pyjob-jdockerty

You will also need to register for a [Reed API](https://www.reed.co.uk/developers/jobseeker) key and export this, e.g.

    export REED_API_KEY=<your_key>

## CLI Usage

A simple search can be conducted using the command

    pyjob search --term "software engineer" --max-results 3

This displays results for jobs which match the term `software engineer` according to Reed's API, displaying the first 3 results to you.

To view available flags, use the `--help` flag

    pyjob search --help

This provides a greater list of options to pass into the CLI.

## TODO

* ~~Finish **Search** class for API interaction.~~
* Add CI pipeline.
* Add custom exceptions for raising errors, currently just exiting on error and printing a log message with `sys.exit`. Instead will raise exception and move the current logging message to the raised exception.
* ~~Build out a **Detail** class for finding more information around a job with the ID. [Response is similar, just with extended description, using this for now.~~
* ~~Create CLI wrapper for this API for job searches on the command line.~~
