import hashlib
from datetime import datetime


def validate_checksum(
        request: dict,
        shared_secret: str,
        salt: str = "",
        time_delta: int = 5,
        checksum_key: str = "checksum"
) -> bool:
    """
    Use this method to validate a dict with a given checksum

    :param request: The dictionary with all parameters
    :param shared_secret: Shared secret the request is hashed with
    :param salt: Additional salt to use. Defaults to empty str
    :param time_delta: Time delta (+ and -) the requests should be valid, in seconds
    :param checksum_key: The key to access to checksum in request. Defaults to "checksum".

    :return: bool
    """
    # Get current (utc) timestamp
    current_timestamp = int(datetime.utcnow().timestamp())

    # Save checksum and delete from dict
    if checksum_key not in request:
        raise ValueError("Missing " + checksum_key + " as checksum key in request")
    checksum = request[checksum_key]
    del request[checksum_key]

    # Build sorted list
    sorted_request = [key + str(request[key]) for key in sorted(request)]

    # Build static_str
    static_str = "".join([str(x) for x in sorted_request])

    # Append with shared_secret
    static_str += shared_secret

    # Iterate over the last +- time_delta timestamps
    for i in range(-time_delta, time_delta):
        tmp_timestamp = current_timestamp + i

        # Append static_str with timestamp
        not_so_static_str = static_str + str(tmp_timestamp)

        # Add salt and hash with SHA512
        hashed = hashlib.sha512((salt + not_so_static_str).encode("utf-8")).hexdigest()
        if hashed == checksum:
            return True
    return False


def get_checksum(
        request: dict,
        shared_secret: str,
        salt: str = ""
) -> str:
    """
    Use this method to retrieve a checksum of a given dict

    :param request: The dictionary with all parameters
    :param shared_secret: Shared secret the request is hashed with
    :param salt: Additional salt to use. Defaults to empty str

    :return: Checksum str
    """
    # Get current (utc) timestamp
    current_timestamp = int(datetime.utcnow().timestamp())

    # Build sorted list
    sorted_request = [key + str(request[key]) for key in sorted(request)]

    # Build static_str
    static_str = "".join([str(x) for x in sorted_request])

    # Append with shared_secret
    static_str += shared_secret

    # Append with timestamp
    static_str += str(current_timestamp)

    # Add salt and hash with SHA512
    hashed = hashlib.sha512((salt + static_str).encode("utf-8")).hexdigest()

    return hashed
