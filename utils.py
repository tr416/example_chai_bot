def truncate(text, max_len):
    for end in reversed(range(max_len)):
        if text[end] in '.!?~"':
            break
    if end <= 1:
        for end in range(max_len, len(text)):
            if text[end] in '.!?~"':
                break
    return text[:end + 1]
