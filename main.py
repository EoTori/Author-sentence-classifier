import math

def make_ngrams(text):
    grams = []
    text = text.lower()

    for i in range(4, 8):
        for j in range(len(text) - i + 1):
            grams.append(text[j:j+i])

    return grams

def processtext(text):
    with open(text, "r", encoding="utf-8") as f:
        before_process_lines = [line.strip() for line in f if line.strip()]

    lines = " ".join(before_process_lines)

    letter_list = make_ngrams(lines)
    letter_count = {}
    total_count = 0

    for letter in letter_list:
        letter_count[letter] = letter_count.get(letter, 0) + 1

    for i in letter_count.values():
        total_count += i

    return letter_count, total_count

target_count, target_total = processtext("shakespeare.txt")
other_count, other_total = processtext("other.txt")

def get_vocab_size(target_count, other_count):
    all_grams = {}

    for gram in target_count:
        all_grams[gram] = 1

    for gram in other_count:
        all_grams[gram] = 1

    return len(all_grams)

def predict_probability(text, target_counts, other_counts, target_total, other_total, vocab_size):
    text = text.lower().strip()
    grams = make_ngrams(text)

    if len(grams) == 0:
        return None

    target_score = 0
    other_score = 0

    for gram in grams:
        if gram in target_counts:
            target_count = target_counts[gram]
        else:
            target_count = 0

        if gram in other_counts:
            other_count = other_counts[gram]
        else:
            other_count = 0

        target_prob = (target_count + 1) / (target_total + vocab_size)
        other_prob = (other_count + 1) / (other_total + vocab_size)
        target_score += math.log(target_prob)
        other_score += math.log(other_prob)

    diff = ((target_score - other_score)/ len(grams))
    probability = 1 / (1 + math.exp(-diff))
    print("Probability:", probability)
    return probability

def main():
    while True:
        user_check = input("Enter text to be checked: ")
        if user_check.lower() == "exit":
            break
        else:
            probability = predict_probability(user_check, target_count, other_count, target_total, other_total, get_vocab_size(target_count, other_count))
            if probability is None:
                print("Please enter a longer prompt.")
            elif probability > 0.5:
                print("It's possibly shakespeare's piece.")
            else:
                print("It has low possibility of being shakespeare's piece.")

if __name__ == "__main__":
    main()