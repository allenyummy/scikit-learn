# K nearest neighbors (KNN)
## Run program without grid search

It's enough to directly run the script of `run_knn.sh`, which delivers lot of flags to run with the `knn.py`.

```
$ bash run_knn.sh

#!/bin/bash
data_dir=../data/         ## dir where data are
train_valid_file=Data_train_validation_2019-1126.xlsx   ## file of training set and validation set
test_file=Data_test_2019-1126.xlsx                      ## file of test set
feature_in='A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 A15 A16 A17'    ## features used for knn model
output_col='Type'      ## output for knn model
is_shuffle=True        ## whether train_valid_file is shuffle 
k_fold=1               ## 1 means no k fold validaiton. >1 means k fold validation. 
n_neighbors=3          ## knn param.
weights=uniform        ## knn param.
power_param=2          ## knn param.
output_dir=output/${k_fold}-fold_n-${n_neighbors}_${weights}_p-${power_param}  ## dir where results are 

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
```

Parsing the `knn.py` for details, and `knn.ipynb` is the same code as `knn.py` but jupyter version. More details can be checked in the `knn.ipynb`.
* Import Library
* DataReader Class: functions of reading train_valid_file and test_file w/ or w/o k_fold validation.
* Model Class: functions of knn model setting, training model, evaluating metrics and predicting.
* Func. of no_k_fold, reponsible for reading data, training model, evaluating model, predicting, and reporting results without k fold validation (K=1).
* Func. of k_fold_validaiton, reponsible for reading data, training model, evaluating model, predicting, and reporting results with k fold validation.
* Func. of configuration for recording experimental setting.
* Func. of main, reponsible for taking appropriate actions from the flags which is set in `run_knn.sh`.

---
## Run program with grid search with k fold validation
esp. for n_neighbors, weights, power_param of knn model.
All details are in `grid_search.ipynb`. It also supports the plot function by contourf of matplotlib.