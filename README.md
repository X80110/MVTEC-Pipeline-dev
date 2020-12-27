# Data pipeline
### Deploy to Heroku 
Using Heroku CLI to set the repository and push it. 
```
$ git:remote -a r-pipeline
$ git add .
$ git commit -am "make it better"
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

## Pipeline workflow steps
  1. Run R scripts (`read-scripts.py`)
  2. Load output in Python
  3. Upload desired data to AWS S3 (`app.py`)
  4. Send email notification with success/error status (`notify.py`)
  5. Set schedule to run daily

