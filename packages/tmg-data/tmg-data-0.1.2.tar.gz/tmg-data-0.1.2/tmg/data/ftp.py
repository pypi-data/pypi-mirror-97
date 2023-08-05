import parse
import paramiko
import os
from tmg.data import logs
import stat


class Client:
    """
    Creates a client which manages the connection to the FTP server.

    Args:
        connection_string (str): The FTP connection string in the format {username}:{password}@{host}:{port}
    """

    def __init__(self, connection_string):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        parsed_connection = parse.parse('{username}:{password}@{host}:{port}', connection_string)

        ssh_client.connect(hostname=parsed_connection['host'],
                            username=parsed_connection['username'],
                            password=parsed_connection['password'],
                            port=int(parsed_connection['port']))
        self.connection = ssh_client.open_sftp()

    def list_files(self, dir_path='.'):
        """Lists the files in a directory on the FTP server

        Args:
            dir_path (str): the path of the directory to list the contents of

        Returns:
            list: The list of the contents
        """

        return self.connection.listdir(dir_path)

    def upload_file(self, local_path, remote_path='.'):
        """Uploads a file from the local to the sFTP. If the remote path provided is a directory the filename
        of the local file will be used.

        Args:
            local_path (str): local path to the file to load
            remote_path (str): path to load the file to on the sFTP

        Returns:
            str: The path to the file loaded onto the sFTP
        """

        try:
            fileattr = self.connection.lstat(remote_path)
            if stat.S_ISDIR(fileattr.st_mode):
                filename = os.path.basename(local_path)
                remote_path = os.path.join(remote_path, filename)
        except IOError:
            pass

        self.connection.put(localpath=local_path, remotepath=remote_path)

        return remote_path

    def download_file(self, remote_path, local_path='.'):
        """Downloads a file from the sFTP to the local system. If the local path is a directory the filename of the
        remote file is used.

        Args:
            remote_path (str): The path to the file to download.
            local_path (str): The path to download the file to on the local system

        returns:
            str: The local path the file has been place.
        """

        if os.path.isdir(local_path):
            filename = os.path.basename(remote_path)
            local_path = os.path.join(local_path, filename)

        logs.client.logger.info("Starting file download.")

        self.connection.get(remotepath=remote_path, localpath=local_path)

        logs.client.logger.info("Finished downloading file.")

        return local_path

    def change_file_permission(self, remote_path, permission=stat.S_IRWXU):
        """Changes the permissions of the file on the sFTP

        Args:
            remote_path (str): The path to the file to change to permissions on
            permission (int): The permissions to set the file to
        """

        self.connection.chmod(path=remote_path, mode=permission)

    def delete_file(self, remote_path):
        """Deletes the specified file off the sFTP server

        Args:
            remote_path: path to the file to delete
        """

        self.connection.remove(remote_path)

    def close(self):
        """Closes the connection to the ftp server
        """
        self.connection.close()
