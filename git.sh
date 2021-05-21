#!/bin/bash
date=`date -d "2 second" +"%Y-%m-%d %H:%M.%S"`
git add .
git commit -m "$date"
git push -u origin master
