# **scikit-learn-demo**
This is a demo of multi-class classification using K nearest neighbors (KNN) and support vector classification (SVC) from scikit-learn 0.21.3.

The released github code can be divided into four parts, such as Docker Environment, Open Jupyter, KNN code, SVC code.

---
# Build the Environment
It's easy and convinent to get the entire environment without any efforts on your own. What you need to do is to build up the docker image in the local pc and run the docker image. 

There are two ways to build up the docker image in the local pc. First, by `DockerFile` which is in `env/` directory. Second, by pulling image, called `allenyummy/sklearn-jupyter:19.11.2`, from docker hub. I highly recommended the second way if you want to skip the process of building up. If you want to check what packages are established, check `env/DockerFile` and `requirements.txt`. 
* Method 1: build up docker image via DockerFile in the local directory. It has to enter in the directory where DockerFile is, and run it with custom image name.

```
$ cd env/
$ docker build . -t allenyummy/sklearn-jupyter:19.11.2
```  

* Method 2: pull the docker image from docker hub, which is highly recommended. 

```
$ docker pull allenyummy/sklearn-jupyter:19.11.2
```


Check image by the command `$ docker images`, and you'll see the custom image name you have build or `allenyummy/sklearn-jupyter:19.11.2`. If the image doesn't show up, please turn back to re-build the image.

Now, you can run the image, and get the whole word. All you need yo change is the directory `{usr}` you want to mount with the container. If you want to check the flag options, go https://docs.docker.com/engine/reference/run/.

```
$ docker run --name sklearn-knn -t -i -p 8886:8886 --rm -v /home/{usr}/:/workspace allenyummy/sklearn-jupyter:19.11.2
```

Now, the container is running. Check with `$ docker ps -a`.

---
# Git Clone Code and Open Jupyter Notebook
Git clone the github code to the directory you mount with, and open jupyter IDE. Jupyter IDE is not necessary for this project.

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
# K Nearest Neighbor (KNN)
Please enter knn directory and check with another `README.md`.


---
# Support Vector Classification (SVC)
Please enter svc directory and check with another `README.md`.
