#! /bin/bash

user=$1;
problem=$2;
filename=${problem}_${user};
file=${filename}.py;

for i in 0 1 2 3 4 5 6 7 8 9
do
    { /bin/mytime python3 /lidi_files/prog/${file} < /lidi_files/testcases/${problem}_${i} > /lidi_files/out/out_${filename}_${i}; } 2>> /lidi_files/out/time;
    errors[$i]=$?;
done;

echo ${errors[*]} > /lidi_files/out/errors;