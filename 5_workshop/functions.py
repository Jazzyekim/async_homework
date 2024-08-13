from gc import disable as gc_disable, enable as gc_enable


def count_words(lines: list[str], counter, lock):
    words = {}
    for line in lines:
        word, _, match_count, _ = line.split("\t")
        if word in words:
            words[word] += int(match_count)
        else:
            words[word] = int(match_count)
    with lock:
        counter.value += len(lines)
    return words


def _process_file_chunk(
        file_name: str,
        chunk_start: int,
        chunk_end: int,
) -> dict:
    words = {}
    with open(file_name,  mode="r") as f:
        f.seek(chunk_start)
        gc_disable()
        for line in f:
            chunk_start += len(line)
            if chunk_start > chunk_end:
                break
            word, _, match_count, _ = line.split("\t")
            if word in words:
                words[word] += int(match_count)
            else:
                words[word] = int(match_count)
        gc_enable()
        return words


