Script that parses the output of the [FILET](https://github.com/kr-colab/FILET/) pipeline and transforms it into one file with one line per window in the following format:

`contig_name  window_position no_intr_cnt intr_1_2_cnt  intr_2_1_cnt`

where `no_intr_cnt`, `intr_1_2_cnt` and `intr_2_1_cnt` are the number of times this window was classified as belonging to respectively "no introgression", "introgression 1 -> 2" and "introgression 2 -> 1" categories.

If all the windows in the output files are non overlapping, the total sum of the three last columns will be equal to 1. If some windows are overlapping, the three last columns will contain the number of times this window was classified in the corresponding categories.
