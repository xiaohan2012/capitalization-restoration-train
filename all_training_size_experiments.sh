modes=(upper lower cap)
features=1+2+3+4+5+6
# sizes=(5000 10000 15000 20000 25000 30000)
sizes=(30000)

DATA_ROOT="/cs/taatto/home/hxiao/capitalization-recovery/corpus"

output_path="training_size_experiments_commands.sh"

if [ -e $output_path ]; then
	rm $output_path
fi

for mode in "${modes[@]}"
do
	echo "mode: $mode"
	for size in "${sizes[@]}"
	do
		echo "size: $size"
		echo "./run_training_size_experiment.sh $features  $mode $size $DATA_ROOT/news_title_$mode/$size/train.txt $DATA_ROOT/news_title_$mode/$size/test.txt" >> $output_path
	done
done
