import hashlib


def cluster_id_to_color(cluster_id):
    h = hashlib.md5(str(cluster_id).encode()).hexdigest()
    return f"#{h[:6]}"