from rc_protocol import get_checksum

SHARED_SECRET = "s3cr3t_p@ssw0rd"

my_dict = {
    "key1": "value1",
    "key2": "value2"
}

my_dict["checksum"] = get_checksum(my_dict, SHARED_SECRET)
print(my_dict["checksum"])
