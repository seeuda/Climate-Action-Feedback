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
    st.caption("版本更新：5分制量表與產業分類優化")
    
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
        
        # 1. 社會角色：優化互斥性與選填欄位
        identity_role = st.radio(
            "您的主要身分（社會角色）：",
            ["一般民眾（不具備社區幹部或志工身分）", "村里鄰長 / 社區幹部 / 志工", "其他"],
            index=None
        )
        
        other_role_text = ""
        if identity_role == "其他":
            other_role_text = st.text_input("請說明身分（選填）：")

        # 2. 從業類別：合併工、商、服務業並增加選填欄位
        industry_type = st.radio(
            "您的從業類別：",
            ["軍公教", "農林漁牧業", "工/商/服務業", "家庭管理 / 退休", "學生", "其他"],
            index=None,
            horizontal=True
        )
        
        other_industry_text = ""
        if industry_type == "其他":
            other_industry_text = st.text_input("請說明行業（選填）：")

        # 3. 特定族群
        specific_group = st.selectbox(
            "特定族群屬性（選填）：",
            ["不具備下述身分", "新住民", "原住民", "其他特定族群"],
            index=0
        )

        st.divider()
        st.subheader("二、 活動感受與友善評估")
        
        # 4. 五分制量表：預設在 4分 (同意)
        scores = {
            "1分 (非常不同意)": 1,
            "2分 (不同意)": 2,
            "3分 (普通)": 3,
            "4分 (同意)": 4,
            "5分 (非常同意)": 5
        }
        opts = list(scores.keys())

        q1 = st.select_slider("1. 資訊易讀性（簡單易懂）", options=opts, value="4分 (同意)")
        q2 = st.select_slider("2. 意識提升（了解氣候對生活影響）", options=opts, value="4分 (同意)")
        q3 = st.select_slider("3. 環境友善（場地安全便利）", options=opts, value="4分 (同意)")
        q4 = st.select_slider("4. 參與便利（時段符合家庭工作）", options=opts, value="4分 (同意)")
        q5 = st.select_slider("5. 整體滿意度", options=opts, value="4分 (同意)")

        st.divider()
        st.subheader("三、 開放性建議")
        gain = st.text_area("最有印象或收穫最多的內容：")
        need = st.text_area("參與不便之處（例如：交通、照顧需求）：")

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

            # 合併其他選項文字
            final_role = f"其他 ({other_role_text})" if identity_role == "其他" and other_role_text else identity_role
            final_industry = f"其他 ({other_industry_text})" if industry_type == "其他" and other_industry_text else industry_type

            record = {
                "時間戳記": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "性別": gender,
                "年齡": age,
                "行政區": township,
                "首次參加": is_first,
                "社會角色": final_role,
                "從業類別": final_industry,
                "族群屬性": specific_group if specific_group != "不具備下述身分" else "",
                "Q1資訊易讀": scores[q1],
                "Q2意識提升": scores[q2],
                "Q3環境友善": scores[q3],
                "Q4參與便利": scores[q4],
                "Q5整體滿意": scores[q5],
                "正面獲益": gain,
                "改善建議": need
            }

            with st.spinner("資料上傳中..."):
                if save_to_gsheet(record):
                    st.success("提交成功")
                    st.balloons()
                else:
                    st.error("系統連線失敗")

if __name__ == "__main__":
    main()
