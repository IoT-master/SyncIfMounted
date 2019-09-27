import subprocess
from time import perf_counter
# import concurrent.futures
def exist_with_grep(volume_name, my_output):
    my_bool = any(filter(lambda line: len(line.split(volume_name)) > 1, my_output.split('\n')))
    return my_bool

start = perf_counter()
command = subprocess.check_output('mount', shell=True)
output_string = command.decode()

mapped_paths = ['/dev/sda', '/dev/sdb']
mapped_output = [output_string] *len(mapped_paths)
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     results = executor.map(exist_with_grep, mapped_paths, mapped_output)

results = list(map(lambda each_path, each_output: exist_with_grep(each_path, each_output), mapped_paths, mapped_output))
if all(results):
    subprocess.run('/usr/bin/rsync -zar --delete-after /media/pi/Burtha/ /media/pi/Copycat/ >/dev/null 2>&1', shell=True)
finished = perf_counter()
print(f'Finished in {round(finished-start, 5)} second(s)')