# Character Frequency Counter using MapReduce

from collections import defaultdict

# MAP: Convert each alphabetic character into (character, 1)
def map_phase(text):
    result = []

    for char in text.lower():
        if char.isalpha():
            result.append((char, 1))

    return result


# REDUCE: Count occurrences of each character
def reduce_phase(mapped_data):
    counts = defaultdict(int)

    for char, value in mapped_data:
        counts[char] += value

    return counts


# Main program
text = input("Enter the dataset: ")

mapped_data = map_phase(text)
result = reduce_phase(mapped_data)

print("\n===== CHARACTER FREQUENCY =====")
for char in sorted(result):
    print(f"{char}: {result[char]}")
