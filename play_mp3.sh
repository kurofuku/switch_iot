#!/bin/bash

ORIG_IFS=${IFS}
IFS=$'\n'

dir=/home/pi/chinese_lesson/

pkill mpg321

file_count=$(find ${dir} -name *.mp3 | wc -l)
index=`expr ${RANDOM} % ${file_count}`

mpg321 "$(find ${dir} -name *.mp3 | sed -n "${index},${index}p")" &

IFS=${ORIG_IFS}


