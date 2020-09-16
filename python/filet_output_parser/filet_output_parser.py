# -*-coding:Utf-8 -*


import glob


window_size = 10000
window_step = 1000
sub_windows_count = window_size / window_step

windows_dict = {}

output_file_name = "result_output.sv"

dir_name = "G:filet\\27_real_data_classification\\sliding\\results\\*"
all_files = glob.glob(dir_name)


files_count = len(all_files)
current_count = 0
for file_name in all_files:
    current_count += 1
    if(current_count % 100 == 0):
        print("Handling file", str(current_count), "out of", str(files_count), "...")

    file = open(file_name, "r")
    lines = file.readlines()
    print

    for line in lines:
        # we read a line in format "ctg1    240000  250000  2506    0       0.272324310641391       0.46094588887839616     0.2667298004802128"
        line_items = line.split()
        ctg_name = line_items[0]
        ctg_start = int(line_items[1])
        ctg_category = int(line_items[4])

        for idx in range (ctg_start, ctg_start + window_size, window_step):
            if (not (ctg_name, idx) in windows_dict):
                windows_dict[(ctg_name, idx)] = [0, 0, 0, 0]
            windows_dict[(ctg_name, idx)][ctg_category] += 1

    file.close()


print("Writing the output file...")
output_file = open(output_file_name, "w")

output_file.write("contig_name\tstart\tno_intr\tintr_12\tintr_21\tinvalid\n")
for key in windows_dict:
    categories = windows_dict[key]
    line = key[0] + "\t" + str(key [1]) + "\t" + str(categories[0]) + "\t" + str(categories[1]) + "\t" + str(categories[2]) + "\t" + str(categories[3]) + "\n"
    output_file.write(line)

output_file.close()
print("Done.")