parents:
	for i in $(seq 3 9); do ./merge_go.py -d $i -n log -o ../data/freqs/d1_sub_log_0${i}parents.csv ../data/go/d1_subsample/; done

figures:
	for file in ../data/freqs/*; do ./compare_models.py -o figures/$(basename $file '.csv').png -T $(basename $file '.csv') -q $file; done
