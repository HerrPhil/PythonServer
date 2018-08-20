# PythonServer

Here are the basic command line calls needed to use this server.

```
nohup python3 fileserver.py 8000 &
nohup python3 fileserver.py 8001 &
ps ax | grep 'fileserver'
curl --verbose --data "http://localhost:8001/remote/log.zip" http://localhost:8000
```

The "http://localhost:8001/remote/log.zip" should be replaced with a real remote archive file, for example, an S3 amazon-stored file.
