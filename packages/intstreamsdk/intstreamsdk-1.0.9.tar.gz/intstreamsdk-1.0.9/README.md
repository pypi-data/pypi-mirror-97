# intstreamsdk

# installation
`pip install instreamjob`

# Job
Jobs run on instream to pull data from external sources and input
that data into instreams database.  Typically
## quickstart
create a zip file with 2 files
1. requirements.txt
    1. contains the pip requirements to install
2. create ```job.py``` file  
    1. example at `/demojob/job.py`
3. run
    ```bash
    export JOB_USERNAME=xxx
    export JOB_PASSWORD=xxx
    export JOB_SERVER_URL=http://localhost:8080/
    python job.py arg1=true arg2=false file=test
    ```
