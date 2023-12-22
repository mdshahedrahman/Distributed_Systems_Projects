#!/bin/bash

SHARED_DIRECTORY="shared_directory"
if [ -d "$SHARED_DIRECTORY" ]
then
	# Clean all the old files
	rm -rf ${SHARED_DIRECTORY}/*
else
	mkdir $SHARED_DIRECTORY
fi

# Generate new files
for i in {1..10}
do
	echo '{"filename": "file_'${i}'.json", "counter": 0, "status": "unlocked"}' > ${SHARED_DIRECTORY}/file_${i}.json
done
