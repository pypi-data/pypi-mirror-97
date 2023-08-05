import parse
import csv
from time import sleep

from simple_salesforce import Salesforce, exceptions
from tmg.data import logs


class Client:
    """
    Client to bundle Salesforce functionality.

    Args:
        connection_string (str): The Salesforce connection string in the format {username}:{password}:{token}@{domain}
                                 Domain should be either ``'login'`` for production server or ``'test'`` for UAT servers

    """

    MAX_RETRIES = 10
    WAIT_BETWEEN_RETRY = 10

    def __init__(self, connection_string):

        parsed_connection = parse.parse('{username}:{password}:{token}@{domain}', connection_string)
        self.sf = Salesforce(
            username=parsed_connection['username'],
            password=parsed_connection['password'],
            security_token=parsed_connection['token'],
            domain=parsed_connection['domain']
        )

    def run_query(self, query, include_deleted=False):
        """Run the query on Salesforce server and return the result

        Args:
            query (str): The query string.
            include_deleted (:obj:`boolean`, Optional): Include deleted records in the returned result.
                                                        IsDeleted field is available for each record. Defaults to :data:`False`
        Returns:
            The query results

        """

        data = []
        try_count = 0
        while try_count < self.MAX_RETRIES:
            try:
                logs.client.logger.info('Running query on Salesforce: {}'.format(query))
                data = self.sf.query_all(query, include_deleted=include_deleted)
                break
            except (
                exceptions.SalesforceExpiredSession,
                exceptions.SalesforceMalformedRequest,
                exceptions.SalesforceAuthenticationFailed
            ) as e:
                logs.client.logger.warning(
                    "Reading from Salesforce failed with this message: {message}."
                    "Sleeping for {wait_time} seconds before next try".format(
                        message=e.content[0]["message"],
                        wait_time=self.WAIT_BETWEEN_RETRY
                    )
                )
                sleep(self.WAIT_BETWEEN_RETRY)
                try_count += 1

        if try_count == self.MAX_RETRIES:
            raise Exception("Reading from Salesforce failed. Reached maximum retries.")

        return data.get('records', [])

    def download_table(self, table, columns, condition=None, include_deleted=False, local_folder='.', separator=',', print_header=True):
        """
        Export the table to the local file in CSV format.

        Args:
            table (str):  Table name. For example: ``Account``.
            columns (tuple): Table columns. For example: ``('Id', 'FirstName', 'LastName')``.
            condition (:obj:`str`, Optional): The condition which should apply to the table. For example: ``ModifiedDate > 2020-01-01``. Defaults to :data:`None`
            include_deleted (:obj:`boolean`, Optional): Include deleted records in the returned result.
                                                        IsDeleted field is available for each record. Defaults to :data:`False`
            local_folder (:obj:`str`, Optional):  The local folder with out the slash at end. For example: ``/some_path/some_inside_path``. Defaults to current path :data:`.`
            separator (:obj:`str`, Optional): The separator. Defaults to :data:`,`
            print_header (:obj:`boolean`, optional):  True to print a header row in the exported file otherwise False. Defaults to :data:`True`.

        Returns:
            str: The output file path

        Examples:
            >>> from tmg.data import salesforce
            >>> client = salesforce.Client(username='username',password='password',token='token')
            >>> client.download_table(table='Account',columns=('Id', 'FirstName', 'LastName'))
        """

        query_str = 'SELECT {columns} FROM {table} {where_clause}'.format(
            columns=','.join(columns),
            table=table,
            where_clause='WHERE {}'.format(condition) if condition else ''

        )
        rows = self.run_query(query_str, include_deleted)

        output_file = '{}/{}.csv'.format(local_folder, table)
        logs.client.logger.info('Exporting data into {}'.format(output_file))
        with open(output_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns, delimiter=separator)
            if print_header:
                writer.writeheader()

            for row in rows:
                row.pop('attributes')
                writer.writerow(row)

        return output_file
