# API for Netflix Titles

# programs
*  local/netflix.py - original version ran locally
*  local/load.py local program to load Titles from CSV file to Postgres DB hosted in GCP
*  app_engine/main.py Version running in GCP App Engine
*  app_engine/requirements.txt - python libraries

# csv files
* csv_files/netflix_titles.csv.  file containg titles

# Open API Spec
netflix_openapi_spec.yaml

# Approach

Initial API designed using Flask, SQLAlchemy which leveraged SQLite

Once Core API created, I enhanced it to leverage Postgres instance in GCP Cloud SQL.  Locally everything ran fine.

Deployed to GCP App Engine, however had connectivity issues,  original postgres created with public ip address, and my local code worked.
issues with app engine, researched and created a postgres instance with a private ip address.  researched and found that needed Serverless VPC Connector setup to allow App Engine to talk to private Postgres.

Spent a good amount of time coming up to speed on GCP Cloud SQL and App Runtime.  Wanted something functional that required a real database.

## Remaining
* Add abiility to update a specific Title

Working through the GCP tasks took more time than I thought.  It was a good exercise and have a pretty good handle on this.
Next Steps for me are to leverage Unit Testing, CI/CD and leverage API Gateway for Authorization.
