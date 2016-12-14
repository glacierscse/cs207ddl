import os, sys
curr_dir = os.getcwd().split('/')
sys.path.append('/'.join(curr_dir[:-1]))
ts_dir = curr_dir[:-1]
ts_dir.append('timeseries')
sys.path.append('/'.join(ts_dir))
from pytest import raises
import unittest
import numpy as np
from timeseries.cs207rbtree import *
import os

# smoke test to make sure red black tree is working
def test_smoke():
    db = connect("/tmp/test2.dbdb")
    db.set("rahul", "aged")
    db.set("pavlos", "aged")
    db.set("kobe", "stillyoung")
    db.commit()
    db.close()
    newdb = connect("/tmp/test2.dbdb")
    assert newdb.get("pavlos")=="aged"
    newdb.close()
    os.remove('/tmp/test2.dbdb')


# test init methods
def test_inits():
    dbname = "/tmp/test2.dbdb"
    try:
        f = open(dbname, 'r+b')
    except IOError:
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    storage = Storage(f)
    redBlackTree = RedBlackTree(storage)
    db = DBDB(f)
    db.close()
    os.remove('/tmp/test2.dbdb')


# test whether the change is successfully made if it is not commited
def test_commite():
    db = connect("/tmp/test2.dbdb")
    db.set("rahul", "aged")
    db.set("pavlos", "aged")
    db.set("kobe", "stillyoung")
    db.close()
    db = connect("/tmp/test2.dbdb")
    with raises(KeyError):
        db.get("pavlos")
    db.close()
    os.remove('/tmp/test2.dbdb')


# change the input order to test more rotation
def test_more_rotate():
    db = connect("/tmp/test2.dbdb")
    db.set("kobe", "stillyoung")
    db.set("pavlos", "aged")
    db.set("rahul", "aged")
    db.commit()
    db.close()
    newdb = connect("/tmp/test2.dbdb")
    assert newdb.get("pavlos")=="aged"
    newdb.close()
    os.remove('/tmp/test2.dbdb')


# test find all smaller method
def test_smaller():
    db = connect("/tmp/test2.dbdb")
    db.set("kobe", "stillyoung")
    db.set("pavlos", "aged")
    db.set("rahul", "aged")
    db.commit()
    db.close()
    newdb = connect("/tmp/test2.dbdb")
    assert newdb.find_all_smaller("pavlos")==['stillyoung', 'aged']
    newdb.close()
    os.remove('/tmp/test2.dbdb')



