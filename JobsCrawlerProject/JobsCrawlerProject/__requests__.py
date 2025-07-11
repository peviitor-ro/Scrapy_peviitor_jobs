

def get_curl_requests():
    try:
        from curl_cffi import requests
        return requests
    except ImportError:
        raise RuntimeError("curl_cffi nu este instalat")
