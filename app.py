def inject_custom_css() -> None:
    st.markdown(
        """
        <style>

        /* ========= 基本版面 ========= */
        .block-container {
            padding-top: 2.2rem;
            padding-bottom: 1.2rem;
            padding-left: 0.9rem;
            padding-right: 0.9rem;
            max-width: 760px;
        }

        /* ========= 主標題 ========= */
        h1 {
            font-size: 2.8rem !important;
            line-height: 1.25 !important;
            font-weight: 700 !important;
            margin-top: 0.4rem !important;
            margin-bottom: 0.5rem !important;
            padding-top: 0 !important;
        }

        /* ========= 區段標題 ========= */
        h2, h3 {
            font-size: 2rem !important;
            line-height: 1.35 !important;
            font-weight: 700 !important;
            margin-top: 0.5rem !important;
            margin-bottom: 0.7rem !important;
        }

        /* ========= 說明文字 ========= */
        div[data-testid="stCaptionContainer"] p,
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] li {
            font-size: 1.15rem !important;
            line-height: 1.5 !important;
        }

        /* ========= 欄位標題 ========= */
        label,
        .stRadio > label,
        .stSelectbox > label,
        .stTextInput > label,
        .stTextArea > label {
            font-size: 1.4rem !important;
            line-height: 1.4 !important;
            font-weight: 600 !important;
        }

        /* ========= Radio 選項 ========= */
        div[role="radiogroup"] label {
            font-size: 1.25rem !important;
            line-height: 1.4 !important;
            font-weight: 500 !important;
            margin-right: 1rem !important;
            white-space: nowrap;
        }

        /* ========= Selectbox ========= */
        div[data-baseweb="select"] > div {
            min-height: 52px !important;
            font-size: 1.2rem !important;
            border-radius: 0.75rem !important;
        }

        div[data-baseweb="select"] span {
            font-size: 1.2rem !important;
        }

        /* ========= Input ========= */
        .stTextInput input,
        .stTextArea textarea {
            font-size: 1.2rem !important;
            line-height: 1.45 !important;
            border-radius: 0.75rem !important;
        }

        .stTextInput input {
            min-height: 52px !important;
        }

        .stTextArea textarea {
            min-height: 140px !important;
        }

        /* ========= placeholder ========= */
        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            font-size: 1.05rem !important;
            color: #8c8c95 !important;
        }

        /* ========= 按鈕 ========= */
        .stButton > button {
            min-height: 54px !important;
            font-size: 1.25rem !important;
            font-weight: 700 !important;
            border-radius: 0.8rem !important;
        }

        /* ========= 手機版 ========= */
        @media (max-width: 640px) {
            .block-container {
                padding-top: 2rem;
                padding-left: 0.8rem;
                padding-right: 0.8rem;
            }

            h1 {
                font-size: 2.4rem !important;
            }

            h2, h3 {
                font-size: 1.8rem !important;
            }

            label {
                font-size: 1.28rem !important;
            }

            div[role="radiogroup"] label {
                font-size: 1.15rem !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
