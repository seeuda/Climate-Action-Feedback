# Base Indent: 0 spaces
import streamlit as st
import pandas as pd
import datetime
import logging
import os
from typing import Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

def save_to_csv(data: Dict[str, Any], filename: str = "feedback_data.csv") -> bool:
    """
    將結構化資料儲存至本地 CSV 檔案。
    """
    try:
        df = pd.DataFrame([data])
        file_exists = os.path.isfile(filename)
        df.to_csv(
            filename, 
            mode='a', 
            index=False, 
            header=not file_exists, 
            encoding="utf-8-sig"
        )
        return True
    except Exception as e:
        logger.error(f"資料寫入錯誤: {str(e)}")
        return False

def main() -> None:
    st.set_page_config(
        page_title="Climate-Action-Feedback",
        page_icon="🌍",
        layout="centered"
    )

    st.title("氣候變遷公眾參與活動問卷")
    st.caption("Climate-Action-Feedback System")
    
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
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "gender": gender,
                "age": age,
                "township": township,
                "is_first": is_first,
                "identities": ",".join(identities),
                "q1_info": scores[q1],
                "q2_aware": scores[q2],
                "q3_env": scores[q3],
                "q4_conv": scores[q4],
                "q5_total": scores[q5],
                "gain": gain,
                "need": need
            }

            if save_to_csv(record):
                st.success("提交成功")
                st.balloons()

if __name__ == "__main__":
    main()