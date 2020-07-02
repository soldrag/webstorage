## Simple aiohttp server for file storage

- For upload file, use form on /upload, server return status and file_id in json response.

- For download file, use query POST /download?file_id={file_id}, server return file

- For delete file, use query DELETE /delete?file_id={file_id}, server return status command.

- Server have settings */http_storage/config/http_storage.yml
    * server:
        * host - address for server listening
        * port - port for server listening
    * http_storage:
        * hash_type - type for hashing files
            * simple {0} - the hash of files with the same name will also be the same
            * unique {1} - the hash of files with the same name will be different
    
