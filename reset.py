import os
import shutil
import glob

folder = '壹電視新聞-2023(7-9月)'
for path in glob.glob(os.path.join(folder, "*/*/"), recursive=True):
    if('skip/'in path): continue
    if(os.path.isdir(path)):
        shutil.rmtree(path)
        continue
    os.remove(path)
    continue

