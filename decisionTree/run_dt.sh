#!/bin/bash
data_dir=../data/
train_valid_file=Data_train_validation_2019-1126.xlsx
test_file=Data_test_2019-1126.xlsx
feature_in='A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 A15 A16 A17'
output_col='Type'
is_shuffle=True
k_fold=1
criterion=gini

output_dir=output_best/${k_fold}-fold_${criterion}

python dt.py \
  --data_dir $data_dir \
  --train_valid_file $train_valid_file \
  --test_file $test_file \
  --output_dir $output_dir \
  --feature_in $feature_in \
  --output_col $output_col \
  --is_shuffle $is_shuffle \
  --k_fold $k_fold \
  --criterion $criterion

