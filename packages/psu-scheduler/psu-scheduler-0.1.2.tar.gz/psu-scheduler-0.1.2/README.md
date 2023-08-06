# PSU Scheduler

Schedule tasks to run in our AWS Django apps

## Installation/Configuration

Step 1: Add `psu-scheduler` to requirements.txt

Step 2: Add to `INSTALLED_APPS` in `settings.py`

Step 3: Add to urls.py
```
url('scheduler/', include(('psu_scheduler.urls', 'psu_scheduler'), namespace='scheduler')),
```

Step 4: Ensure `HOST_URL` is defined in your AWS settings (as required by psu_base). 
The `HOST_URL` setting can be overridden if needed by a setting named `SCHEDULER_URL`

## Preparing your scheduled task
Your scheduled task must be a view with a defined URL in urls.py. 
You must prefix it with the `@scheduled_job()` decorator, which verifies the job is allowed to run.
```buildoutcfg
# views.py

from psu_scheduler.decorators import scheduled_job


@scheduled_job()
def test_job(request):
    """A test job that does nothing"""
    return HttpResponse('The test job has completed.')
```

Your scheduled job URL must be made public since no user is authenticated when ran on a schedule.
If you define your endpoint URL to include "scheduled/", it will be considered public by convention.
Otherwise, you can make it public in your app's __init__.py file
```buildoutcfg
# __init__.py

# Default settings
_DEFAULTS = {
    # Public URLs
    'MY_APP_PUBLIC_URLS': ['.*/my_test_job', ...],
    
    # Admin Menu Items
    'MY_APP_ADMIN_LINKS': [ ... ]
}
```

## Scheduling Jobs
In the Admin Menu, you'll find a link for "Scheduled Jobs" which takes you to the list 
of jobs defined for your app. At the bottom of list is a button to create a new scheduled 
job record (only available to developers).

The UI for this is very bare-bones.  Once a schedule is created, it cannot be modified, only deleted.  
*More development is needed!*

## Process Overview
1. Define your AWS health check to hit `/scheduler/aws/run` every minute
1. Every minute, AWS calls a Finti endpoint. 
   The Finti endpoint calls back to your app's `/scheduler/run` endpoint to see if any jobs need to run.  
   *(You cannot simply call `/scheduler/run` as your AWS health check endpoint because it results in network errors)*    
     
   *UPDATE:* I accidentally called `/scheduler/run` as the AWS health check endpoint for Laptop Scholarship, and it worked!
   It may now be possible to call it directly and avoid the extra Finti call.
   

1. The `/scheduler/run` endpoint called from Finti will:
   1. Select all job definitions
   1. See if job has been run since the last scheduled time
   1. If it has not been run
      1. Create a JobExecution record
      1. Call the job's URL (GET request) and pass the JobExecution record ID and key
      1. The `@scheduled_job()` decorator verifies the ID and Key, and ensures the job has not already been run
      1. The `@scheduled_job()` decorator updates the status of the JobExecution record
      1. The job runs and returns a normal HttpResponse object
      1. The `@scheduled_job()` decorator updates the status of the JobExecution record again to indicate the job has completed or failed
   1. Return the number of jobs that were run
   