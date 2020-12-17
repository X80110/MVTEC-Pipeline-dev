# Data pipeline
Deploy to Heroku 
```
$ git:remote -a r-pipeline
$ git add .
$ git commit -am "make it better"
$ git push heroku main
$ heroku buildpacks:add https://github.com/virtualstaticvoid/heroku-buildpack-r.git
```
