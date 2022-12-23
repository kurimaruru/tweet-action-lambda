until (/usr/bin/mc config host add minio http://minio:9000 ${MINIO_ACCESS_KEY} ${MINIO_SECRET_KEY}) do echo '...waiting...' && sleep 1; done;

for bucket in ${MINIO_BUCKET_LAMBDA} ; do
    # make a bucket
    /usr/bin/mc mb minio/${bucket}
    # manage bucket lifecycle
    /usr/bin/mc ilm import minio/${bucket} < minio/lifecycle_rule.json
    /usr/bin/mc version enable minio/${bucket}
done

exit 0