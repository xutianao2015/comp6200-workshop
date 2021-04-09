from datetime import datetime, timedelta
import csv
import os
import shutil

# copy only the first rows and last row and those with 6 pipes.

today = (datetime.utcnow() + timedelta(hours = 10)).date()

print('current directory: '+os.getcwd())

input_files = [x for x in os.listdir() if 'CLG_HL' in x and x.endswith('_.DAT')]
print(input_files)

for input_file in input_files:
    print('Processing file: ' + input_file)
    row_count = 0
    final_row_count = 0
    property_id_sum = 0
    ## output file
    output_file_name = input_file.replace('_.DAT', '_v2.DAT')
    if os.path.isfile(output_file_name):
        os.remove(output_file_name)
    
    with open(input_file, 'r') as input_fl:    
        with open(output_file_name, 'w', newline='\n') as output_fl:
        # output_fl.write(header_str + '\n')
        # row_count_final = row_count_final + 1
            for line in input_fl:
                row_count += 1
                # skip header row
                if line.split('|')[0] =='H':
                    output_fl.write(line)
                    final_row_count += 1
                elif line.split('|')[0] =='D':
                    output_fl.write(line)
                    final_row_count += 1
                    property_id_sum += int(line.split('|')[3])
                elif line.split('|')[0] == 'T':
                    footer_str = 'T|{}|{}|CL_PROPERTY_ID\n'.format(final_row_count + 1, property_id_sum) ## + 1 header +1 footer - 1 column name. Got same result as the row_count_final.
                    output_fl.write(footer_str)
                    final_row_count += 1
    # ## remove input (otherwise it will get packaged up and delivered)
    # os.remove(input_file)
    print(input_file + ' original row_count: ' + str(row_count) + ' , final row count: ' + str(final_row_count)) 

print('done')
