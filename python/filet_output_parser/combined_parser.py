# -*-coding:Utf-8 -*


import glob


window_size = 10000
window_step = 1000
sub_windows_count = window_size / window_step
stats_count = 27

windows_dict = {}

output_file_name = "combined_output.sv"

result_dir_name = "G:filet\\27_real_data_classification\\sliding\\results\\*"
all_result_files = glob.glob(result_dir_name)
stats_dir_name = "G:filet\\26_empty_contigs_and_statistics_removal\\sliding\\result\\result\\*"
all_stats_files = glob.glob(stats_dir_name)


print("Reading result files...")
files_count = len(all_result_files)
current_count = 0
for file_name in all_result_files:
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
                windows_dict[(ctg_name, idx)] = [0, 0, 0, 0, 0]  # 4 categories and statistics occurrences counter
                for stat_idx in range (0, stats_count):
                    windows_dict[(ctg_name, idx)].append(0)  # other positions correspond to the statistics
            windows_dict[(ctg_name, idx)][ctg_category] += 1

    file.close()


print("Reading statistics files...")
files_count = len(all_stats_files)
current_count = 0
for file_name in all_stats_files:
    current_count += 1
    if(current_count % 100 == 0):
        print("Handling file", str(current_count), "out of", str(files_count), "...")

    file = open(file_name, "r")
    lines = file.readlines()
    
    iter_lines = iter(lines)
    next(iter_lines)  # we skip the title line

    for line in iter_lines:
        # we read a line in format "ctg1    start  end  num_sites    stat_1  stat_2  ..."
        line_items = line.split()
        ctg_name = line_items[0]
        ctg_start = int(line_items[1])

        for idx in range (ctg_start, ctg_start + window_size, window_step):
            if ((ctg_name, idx) in windows_dict):  # for some windows statistics are computed but the window is not taken for the result
                windows_dict[(ctg_name, idx)][4] += 1
                for stat_idx in range (0, stats_count):
                    windows_dict[(ctg_name, idx)][stat_idx + 5] += float(line_items[stat_idx + 4])

    file.close()


print("Computing mean stats values...")
for key in windows_dict:
    for stat_idx in range (5, stats_count + 5):
        windows_dict[key][stat_idx] = windows_dict[key][stat_idx] / windows_dict[key][4]


print("Writing the output file...")
output_file = open(output_file_name, "w")

output_file.write("contig_name\tstart\tno_intr\tintr_12\tintr_21\tinvalid\tpi1\thetVar1\tss1\tprivate1\ttajd1\tHapCount1\tZnS1\tpi2\thetVar2\tss2\tprivate2\ttajd2\tHapCount2\tZnS2\tFst\tsnn\tdxy_mean\tdxy_min\tgmin\tzx\tdd1\tdd2\tddRank1\tddRank2\tibsMaxB\tibsMean1\tibsMean2\n")
for key in windows_dict:
    values = windows_dict[key]
    line = key[0] + "\t" + str(key [1]) + "\t" + str(values[0]) + "\t" + str(values[1]) + "\t" + str(values[2]) + "\t" + str(values[3])
    for stat_idx in range (5, stats_count + 5):
        line += "\t" + str(values[stat_idx])
    line += "\n"
    output_file.write(line)

output_file.close()
print("Done.")