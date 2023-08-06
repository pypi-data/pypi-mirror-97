import hashlib

default_salt: str = "3CD13NwnvxQmwc3WLaeE"


def get_user_id_with_uid(user_hash, salt=default_salt):
    """
      params: user_hash and salt
      return: user_id
    """
    user_list = {}

    while len(user_hash) < 32:
        user_hash = f'0{user_hash}'

    for i in range(100000):
        text = str(i) + salt
        hash_object = hashlib.md5(text.encode('utf-8'))
        user_list[hash_object.hexdigest()] = str(i)

    return user_list[user_hash]


def get_user_hash(id, salt=default_salt):
    to_hash = str(id) + salt
    return hashlib.md5(to_hash.encode('utf-8')).hexdigest()
