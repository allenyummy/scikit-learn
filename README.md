# **sklearn-jupyter**
This is a demo of multi-class classification using K nearest neighbors (KNN) and support vector classification (SVC) rom scikit-learn 0.21.3.

The released github code can be divided into three parts, such as Docker Environment, KNN code, Grid search code.

---
# Build the Environment
It's easy and convinent to get the entire environment without any efforts on your own. What you need to do is to build up the docker image in the local pc and run the docker image. 

There are two ways to build up the docker image in the local pc. First, by `DockerFile` which is in `env/` dir. Second, by pulling image, called `allenyummy/sklearn-jupyter:19.11.2`, from docker hub. I highly recommended the second way if you want to skip the process of building up. If you want to check what packages are established, check `env/DockerFile` and `requirements.txt`. 
* Method 1: build up docker image via DockerFile in the local dir. It has to enter in the dir where DockerFile is, and run it with custom image name.

```
$ cd env/
$ docker build . -t allenyummy/sklearn-jupyter:19.11.2
```  

* Method 2: pull the docker image from docker hub, which is highly recommended. 

```
$ docker pull allenyummy/sklearn-jupyter:19.11.2
```


Check image by the command `$ docker images`, and you'll see the custom image name you have build or `allenyummy/sklearn-jupyter:19.11.2`. If the image doesn't show up, please turn back to re-build the image.

Now, you can run the image, and get the whole word. All you need yo change is the dir `{usr}` you want to mount with the container. If you want to check the flag options, go https://docs.docker.com/engine/reference/run/.

```
$ docker run --name sklearn-knn -t -i -p 8886:8886 --rm -v /home/{usr}/:/workspace allenyummy/sklearn-jupyter:19.11.2
```

Now, the container is running. Check with `$ docker ps -a`.

---
# Git Clone Code and Open Jupyter Notebook
Git clone the github code to the dir you mount with, and open jupyter IDE. Jupyter IDE is not necessary for this project.

1. set up jupyter passwd

```
$ jupyter notebook --generate-config
$ jupyter notebook password
```

2. run jupyter lab

```
$ jupyter lab --ip 0.0.0.0 --port 8886 --allow-root
```

3. open jupyter ide by visiting `https://localhost:8886` or `https://ip:8886`.

---
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
* DataReader Class, functions of reading train_valid_file and test_file w/ or w/o k_fold validation.
* KNN Class, functions of knn model setting, training knn model, evaluating metrics and predicting.
* Func. of no_k_fold, reponsible for reading data, training knn model, evaluating model, predicting, and reporting results without k fold validation (K=1).
* Func. of k_fold_validaiton, reponsible for reading data, training knn model, evaluating model, predicting, and reporting results with k fold validation. 
* Func. of configuration for args, reponsible for recording the args.
* Func. of configuration for grid_search.ipynb or any programs, reponsible for recording the args.
* Func. of main, reponsible for taking appropriaate actions from the flags which is set in `run_knn.sh`.

---
## Run program with grid search with k fold validation
esp. for n_neighbors, weights, power_param of knn model.
All details are in `grid_search.ipynb`. It also supports the plot function by contourf of matplotlib.


