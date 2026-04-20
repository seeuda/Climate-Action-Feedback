import streamlit as st
import datetime
import logging
import gspread
from google.oauth2.service_account import Credentials
from typing import Dict, Any, Optional

# 初始化日誌紀錄
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


def save_to_gsheet(data: Dict[str, Any]) -> bool:
    """
    將調查結果傳送至指定 Google 試算表。
    """
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scopes,
        )
        client = gspread.authorize(creds)
        spreadsheet_id = "1CRbnOGaIfbXu-ZIeKQMgThN2JT3fT6qWRqaMQamQmMo"
        sheet = client.open_by_key(spreadsheet_id).get_worksheet(0)

        # 自動初始化標題列
        if not sheet.get_all_values():
            sheet.append_row(list(data.keys()))

        sheet.append_row(list(data.values()))
        return True

    except Exception as e:
        logger.error(f"雲端儲存失敗: {str(e)}")
        return False


def inject_custom_css() -> None:
    """
    手機優先樣式
    目標：
    1. 字級整體再放大
    2. 保持畫面緊湊
    3. 修正標題上半部被裁切
    4. 增加點擊區
    """
    st.markdown(
        """
        <style>
        /* ===== 頁面容器 ===== */
        .block-container,
        div[data-testid="stAppViewBlockContainer"] {
            padding-top: 2.2rem !important;
            padding-bottom: 1.2rem !important;
            padding-left: 0.9rem !important;
            padding-right: 0.9rem !important;
            max-width: 760px;
        }

        /* 避免主內容被上方空白/固定區域擠壓 */
        div[data-testid="stAppViewContainer"] > .main {
            padding-top: 0 !important;
        }

        /* ===== 主標題 ===== */
            h1 {
                font-size: 2.8rem !important;
                line-height: 1.25 !important;
                font-weight: 700 !important;
                margin-top: 0 !important;
                margin-bottom: 0.45rem !important;
                padding-top: 0.16rem !important;
                overflow: visible !important;
            }

        /* ===== 區段標題 ===== */
        h2, h3 {
            font-size: 2.15rem !important;
            line-height: 1.35 !important;
            font-weight: 700 !important;
            margin-top: 0.45rem !important;
            margin-bottom: 0.6rem !important;
            overflow: visible !important;
        }

        /* ===== 說明文字 ===== */
        div[data-testid="stCaptionContainer"] p,
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] li,
        div[data-testid="stAlertContainer"] {
            font-size: 1.4rem !important;
            line-height: 1.7 !important;
        }

        /* ===== 欄位標題 ===== */
        .stRadio > label,
        .stSelectbox > label,
        .stTextInput > label,
        .stTextArea > label {
            font-size: 1.45rem !important;
            line-height: 1.6 !important;
            font-weight: 600 !important;
            padding-top: 0.05rem !important;
        }

        /* ===== radio 選項 ===== */
        div[role="radiogroup"] label {
            font-size: 1.3rem !important;
            line-height: 1.4 !important;
            font-weight: 500 !important;
            margin-right: 0.7rem !important;
            white-space: normal !important;
            word-break: break-word !important;
            display: inline-flex !important;
            align-items: center !important;
            column-gap: 0.25rem !important;
        }

        div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child {
            margin-top: 0 !important;
            transform: translateY(1px);
            min-width: 22px !important;
            min-height: 22px !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        div[role="radiogroup"] {
            gap: 0.12rem 0.3rem !important;
            overflow-x: auto !important;
            overflow-y: hidden !important;
            scrollbar-width: thin !important;
        }

        div[role="radiogroup"] input[type="radio"] {
            width: 20px !important;
            height: 20px !important;
            min-width: 20px !important;
            margin-right: 6px !important;
            accent-color: #111111 !important;
            cursor: pointer !important;
        }

        div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child > div {
            border-width: 2px !important;
            border-color: #2f3440 !important;
            background: #ffffff !important;
            width: 20px !important;
            height: 20px !important;
        }

        div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child > div > div {
            background: #111111 !important;
        }

        /* ===== selectbox ===== */
        div[data-baseweb="select"] > div {
            min-height: 54px !important;
            font-size: 1.22rem !important;
            line-height: 1.3 !important;
            border-radius: 0.75rem !important;
        }

        div[data-baseweb="select"] span {
            font-size: 1.22rem !important;
            line-height: 1.3 !important;
        }

        /* ===== 輸入框 ===== */
        .stTextInput input,
        .stTextArea textarea {
            font-size: 1.22rem !important;
            line-height: 1.45 !important;
            border-radius: 0.75rem !important;
        }

        .stTextInput input {
            min-height: 54px !important;
        }

        .stTextArea textarea {
            min-height: 140px !important;
        }

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            font-size: 1.05rem !important;
            color: #8c8c95 !important;
        }

        /* ===== 按鈕 ===== */
        .stButton > button {
            min-height: 56px !important;
            font-size: 1.35rem !important;
            font-weight: 700 !important;
            border-radius: 0.85rem !important;
        }

        /* ===== 分隔線與元件間距 ===== */
        hr {
            margin-top: 1rem !important;
            margin-bottom: 1rem !important;
        }

        .stRadio,
        .stSelectbox,
        .stTextInput,
        .stTextArea {
            margin-bottom: 0.6rem !important;
        }

        /* ===== 手機版微調 ===== */
        @media (max-width: 640px) {
            .block-container,
            div[data-testid="stAppViewBlockContainer"] {
                padding-top: 1.35rem !important;
                padding-left: 0.8rem !important;
                padding-right: 0.8rem !important;
                padding-bottom: 1rem !important;
            }

            h1 {
                font-size: 2.25rem !important;
                line-height: 1.25 !important;
                margin-top: 0 !important;
                padding-top: 0.2rem !important;
            }

            h2, h3 {
                font-size: 1.65rem !important;
            }

            .stRadio > label,
            .stSelectbox > label,
            .stTextInput > label,
            .stTextArea > label {
                font-size: 1.3rem !important;
            }

            div[role="radiogroup"] label {
                font-size: 1rem !important;
                margin-right: 0.2rem !important;
                column-gap: 0.2rem !important;
                white-space: nowrap !important;
            }

            div[role="radiogroup"] input[type="radio"] {
                width: 18px !important;
                height: 18px !important;
                min-width: 18px !important;
                margin-right: 4px !important;
            }

            div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child > div {
                width: 18px !important;
                height: 18px !important;
                border-width: 2px !important;
                border-color: #2f3440 !important;
                background: #ffffff !important;
            }

            div[role="radiogroup"] {
                gap: 0.1rem 0.1rem !important;
                flex-wrap: wrap !important;
                overflow-x: visible !important;
            }

            /* 1~5 分量表：固定五等分，避免每題看起來寬度不一致 */
            div[role="radiogroup"]:has(> label:nth-child(5):last-child) {
                display: grid !important;
                grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
                gap: 0.1rem !important;
                overflow-x: visible !important;
                width: 100% !important;
            }

            div[role="radiogroup"]:has(> label:nth-child(5):last-child) > label {
                min-width: 0 !important;
                width: 100% !important;
                margin-right: 0 !important;
                justify-content: center !important;
                column-gap: 0.14rem !important;
            }

            div[data-baseweb="select"] > div,
            .stTextInput input {
                min-height: 52px !important;
            }

            .stButton > button {
                min-height: 54px !important;
                font-size: 1.2rem !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def build_required_error_list(
    township: str,
    age: str,
    identity_role: Optional[str],
    industry_type: Optional[str],
    q1: Optional[int],
    q2: Optional[int],
    q3: Optional[int],
    q4: Optional[int],
    q5: Optional[int],
) -> list[str]:
    """
    建立必填欄位錯誤清單。
    """
    errors = []

    if not township.strip():
        errors.append("「居住地區」尚未填寫")
    if age == "請選擇":
        errors.append("「年齡層」尚未選擇")
    if identity_role is None:
        errors.append("「主要身分」尚未選擇")
    if industry_type is None:
        errors.append("「從業類別」尚未選擇")
    if q1 is None:
        errors.append("「資訊易讀性」尚未選擇")
    if q2 is None:
        errors.append("「意識提升」尚未選擇")
    if q3 is None:
        errors.append("「環境友善」尚未選擇")
    if q4 is None:
        errors.append("「參與便利」尚未選擇")
    if q5 is None:
        errors.append("「整體滿意度」尚未選擇")

    return errors


def main() -> None:
    st.set_page_config(
        page_title="Climate-Action-Feedback",
        page_icon="🌍",
        layout="centered",
    )

    inject_custom_css()

    st.title("氣候變遷公眾參與活動問卷")
    st.caption("彰化縣環境保護局感謝您的參與")

    with st.container():
        st.markdown('<div id="basic-info-section"></div>', unsafe_allow_html=True)
        st.subheader("一、基本資料統計")

        c1, c2 = st.columns(2)

        with c1:
            gender = st.radio(
                "您的性別：",
                ["男", "女", "其他／不想透露"],
                horizontal=True,
            )
            age = st.selectbox(
                "您的年齡層：",
                ["請選擇", "18 歲以下", "19-35 歲", "36-50 歲", "51-64 歲", "65 歲以上"],
            )

        with c2:
            township = st.text_input(
                "居住地區（彰化縣）：",
                placeholder="例如：彰化市",
            )
            is_first = st.radio(
                "首次參加此類活動？",
                ["是", "否"],
                horizontal=True,
            )

        st.divider()

        identity_role = st.radio(
            "您的主要身分（社會角色）：",
            [
                "一般民眾（非社區幹部或志工身分）",
                "村里鄰長／社區幹部／志工",
                "其他",
            ],
            index=None,
        )
        other_role_text = ""
        if identity_role == "其他":
            other_role_text = st.text_input(
                "請說明身分（選填）：",
                key="role_other",
                placeholder="請輸入您的身分說明",
            )

        industry_type = st.radio(
            "您的從業類別：",
            ["軍公教", "農林漁牧業", "工／商／服務業", "家庭管理／退休", "學生", "其他"],
            index=None,
            horizontal=True,
        )
        other_industry_text = ""
        if industry_type == "其他":
            other_industry_text = st.text_input(
                "請說明行業（選填）：",
                key="ind_other",
                placeholder="請輸入您的行業類別",
            )

        specific_group = st.selectbox(
            "特定族群屬性（選填，僅供去識別化統計使用）：",
            ["無", "新住民", "原住民", "其他特定族群"],
            index=0,
        )
        other_group_text = ""
        if specific_group == "其他特定族群":
            other_group_text = st.text_input(
                "請說明特定族群身分（選填）：",
                key="group_other",
                placeholder="請輸入您的族群屬性說明",
            )

        st.divider()
        st.subheader("二、活動感受與友善評估")

        score_options = [1, 2, 3, 4, 5]

        st.caption("請點選分數：1=非常不同意，2=不同意，3=普通，4=同意，5=非常同意")

        q1 = st.radio(
            "1. 資訊易讀性（簡單易懂）",
            score_options,
            index=None,
            horizontal=True,
            format_func=lambda x: f"{x}分",
        )
        q2 = st.radio(
            "2. 意識提升（了解氣候對生活影響）",
            score_options,
            index=None,
            horizontal=True,
            format_func=lambda x: f"{x}分",
        )
        q3 = st.radio(
            "3. 環境友善（場地安全便利）",
            score_options,
            index=None,
            horizontal=True,
            format_func=lambda x: f"{x}分",
        )
        q4 = st.radio(
            "4. 參與便利（時段符合家庭工作）",
            score_options,
            index=None,
            horizontal=True,
            format_func=lambda x: f"{x}分",
        )
        q5 = st.radio(
            "5. 整體滿意度（必填）",
            score_options,
            index=None,
            horizontal=True,
            format_func=lambda x: f"{x}分",
        )

        overall_score_text = f"{q5}/5" if q5 is not None else "尚未選擇"
        st.info(f"目前整體滿意度分數：{overall_score_text}")

        st.divider()
        st.subheader("三、開放性建議")

        gain = st.text_area(
            "最有印象或收穫最多的內容：",
            placeholder="請自由填寫",
        )
        need = st.text_area(
            "參與不便之處（例如：交通、照顧需求）：",
            placeholder="請自由填寫",
        )

        if st.button("提交問卷", type="primary", use_container_width=True):
            errors = build_required_error_list(
                township=township,
                age=age,
                identity_role=identity_role,
                industry_type=industry_type,
                q1=q1,
                q2=q2,
                q3=q3,
                q4=q4,
                q5=q5,
            )

            if errors:
                for err in errors:
                    st.error(err)
                st.markdown("👉 [前往補充填寫資料](#basic-info-section)")
                return

            final_role = (
                f"其他 ({other_role_text.strip()})"
                if identity_role == "其他" and other_role_text.strip()
                else identity_role
            )
            final_industry = (
                f"其他 ({other_industry_text.strip()})"
                if industry_type == "其他" and other_industry_text.strip()
                else industry_type
            )
            final_group = (
                f"其他 ({other_group_text.strip()})"
                if specific_group == "其他特定族群" and other_group_text.strip()
                else (specific_group if specific_group != "無" else "")
            )

            record = {
                "時間戳記": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "性別": gender,
                "年齡": age,
                "行政區": township.strip(),
                "首次參加": is_first,
                "社會角色": final_role,
                "從業類別": final_industry,
                "族群屬性": final_group,
                "Q1資訊易讀": q1,
                "Q2意識提升": q2,
                "Q3環境友善": q3,
                "Q4參與便利": q4,
                "Q5整體滿意": q5,
                "正面獲益": gain.strip(),
                "改善建議": need.strip(),
            }

            with st.spinner("正在同步至雲端資料庫..."):
                if save_to_gsheet(record):
                    st.success("提交成功，資料已完成去識別化儲存。")
                    st.balloons()
                else:
                    st.error("上傳失敗，請確認網路連線或系統 Secrets 設定。")


if __name__ == "__main__":
    main()
