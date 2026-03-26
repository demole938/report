import streamlit as st
import pandas as pd
import numpy as np

# إعدادات الصفحة
st.set_page_config(page_title="Meta Ads Deep Audit", layout="wide")
st.title("لوحة فحص الحملات الإعلانية - Zero Tolerance")

# داتا مبدئية لشكل الجدول
init_data = pd.DataFrame({
    'Campaign_Name': ['Campaign_A'],
    'Amount_Spent': [0.0],
    'Impressions': [0],
    'Link_Clicks': [0],
    'New_Messages': [0],
    'Total_Orders': [0],
    'Total_Revenue': [0.0],
    'Total_Product_Cost': [0.0]
})

st.write("### 1. أدخل الأرقام الخام:")
# جدول قابل للتعديل والإضافة من الواجهة
edited_df = st.data_editor(init_data, num_rows="dynamic", use_container_width=True)

if st.button("تنفيذ الفحص العميق"):
    df = edited_df.copy()
    
    # تجنب القسمة على صفر
    df.replace(0, np.nan, inplace=True)
    
    # حساب المؤشرات التقنية والمالية
    df['CPM'] = np.round((df['Amount_Spent'] / df['Impressions']) * 1000, 2)
    df['CTR (%)'] = np.round((df['Link_Clicks'] / df['Impressions']) * 100, 2)
    df['Cost/Message'] = np.round(df['Amount_Spent'] / df['New_Messages'], 2)
    df['Conv. Rate (%)'] = np.round((df['Total_Orders'] / df['New_Messages']) * 100, 2)
    df['CPA'] = np.round(df['Amount_Spent'] / df['Total_Orders'], 2)
    df['ROAS'] = np.round(df['Total_Revenue'] / df['Amount_Spent'], 2)
    df['Net Profit'] = df['Total_Revenue'] - (df['Amount_Spent'] + df['Total_Product_Cost'])
    
    df.fillna(0, inplace=True) # إرجاع الأصفار مكان الـ NaN
    
    st.write("### 2. نتائج الفحص:")
    st.dataframe(df, use_container_width=True)
    
    # قرار الإدارة المالي
    st.write("### 3. الخلاصة المالية:")
    total_profit = df['Net Profit'].sum()
    total_roas = np.round(df['Total_Revenue'].sum() / df['Amount_Spent'].sum(), 2) if df['Amount_Spent'].sum() > 0 else 0
    
    col1, col2 = st.columns(2)
    with col1:
        if total_profit > 0:
            st.success(f"إجمالي صافي الربح الحقيقي: {total_profit} جنيه")
        else:
            st.error(f"انتباه! نزيف ميزانية. العجز الحالي: {total_profit} جنيه")
    with col2:
        st.info(f"متوسط عائد الإنفاق (ROAS): {total_roas}")
