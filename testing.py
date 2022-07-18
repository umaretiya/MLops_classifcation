from banking.pipeline.pipeline import Pipeline
from banking.component import data_ingestion, kaggle_data
from banking.constant import * 
from banking.config.configuration import Configuration

def test():
    p = Pipeline(config=Configuration(config_file_path=CONFIG_FILE_PATH,current_time_stamp=CURRENT_TIME_STAMP))

    data_ingestion = p.start_data_ingestion()
    
    data_validation = p.start_data_validation(data_ingestion_artifact=data_ingestion)
    
    # data_transformation = p.start_data_transformation()
    print(data_validation)
    
if __name__ == '__main__':
    test()