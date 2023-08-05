import boto3
import logging
import psycopg2
import psycopg2.extras


logger = logging.getLogger()
logger.level = logging.INFO


class RedshiftHelper:

    # TODO: Initialize from the environment to generalize
    USER = "awsuser"
    DATABASE = "analytics"
    CLUSTER = "properly-general-002"
    ENDPOINT = "properly-general-002.c25yretklzxj.us-east-1.redshift.amazonaws.com"
    PORT = 5439

    def __init__(self, user_to_emulate: str):
        self.conn = None
        self.creds = None
        self.user = user_to_emulate or RedshiftHelper.USER

    def _get_temp_creds(self):
        # Inspiration from:
        # https://blog.mitocgroup.com/aws-lambda-to-redshift-connection-using-iam-authentication-and-nat-gateway-b40c6002082b
        try:
            client = boto3.client('redshift')
            creds = client.get_cluster_credentials(
                DbUser=self.user,
                DbName=RedshiftHelper.DATABASE,
                ClusterIdentifier=RedshiftHelper.CLUSTER,
                DurationSeconds=3600)
        except Exception as ex:
            logger.error("Credentials Issue: {}".format(ex))
            raise

        return creds

    def _create_connection(self):
        try:
            self.conn = psycopg2.connect(
                dbname=RedshiftHelper.DATABASE,
                user=self.creds['DbUser'],
                password=self.creds['DbPassword'],
                port=RedshiftHelper.PORT,
                host=RedshiftHelper.ENDPOINT)
        except Exception as ex:
            logger.error("Connection Issue: {}".format(ex))
            raise

    def _initialize_conn(self):
        self.creds = self._get_temp_creds()

        self._create_connection()

    def create_cursor(self):
        if not self.conn:
            self._initialize_conn()

        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return cursor

    def commit(self):
        if not self.conn:
            self._initialize_conn()
        self.conn.commit()

    def close(self):
        if not (self.conn is None):
            self.conn.close()
            self.conn = None
