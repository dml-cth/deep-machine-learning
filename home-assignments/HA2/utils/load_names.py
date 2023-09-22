import codecs

import numpy as np

population = {
    "Great Britain": 66.04,
    "Ireland": 4.784,
    "U.S.A.": 327.2,
    "Italy": 60.59,
    "Malta": 0.460,
    "Portugal": 10.31,
    "Spain": 46.72,
    "France": 66.99,
    "Belgium": 11.35,
    "Luxembourg": 0.590,
    "the Netherlands": 17.08,
    "East Frisia": 0.465,
    "Germany": 82.79,
    "Austria": 8.773,
    "Swiss": 8.42,
    "Iceland": 0.338,
    "Denmark": 5.749,
    "Norway": 5.285,
    "Sweden": 9.995,
    "Finland": 5.503,
    "Estonia": 1.316,
    "Latvia": 1.95,
    "Lithuania": 2.848,
    "Poland": 38.43,
    "Czech Republic": 10.58,
    "Slovakia": 5.435,
    "Hungary": 9.798,
    "Romania": 19.64,
    "Bulgaria": 7.102,
    "Bosnia and Herzegovina": 3.507,
    "Croatia": 4.154,
    "Kosovo": 1.831,
    "Macedonia": 2.074,
    "Montenegro": 0.622,
    "Serbia": 7.022,
    "Slovenia": 2.066,
    "Albania": 2.873,
    "Greece": 10.77,
    "Russia": 144.5,
    "Belarus": 9.508,
    "Moldova": 3.55,
    "Ukraine": 44.83,
    "Armenia": 2.93,
    "Azerbaijan": 9.862,
    "Georgia": 3.717,
    "Kazakhstan/Uzbekistan,etc.": 71.311,
    "Turkey": 79.81,
    "Arabia/Persia": 32.94,
    "Israel": 8.712,
    "China": 1386,
    "India/Sri Lanka": 1399,
    "Japan": 126.8,
    "Korea": 51.47,
    "Vietnam": 95.54,
}


def char2value(c):
    if c == " ":
        return 0
    else:
        return int(c, 16)


def get_values_from_line(line, use_population_normalizer=True):
    freqs = list(map(char2value, list(line[30:85])))
    if use_population_normalizer:
        pop_list = list(population.values())
        return [
            pop * 2 ** (freq - 10) if freq != 0 else 0
            for freq, pop in zip(freqs, pop_list)
        ]
    else:
        return freqs


def get_name_from_line(line):
    names = []
    name = line[3:29].strip()
    if "+" in name:
        # names.append(name.replace('+', ''))
        # names.append(name.replace('+', '-'))
        names.append(name.replace("+", " "))
    else:
        names.append(name)
    return names


def get_data_from_file(filename):

    # Get name of all countries in the dataset
    countries = []
    with codecs.open(filename, encoding="iso8859-1") as f:
        for i, line in enumerate(f):
            if i >= 177 and i <= 341:
                if len(line.split()) > 2 and "|" not in line:
                    countries.append(line.split("#")[1][:-3].strip())
    names_dict = {c: [] for c in countries}

    # Put each name in its corresponding country
    with codecs.open(filename, encoding="iso8859-1") as f:
        for line in f:
            if line[0] != "#" and line[29] != "+":
                country = countries[
                    np.argmax(
                        get_values_from_line(line, use_population_normalizer=True)
                    )
                ]
                names = get_name_from_line(line)
                for name in names:
                    if (
                        "<" not in name
                        and "" not in name
                        and "" not in name
                        and "" not in name
                        and "" not in name
                    ):
                        names_dict[country].append(name)

    # Drop countries with less than 100 names
    for country in countries:
        if len(names_dict[country]) < 200:
            del names_dict[country]

    return names_dict
