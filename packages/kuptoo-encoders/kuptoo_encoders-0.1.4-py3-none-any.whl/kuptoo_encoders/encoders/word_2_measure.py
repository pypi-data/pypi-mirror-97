import re
from collections import defaultdict
from fractions import Fraction
import numpy as np


class Word2Measure:

    def __init__(self, max_chars, skip_if_in=None):

        self.skip_if_in = skip_if_in
        self._alpha_numerics = {
            "ilość pokoi": ['pokojowy'],
            "baterie": ['komorowy'],
            "ilość szuflad": ['szufladowy'],
            "ilość biegów": ['biegowy']
        }

        self._measures = {
            "prędkość danych": ['mb/s', 'kb/s', 'gb/s', 'tb/s', 'mbps', 'kbps', 'km/s', 'm/s'],
            "prędkość": ['mph', 'km/h'],
            "spalanie": ['l/km', 'l/h'],
            "udział": ['proc', '%'],
            "czas": ['sek', 's', 'ms', 'ns', 'μs', 'nanosek', 'milisek', 'min', 'h', 'godz'],
            "ciśnienie": ['mmhg', 'pa', 'hpa', 'kpa', 'mbar', 'bar'],
            "ciężar": ['kilo', 'kg', 'kilogram', 'gr', 'gram', 'gr.', 'g', 'dg', 'dgram', 'dekagram', 't', 'ton', 'lb'],
            "objętość": ['l', 'ml', 'hl', 'fl.oz.', 'fl.oz', 'oz', "F, nF, mF, μF"],
            'pamięć': ['mb', 'kb', 'gb', 'tb'],
            "oporność": ['kohm', 'ohm', 'Ω', 'μΩ', 'kΩ'],
            "średnica": ['ø', 'fi'],
            "częstotliwość": ['μhz', 'hz', 'khz', 'ghz'],
            "moc": ['w', 'mw', 'kw', 'km', 'wat', 'watt'],
            "siła": ['nm', 'n/m', 'n', 'kn', 'mn'],
            "energia": ['μv', "v", 'kv', 'mv', 'kwh', 'mwh', 'kj', 'μa', 'µa', 'ma', 'a', 'ka', 'ah', 'mah', 'kah'],
            'kaloryczność': ['°c', 'c', 'f', '°f', 'k', '°k'],
            "jasność": ['lm', 'lx', 'nx', 'mx', 'cd·sr/m2', 'cd'],
            "głośność": ['db', 'dbi', 'dbm'],
            "powierzchnia": ['ha', 'ar', 'm2', 'mm2', 'cm2', 'ha', 'm3', 'm³', 'mm3', 'cm3', 'dm3', 'km3',
                             'm.kw.'],
            "rozmiar": ['mm', 'm', 'dm', 'km', 'cm', 'inch', '"', 'in', 'cali', 'cala', 'metrów', 'centymetrów',
                        'decymetrów', 'ft', 'metr.', 'metra'],
            "rozdzielczość": ['p', 'i', 'px', 'pix'],
            "obroty": ['rpm'],
            "pojemność silnika": ['tdi', 'tdci', 'jtd', 'hdi', 'tsi', 'fsi', 'vti', 'dci', 'dti'],
            "cena": ['pln', 'zł', '$'],
            'ilość': ['szt', 'szt.', 'sztuk', 'sztuka', 'el', 'elementów', 'elem.', 'kpl', 'kompletów', 'kaps.'],
            'rok': ['r', 'rok', 'year', 'month', 'months', 'lat']
        }
        self._measure_type_dict = {m: i for i, m in enumerate(self._measures.keys())}
        self._measure_type_dim = max(self._measure_type_dict.values()) + 1
        self._measure2type = defaultdict(list)
        for t, measures_list in self._measures.items():
            _idx = self._measure_type_dict[t]
            for measure_unit in measures_list:
                self._measure2type[measure_unit].append(_idx)

        self.measures = [m for type, measures in self._measures.items() for m in measures]
        self._measure2idx = {v: k for k, v in enumerate(self.measures)}

        self._max_chars = max_chars
        self._char_features_dim = 10
        self._no_of_measures = len(self.measures)
        self._measure_dim = self._no_of_measures * 3

        self.dim = self._max_chars + self._char_features_dim + self._measure_dim + self._measure_type_dim
        base = 20
        self._char2idx = {
            "1": -101 / base,
            "2": -102 / base,
            "3": -103 / base,
            "4": -104 / base,
            "5": -105 / base,
            "6": -106 / base,
            "7": -107 / base,
            "8": -108 / base,
            "9": -109 / base,
            "0": -110 / base,
            ".": -10 / base,
            ",": -11 / base,
            "/": -12 / base,
            "-": -14 / base,
            "+": -15 / base,
            "=": -20 / base,
            " ": 30 / base,
            "q": 40 / base,
            "w": 41 / base,
            "e": 42 / base,
            "r": 43 / base,
            "t": 44 / base,
            "y": 45 / base,
            "u": 46 / base,
            "i": 47 / base,
            "o": 48 / base,
            "p": 49 / base,
            "a": 50 / base,
            "s": 51 / base,
            "d": 52 / base,
            "f": 53 / base,
            "g": 54 / base,
            "h": 55 / base,
            "j": 56 / base,
            "k": 57 / base,
            "l": 58 / base,
            "z": 60 / base,
            "x": 61 / base,
            "c": 62 / base,
            "v": 63 / base,
            "b": 64 / base,
            "n": 65 / base,
            "m": 66 / base,
            "<": -71 / base,
            ">": -72 / base,
            "{": -75 / base,
            "}": -76 / base,
            "[": -78 / base,
            "]": -79 / base,
            "(": -82 / base,
            ")": -83 / base,
            "\"": -90 / base,
            "'": -91 / base,
            "$": -99 / base,
        }
        self._idx2char = {v: k for k, v in self._char2idx.items()}
        self._measures_escaped = [re.escape(m) for m in self.measures]
        self._measure_reg = r'^(((\d+[.,\/]\d+|\d+)\s*x\s*)?(\d+[.,\/]\d+|\d+)\s*[x-]\s*)?(\d+[.,\/]\d+|\d+)\s*(' \
                            + "|".join(sorted(self._measures_escaped, reverse=True, key=lambda x: len(x))) \
                            + ')$'

        self._measure_reg = re.compile(self._measure_reg, re.IGNORECASE | re.UNICODE)
        self._serial_reg = r'^[a-z0-9\-\/\.]+$'
        self._serial_reg = re.compile(self._serial_reg, re.IGNORECASE | re.UNICODE)
        self._number_reg = r'^(?:(\d+(?:[.,]\d+)?)?\s*[x]\s*)?(\d+(?:[.,]\d+)?)\s*x\s*(\d+(?:[.,]\d+)?)|' \
                           r'(\d+(?:[.,]\d+)?\s*[-]\s*\d+(?:[.,]\d+)?)|' \
                           r'(\d+[\/]\d+)|' \
                           r'(\d+[.,]\d+|\d+)$'
        self._number_reg = re.compile(self._number_reg, re.IGNORECASE | re.UNICODE)

    @staticmethod
    def _fraction(value):
        try:
            return Fraction(value)
        except ZeroDivisionError:
            return 0.

    def __getitem__(self, item):

        if self.skip_if_in and item in self.skip_if_in:
            return np.zeros(self.dim)

        if not isinstance(item, str):
            item = str(item)

        char_encoded_vector = np.zeros(self._max_chars)
        measure_vector = np.zeros(self._measure_dim)
        char_feature_vector = np.zeros(self._char_features_dim)
        measure_type_vector = np.zeros(self._measure_type_dim)

        is_numeric_flag = False
        is_measure_flag = False

        # encode features
        m = self._number_reg.match(item)
        if m:
            _3d_number1, _3d_number2, _3d_number3, _range_number, _fraction_number, _number = m.groups()
            if _number:
                char_feature_vector[0] = 1
                # char_feature_vector[0] = float(_number.replace(",", "."))  # numeric
            elif _range_number:
                char_feature_vector[1] = 1
                # value1, value2 = _range_number.split('-')
                # char_feature_vector[1] = 0.
                # char_feature_vector[2] = float(value1.replace(",", "."))
                # char_feature_vector[3] = float(value2.replace(",", "."))
            elif _fraction_number:
                char_feature_vector[2] = 1
                # value1, value2 = _fraction_number.split('/')
                # char_feature_vector[1] = 0.
                # char_feature_vector[2] = float(value2)
                # char_feature_vector[3] = self._fraction(_fraction_number)
            elif _3d_number1 or _3d_number2 or _3d_number3:
                char_feature_vector[3] = 1
                # char_feature_vector[1] = float(_3d_number1.replace(",", ".")) if _3d_number1 else 0.
                # char_feature_vector[2] = float(_3d_number2.replace(",", ".")) if _3d_number2 else 0.
                # char_feature_vector[3] = float(_3d_number3.replace(",", ".")) if _3d_number3 else 0.

            # is_numeric_flag = True
        elif item.isalpha():
            char_feature_vector[7] = 1.0  # alpha
        elif self._serial_reg.match(item):
            char_feature_vector[8] = 1.0  # serial
        else:
            char_feature_vector[9] = 1.0  # other

        # encode measures

        m = self._measure_reg.match(item)
        if m:
            # print(m.groups())
            _, _, value1, value2, value3, measure = m.groups()
            value1 = self._fraction(value1.replace(",", ".")) if value1 is not None else 0
            value2 = self._fraction(value2.replace(",", ".")) if value2 is not None else 0
            value3 = self._fraction(value3.replace(",", ".")) if value3 is not None else 0

            # find position in measure vector
            # if measure in self._measure2idx:
            # ω
            if measure in self._measure2idx:
                position = self._measure2idx[measure]

                measure_vector[position * 3 + 0] = value1 if value1 < 100000 else 0
                measure_vector[position * 3 + 1] = value2 if value2 < 100000 else 0
                measure_vector[position * 3 + 2] = value3 if value3 < 100000 else 0
            else:
                print("Unknown measure {}".format(measure))

            measure_type_idxes = self._measure2type[measure]
            for _measure_idx in measure_type_idxes:
                measure_type_vector[_measure_idx] = 1.0

            is_measure_flag = True

        if not is_measure_flag and not is_numeric_flag:

            # encode chars

            for i, c in enumerate(item[-self._max_chars:]):
                if c in self._char2idx:
                    char_encoded_vector[i] = self._char2idx[c]

        return np.concatenate([char_encoded_vector, char_feature_vector, measure_vector, measure_type_vector])

    def __contains__(self, item):
        return True

    def decode(self, vector):
        for v in vector:
            v = int(v)
            if v in self._idx2char:
                print(v, self._idx2char[v])

if __name__ == "__main__":
    e = Word2Measure(10)
    x= e['24150237020140050905205a']
    print(x)
    print(e.decode(x))