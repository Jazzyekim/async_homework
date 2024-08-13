def count_words(lines: list[str]):
    words = {}
    for line in lines:
        word, _, match_count, _ = line.split("\t")
        if word in words:
            words[word] += int(match_count)
        else:
            words[word] = int(match_count)
    return words