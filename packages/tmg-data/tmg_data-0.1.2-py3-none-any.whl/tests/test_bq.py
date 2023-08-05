import unittest
import csv
from google.cloud import bigquery

from tmg.data import bq
from tests.setup import setup


def setUpModule():
    setup.create_bq_table()
    setup.create_bucket()


def tearDownModule():
    setup.delete_bq_dataset()
    setup.delete_bucket()


class TestBQ(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestBQ, self).__init__(*args, **kwargs)
        self.setup = setup

    def test_download_table(self):

        bq_client = bq.Client(project=self.setup.project)
        downloaded_file_names = bq_client.download_table(
            table='{}.{}.{}'.format(self.setup.project, self.setup.dataset_id, self.setup.table_id)
        )

        # creating list based on destination bucket file values
        with open(downloaded_file_names[0], newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            storage_keys = []
            for row in reader:
                storage_keys.append(
                    str(row['profile_id']) + row['first_name'] + row['last_name']
                )

        # creating list based on source big query table values
        bq_keys = []
        bigquery_client = bigquery.Client(project=self.setup.project)
        job = bigquery_client.query(
            'SELECT profile_id, first_name, last_name from {}.{}'.format(
                self.setup.dataset_id,
                self.setup.table_id
            )
        )
        for row in job.result():
            bq_keys.append('{}{}{}'.format(
                row.profile_id,
                '' if row.first_name is None else row.first_name,
                '' if row.last_name is None else row.last_name,
            ))

        # creating list based on destination bucket file values

        self.assertEqual(storage_keys, bq_keys)

    def test_upload_table(self):

        bq_client = bq.Client(project=self.setup.project)
        bq_client.upload_table(
            file_path='tests/data/sample.csv',
            table='{}.{}.{}'.format(self.setup.project, self.setup.dataset_id, 'uploaded_actors')
        )

        # creating list based on destination bucket file values
        with open('tests/data/sample.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            storage_keys = []
            for row in reader:
                storage_keys.append(
                    str(row['profile_id']) + row['first_name'] + row['last_name']
                )

        # creating list based on source big query table values
        bq_keys = []
        bigquery_client = bigquery.Client(project=self.setup.project)
        job = bigquery_client.query(
            'SELECT profile_id, first_name, last_name from {}.{}'.format(
                self.setup.dataset_id,
                'uploaded_actors'
            )
        )
        for row in job.result():
            bq_keys.append('{}{}{}'.format(
                row.profile_id,
                '' if row.first_name is None else row.first_name,
                '' if row.last_name is None else row.last_name,
            ))

        # creating list based on destination bucket file values

        self.assertEqual(storage_keys, bq_keys)

    def test_run_query(self):

        # creating list based on run_query return's results
        bq_client = bq.Client(project=self.setup.project)
        results = bq_client.run_query(
            query='SELECT * FROM {}.{} where profile_id={{{{id}}}}'.format(self.setup.dataset_id, self.setup.table_id),
            params={'id': 1}

        )
        keys = []
        for row in results:
            keys.append('{}{}{}'.format(
                row.profile_id,
                '' if row.first_name is None else row.first_name,
                '' if row.last_name is None else row.last_name,
            ))

        # creating list based on source big query table values
        bigquery_client = bigquery.Client(project=self.setup.project)
        job = bigquery_client.query(
            query='SELECT profile_id, first_name, last_name from {}.{} where profile_id=@id'.format(
                self.setup.dataset_id,
                self.setup.table_id
            ),
            job_config=bigquery.QueryJobConfig(
                query_parameters=[bigquery.ScalarQueryParameter('id', 'INT64', 1)]
            )
        )
        bq_keys = []
        for row in job.result():
            bq_keys.append('{}{}{}'.format(
                row.profile_id,
                '' if row.first_name is None else row.first_name,
                '' if row.last_name is None else row.last_name,
            ))

        self.assertEqual(keys, bq_keys)

    def test_create_table_with_schema_fields(self):

        bq_client = bq.Client(project=self.setup.project)
        bq_client.create_table(
            table='{}.{}.{}'.format(self.setup.project, self.setup.dataset_id, 'venue'),
            schema_fields=(('venue_id', 'STRING', 'REQUIRED'), ('name', 'STRING', 'REQUIRED'))
        )

        bigquery_client = bigquery.Client(project=self.setup.project)
        table_ref = bigquery_client.get_table('{}.{}.{}'.format(self.setup.project, self.setup.dataset_id, 'venue'))
        self.assertEqual(table_ref.schema, [
            bigquery.SchemaField("venue_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("name", "STRING", mode="REQUIRED")
        ])

    def test_create_table_with_schema_file_name(self):

        bq_client = bq.Client(project=self.setup.project)
        bq_client.create_table(
            table='{}.{}.{}'.format(self.setup.project, self.setup.dataset_id, 'venue2'),
            schema_file_name='tests/data/schema.csv'
        )

        bigquery_client = bigquery.Client(project=self.setup.project)
        table_ref = bigquery_client.get_table('{}.{}.{}'.format(self.setup.project, self.setup.dataset_id, 'venue2'))
        self.assertEqual(table_ref.schema, [
            bigquery.SchemaField("venue_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("address", "STRING", mode="REQUIRED")

        ])
