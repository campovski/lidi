#! /bin/bash

user=$1;
problem=$2;
filename=${problem}_${user};

for i in 0 1 2 3 4 5 6 7 8 9
do
    { time mono /lidi_files/prog/${filename}.exe < /lidi_files/testcases/${problem}_${i} > /lidi_files/out/out_${filename}_${i}; } 2>> /lidi_files/out/time;
    errors[$i]=$?;
done;

echo ${errors[*]} > /lidi_files/out/errors;