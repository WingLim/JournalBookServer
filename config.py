import os

if 'TOKEN' in os.environ:
    pwd = os.environ['TOKEN']
else:
    pwd = "yourtoken"