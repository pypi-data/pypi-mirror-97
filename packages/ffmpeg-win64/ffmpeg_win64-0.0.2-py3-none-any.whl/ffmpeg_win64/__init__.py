from pkg_resources import resource_filename
import os
os.environ['PATH'] += ';'+resource_filename(__name__, "")
