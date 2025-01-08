#!/bin/bash

mongoimport --host mongo --db platform --collection channels --type json --file /mongo_seed/channels.json --jsonArray

mongoimport --host mongo --db platform --collection contents --type json --file /mongo_seed/contents.json --jsonArray