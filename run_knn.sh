#!/bin/bash
data_dir=data/
train_valid_file=Data_train_validation_2019-1126.xlsx
test_file=Data_test_2019-1126.xlsx
feature_in='A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 A15 A16 A17'
output_col='Type'
is_shuffle=True
k_fold=1
weights=distance
n_neighbors=5
power_param=1
output_dir=output_best/${k_fold}-fold_${weights}_n-${n_neighbors}_p-${power_param}

python knn.py \
  --data_dir $data_dir \
  --train_valid_file $train_valid_file \
  --test_file $test_file \
  --output_dir $output_dir \
  --feature_in $feature_in \
  --output_col $output_col \
  --is_shuffle $is_shuffle \
  --k_fold $k_fold \
  --n_neighbors $n_neighbors \
  --weights $weights \
  --power_param $power_param

