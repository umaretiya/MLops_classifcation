# MLops_classifcation


[repo link]("https://github.com/umaretiya/MLops_classifcation")

Create first flask classifciation  machine learning project
```{link of repo}
[repo link](https://github.com/umaretiya/MLops_classifcation.git)
```

XGBoost model for credit card default prediction : ML projects
### Buld docker image
- Image name banking:latest
```
docker build -t <image name>:<tag name> .
```
> Note: imagename fro docker must be lowercase

To list docker image
```
docker images
```
Run docker image
```
docker run -p 5000:5000 -e PORT=5000 d033f59ea12f
```

To check runnig container in docker
```
docker ps
```

to stop docker container
```
docker stop <container_id> ad6cabc7a281
```
Creating yaml file
```
.github/workflows/main.yaml
```