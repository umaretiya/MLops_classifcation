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
docker run -p 5000:5000 -e PORT=5000 f3322f5e3b00
```
python -c 'import secrets; print(secrets.token_hex())'

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

### Final ramarks: ML Clssification projects
- docker images - banking
- get repo - MLops_classifcation
- heroku app - ml-classify
- local dir - MLops_classifcation
- Author - Keshav
- Sector - Banking
- Use case - Default of Credit Card clients of Bank
- Datasets - archive.ics.uci.edu/ml/datasets
- Final Data - kaggle - default-of-credit-card-clients-dataset
- labels 0 or 1 - 1 for default and 0 for not default
- Model - XGBClassifier
- Accuracy - 81 %
- Framework - Flask-Python
- environment - conda
