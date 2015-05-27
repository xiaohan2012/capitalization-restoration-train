modes=(upper lower cap)
feature_groups=(1 2 3 4 5 6 1+2 1+3 1+4 1+5 1+6 1+2+3+4+5+6)
size=30000

DATA_ROOT="/cs/taatto/home/hxiao/capitalization-recovery/corpus"

output_path="feature_experiments_commands.sh"

if [ -e $output_path ]; then
	rm $output_path
fi

for mode in "${modes[@]}"
do
	echo "mode: $mode"
	for features in "${feature_groups[@]}"
	do
		echo "features: $features"
		echo "./run_feature_experiment.sh $features  $mode $DATA_ROOT/news_title_$mode/$size/train.txt $DATA_ROOT/news_title_$mode/$size/test.txt" >> $output_path
	done
done
