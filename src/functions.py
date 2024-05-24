# LIBRARY / MODULE / PUSTAKA

import streamlit as st

import os, re, csv
from collections import defaultdict

import pandas as pd
import emoji
import swifter
from PIL import Image

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download("punkt")
nltk.download("stopwords")

from warnings import simplefilter

simplefilter(action= "ignore", category= FutureWarning)

# DEFAULT FUNCTIONS

"""Make Space

Fungsi-fungsi untuk membuat jarak pada webpage menggunakan margin space dengan
ukuran yang bervariatif.
"""

def ms_20():
    st.markdown("<div class= \"ms-20\"></div>", unsafe_allow_html= True)

def ms_40():
    st.markdown("<div class= \"ms-40\"></div>", unsafe_allow_html= True)

def ms_60():
    st.markdown("<div class= \"ms-60\"></div>", unsafe_allow_html= True)

def ms_80():
    st.markdown("<div class= \"ms-80\"></div>", unsafe_allow_html= True)

"""Make Layout

Fungsi-fungsi untuk layouting webpage menggunakan fungsi columns() dari
Streamlit.

Returns
-------
self : object containers
    Mengembalikan layout container.
"""

def ml_center():
    left, center, right = st.columns([.3, 2.5, .3])
    return center

def ml_split():
    left, center, right = st.columns([1, .1, 1])
    return left, right

def ml_left():
    left, center, right = st.columns([2, .1, 1])
    return left, right

def ml_right():
    left, center, right = st.columns([1, .1, 2])
    return left, right

"""Cetak text

Fungsi-fungsi untuk menampilkan teks dengan berbagai gaya menggunakan method
dari Streamlit seperti write() dan caption().

Parameters
----------
text : str
    Teks yang ingin ditampilkan dalam halaman.

size : int
    Ukuran Heading untuk teks yang akan ditampilkan.

division : bool
    Kondisi yang menyatakan penambahan garis divisi teks ditampilkan.
"""

def show_title(text: str, size: int= 3, division: bool= False):
    heading = "#" if size == 1 else (
        "##" if size == 2 else (
            "###" if size == 3 else "####"
        )
    )

    st.write(f"{heading} {text}")
    st.markdown("---") if division else None

def show_text(text: str):
    st.markdown(f"<div class= \"paragraph\">{text}</div>",
                unsafe_allow_html= True)
    
def show_caption(text: str, size: int= 3, division: bool= False):
    heading = "#" if size == 1 else (
        "##" if size == 2 else (
            "###" if size == 3 else "####"
        )
    )

    st.caption(f"{heading} {text}")
    st.markdown("---") if division else None

"""Load file

Fungsi-fungsi untuk membaca file dalam lokal direktori.

Parameters
----------
filepath : str
    Jalur tempat data tersedia di lokal direktori.
    
Returns
-------
self : object
    Obyek dengan informasi yang berhasil didapatkan.

**kwargs : any
    Argumen untuk diteruskan ke fungsi terkait.
"""

def get_csv(filepath: str, **kwargs):
    return pd.read_csv(filepath, **kwargs)

def get_excel(filepath: str, **kwargs):
    return pd.read_excel(filepath, **kwargs)

def get_img(filepath: str, **kwargs: any):
    return Image.open(filepath, **kwargs)

#-------------------------------------------------------------------------------

def mk_dir(dirpath):
    """Buat folder
    
    Fungsi ini akan memeriksa path folder dari parameter fungsi. Jika tidak ada
    folder sesuai path yang diberikan, maka folder akan dibuat.
    
    Parameters
    ----------
    dirpath : str
        Jalur tempat folder akan dibuat.
    """
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

# CUSTOM FUNCTIONS

def write_unique_words(arr):
    """Menghitung kata unik dan menyimpan frekuensinya ke file CSV

    Fungsi ini digunakan untuk memetakan fitur (kata) yang ada dalam kumpulan
    tweet dan menghitung frekuensi masing-masing kata tersebut. Hasilnya
    disimpan dalam file CSV.

    Parameters
    ----------
    arr : ndarray
        Array yang memuat data tweet (teks) yang akan diolah.
    """
    # Buat dictionary untuk menyimpan jumlah kemunculan setiap kata
    word_counts = defaultdict(int)
    for text in arr:
        # Pisahkan teks menjadi kata-kata individual
        words = text.split()
        # Hitung jumlah kemunculan setiap kata
        for word in words:
            word_counts[word] += 1
    # Tulis semua informasi yang didapat ke dalam file CSV
    with open("./data/corpus/word_counts.csv", "w", newline= "", encoding= \
              "utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Word", "Count"])
        for word, count in word_counts.items():
            writer.writerow([word, count])

def text_cleaning(tweet: str):
    """Text cleaning

    Membersihkan teks tweet dari berbagai karakter yang dianggap tidak berguna
    dalam proses ekstraksi informasi nantinya.

    Fungsi ini akan melakukan pembersihan teks dengan langkah-langkah berikut:
    1. Menghapus URL.
    2. Menghapus mentions (@username).
    3. Menghapus hashtag.
    4. Menghapus karakter escape.
    5. Menghapus angka.
    6. Menghapus tanda baca.
    7. Menghapus emotikon.
    8. Menghapus karakter khusus.
    9. Menghapus karakter tunggal.
    10. Menghapus spasi berlebih.
    11. Menghapus tanda hubung jika berdiri sendiri.
    12. Mengubah semua teks menjadi LowerCase.

    Parameters
    ----------
    tweet : str
        Teks tweet yang akan dibersihkan.

    Returns
    -------
    self : str
        Teks tweet yang telah dibersihkan.
    """
    # Menghapus URL
    tweet = re.sub(r"http\S+|www\S+|https\S+", "", tweet, flags= re.MULTILINE)
    # Menghapus mentions (@username)
    tweet = re.sub(r"@\w+", "", tweet)
    # Menghapus hashtag
    tweet = re.sub(r"#(\w+)", "", tweet)
    # Menghapus semua karakter escape
    tweet = re.sub(r"\\[tnufr]", " ", tweet)
    # Menghapus angka
    tweet = re.sub(r"\d+", "", tweet)
    # Menghapus tanda baca
    tweet = re.sub("[%s]" % re.escape("[!\"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~]"), \
                    "", tweet)
    # Menghapus emoticon
    tweet = emoji.replace_emoji(tweet, replace= "")
    # Menghapus karakter khusus
    tweet = re.sub(r'[^\x00-\x7F]+', '', tweet)
    # Menghapus karakter tunggal
    tweet = re.sub(r"\b[a-zA-Z]\b", "", tweet)
    # Menghapus spasi berlebih
    tweet = " ".join(tweet.split())
    # Menghapus tanda hubung jika berdiri sendiri
    tweet = re.sub(r"\b - \b|\b -\b|\b- \b", " ", tweet)
    # Mengubah semua teks menjadi LowerCase
    tweet = tweet.lower()

    return tweet

def remv_slang(data):
    """
    Mengganti slang-word dengan kata-kata yang sesuai berdasarkan kamus
    slang-word.

    Parameters
    ----------
    data : pandas.Series
        Series yang memuat teks yang akan diolah.

    Returns
    -------
    res : pandas.Series
        Series yang sudah dihilangkan slang word-nya.
    """
    # Dapatkan file dari kamus slang-word
    corpus = pd.read_csv("./data/corpus/slang_word.csv", delimiter= ";")
    # Dictionary kosong untuk menampung slang-word
    slangs = {}
    # Isi dictionary slang-word
    for index, word in corpus.iterrows():
        if word[0] not in slangs:
            slangs[word[0]] = str(word[1])

    # Function untuk menghilangkan slang-word
    def slangs_remover(document):
        """
        Mengganti slang-word di dalam dokumen dengan kata yang sesuai.

        Parameters
        ----------
        document : str
            Teks yang akan diolah.
        
        Returns
        -------
        str
            Teks yang sudah dihilangkan slang word-nya
        """
        return " ".join([slangs[word] if word in slangs else word for word in \
                         document.split()])
    
    # Terapkan fungsi slangs_remover ke setiap elemen di data
    return data.apply(slangs_remover)

@st.cache_data(ttl=3600, show_spinner="Fetching data corpus...")
def stemming(data):
    """Stemming

    Mengubah kata menjadi bentuk dasarnya.

    Parameters
    ----------
    data : pandas.Series
        Series yang memuat teks yang akan distemming.

    Returns
    -------
    pandas.Series
        Series yang sudah distemming.
    """
    # Inisialisasi objek stemmer
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    # Daftar kata yang ingin dikecualikan dari stemming
    exceptions = {"pemilu"}

    # Fungsi pembungkus untuk stemming
    def stemmed_wrapper(term):
        """
        Melakukan stemming pada sebuah kata.

        Parameters
        ----------
        term : str
            Kata yang akan distemming.

        Returns
        -------
        str
            Kata yang sudah distemming.
        """
        if term in exceptions:
            return term
        else:
            return stemmer.stem(term)
    
    # Membuat corpus untuk kamus kata
    corpus = {}
    for document in data:
        for term in document:
            if term not in corpus:
                corpus[term] = " "

    # Melakukan stemming pada setiap kata dalam corpus
    for term in corpus:
        corpus[term] = stemmed_wrapper(term)

    # Fungsi untuk mengganti kata dalam dokumen dengan bentuk stemmed
    def get_stemmed_term(document):
        """
        Mengganti kata dalam dokumen dengan bentuk stemmed.

        Parameters
        ----------
        document : list of str
            Dokumen yang berisi kata-kata.

        Returns
        -------
        list of str
            Dokumen dengan kata-kata yang sudah distemming.
        """
        return [corpus[term] for term in document]
    # Menerapkan stemming pada setiap dokumen
    return data.swifter.apply(get_stemmed_term)

def stopword_removal(data):
    """
    Menghapus kata-kata stopword dari data.

    Parameters
    ----------
    data : pandas.Series
        Data yang berisi teks yang akan diproses, di mana setiap elemen adalah 
        list dari kata-kata.

    Returns
    -------
    pandas.Series
        Data yang berisi teks yang sudah dihapus stopword-nya.
    """
    nltk_corpus = stopwords.words("indonesian")
    self_corpus = pd.read_csv("./data/corpus/stopwords.txt",
                              names= ["stopword"], header= None)
    for i in range(len(self_corpus)):
        nltk_corpus.extend(self_corpus["stopword"][i].split(" "))
    
    corpus = set(nltk_corpus)

    def removes(words):
        """
        Menghapus stopword dari list kata-kata.

        Parameters
        ----------
        words : list of str
            List dari kata-kata yang akan diproses.

        Returns
        -------
        list of str
            List dari kata-kata yang sudah dihapus stopword-nya.
        """
        return [word for word in words if word not in corpus]
    
    return data.apply(removes)
#-------------------------------------------------------------------------------