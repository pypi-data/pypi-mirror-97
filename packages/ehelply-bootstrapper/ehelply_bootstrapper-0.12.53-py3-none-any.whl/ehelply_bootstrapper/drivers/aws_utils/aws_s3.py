import boto3
from collections import namedtuple
from operator import attrgetter
import os
from ehelply_bootstrapper.utils.state import State

S3Obj = namedtuple('S3Obj', ['key', 'mtime', 'size', 'ETag'])


class S3:
    def __init__(self, bucket_name: str) -> None:
        self.s3 = State.aws.make_resource(name="s3")
        self.bucket_name = bucket_name
        self.bucket = self.s3.Bucket(bucket_name)

    def read(self, file_path: str) -> str:
        obj = self.s3.Object(self.bucket_name, file_path)
        return obj.get()['Body'].read().decode('utf-8').replace("\r\n", "\n")

    def write(self, file_path: str, content: str):
        self.s3.Object(self.bucket_name, file_path).put(Body=content)

    def delete(self, file_path: str):
        self.s3.Object(self.bucket_name, file_path).delete()

    def list(self, path, start=None, end=None, recursive=True, list_dirs=True, list_objs=True, limit=None):
        """
        Iterator that lists a bucket's objects under path, (optionally) starting with
        start and ending before end.
    
        If recursive is False, then list only the "depth=0" items (dirs and objects).
    
        If recursive is True, then list recursively all objects (no dirs).
    
        Args:
            bucket:
                a boto3.resource('s3').Bucket().
            path:
                a directory in the bucket.
            start:
                optional: start key, inclusive (may be a relative path under path, or
                absolute in the bucket)
            end:
                optional: stop key, exclusive (may be a relative path under path, or
                absolute in the bucket)
            recursive:
                optional, default True. If True, lists only objects. If False, lists
                only depth 0 "directories" and objects.
            list_dirs:
                optional, default True. Has no effect in recursive listing. On
                non-recursive listing, if False, then directories are omitted.
            list_objs:
                optional, default True. If False, then directories are omitted.
            limit:
                optional. If specified, then lists at most this many items.
    
        Returns:
            an iterator of S3Obj.
    
        Examples:
            # set up
            >>> s3 = boto3.resource('s3')
            ... bucket = s3.Bucket(name)
    
            # iterate through all S3 objects under some dir
            >>> for p in s3ls(bucket, 'some/dir'):
            ...     print(p)
    
            # iterate through up to 20 S3 objects under some dir, starting with foo_0010
            >>> for p in s3ls(bucket, 'some/dir', limit=20, start='foo_0010'):
            ...     print(p)
    
            # non-recursive listing under some dir:
            >>> for p in s3ls(bucket, 'some/dir', recursive=False):
            ...     print(p)
    
            # non-recursive listing under some dir, listing only dirs:
            >>> for p in s3ls(bucket, 'some/dir', recursive=False, list_objs=False):
            ...     print(p)
    """
        kwargs = dict()
        if start is not None:
            if not start.startswith(path):
                start = os.path.join(path, start)
            # note: need to use a string just smaller than start, because
            # the list_object API specifies that start is excluded (the first
            # result is *after* start).
            kwargs.update(Marker=self.__prev_str(start))
        if end is not None:
            if not end.startswith(path):
                end = os.path.join(path, end)
        if not recursive:
            kwargs.update(Delimiter='/')
            if not path.endswith('/'):
                path += '/'
        kwargs.update(Prefix=path)
        if limit is not None:
            kwargs.update(PaginationConfig={'MaxItems': limit})

        paginator = self.bucket.meta.client.get_paginator('list_objects')
        for resp in paginator.paginate(Bucket=self.bucket.name, **kwargs):
            q = []
            if 'CommonPrefixes' in resp and list_dirs:
                q = [S3Obj(f['Prefix'], None, None, None) for f in resp['CommonPrefixes']]
            if 'Contents' in resp and list_objs:
                q += [S3Obj(f['Key'], f['LastModified'], f['Size'], f['ETag']) for f in resp['Contents']]
            # note: even with sorted lists, it is faster to sort(a+b)
            # than heapq.merge(a, b) at least up to 10K elements in each list
            q = sorted(q, key=attrgetter('key'))
            if limit is not None:
                q = q[:limit]
                limit -= len(q)
            for p in q:
                if end is not None and p.key >= end:
                    return
                yield p

    def __prev_str(self, s):
        if len(s) == 0:
            return s
        s, c = s[:-1], ord(s[-1])
        if c > 0:
            s += chr(c - 1)
        s += ''.join(['\u7FFF' for _ in range(10)])
        return s
