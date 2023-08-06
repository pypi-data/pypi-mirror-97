from collections import defaultdict
from kuptoo_encoders.encoders.utils.padding import pad_3d
from kuptoo_encoders.encoders.utils.math import zeros

annotation_tags = [
    'unknown',
    'brand',
    'products',
    'creation',
    'complement',
    'feature',
    'anty',
    'bez',
    'dla',
    'do',
    'na',
    'nad',
    'od',
    'po',
    'pod',
    'przeciw',
    'przed',
    'przez',
    'w',
    'z',
    'za',
    'ze',
    'set',
    'noise',
]

measures_tag = [
    'unknown',
    'board_type',
    'cable_type',
    'capacity',
    'cmd2',
    'connector_type',
    'cpu_type',
    'current',
    'data_speed',
    'drive_type',
    'energy_class',
    'focus',
    'fraction',
    'freqency',
    'group',
    'in',
    'inches',
    'ip_type',
    'light_type',
    'lumen',
    'nr',
    'paper_size',
    'pieces',
    'pins',
    'price',
    'product_set',
    'ram',
    'ram_kind',
    'range',
    'resist',
    'resolution',
    'scale',
    'screen_type',
    'screw_type',
    'serial',
    'size',
    'sound',
    'spf',
    'surface',
    'thickness',
    'time',
    'tire_size',
    'voltage',
    'weight',
    'year',
]


class Word2NerEncoder:

    def __init__(self, max_words, tags, smooth=.0, smooth_per_class=None):
        self._smooth_per_class = smooth_per_class if smooth_per_class else {}
        self.max_words = max_words
        self.tags = tags + ['<<pad>>']
        self.tag2idx = {v: k for k, v in enumerate(self.tags)}
        self.idx2tag = {k: v for k, v in enumerate(self.tags)}
        self._dim = len(self.tags)
        self._shape = (self.max_words, self._dim)
        self._type = "float32"
        self._alpha = smooth

    def _smooth(self, y_hot, alpha):
        return (1 - alpha) * y_hot + alpha / self._dim

    @staticmethod
    def _convert(tags):
        word2tag = defaultdict(list)
        for tag_type, tag_words in tags.items():
            for tag_chunk in tag_words:
                tag_words = tag_chunk.split()
                for tag_word in tag_words:
                    word2tag[tag_word].append(tag_type)
        return word2tag

    def _get_tags(self, title, tags):
        vectors = []
        word2tag = self._convert(tags)

        for word in title.split()[0:self.max_words]:
            vec = zeros(self._dim)
            tags = word2tag[word] if word in word2tag else ['unknown']
            for tag in tags:
                tag_idx = self.tag2idx[tag] if tag in self.tag2idx else self.tag2idx['unknown']
                vec[tag_idx] = 1.0

            if self._alpha > 0:
                alpha = self._alpha
                if self._smooth_per_class and len(tags) == 1:
                    tag = tags[0]
                    if tag in self._smooth_per_class:
                        alpha = self._smooth_per_class[tag]

                if alpha > 0:
                    vec = self._smooth(vec, alpha)

            vectors.append(vec)
        return vectors

    def encode(self, data):
        text, tags = data
        tag_vector = self._get_tags(text, tags)
        return pad_3d(tag_vector, self.max_words, self._dim)

    def decode(self, prediction, threshold=.5, sort=False):

        def __get_words(result):
            for vector in result:
                set_of_tags = []
                for idx, x in enumerate(vector):
                    if x >= threshold:
                        set_of_tags.append((self.idx2tag[idx], vector[idx]))
                if sort:
                    set_of_tags = list(sorted(set_of_tags, key=lambda x: x[1], reverse=True))
                yield set_of_tags

        def __get_sentences(prediction):
            for result in prediction:
                yield list(__get_words(result))

        return list(__get_sentences(prediction))

    def shape(self):
        return self._shape

    def type(self):
        return self._type

    def dim(self):
        return self._dim


if __name__ == "__main__":
    import pprint

    wae = Word2NerEncoder(16, measures_tag + annotation_tags, smooth=.2, smooth_per_class={
        "products": 0
    })
    title = "ładny kapsle na monety 21mm / 100 sztuk 1askkda apple air"
    words = title.split()
    a = wae.encode(
        (title,
         {
             "feature": ['ładny'],
             "serial": ["1askkda"],
             "pieces": ["100 sztuk"],
             "size": ["21mm"],
             "brand": ['apple air'],
             "products": ["kapsle", "monety"],
             "na": ["monety", "kapsle"]
         })
    )
    pprint.pprint(wae.decode([a]))

    # idx2tag = {v: k for k, v in wae.tag2idx.items()}
    # for i, x in enumerate(a):
    #     for p, _x in enumerate(x):
    #         if _x>.5:
    #             print(words[i] if len(words) > i else '<pad>', idx2tag[p])
