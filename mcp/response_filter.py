def filter_response(response: str):
    blacklist = ["password", "secret", "token"]
    for word in blacklist:
        if word in response.lower():
            return "[REDACTED]"
    return response
