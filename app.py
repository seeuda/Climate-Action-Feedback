# Base Indent: 0 spaces
import streamlit as st
import pandas as pd
import datetime
import logging
import gspread
from google.oauth2.service_account import Credentials
from typing import Dict, Any

# 初始化日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

def save_to_gsheet(data: Dict[str, Any]) -> bool:
    """
    將調查結果傳送至指定 Google 試算表。
    """
    try:
        # 定義存取範圍
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # 從 Streamlit Secrets 讀取憑證
        # 請於 Streamlit Cloud 控制面板或本地 .streamlit/secrets.toml 設定憑證
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], 
            scopes=scopes
        )
        
        # 授權並開啟試算表
        client = gspread.authorize(creds)
        spreadsheet_id = "1CRbnOGaIfbXu-ZIeKQMgThN2JT3fT6qWRqaMQamQmMo"
        sheet = client.open_by_key(spreadsheet_id).get_worksheet(0)
        
        # 檢查是否需要寫入標題列（若表單為空）
        if not sheet.get_all_values():
            sheet.append_row(list(data.keys()))
            
        # 寫入數據
        sheet.append_row(list(data.values()))
        return True
    except Exception as e:
        logger.error(f"雲端儲存失敗: {str(e)}")
        return False

def main() -> None:
    st.set_page_config(
        page_title="Climate-Action-Feedback",
        page_icon="🌍",
        layout="centered"
    )

    st.title("氣候變遷公眾參與活動問卷")
    st.caption("連線至彰化縣氣候變遷雲端資料庫")
    
    with st.form("survey_form", clear_on_submit=True):
        st.subheader("基本資料統計")
        
        c1, c2 = st.columns(2)
        with c1:
            gender = st.radio("性別：", ["男", "女", "其他/不想透露"], horizontal=True)
            age = st.selectbox("年齡層：", ["18 歲以下", "19-35 歲", "36-50 歲", "51-64 歲", "65 歲以上"])
        
        with c2:
            township = st.text_input("居住地區（彰化縣）：", placeholder="例如：彰化市")
            is_first = st.radio("首次參加此類活動？", ["是", "否"], horizontal=True)

        identity_list = ["環保志工", "新住民", "社區發展協會幹部", "一般居民", "公務人員", "其他"]
        identities = st.multiselect("身分：", identity_list)

        st.divider()
        st.subheader("活動滿意度評估")
        
        scores = {"非常同意": 4, "同意": 3, "不同意": 2, "非常不同意": 1}
        opts = list(scores.keys())

        q1 = st.select_slider("1. 資訊易讀性（簡單易懂）", options=opts, value="同意")
        q2 = st.select_slider("2. 意識提升（了解氣候對生活影響）", options=opts, value="同意")
        q3 = st.select_slider("3. 環境友善（場地安全便利）", options=opts, value="同意")
        q4 = st.select_slider("4. 參與便利（時段符合家庭工作）", options=opts, value="同意")
        q5 = st.select_slider("5. 整體滿意度", options=opts, value="同意")

        st.divider()
        st.subheader("開放性建議")
        gain = st.text_area("收穫最多的內容：")
        need = st.text_area("參與不便之處（交通、時間、照顧）：")

        if st.form_submit_button("送出問卷"):
            if not township:
                st.error("請提供居住地區資訊")
                return

            record = {
                "時間戳記": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "性別": gender,
                "年齡": age,
                "行政區": township,
                "首次參加": is_first,
                "身分標籤": ",".join(identities),
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
                    st.success("提交成功，資料已更新至雲端試算表。")
                    st.balloons()
                else:
                    st.error("上傳失敗，請檢查網路連線或系統設定。")

if __name__ == "__main__":
    main()
