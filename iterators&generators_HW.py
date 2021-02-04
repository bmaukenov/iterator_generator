import wikipedia
import json
import hashlib


class CountriesIterator():
    def __init__(self, file_path):
        self.start = -1
        with open(file_path, encoding="utf-8") as f:
            json_data = json.load(f)
            self.end = len(json_data)

    def __iter__(self):
        return self

    def __next__(self):
        self.start += 1
        if self.start == self.end:
            raise StopIteration
        return self.country_search(self.start)

    def country_search(self, n):
        with open("countries.json") as f:
            json_data = json.load(f)
            country = json_data[n]["name"]["common"]
        try:
            link = wikipedia.page(country, auto_suggest=False).url
        except wikipedia.exceptions.DisambiguationError:
            for spelling in json_data[n]["altSpellings"]:
                try:
                    country = spelling
                    link = wikipedia.page(country, auto_suggest=False).url
                except wikipedia.exceptions.DisambiguationError:
                    continue
                else:
                    break
        with open("final-countries-links.txt", "a") as new_file:
            new_file.write(f"{country} - {link} \n")
        return link


def hash_Lines(file_path):
    with open(file_path, "r") as f:
        start = 0
        end = 10
        while start <= end:
            data = f.readline()
            hashed_data = hashlib.md5(data.encode()).hexdigest()
            yield hashed_data
            start += 1


if __name__ == "__main__":
    for item in CountriesIterator("countries.json"):
        print(item)
    for hash_data in hash_Lines('countries.json'):
        print(f'hash: {hash_data}')
