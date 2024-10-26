#!/bin/bash

mongodump --host localhost
rm -rf dump/admin
zip -r dump.zip dump
rm -rf dump
