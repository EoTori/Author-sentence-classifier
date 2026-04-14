import math

# This function makes the text into N-grams and returns as list
def make_ngrams(text):
    grams = []
    text = text.lower()

    #Character N-grams with length of 4 - 7 letters (Can be adjusted depending on result)
    for i in range(4, 8):
        for j in range(len(text) - i + 1):
            grams.append(text[j:j+i])

    return grams

# This function opens txt file and processes it into dictionary with N-gram Key and frequency Value
def processtext(text):
    with open(text, "r", encoding="utf-8") as f:
        before_process_lines = [line.strip() for line in f if line.strip()]

    lines = " ".join(before_process_lines)

    letter_list = make_ngrams(lines)
    letter_count = {}
    total_count = 0

    # Used for counting and adding the frequency of appearance
    for letter in letter_list:
        letter_count[letter] = letter_count.get(letter, 0) + 1

    # Used for counting total frequency of everything
    for i in letter_count.values():
        total_count += i

    # Returns above two
    return letter_count, total_count

target_count, target_total = processtext("shakespeare.txt")
other_count, other_total = processtext("other.txt")

# This is function for getting total vocab size in both target_count and other_count
def get_vocab_size(target_count, other_count):
    all_grams = {}

    for gram in target_count:
        all_grams[gram] = 1

    for gram in other_count:
        all_grams[gram] = 1

    return len(all_grams)

# This is the function that gets the probability
def predict_probability(text, target_counts, other_counts, target_total, other_total, vocab_size):
    text = text.lower().strip()
    grams = make_ngrams(text)

    # If user input is too short, it returns None
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
    # Although I have used log and exponential for getting probability that ranges 0.0 - 1.0, this could be modified
    print("Probability:", probability)

    return probability

# This is main function that loops to keep checking user inputs until "exit" is entered by user
def main():
    while True:
        user_check = input("Enter text to be checked: ")
        if user_check.lower() == "exit":
            break
        else:
            probability = predict_probability(user_check, target_count, other_count, target_total, other_total, get_vocab_size(target_count, other_count))
            if probability is None:
                print("Please enter a longer prompt.")
            # I have used probability > 0.5 since the result best came out like that for me, but can be modified depending on result
            elif probability > 0.5:
                print("It's possibly shakespeare's piece.")
            else:
                print("It has low possibility of being shakespeare's piece.")

if __name__ == "__main__":
    main()