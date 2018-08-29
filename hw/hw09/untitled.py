ints = make_integer_stream(1)
twos = scale_stream(ints, 2)
threes = scale_stream(ints, 3)
m = merge(twos, threes)
stream_to_list(m, 10)

[2, 3, 4, 6, 8, 9, 10, 12, 14, 15]