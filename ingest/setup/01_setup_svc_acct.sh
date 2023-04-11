#!/bin/bash

SVC_ACCT=fantasy-football-ingest
PROJECT_ID=$(gcloud config get-value project)
REGION=europe-west2
SVC_PRINCIPAL=serviceAccount:${SVC_ACCT}@${PROJECT_ID}.iam.gserviceaccount.com

gsutil ls gs://$BUCKET || gsutil mb -l $REGION gs://$BUCKET
gsutil uniformbucketlevelaccess set on gs://$BUCKET

gcloud iam service-accounts create $SVC_ACCT --display-name "fantasy football ingest"

# make the service account the admin of the bucket
# it can read/write/list/delete etc. on only this bucket
gsutil iam ch ${SVC_PRINCIPAL}:roles/storage.admin gs://$BUCKET

# ability to create/delete partitions etc in BigQuery table
bq --project_id=${PROJECT_ID} query --nouse_legacy_sql \
  "GRANT \`roles/bigquery.dataOwner\` ON SCHEMA fantasy_football_raw TO '$SVC_PRINCIPAL' "

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member ${SVC_PRINCIPAL} \
  --role roles/bigquery.jobUser

# At this point, test running as service account
# download a json key from the console (temporarily)
# either add this to .gcloudignore and .gitignore or put it in a different directory!
# gcloud auth activate-service-account --key-file tempkey.json
# ./ingest_flights.py --bucket $BUCKET --year 2015 --month 03 --debug
# after this, go back to being yourself with gcloud auth login

# Make sure the sevice account can invoke cloud functions
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member ${SVC_PRINCIPAL} \
  --role roles/run.invoker
