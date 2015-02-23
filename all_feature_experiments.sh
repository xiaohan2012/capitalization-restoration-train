modes=(upper lower cap)
feature_groups=(1 2 3 4 5 6 1+2 1+3 1+4 1+5 1+6 1+2+3+4+5+6)
size=5000
for mode in "${modes[@]}"
do
	echo "mode: $mode"
	for features in "${feature_groups[@]}"
	do
		echo "features: $features"
		./run_feature_experiment.sh $features   corpus/news_title_$mode/$size/train.txt corpus/news_title_$mode/$size/test.txt 
	done
done
