# sklearn-knn-jupyter

### Build the Environment
-- Step 1: build up docker image --

    Method 1: build up docker image via DockerFile in the local dir
```
$ cd env/
$ docker build . -t allenyummy/sklearn-knn-jupyter:19.11.3
```

    Method 2: pull the docker image from docker hub 
```
$ docker pull allenyummy/sklearn-knn-jupyter:19.11.3
```

-- Step 2: run image --
```
$ docker run --name sklearn-knn -t -i -p 8886:8886 --rm -v /home/{usr}/:/workspace allenyummy/sklearn-knn-jupyter:19.11.3
```

### Run program
```
$ bash run_knn.sh

    #!/bin/bash
    data_dir=data/
    train_valid_file=Data_train_validation_2019-1126.xlsx
    test_file=Data_test_2019-1126.xlsx
    feature_in='A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 A15 A16 A17'
    output_col='Type'
    is_shuffle=True
    k_fold=1
    n_neighbors=3
    weights=uniform
    power_param=2
    output_dir=output/${k_fold}-fold_n-${n_neighbors}_${weights}_p-${power_param}

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

### Open jupyter IDE
-- Step 1: set up jupyter passwd --
```
$ jupyter notebook --generate-config
$ jupyter notebook password
```
-- Step 2: run jupyter lab --
```
$ jupyter lab --ip 0.0.0.0 --port 8886 --allow-root
```
-- Step 3: open jupyter ide --

https://localhost:8886
or
https://ip:8886


### Grid Search for best hyperparameters of KNN model
esp. for n_neighbors, weights, power_param

run grid_search.ipynb


