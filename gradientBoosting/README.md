# Gradient Boosting (GB)
## Run program without grid search

It's enough to directly run the script of `run_gb.sh`, which delivers lot of flags to run with the `gb.py`.

```
$ bash run_gb.sh

#!/bin/bash
data_dir=../data/
train_valid_file=Data_train_validation_2019-1126.xlsx
test_file=Data_test_2019-1126.xlsx
feature_in='A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 A15 A16 A17'
output_col='Type'
is_shuffle=True
k_fold=1
learning_rate=0.7
n_estimators=200
output_dir=output_best/${k_fold}-fold_lr-${learning_rate}_n-${n_estimators}

python gb.py \
  --data_dir $data_dir \
  --train_valid_file $train_valid_file \
  --test_file $test_file \
  --output_dir $output_dir \
  --feature_in $feature_in \
  --output_col $output_col \
  --is_shuffle $is_shuffle \
  --k_fold $k_fold \
  --learning_rate $learning_rate \
  --n_estimators $n_estimators 

```

Parsing the `gb.py` for details.
* Import Library
* DataReader Class: functions of reading train_valid_file and test_file w/ or w/o k_fold validation.
* Model Class: functions of model setting, training model, evaluating metrics and predicting.
* Func. of no_k_fold, reponsible for reading data, training model, evaluating model, predicting, and reporting results without k fold validation (K=1).
* Func. of k_fold_validaiton, reponsible for reading data, training model, evaluating model, predicting, and reporting results with k fold validation. 
* Func. of configuration for recording experimental setting.
* Func. of main, reponsible for taking appropriate actions from the flags which is set in `run_gb.sh`.

---
## Run program with grid search with k fold validation
esp. for learning rate and n estimators of gb model.
All details are in `grid_search.ipynb`. It also supports the plot function by contourf of matplotlib.