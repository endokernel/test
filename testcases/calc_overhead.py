# Usage: calc_overhead.py result_folder test_name
import os
import csv

inv = {
    # transfer rate, higher is better
    "lighttpd": True,
    "nginx": True,
    "sysbench": True,
    "file_bw": lambda baseline, current: (current) / (baseline),
    # time, lower is better
    "curl": False,
    "zip": False,
    "sqlite": False,
    "lmbench": False,
}

avg_only = ['lmbench', "sysbench"]

is_sysbench = False

def read_single_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    headers = data[0]
    # remove last column if it is empty
    if is_sysbench:
        # the header is 1,,2,,4,,8,,16,,; filter out empty columns
        headers = [header for header in headers if header]
        data = data[2:] # remove first two rows
        # for each data, keep 0, 2, 4, 6, only.. 
        # the header in the csv is incorrect because the script actually run fileio first..
        data = [[row[i] for i in range(len(row)) if i % 2 == 0] for row in data]
    else:
        if not headers[-1]:
            headers = headers[:-1]
        data = data[1:]
    
    # get average of each column
    averages = {}
    for i in range(len(headers)):
        column = [float(row[i]) for row in data]
        averages[headers[i]] = sum(column) / len(column)
    return averages

def read_multiple_files(file_paths, test_name):
    averages = {}
    for file_path in file_paths:
        single_average = read_single_file(file_path)
        runname = os.path.basename(file_path).split('.')[0]
        if runname.startswith(test_name):
            runname = runname[len(test_name) + 1:]
        else:
            raise Exception("Cannot find runname in file name: " + file_path)

        averages[runname] = single_average
    return averages

def read_and_process_data(folder_path, test_name):
    results = {}
    avg_mode = False
    if test_name in avg_only:
        avg_mode = True
        def calculate_overhead(baseline, current):
            return current
    else:
        if inv[test_name]:
            # if inv[test_name] is a lambda function, use that to calculate overhead
            if callable(inv[test_name]):
                calculate_overhead = inv[test_name]
            else:
                def calculate_overhead(baseline, current):
                    return ((baseline - current) / baseline) * 100
        else:
            def calculate_overhead(baseline, current):
                return ((current - baseline) / baseline) * 100
    def calculate_overheads(baseline, current):
        keys = baseline.keys()
        result = {}
        for key in keys:
            result[key] = calculate_overhead(baseline[key], current[key])
        return result
        
    files = os.listdir(folder_path)
    test_files = [os.path.join(folder_path, file) for file in files if test_name in file and '.pickle' not in file]

    if len(test_files) > 1:
        averages = read_multiple_files(test_files, test_name)

        overheads = {}
        for runname, average in averages.items():
            if not avg_mode and runname == 'baseline':
                continue
            overhead = calculate_overheads(averages['baseline'], average)
            results[runname + '_overhead'] = overhead
        
        overall_overhead = {}
        for runname, overhead in results.items():
            print("Overhead for " + runname)
            print(overhead)
            avg = sum(overhead.values()) / len(overhead)
            overall_overhead[runname] = avg
        print("Aggregate overhead:")
        print(results)
        print("Average over columns:")
        print(overall_overhead)


    elif len(test_files) == 1:  
        averages = read_single_file(test_files[0])
        
        for runname, average in averages.items():
            if runname == 'baseline':
                continue
            overhead = calculate_overhead(averages['baseline'], average)
            results[runname + '_overhead'] = overhead

        print("Overhead:")
        print(results)
    else:
        print('No files found')

if __name__ == '__main__':
    # usage calc_overhead.py result_folder test_name
    import sys
    if len(sys.argv) < 3:
        print('Usage: calc_overhead.py result_folder test_name')
        sys.exit(1)
    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print('Folder path does not exist')
        sys.exit(1)
    test_name = sys.argv[2]
    if test_name not in inv:
        print('Test name not found')
        sys.exit(1)
    if test_name == 'sysbench':
        is_sysbench = True
    read_and_process_data(folder_path, test_name)
