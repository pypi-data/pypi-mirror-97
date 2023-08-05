import struct

def parse_last_entry(input_string):
    print(input_string)
    print("______________________________")

    input_string_reversed = input_string[::-1]
    ret_string_reversed = []
    for i in range(0, len(input_string)):
        if(input_string_reversed[i] == '#'):
            if(input_string_reversed[i+1] == '#'):
                if(input_string_reversed[i+2] == '#'):
                    j = i + 3
                    while(not(input_string_reversed[j] == '&' and input_string_reversed[j + 1] == '&' and input_string_reversed[j+2] == '&')):
                        ret_string_reversed.append(input_string_reversed[j])
                        j += 1
                    break

    ret_string = ret_string_reversed[::-1]


def parse_input_packet(last_overlap, input_string):
    complete_string = last_overlap
    complete_string += input_string
    x = complete_string.split(b'&&&')
    new_overlap = b''
    ret_array = []
    for data in x:
        if data.endswith(b'###'):
            tmp = data.strip(b'###')
            ret_array.append(tmp)
        else:
            new_overlap = data
    return new_overlap, ret_array

def convert_single_value(value, type):
    if type == "s":
        return None, value
    if type == "f":
        return value[4:], struct.unpack("f", value[:4])[0]
