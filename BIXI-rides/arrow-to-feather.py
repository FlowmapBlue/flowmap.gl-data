import sys
import pyarrow.feather as feather

input_file = sys.argv[1]
output_file = sys.argv[2]
# zstd is smaller than lz4 but might be slower
# https://arrow.apache.org/docs/python/feather.html#using-compression
compression = sys.argv[3]

df = feather.read_table(input_file)
feather.write_feather(df, output_file, compression=compression)
