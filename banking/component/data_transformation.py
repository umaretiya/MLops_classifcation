from banking.logger import logging
from banking.exception import BankingException
from banking.entity.config_entity import DataTrasformationConfig
from banking.entity.artifact_entity import DataTransformationArtifact,DataIngestionArtifact,DataValidationArtifact
from banking.util.util import read_yaml_file,save_numpy_array_data,save_object,load_data
from banking.constant import *

import os, sys, pandas as pd, numpy as np

from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline 
from sklearn.preprocessing import StandardScaler,OneHotEncoder


class FeatureGenerator(BaseEstimator,TransformerMixin):
    
    def __init__(self, add_bedrooms_per_room=True,
                 total_rooms_ix=3,
                 population_ix=5,
                 households_ix=6,
                 total_bedrooms_ix=4, columns=None):
        try:
            self.columns = columns
            if self.columns is not None:
                total_rooms_ix = self.columns.index(COLUMN_TOTAL_ROOMS)
                population_ix = self.columns.index(COLUMN_POPULATION)
                households_ix = self.columns.index(COLUMN_HOUSEHOLDS)
                total_bedrooms_ix = self.columns.index(COLUMN_TOTAL_BEDROOM)

            self.add_bedrooms_per_room = add_bedrooms_per_room
            self.total_rooms_ix = total_rooms_ix
            self.population_ix = population_ix
            self.households_ix = households_ix
            self.total_bedrooms_ix = total_bedrooms_ix
        except Exception as e:
            raise BankingException(e, sys) from e

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        try:
            room_per_household = X[:, self.total_rooms_ix] / \
                                 X[:, self.households_ix]
            population_per_household = X[:, self.population_ix] / \
                                       X[:, self.households_ix]
            if self.add_bedrooms_per_room:
                bedrooms_per_room = X[:, self.total_bedrooms_ix] / \
                                    X[:, self.total_rooms_ix]
                generated_feature = np.c_[
                    X, room_per_household, population_per_household, bedrooms_per_room]
            else:
                generated_feature = np.c_[
                    X, room_per_household, population_per_household]

            return generated_feature
        except Exception as e:
            raise BankingException(e, sys) from e

class DataTransformation:
    
    def __init__(self, data_transformation_config:DataTrasformationConfig,
                 data_ingestion_artifact:DataIngestionArtifact ,
                 data_validation_artifact:DataValidationArtifact):
        
        try:
            logging.info(f"{'>>' * 30}Data Transformation log started.{'<<' * 30} ")
            self.data_transformation_config= data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            
        except Exception as e:
            raise BankingException(e, sys) from e 
        
    def get_data_transformer_object(self):
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path
            dataset_schema = read_yaml_file(file_path=schema_file_path)
            
            numerical_columns = dataset_schema[NUMERICAL_COLUMN_KEY]
            categorical_columns = dataset_schema[CATEGORICAL_COLUMN_KEY]
            
            num_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("feature_gererator", FeatureGenerator(
                    add_bedrooms_per_room=self.data_transformation_config.add_bedroom_per_room,
                    columns=numerical_columns
                ) ),
                ("scaler",StandardScaler())
            ])
            
            cat_pipeline = Pipeline(steps=[
                ("impute",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler()),
            ])
            
            logging.info(f"Numerical Column: {numerical_columns}")
            logging.info(f"Categorical columns: {categorical_columns}")
            
            preprocessing = ColumnTransformer([
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipeline", cat_pipeline,categorical_columns),
            ])
            return preprocessing
            
        except Exception as e:
            raise BankingException(e, sys) from e 
        
    def initiate_data_transformation(self):
        try:
            logging.info(f"Obtaining preprocessing object.")
            preprocessing_obj =self.get_data_transformer_object()
            
            logging.info(f"Obtainig training adn test file path")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            schema_file_path = self.data_validation_artifact.schema_file_path
            
            logging.info(f"Loading train and test data as pandas Dataframe")
            train_df = load_data(file_path=train_file_path, schema_file_path=schema_file_path)
            test_df = load_data(file_path=test_file_path,schema_file_path=schema_file_path)
            schema = read_yaml_file(file_path=schema_file_path)
            target_column_name = schema[TARGET_COLUMN_KEY]
            
            logging.info(f"Spliting input and target feature from dataframe")
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]            
            
            logging.info(f"Applying preprocessing object on data")
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[input_feature_train_arr, np.array[target_feature_train_df]]
            test_arr = np.c_[input_feature_test_arr, np.array[target_feature_test_df]]
            
            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir
            
            train_file_name = os.path.basename(train_file_path).replace(".csv",".npz")
            test_file_name= os.path.basename(test_file_path).replace(".csv",".npz")
            
            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir,test_file_name)
            
            logging.info(f"Saving transformed traing and testing array")
            save_numpy_array_data(file_path=transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path, array=test_arr)
            
            preprocessing_obj_file_path = self.data_transformation_config.preprocessed_object_file_path
            
            logging.info(f"Saving preprocessing object.")
            save_object(file_path=preprocessing_obj_file_path, obj=preprocessing_obj)
            
            data_transformation_artifact = DataTransformationArtifact(
                is_transformed=True,
                message="Data Transformation successfull.",
                transformed_train_file_path=transformed_train_file_path,
                transformed_test_file_path=transformed_test_file_path,
                preprocessed_object_file_path=preprocessing_obj_file_path
            )
            print(f"--data_transformation---->>>>>>>{data_transformation_artifact}<<<<<<<<---data_transformation_artifact-------------")
            logging.info(f"Data transforamtion artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise BankingException(e, sys) from e 
            
    def __del__(self):
        logging.info(f"{'>>'*30}Data Transformation log completed.{'<<'*30} \n\n")
