# 環境構築

- create table

```bash
$ docker exec -i -t lambda-app bash
$ python3 createTable.py
$ exit
# http://localhost:8001/
```

# test

```bash
# insert
$ python3 -c "import request; request.put()"
# select where
$ python3 -c "import request; request.query()"
# select all
$ python3 -c "import request; request.scan()"
# delete
$ python3 -c "import request; request.delete()"
```
# tweet-action-lambda
