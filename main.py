import string
import random


# https://en.wikipedia.org/wiki/Letter_frequency
freq = {
    'a': 0.082,
    'b': 0.015,
    'c': 0.028,
    'd': 0.043,
    'e': 0.127,
    'f': 0.022,
    'g': 0.020,
    'h': 0.061,
    'i': 0.070,
    'j': 0.0015,
    'k': 0.0077,
    'l': 0.04,
    'm': 0.024,
    'n': 0.067,
    'o': 0.075,
    'p': 0.019,
    'q': 0.00095,
    'r': 0.060,
    's': 0.063,
    't': 0.091,
    'u': 0.028,
    'v': 0.0098,
    'w': 0.024,
    'x': 0.0015,
    'y': 0.02,
    'z': 0.00074,
    ',': 0.0,
    '.': 0.0,
    '/': 0.0,
    ';': 0.0,
}

print(sum(freq.values()))


class Layout:
    def __init__(self):
        self.dimensions = (3, 10)
        self.keys = [['' for _ in range(self.dimensions[1])]
                     for _ in range(self.dimensions[0])]

    def randomize(self):
        unused = list(string.ascii_lowercase + ',./;')

        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                letter = random.choice(unused)
                self.keys[i][j] = letter
                unused.remove(letter)

    def __repr__(self):
        final = ''
        for row in self.keys:
            final += ' '.join(row[:5])
            final += '\t'
            final += ' '.join(row[5:])
            final += '\n'
        return final

    def score(self, frequencies):
        row_priorities = (0.5, 2.0, 0.2)
        score = 0
        for i in range(self.dimensions[0]):
            for key in self.keys[i]:
                score += (freq[key] * row_priorities[i]) ** 2
        return score


def combine_layouts(a: Layout, b: Layout):
    new = Layout()
    tries = 1
    for _ in range(tries):
        used = []
        success = True
        for i in range(a.dimensions[0]):
            if not success:
                break
            for j in range(a.dimensions[1]):
                if not success:
                    break
                if a.keys[i][j] in used and b.keys[i][j] in used:
                    success = False
                    break

                k = random.choice((a.keys[i][j], b.keys[i][j]))
                while k in used:
                    k = random.choice((a.keys[i][j], b.keys[i][j]))
                new.keys[i][j] = k
                used.append(k)

        if success:
            return new
    return None


def main():
    COUNT = 1000
    TOP = 100
    ITERATIONS = 10000

    layouts = [Layout() for _ in range(COUNT)]
    for layout in layouts:
        layout.randomize()
    best = layouts[0]

    for i in range(ITERATIONS):
        print(f'iteration {i}...')
        layouts.sort(key=lambda layout: layout.score(freq), reverse=True)
        if layouts[0].score(freq) > best.score(freq):
            best = layouts[0]
            print(f'new best, score={best.score(freq)}')
            print(best)
        layouts = layouts[:TOP]
        for _ in range(COUNT - TOP):
            c = None
            while c is None:
                a = random.choice(layouts[:TOP])
                b = random.choice(layouts[:TOP])
                c = combine_layouts(a, b)

            layouts.append(c)

    print('#' * 40)
    print(best)


if __name__ == "__main__":
    main()
