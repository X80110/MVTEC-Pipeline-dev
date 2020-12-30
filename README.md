# Data pipeline
*Group-3*
The code takes the Covid-19 dataset from [Our World in Data](http://ourworldindata.org) and process the statistical models, the output is adapted for its use in visualizations and it is uploaded to an AWS S3 bucket to make it available to web browsers. 

The pipeline core runs mostly in `python`, the statistical models which are made in `R` run in a subprocess terminal and interact with the pipeline through the standard streams of the system.

The code is deployed on a free Heroku dyno properly set to be able to run both `python` and `R`code.
Heroku has default buildpacks for `python` but none to run `R` code. The set up uses a third-party buildpack for R in Heroku which is [available here.](https://github.com/virtualstaticvoid/heroku-buildpack-r) 

## Pipeline structure
  1. Main file (`app.py`)
   Orchestrate the whole process. It calls the system runtime to process the statistical models (`.R` files) and connects with all the processes which interact with S3 storage interface and email notifications. 
    - If succeed, the output is stored and uploaded to an AWS S3 bucket.
    - If files could not be read, status emails is sent.
    - If Heroku fails to run code, status emails is sent.
    - If an error occurs while uploading to S3, status emails is sent.

  2. Upload desired data to AWS S3 (`upload_to_s3.py`)
  3. Check file and output content into notification (`check_uploaded_file`)
  4. Send email notification with success/error status (`notify.py`)
  5. Set schedule to run daily

### Deploy to Heroku 
Using Heroku CLI to set the repository and push it. 
```
$ git:remote -a r-pipeline
$ git add .
$ git commit -am "deploy"
$ git push heroku main
```
Installing R runtime with buildpacks.
```
$ heroku buildpacks:add https://github.com/virtualstaticvoid/heroku-buildpack-r.git
```
### Installing R packages
[Docs](https://github.com/virtualstaticvoid/heroku-buildpack-r)
When the r buildpack is deployed, init.R file will be executed so we use it to install the libraries. 

```
### Example R code to install packages if not already installed


my_packages = c("tidyverse", "readxl", "countrycode","scales")

install_if_missing = function(p) {
  if (p %in% rownames(installed.packages()) == FALSE) {
    install.packages(p)
  }
}

invisible(sapply(my_packages, install_if_missing))
```

## Pipeline structure
  1. Run R scripts (`read-scripts.py`)
  2. Load output in Python
  3. Upload desired data to AWS S3 (`app.py`)
  4. Send email notification with success/error status (`notify.py`)
  5. Set schedule to run daily

