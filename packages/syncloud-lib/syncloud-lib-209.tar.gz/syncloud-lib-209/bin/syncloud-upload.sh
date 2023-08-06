#!/bin/bash -e

if [ -z "$AWS_ACCESS_KEY_ID" ]; then
  echo "AWS_ACCESS_KEY_ID must be set"
  exit 1
fi
if [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
  echo "AWS_SECRET_ACCESS_KEY must be set"
  exit 1
fi
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

app=$1
branch=$2
build_number=$3
FILE_NAME=$4
bucket=apps.syncloud.org

if [ "${branch}" == "master" ] || [ "${branch}" == "stable" ] ; then

  s3cmd put $FILE_NAME s3://${bucket}/apps/$FILE_NAME
  
  if [ "${branch}" == "stable" ]; then
    branch=rc
  fi

  printf ${build_number} > ${app}.version
  s3cmd put ${app}.version s3://${bucket}/releases/${branch}/${app}.version

fi
