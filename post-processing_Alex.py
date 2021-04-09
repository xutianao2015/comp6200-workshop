from datetime import datetime, timedelta
import csv
import os
today = (datetime.utcnow() + timedelta(hours = 10)).date()


input_files = [x for x in os.listdir() if 'CLG_REFRESH' in x and x.endswith('.txt')]
print(input_files)
for input_file in input_files:
    
    property_id_sum = 0
    row_count = 0
    row_count_final = 0
    
    print('Processing file: ' + input_file)
    ## calculate property ID sum
    with open(input_file, newline='', encoding = 'utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='|', quoting=csv.QUOTE_NONE)
        for row in reader:
            row_count = row_count + 1
            if row_count == 1:
                pid_col = row.index('CL_PROPERTY_ID')
                print('CL_PROPERTY_ID is in column: {}'.format(pid_col))
            else:
                try:
                    if row[pid_col] != '':
                        property_id_sum = property_id_sum + int(row[pid_col])
                except Exception as e:
                    print(row)
                    print(row[pid_col])
                    raise Exception(e)
    
        
    ## output file
    output_file_name = input_file.replace('.txt', '.DAT')
    if os.path.isfile(output_file_name):
        os.remove(output_file_name)
        
    ## write final final
    header_str = 'H|{}|{}|{}'.format(today.strftime('%Y%m%d'), today.strftime('%Y%m%d%H%m%S'), output_file_name)
    footer_str = 'T|{}|{}|CL_PROPERTY_ID'.format(row_count+1, property_id_sum) ## + 1 header +1 footer - 1 column name. Got same result as the row_count_final.
    print("header: ", header_str)
    print("footer: ", footer_str)
    
    is_first_row = True
    
    with open(output_file_name, 'w', newline='\r\n', encoding = 'utf-8') as output_fl:
        output_fl.write(header_str + '\n')
        row_count_final = row_count_final + 1
        with open(input_file, encoding = 'utf-8') as input_fl:    
            for line in input_fl:
                # skip header row
                if is_first_row:
                   is_first_row = False
                else:
                    output_fl.write(line) 
                    row_count_final = row_count_final + 1

        output_fl.write(footer_str) #  Final row does not need '\r\n'
        row_count_final = row_count_final

    print('Input file "{}" row count: {}'.format(input_file, row_count))
    print('Output file "{}" row count: {}'.format(output_file_name, row_count_final))
    print('\n')

    ## remove input (otherwise it will get packaged up and delivered)
    os.remove(input_file)
    
print('done')
