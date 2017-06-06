# If solution was better than the previous, move solution to subdir
# in which the best output is kept. Otherwise delete the output files.
#
# Call the program as 'bash * username task is_better'


move_to_best=$CG_FILES_UPLOADED/$1/$2/best_out/;
move_to_last=$CG_FILES_UPLOADED/$1/$2/last_out/;
mkdir -p $move_to_best;
mkdir -p $move_to_last;

move_from=$CG_FILES_UPLOADED/$1/$2/;

for i in 0 1 2 3 4 5 6 7 8 9
do
	if [ $3 -eq 1 ]
	then
		cp $move_from/out_${2}_${1}_${i} $move_to_best;
	fi

	mv $move_from/out_${2}_${1}_${i} $move_to_last;
done
