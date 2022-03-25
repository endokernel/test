#!/bin/bash
python3 -u lmbench.py
python3 -u lighttpd.py
python3 -u sqlite.py
python3 -u curl.py
python3 -u file_bw.py
python3 -u nginx.py
python3 -u nginx_safe.py
python3 -u nginx_sand.py
python3 -u nginx_safe_sand.py
python3 -u zip.py
python3 -u sysbench.py
python3 -u zlib.py