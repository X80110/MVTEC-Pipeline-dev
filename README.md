# Assignment 7 - Cloud ETL

This assignment brings together some basic elements for running an automated data pipeline in the cloud. The goal is to read a remote data source, transform it, and push the resulting data to our own AWS S3 bucket. This forms the basis for a simple ETL process:

- **Extract** (read remote data)
- **Transform** (transform data for our uses)
- **Load** (upload transformed data)

**Part 1** will help you get your AWS credentials set up

**Part 2** will get your project deployed on Heroku

**Part 3** is about bringing these two together to implement a basic, cloud-based, ETL data pipeline

**Part 4** is an extra data wrangling / transformation challenge if you want some more programming practice

## Part 1 - AWS S3 uploading example

*[AWS S3](https://aws.amazon.com/s3/)* is a cloud service for storing and hosting files. It is commonly used in the web world for hosting static files of all kinds, including images, JavaScript, data files, etc.

Uploading to AWS S3 can be done programmatically with libraries in most languages. The Python library for AWS is called `boto3`.

This part of the assignment is just to show you a basic example of how to upload to S3, and set up your AWS credentials so you can do it yourself. 

1. Set up your AWS credentials as described in the *Notes* section below (ask me for credentials if you don't have them)
2. Update the value of `folder` in the `config.py` file (this will set the target upload folder)
3. Run `part1.py`

### Extra challenge

If you want a short programming challenge here you can try to rewrite `part1.py` to use the [boto3 library's put_object function](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object) directly to upload a test file to S3. Use the S3 bucket named in the `config.py` file. Upload the file to a folder with your name.

## Part 2 - Heroku hello world

*[Heroku](https://www.heroku.com/)* is a cloud platform offering various cloud hosting services. It's designed to be very simple and easy to use and offers a free tier with some great functionality. In this project we are going to use it to run a Python app in the cloud. This part of the assignment will help you deploy a simple app to get you familiar with the platform and the process of deploying.

### Steps

1. Create a [Heroku](https://www.heroku.com/) account and download the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) if you haven't already
2. Create a new Heroku app
3. Deploy the app to Heroku. You should see the instructions for this in the Heroku dashboard:
    - Add Heroku as a remote repo
    - Push to that remote repo
4. Enable the dyno from the *Configure Dynos* page (linked from the *Overvie*w page of your app)
5. Your dyno should now be started and running. You can see any logs coming out of the dyno by clicking *More → View Logs* from your Heroku dashboard. If running, the app should be logging "log test" once every minute, and this should be visible in the logs.
6. Make a change (for example, to the log message) and redeploy the app:
    - commit your changes to git
    - push to the Heroku remote repo
7. Watch the logs for information about the deploy. Once built and running, the test log message should be updated.

**Note:** We are using the *Procfile* to tell Heroku which file to run (`app.py` in this case). See the notes below for more info.

## Part 3 - Basic pipeline

This part will help you set up the foundations for a basic data pipeline. We will ignore the *transform* step for now and just fetch some data and upload it to S3.

1. Modify your `app.py` to retrieve the up-to-date covid data set from [https://coviddata.github.io/coviddata/v1/countries/stats.json](https://coviddata.github.io/coviddata/v1/countries/stats.json) 
    - you can use the *requests* library (as we used in previous assignments) or *urllib* to fetch the data from the URL
2. Upload the data to S3 using the `upload_to_s3` function
    - You'll need to set up your AWS credentials on your Heroku app (see the *credentials* section in the notes below)
    - As in part 1, if you wan an extra programming challenge you can upload using *boto3*'s `put_object` function directly
3. Set this code to run once per day using `time.sleep`

**Note:** When using extra third-party libraries (e.g. requests, pandas, etc) you'll need to tell Heroku about them. See the *Python library requirements* section in the Notes below.

Remember, you can run your code locally as normal to test before deploying to Heroku.

## Part 4 - Further challenge

With a basic pipeline running we can transform the data to fit our app's requirements before uploading. This might include steps like cleaning messy data, merging multiple datasets, calculating new fields, running models, removing unnecessary data, etc.

For an extra programming challenge try filtering out some of the data. For example if we didn't need cumulative data we could drop that from the dataset.

For a harder challenge try combining this data set with another dataset, for example the *InfoPaisosExtra* dataset linked in Slack, and upload the result to S3.

Feel free to use pandas or any other approach you like here.

## Notes

### AWS S3 uploading

#### Credentials

AWS API requires credentials for authentication. The boto3 library can read your AWS credentials in one of two ways:

- from the file located at `~/.aws/credentials` (`~` is your user's home directory)
- from environment variables. e.g. `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

**On our local machine** we can use the first approach. 

1. Create a file `~/.aws/credentials` with the following contents:

    ```python
    [default]
    aws_access_key_id=<access key id here>
    aws_secret_access_key=<secret access key here>
    ```

**On Heroku** we can use environment variables to give boto3 access to our credentials:

1. Go to the *settings* tab on your Heroku app
2. In the *Config Vars* section on this page add your credentials under the following keys:
    - `AWS_ACCESS_KEY_ID`
    - `AWS_SECRET_ACCESS_KEY`

### Heroku

The following sections are a few notes on Heroku specific features relevant to this project.

#### Python library requirements

Heroku must be told about [third-party library requirements](https://devcenter.heroku.com/articles/python-pip) in the *requirements.txt* file in the format:

```python
<libraryname>=<version>
```

See the existing *requirements.txt* file for an example. Every time you push to Heroku it will check for new requirements and install them when necessary.

If you need to check which package versions you are using you can use the following commands to see all your installed packages and versions. For conda:

```python
conda list --export
```

And for pip:

```python
pip freeze
```

#### Restarting dynos

Heroku will automatically restart your dynos when you push new code. However, if your dyno crashes because of an error you will need to force a restart. You can do this using *More → Restart all dynos* in the dashboard or with the CLI command `heroku restart`

#### Procfile

This file lives in your app directory and tells Heroku how to run your app. In this app we're just specifying a single command, which is `python app.py` to run the main Python file. This will allow you to stop/start this process in Heroku's web dashboard.