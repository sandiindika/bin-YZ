# Library / module / pustaka
import streamlit as st
from streamlit import session_state as ss
from streamlit_option_menu import option_menu

from functions import *
from warnings import simplefilter

# intruksi untuk mengabaikan semua peringatan dalam kategori `FutureWarning`
simplefilter(action= "ignore", category= FutureWarning)

# Page config
st.set_page_config(
    page_title= "App", layout= "wide", initial_sidebar_state= "expanded",
    page_icon= get_img("./assets/favicon.ico")
)

# Hide menu, header, and footer
st.markdown(
    """<style>
        #MainMenu { visibility: hidden; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
        .st-emotion-cache-1jicfl2 { padding-top: 2rem; }
    </style>""",
    unsafe_allow_html= True
)

# CSS on style.css
with open("./css/style.css") as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html= True)

# Params setting
message = False
menu_ = ["Beranda", "Data Tweets", "Pemrosesan Teks", "Pembobotan Teks"]
icons_ = ["house", "database", "code-slash", "layout-text-sidebar"]

# Exception message function
def _exceptionMessage(e):
    """Tampilkan pesan galat
    
    Parameters
    ----------
    e : exception object
        Obyek exception yang tersimpan.
    """
    ms_20()
    with ml_center():
        # Tampilkan pesan galat jika kondisi memenuhi
        st.error("Terjadi masalah...")
        st.exception(e) if message else None

# Halaman beranda
def _pageBeranda():
    """Page beranda
    
    Halaman ini akan menampilkan judul sistem dan abstrak dari proyek.
    """
    try:
        ms_20()
        show_title("Implementasi Metode Logistic Regression Dalam Analisis \
                   Sentimen Twitter Terhadap Perkembangan AI ChatGPT",
                   size= 2, division= True)
        ms_40()
        # Tampilkan teks abstrak
        with ml_center():
            with open("./assets/abstract.txt", "r") as f:
                abstract = f.read()
            show_text(abstract)
    except Exception as e:
        _exceptionMessage(e)

# Halaman data tweets
def _pageDataTweets():
    """Page data twwets
    
    Halaman ini akan menampilkan DataFrame yang berisi data tweets yang telah \
    memiliki label untuk di olah.
    """
    try:
        ms_20()
        show_title("Data Tweets", division= True)
        ms_40()
        # Dapatkan file .csv yang menyimpan data tweet
        df = get_csv("./data/dataframe/tweets.csv", delimiter= ";")
        # Tampilkan DataFrame dari data yang telah didapatkan
        st.dataframe(df, height= 600, use_container_width= True,
                     hide_index= True)
    except Exception as e:
        _exceptionMessage(e)
#-------------------------------------------------------------------------------
# Body
with st.container():
    # Navigation
    with st.sidebar:
        selected = option_menu(
            menu_title= "", options= menu_, icons= icons_,
            styles= {
                "container": {"padding": "0 !important",
                            "background-color": "#E6E6EA"},
                "icon": {"color": "#020122", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "left",
                            "margin": "0", "color": "#020122"},
                "nav-link-selected": {"background-color": "#F4F4F8"}
            }
        )
        ms_60()
        show_caption("Copyright © 2024 | Yafi Zafran", size= 5)

    # Branching halaman yang ditampilkan
    if selected == menu_[0]:
        _pageBeranda()
    elif selected == menu_[1]:
        _pageDataTweets()