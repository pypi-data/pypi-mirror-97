Amocrm custom library
==========

1. Retrieving data from amocrm amocrm.api (v2 and v4).
2. Uploading data to database. 

Supported databases:
-------------
* clickhouse
* vertica 


Usage
```sh
pip3 install amocrm-talenttech-oss
```

Retrieving data from API:
-------------

```python
import datetime
from api.api_loader_amocrm_v4 import AmocrmApiLoader as ApiLoaderV4

 
date_modified_from = datetime.datetime.now() - datetime.timedelta(days=1) #
args_api = {
                "amocrm_api_url": "https://<NAMESPACE>.amocrm.ru/amocrm.api/v4/<ENTITY>?page={page}&limit={limit}",
                "AUTH_URL":"https://<NAMESPACE>.amocrm.ru/oauth2/access_token",
                "CLIENT_SECRET":"xxxx",
                "CLIENT_ID": "xxx-xxx-xxxx-xxxx-xxxxxxx",
                "REDIRECT_URL":"https://xxxx/xx"
           }

args_s3 = {
                "aws_access_key_id": <S3_ACCESS_KEY>,
                "aws_secret_access_key":  <S3_ACCESS_SECRET>,
                "endpoint_url": <S3_ENDPOINT_URL>,
                "bucket": <S3_BUCKET>
          }



api_loader = ApiLoaderV4(
                entity=<ENTITY>,                # leads/tasks/companies or e.t.c
                s3_path=<S3_PATH>,              # this s3 folder should contain retrieved files
                s3_token_path=<S3_TOKEN_PATH>,  # directory for tokens
                args_s3=args_s3,
                args_api=args_api,
                date_modified_from=date_modified_from, #parameters is optional, if want load only updated records from date
                with_offset=True, 
                batch_api=500
            )

api_loader.auth(<CODE_AUTH>) #call it if you need to create or regenerate refresh token the first time
api_loader.extract()      
```


Uploading data to vertica:
-------------
```python
from db.vertica_uploader import UploaderDB as VerticaUploaderDB
sql_credentials = {
                "database": <DATABASE>,
                "schema": <SCHEMA>
                "user": <VERTICA_WRITE_USER>,
                "host": <VERTICA_HOST>,
                "port": <VERTICA_PORT>,
                "password": <VERTICA_WRITE_PASSWORD>,
                "vertica_configs": <VERTICA_CONFIGS>,
            }

args_s3 = {
                "aws_access_key_id": <S3_ACCESS_KEY>,
                "aws_secret_access_key":  <S3_ACCESS_SECRET>,
                "endpoint_url": <S3_ENDPOINT_URL>,
                "bucket": <S3_BUCKET>
          }        

db_uploader = VerticaUploaderDB(
            args_s3=args_s3,
            s3_path=s3_path,
            sql_credentials=sql_credentials,
            entity=<ENTITY>,
            table_name=<TABLE_NAME>,
            json_columns=[<COLUM_JSON_1>, <COLUM_JSON_2>]
        )
db_uploader.load_s3_to_db()        

  