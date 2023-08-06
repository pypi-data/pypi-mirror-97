def create_header(size, type, id):
    return size.to_bytes(4, byteorder='big') + type.to_bytes(1, byteorder='big') + id.to_bytes(1, byteorder='big')


print([x for x in create_header(68, 1, 0)])