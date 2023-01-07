import os
from glob import iglob

for file in iglob("*"):
    print(file)
