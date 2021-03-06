import csv
from nltk.corpus import stopwords as nltk_stopwords
from nltk.stem.porter import *
from collections import Counter


"""
    Chances are if you're reading this comment you're mainly going to want 2 main functions:
        get_captions(ext="") - gets the captions in the form {i : [word_int, word_int, ...]}
        get_words(word_indexes, ext="") - gets the string generated by the given list of word indexes
        get_lookup(ext="") - gets the raw word lookup table for you to use yourself
    get_words DOES open a file every time it is called, so you might want to load in the lookup table with get_lookup
    into your own code and use that if you are calling get_words a lot.

    Run this function once in order to create the files of teh cleaned captions.
    The function that does all the work is vectorize_captions, which is called twice in main
    with no extension (functionally the "default") and usuing the "withstop" extension, which is
    the captions with stopwords included.
"""


def load_captions(filename):
    """
        filename : path to a csv file of captions
        returns the captions as a dictionary
        from index to caption as a string.
    """
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        lines = list(reader)
        # lines = [caption for caption in lines]
        # lines = [caption for name, caption in lines]
    
    
    # return dict(lines)
    return lines


def clean_captions(captions, stopwords=set(), do_stem=True):
    """
        captions : dict from index to caption as a string
        returns a dict with the values replaced with lists of words
    """
    new_captions = []
    if do_stem:
        stemmer = PorterStemmer()
    for idx, (name, caption) in enumerate(captions):
        # Strip and split the caption
        new_caption = []
        for s in caption.split():
            s = s.strip('\'".,?!-;:/')
            if s == "" or s in stopwords:
                continue
            if do_stem:
                s = stemmer.stem(s)
            # 
            if set('1234567890') & set(s):
                s = '#'
            new_caption.append(s)

        new_captions.append((name, new_caption))
    return new_captions

def get_text_corpus(filename):
    """
        filename : path to a csv file of captions
        returns the captions as a large string
    """
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        lines = list(reader)
    s = ''
    for line in lines:
        s += line[1]
    with open('tmp.txt', 'w') as f2:
        f2.write(s)
    
    return s


def get_vocab(captions):
    """
        captions : dict from index to caption as a string
        returns the non-stopword vocabulary of captions as a set
    """
    vocab = set()
    for _, caption in captions.items():
        vocab |= set(caption)
    return vocab

def vectorize_captions(caption_file, ext="", stopwords=set(), do_stem=True):
    """
        filename : path to captions.csv
        ext : extension to append to output filenames
        stopwords : set of stopwords to use, if any
        do_stem : boolean, stems words if True

        This function will create 2 files in data/
            captions_lookup_*ext* : list of the plain strings of the words
            captions_*ext* : csv of the captions but in the format:
                i 5 456 67 10 15
                where i is the index of the caption, and the numbers are the caption
                described with the index of each word in captions_lookup
            the words are sorted by number of occurences
    """
    ext += '.txt'
    captions = load_captions(caption_file)
    captions = clean_captions(captions, stopwords, do_stem=do_stem) 
    corpus = []

    for _, caption in captions:
        corpus += caption
    counts = Counter(corpus).most_common()
    words = [s for s, _ in counts]
    with open("../data/captions_lookup" + ext, "w") as f:
        f.writelines([word + '\n' for word in words])

    word_lookup = {}
    for idx, word in enumerate(words):
        word_lookup[word] = idx

    lines = []
    for name, caption in captions:
        new_caption = list(map(str, map(word_lookup.get, caption)))
        full_list = [name] + new_caption
        lines.append(','.join(full_list))
    with open("../data/captions" + ext, "w") as f:
        f.writelines([line + '\n' for line in lines])

def get_captions(ext=""):
    """
        returns a dictionary from index to integer word indexes
        of the captions saved the the extension ext
    """
    if ext != '':
        ext = '_' + ext
    with open("../data/captions" + ext + '.txt', "r") as f:
        reader = csv.reader(f)
        lines = list(reader)
    captions = {}
    for line in lines:
        line = list(map(int, line))
        captions[line[0]] = line[1:]
    return captions

def get_words(word_indexes, ext=""):
    """
        words : list of integers

        returns a string reconstruction of the given words
    """
    if ext != '':
        ext = '_' + ext
    with open("../data/captions_lookup" + ext + '.txt', "r") as f:
        reader = csv.reader(f)
        words = list(reader)
    return ' '.join([words[i][0] for i in word_indexes])

def get_lookup(ext=""):
    """
        Returns the list of words used to lookup indexes with extension ext
    """
    if ext != '':
        ext = '_' + ext
    with open("../data/captions_lookup" + ext + '.txt', "r") as f:
        reader = csv.reader(f)
        words = list(reader)
    return [word[0] for word in words]

def main():
    # caption_file = '../data/captions.csv'
    caption_file = '../data/flickr_captions.csv'
    # Note:
    # Vocab without stemming: 9k
    # Vocab with stemming: 6.5k
    
    # vectorize_captions(caption_file, stopwords=nltk_stopwords.words('english'))
    # vectorize_captions(caption_file, ext='withstop')
    # vectorize_captions(caption_file, stopwords=nltk_stopwords.words('english'), do_stem=False, ext='nostem')


    # This code visualizes the effect of running the transformation
    # captions_orig = load_captions(caption_file)
    # captions = get_captions()
    # for i in range(20):
    #     if i in captions:
    #         print('Before:', captions_orig[i])
    #         print('After: ', get_words(captions[i]))
    #         print()



if __name__ == '__main__':
    main()