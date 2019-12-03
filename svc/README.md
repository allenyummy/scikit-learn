# Support Vector Classification (SVC)
## Run program without grid search

It's enough to directly run the script of `run_svc.sh`, which delivers lot of flags to run with the `svc.py`.

```
$ bash run_svc.sh

#!/bin/bash
data_dir=../data/         ## dir where data are
train_valid_file=Data_train_validation_2019-1126.xlsx   ## file of training set and validation set
test_file=Data_test_2019-1126.xlsx                      ## file of test set
feature_in='A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 A15 A16 A17'    ## features used for svc model
output_col='Type'      ## output for svc model
is_shuffle=True        ## whether train_valid_file is shuffle 
k_fold=1               ## 1 means no k fold validaiton. >1 means k fold validation. 
c=8.0                  ## svc param.
gamma=0.03125          ## svc param.
output_dir=output/${k_fold}-fold_n-${n_neighbors}_${weights}_p-${power_param}  ## dir where results are 

output_dir=output_best/${k_fold}-fold_c-${c}_g-${gamma}

python svc.py \
  --data_dir $data_dir \
  --train_valid_file $train_valid_file \
  --test_file $test_file \
  --output_dir $output_dir \
  --feature_in $feature_in \
  --output_col $output_col \
  --is_shuffle $is_shuffle \
  --k_fold $k_fold \
  --c $c \
  --gamma $gamma 
```

Parsing the `svc.py` for details.
* Import Library
* DataReader Class, functions of reading train_valid_file and test_file w/ or w/o k_fold validation.
* KNN Class, functions of svc model setting, training svc model, evaluating metrics and predicting.
* Func. of no_k_fold, reponsible for reading data, training knn model, evaluating model, predicting, and reporting results without k fold validation (K=1).
* Func. of k_fold_validaiton, reponsible for reading data, training knn model, evaluating model, predicting, and reporting results with k fold validation. 
* Func. of configuration for args, reponsible for recording the args.
* Func. of configuration for grid_search.ipynb or any programs, reponsible for recording the args.
* Func. of main, reponsible for taking appropriaate actions from the flags which is set in `run_svc.sh`.

---
## Run program with grid search with k fold validation
esp. for c, gamma of svc model.
All details are in `grid_search.ipynb`. It also supports the plot function by contourf of matplotlib.