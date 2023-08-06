#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility to send or fetch files to and from s3 bucket
"""
import boto
import boto.s3
import os
import traceback

try:
    host = 's3-%s.amazonaws.com' % os.environ['AWS_DEFAULT_REGION']
    S3 = boto.connect_s3(host=host)
    BUCKET = S3.get_bucket(os.environ['AWS_S3_BUCKET'])
except KeyError:
    pass


def burrito(description, job):
    """Utility for s3 transfer status
    """
    print(description, 'start', flush=True)
    try:
        job()
        print(description, 'done', flush=True)
        return True
    except:
        print(description, 'failed', flush=True)
        traceback.print_exc()
        return False


def put(path, key):
    """Takes a local file path and puts it into key in the bucket

    Parameters
    ----------
    path : str
        Local filename
    key : str
        Filename in s3 bucket

    Returns
    -------
    burrito : boolean
        Whether the transfer was successful (True) or failed (False)

    Examples
    --------
    >>> s3.put('local_example.png','s3_example.png')
    """
    return burrito('put %s' % path, lambda: boto.s3.key.Key(BUCKET, key).set_contents_from_filename(path))


def get(key, path):
    """Fetch a file from a s3 bucket puts it into local file

    Parameters
    ----------
    key : str
        Filename in s3 bucket
    path : str
        Local filename

    Returns
    -------
    burrito : boolean
        Whether the transfer was successful (True) or failed (False)

    Examples
    --------
    >>> s3.get('s3_example.png','local_example.png')
    """
    return burrito('get %s' % key, lambda: boto.s3.key.Key(BUCKET, key).get_contents_to_filename(path))


def list(prefix):
    """List files in s3 bucket

    Parameters
    ----------
    prefix : str
        s3 bucket path

    Returns
    -------
    bucket_list : list
        List of files in s3 bucket path
    """
    return BUCKET.list(prefix=prefix)
