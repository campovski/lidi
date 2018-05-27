#! /bin/bash

ts=$(date +%s%N);
$@;
tt=$((($(date +%s%N) - $ts)/100000));
(echo $tt 1>&2);