FILE_PATH = "./googlebooks-eng-all-1gram-20120701-a"
WORD = "языку"


def count_words(lines: list[str]):
    words = {}
    for line in lines:
        word, _, match_count, _ = line.split("\t")
        if word in words:
            words[word] += int(match_count)
        else:
            words[word] = int(match_count)
    return words


def reduce_words(results_list: list[dict]) -> dict:
    reduced_words = {}
    for words_dict in results_list:
        for key, value in words_dict.items():
            if key in reduced_words:
                reduced_words[key] += value
            else:
                reduced_words[key] = value
    return reduced_words


def main():
    words = {}
    with open(FILE_PATH, "r") as file:
        count_words(file.readlines())
    print("Total words: ", len(words))
    print("Total count of word : ", words[WORD])


if __name__ == "__main__":
    main()
