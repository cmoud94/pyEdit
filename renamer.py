import os

files = [x for x in os.listdir('./') if x.find('cpython-34.pyc') != -1]
old_files = [x for x in os.listdir('./') if x.find('.pyc') != -1 and x.find('cpython-34') == -1]

if len(old_files) > 1:
    for i in range(len(old_files)):
        os.remove(old_files[i])

print('Removed old files...')

for i in range(len(files)):
    item = files[i].split('.')
    os.rename(files[i], str(item[0] + '.' + item[2]))

print('Done!')
