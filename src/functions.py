# LIBRARY / MODULE / PUSTAKA

import streamlit as st

import os, itertools

import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

import nltk

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

#-------------------------------------------------------------------------------