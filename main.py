import struct

HEADER_FORMAT = "III"


def read_unpack(file, form):
    length = struct.calcsize(form)
    data = file.read(length)
    return struct.unpack(form, data)


def read_header(file):
    ext, length, count = read_unpack(file, HEADER_FORMAT)
    file.seek(length * 4)  # Skip header chunk
    return ext, length, count


def read_data(file):
    result = list()
    ext, length, count = read_header(file)
    # TODO: ext is the additional points count. Source dataset and classes files does not contain them, I do not know
    #  where they come from)
    for i in range(0, count):
        result.append(read_unpack(file, f"{length}f"))
    return result


def read_classes(file):
    result = list()
    ext, length, count = read_header(file)
    for i in range(0, count):
        result.extend(read_unpack(file, f"{length}I"))
    result = result[:ext]
    return result


def main():
    with open("BUTAR.DS", "rb") as f:
        data_subset = read_data(f)

    with open("BUTAR.DF", "rb") as f:
        data_full = read_data(f)

    with open("BUTAR.CS", "rb") as f:
        class_subset = read_classes(f)

    with open("BUTAR.CF", "rb") as f:
        class_full = read_classes(f)
    print(f"DF probes count: {len(data_full)}")
    print(f"DS probes count: {len(data_subset)}")
    print(f"CF probes count: {len(class_full)}")
    print(f"CS probes count: {len(class_subset)}")


if __name__ == '__main__':
    main()
