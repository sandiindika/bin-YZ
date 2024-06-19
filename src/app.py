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
message = True
menu_ = ["Beranda", "Data Tweets", "Pemrosesan Teks", "Pembobotan Teks",
         "Analisis", "Prediksi"]
icons_ = ["house", "database", "code-slash", "layout-text-sidebar",
          "bar-chart"]

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
        if message:
            st.exception(e)

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
        df = get_csv("./data/dataset/tweets.csv", delimiter= ";")
        # Tampilkan DataFrame dari data yang telah didapatkan
        st.dataframe(df, height= 600, use_container_width= True,
                     hide_index= True)
    except Exception as e:
        _exceptionMessage(e)

# Halaman pemrosesan teks
def _pageTextPreprocessing():
    """Page pemrosesan teks

    Halaman ini akan menampilkan data tweets yang telah di proses untuk setiap
    tahapan sesuai dengan alur dalam pemrosesan teks.
    """
    try:
        ms_20()
        show_title("Pemrosesan Teks", division= True)
        ms_40()
        # Dapatkan file .csv yang menyimpan data tweet
        ori_text = get_csv("./data/dataset/tweets.csv", delimiter= ";")
        # Buat DataFrame untuk menampung hasil pemrosesan teks
        pre_text = pd.DataFrame()
        # Pemrosesan text cleaning
        pre_text["text_cleaning"] = ori_text.iloc[:, 0].apply(text_cleaning)
        # Simpan unique word untuk identifikasi lebih lanjut
        write_unique_words(pre_text["text_cleaning"].values)
        # Pemrosesan slang-word removal
        pre_text["slang_removal"] = remv_slang(pre_text["text_cleaning"])
        # Pemrosesan tokenization
        pre_text["tokenization"] = pre_text["slang_removal"].apply(lambda x: word_tokenize(x))
        with st.spinner("Please wait..."):
            # Pemrosesan stemming
            pre_text["stemming"] = stemming(pre_text["tokenization"])
        # Pemrosesan stopword-removal
        pre_text["stopword_removal"] = stopword_removal(pre_text["stemming"])
        # Final Result
        pre_text["final"] = pre_text["stopword_removal"].apply(lambda x: " ".join(x))
        # View result
        with st.expander("**Original Tweets**", expanded= True):
            # Tampilkan DataFrame untuk teks tweet sebelum text cleaning
            st.dataframe(ori_text.iloc[:, 0], height= 500,
                         use_container_width= True, hide_index= True)
        with st.expander("**Text Cleaning**"):
            # Tampilkan DataFrame untuk teks tweet setelah text cleaning
            st.dataframe(pre_text["text_cleaning"], height= 500,
                         use_container_width= True, hide_index= True)
        with st.expander("**Slang-words Removal**"):
            # Tampilkan DataFrame untuk teks tweet setelah slang-word removal
            st.dataframe(pre_text["slang_removal"], height= 500,
                         use_container_width= True, hide_index= True)
        with st.expander("**Tokenization**"):
            # Tampilkan DataFrame untuk teks tweet setelah tokenisasi
            st.dataframe(pre_text["tokenization"], height= 500,
                         use_container_width= True, hide_index= True)
        with st.expander("**Stemming/Lemmatization**"):
            # Tampilkan DataFrame untuk teks tweet setelah proses stemming
            st.dataframe(pre_text["stemming"], height= 500,
                         use_container_width= True, hide_index= True)
        with st.expander("**Stopword Removal**"):
            # Tampilkan DataFrame untuk teks tweet setelah proses stopword removal
            st.dataframe(pre_text["stopword_removal"], height= 500,
                         use_container_width= True, hide_index= True)
        with st.expander("**Final Result**"):
            # Tampilkan DataFrame untuk teks tweet hasil semua text preprocessing
            st.dataframe(pre_text["final"], height= 500,
                         use_container_width= True, hide_index= True)
        # Simpan DataFrame hasil text preprocessing
        pre_text.to_csv("./data/dataset/prepros_result.csv", index= False)
    except Exception as e:
        _exceptionMessage(e)

# Halaman ekstraksi fitur
def _pageFeaturesExtraction():
    """Page ekstraksi fitur

    Halaman ini akan menampilkan data tweets sebelum dan setelah dilakukan
    pembobotan kata.
    """
    try:
        ms_20()
        show_title("Pembobotan Teks", division= True)
        ms_40()
        # Dapatkan file .csv untuk hasil pemrosesan teks dan data sentimen
        # setiap dokumen
        tweets = get_csv("./data/dataset/prepros_result.csv", usecols= ["final"])
        labels = get_csv("./data/dataset/tweets.csv", delimiter= ";",
                         usecols= ["sentimen"])
        # Splitting layout
        left, right = ml_split()
        with left:
            tweets.columns = ["tweets"] # Ubah nama kolom data
            # Gabungkan 2 DataFrame
            data = pd.concat([tweets, labels], axis= 1)
            data = data.dropna()
            # Lakukan splitting data dan pembobotan untuk proses analisis
            train_vectors, test_vectors, vectorizer = feature_extraction(
                data["tweets"].values, data["sentimen"].values)
            # Tampilkan DataFrame
            with open("./data/temp/X_train.pickle", "rb") as file:
                X_train = pickle.load(file)
            show_caption("Original Tweets")
            st.dataframe(X_train, use_container_width= True, hide_index= True)
        with right:
            # Konversi train_vectors dan test_vectors ke DataFrame
            train_df = pd.DataFrame(train_vectors.toarray(),
                                    columns= vectorizer.get_feature_names_out())
            test_df = pd.DataFrame(test_vectors.toarray(),
                                   columns= vectorizer.get_feature_names_out())
            # Tampilkan hasil pembobotan teks
            show_caption("Hasil Pembobotan Kata")
            st.dataframe(train_df, use_container_width= True, hide_index= True)
    except Exception as e:
        _exceptionMessage(e)

# Halaman analisis
def _pageAnalisis():
    """Page Analisis
    """
    try:
        ms_20()
        show_title("Analisis Sentimen Tweets")
        show_caption("Metode Logistic Regression", division= True)
        ms_40()
        # Ambil DataFrame untuk proses analisis
        with open("./data/temp/train_vectors.pickle", "rb") as file:
            train_vectors = pickle.load(file)
        with open("./data/temp/test_vectors.pickle", "rb") as file:
            test_vectors = pickle.load(file)
        with open("./data/temp/X_train.pickle", "rb") as file:
            X_train = pickle.load(file)
        with open("./data/temp/X_test.pickle", "rb") as file:
            X_test = pickle.load(file)
        with open("./data/temp/y_train.pickle", "rb") as file:
            y_train = pickle.load(file)
        with open("./data/temp/y_test.pickle", "rb") as file:
            y_test = pickle.load(file)
        # Training model Regresi Logistik
        model = model_trained(train_vectors, y_train, C= 0.01)
        # Lakukan prediksi pada data test dengan model yang telah dilatih
        y_pred = model.predict(test_vectors)
        # Buat DataFrame yang menggabungkan semua elemen data untuk ditampilkan
        test_df = pd.DataFrame({
            "tweets": X_test,
            "sentimen": y_test,
            "prediksi": y_pred
        })
        train_df = pd.DataFrame({
            "tweets": X_train,
            "sentimen": y_train
        })
        # Tampilkan hasil analisis
        show_caption("Hasil Analisis")
        st.dataframe(test_df, use_container_width= True, hide_index= True)
        # Hitung nilai akurasi
        accuracy = accuracy_score(y_true= y_test, y_pred= y_pred)
        # Tampilkan nilai akurasi
        st.success(f"Nilai Akurasi: {accuracy * 100:.2f}%")
        # Hitung jumlah data di setiap kelas
        positif = test_df["sentimen"].value_counts()[0]
        negatif = test_df["sentimen"].value_counts()[1]
        positif += train_df["sentimen"].value_counts()[0]
        negatif += train_df["sentimen"].value_counts()[1]
        # Tampilkan jumlah data di setiap kelas
        st.info(f"""
                **Jumlah data masing-masing kelas**\n
                Label positif: {positif}\n
                Label negatif: {negatif}
        """)
        ms_20()
        # Buat classification report untuk melihat hasil
        cr = classification_report(y_true= y_test, y_pred= y_pred,
                                   output_dict= True)
        # Tampilkan classification report
        show_caption("Classification Report")
        st.dataframe(pd.DataFrame(cr).transpose(), use_container_width= True)
        ms_20()
        # Tampilkan confusion matrix
        cm = confusion_matrix(y_true= y_test, y_pred= y_pred)
        # Tampilkan confusion matrix
        show_caption("Confusion Matrix")
        with ml_center():
            plot_confusion_matrix(cm, classes= np.unique(y_test))
    except Exception as e:
        _exceptionMessage(e)

def _pagePrediksi():
    """Page Prediksi
    """
    try:
        ms_20()
        show_title("Prediksi Sentimen", division= True)
        ms_40()
        cek = st.text_input("Masukkan Tweet", key= "tweet")

        if st.button("Prediksi"):
            if len(cek) != 0:
                result = np.random.choice(["Positif", "Negatif"])
                st.success(result)
            else:
                st.warning("Input tidak valid")
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
    elif selected == menu_[2]:
        _pageTextPreprocessing()
    elif selected == menu_[3]:
        _pageFeaturesExtraction()
    elif selected == menu_[4]:
        _pageAnalisis()
    elif selected == menu_[5]:
        _pagePrediksi()