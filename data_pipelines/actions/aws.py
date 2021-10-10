# from dotenv import load_dotenv
from airflow.exceptions import AirflowSkipException
from data_pipelines.connections.core import CSVConn
from data_pipelines.connections.aws import S3Conn
from data_pipelines.actions.core import SourceToSink


class CSVToS3(SourceToSink):
    source_class = CSVConn
    sink_class = S3Conn

    def run(self):

        with self.source:
            data = self.get_data()
            data = [*data]
            if data:
                with self.sink:
                    self.load_data(data)
                self.log.info("Data Successfully Loaded!")
            else:
                raise AirflowSkipException("No Data Found on that date !")


# if __name__ == '__main__':
#     load_dotenv()

#     sink_kwargs = {
#         'AWS_ACCESS_KEY': os.getenv('AWS_ACCESS_KEY'),
#         'AWS_SECRET_KEY': os.getenv('AWS_SECRET_KEY'),
#         's3_bucket': 'test-bucket-henry-093',
#         's3_key':'data-pipelines-2/data.json',
#     }

#     source_kwargs = {
#         "date": "2021-06"
#     }

#     kwargs = {
#         "source_kwargs": source_kwargs,
#         "sink_kwargs": sink_kwargs,
#     }

#     action_class = CSVToS3(**kwargs)
#     action_class.run()
#     print('success !')
