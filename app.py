# Base Indent: 0 spaces
import streamlit as st
import pandas as pd
import datetime
import logging
import gspread
from google.oauth2.service_account import Credentials
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

def save_to_gsheet(data: Dict[str, Any]) -> bool:
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
        client = gspread.authorize(creds)
        spreadsheet_id = "1CRbnOGaIfbXu-ZIeKQMgThN2JT3fT6qWRqaMQamQmMo"
        sheet = client.open_by_key(spreadsheet_id).get_worksheet(0)
        
        if not sheet.get_all_values():
            sheet.append_row(list(data.keys()))
            
        sheet.append_row(list(data.values()))
        return True
    except Exception as e:
        logger.error(f"雲端儲存失敗: {str(e)}")
        return False

def main() -> None:
    st.set_page_config(page_title="Climate-Action-Feedback", page_icon="🌍", layout="centered")

    st.title("氣候變遷公眾參與活動問卷")
    st.caption("版本更新：強化在地產業與基層治理分類")
    
    with st.form("survey_form", clear_on_submit=True):
        st.subheader("一、 基本資料統計")
        
        c1, c2 = st.columns(2)
        with c1:
            gender = st.radio("您的性別：", ["男", "女", "其他/不想透露"], horizontal=True)
            age = st.selectbox("您的年齡層：", ["請選擇", "18 歲以下", "19-35 歲", "36-50 歲", "51-64 歲", "65 歲以上"])
        
        with c2:
            township = st.text_input("居住地區（彰化縣）：", placeholder="例如：彰化市")
            is_first = st.radio("首次參加此類活動？", ["是", "否"], horizontal=True)

        st.divider()
        
        # 社會角色：反映基層治理結構
        identity_role = st.radio(
            "您的主要身分（社會角色）：",
            ["一般居民", "村里鄰長 / 地方代表", "社區幹部 / 志工", "政府機關 / 承辦人員", "學生", "其他"],
            index=None,
            help="此為必填項目，用於區分參與者層級。"
        )

        # 產業類別：納入彰化核心產業
        industry_type = st.radio(
            "您的從業類別（影響調適感知）：",
            ["農林漁牧業", "製造業 / 工業", "商業 / 服務業", "家庭管理 / 退休", "學生", "其他"],
            index=None,
            horizontal=True,
            help="氣候變遷對不同產業有不同衝擊，此資料極具參考價值。"
        )

        # 族群屬性：選填模式
        specific_group = st.radio(
            "特定族群屬性（選填）：",
            ["新住民", "原住民", "主要家庭照顧者", "身心障礙者"],
            index=None,
            horizontal=True,
            help="若不具備上述身分，請直接跳過。"
        )

        st.divider()
        st.subheader("二、 活動感受與友善評估")
        
        scores = {"非常同意": 4, "同意": 3, "不同意": 2, "非常不同意": 1}
        opts = list(scores.keys())

        q1 = st.select_slider("1. 資訊易讀性（簡單易懂）", options=opts, value="同意")
        q2 = st.select_slider("2. 意識提升（了解氣候對生活影響）", options=opts, value="同意")
        q3 = st.select_slider("3. 環境友善（場地安全便利）", options=opts, value="同意")
        q4 = st.select_slider("4. 參與便利（時段符合家庭工作）", options=opts, value="同意")
        q5 = st.select_slider("5. 整體滿意度", options=opts, value="同意")

        st.divider()
        st.subheader("三、 開放性建議")
        gain = st.text_area("收穫最多的內容：")
        need = st.text_area("參與不便之處（交通、時間、照顧）：")

        if st.form_submit_button("送出問卷"):
            errors = []
            if not township: errors.append("「居住地區」尚未填寫")
            if age == "請選擇": errors.append("「年齡層」尚未選擇")
            if identity_role is None: errors.append("「主要身分」尚未選擇")
            if industry_type is None: errors.append("「從業類別」尚未選擇")
            
            if errors:
                for err in errors:
                    st.error(err)
                return

            record = {
                "時間戳記": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "性別": gender,
                "年齡": age,
                "行政區": township,
                "首次參加": is_first,
                "社會角色": identity_role,
                "從業類別": industry_type,
                "族群屬性": specific_group if specific_group else "",
                "Q1資訊易讀": scores[q1],
                "Q2意識提升": scores[q2],
                "Q3環境友善": scores[q3],
                "Q4參與便利": scores[q4],
                "Q5整體滿意": scores[q5],
                "正面獲益": gain,
                "改善建議": need
            }

            with st.spinner("資料傳送中..."):
                if save_to_gsheet(record):
                    st.success("提交成功！")
                    st.balloons()
                else:
                    st.error("上傳失敗，請聯繫管理員。")

if __name__ == "__main__":
    main()
