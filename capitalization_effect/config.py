import os

java_path = "/cs/fs/home/hxiao/software/jre1.8.0_31" # replace this

print "setting JAVAHOME to `%s`" %(java_path)

os.environ['JAVAHOME'] = java_path
