#! /bin/bash

source env.sh

pytest test_sl_api.py -k 'TC'
