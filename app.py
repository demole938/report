import streamlit as st
import pandas as pd
import numpy as np

# إعدادات واجهة المستخدم الاحترافية
st.set_page_config(page_title="Strategic Ads Auditor", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Meta Ads Auditor - Zero Tolerance Edition")
st.subheader("تحليل كواليس الحملات واستراتيجية تعظيم الأرباح")

# 1. إدخال البيانات
with st.expander("📝 إدخال بيانات الحملات (المعطيات الخام)", expanded=True):
    init_data = pd.DataFrame([{
        "Campaign": "اسم الحملة", "Spend": 0.0, "Impressions": 0, 
        "Clicks": 0, "Messages": 0, "Orders": 0, "Revenue": 0.0, "Prod_Cost": 0.0
    }])
    df_input = st.data_editor(init_data, num_rows="dynamic", use_container_width=True)

if st.button("🚀 تشغيل الفحص العميق واستخراج التوصيات"):
    df = df_input.copy()
    # الحسابات الذكية
    df['CTR%'] = (df['Clicks'] / df['Impressions']) * 100
    df['CR% (Sales)'] = (df['Orders'] / df['Messages']) * 100
    df['CPA'] = df['Spend'] / df['Orders']
    df['ROAS'] = df['Revenue'] / df['Spend']
    df['Net Profit'] = df['Revenue'] - (df['Spend'] + df['Prod_Cost'])

    # 2. ملخص الأداء (Executive Summary)
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    total_profit = df['Net Profit'].sum()
    c1.metric("صافي الربح الكلي", f"{total_profit:,.2f} EGP", delta=float(total_profit))
    c2.metric("متوسط ROAS", f"{df['ROAS'].mean():.2f}x")
    c3.metric("إجمالي المبيعات", f"{df['Revenue'].sum():,.2f}")
    c4.metric("تكلفة الاستحواذ (CPA)", f"{df['CPA'].mean():.2f}")

    # 3. التحليل النقدي والتوصيات (The Auditor Voice)
    st.markdown("### 🔍 تقرير خبير الكواليس والتوصيات:")
    
    for index, row in df.iterrows():
        with st.container():
            st.info(f"**الحملة: {row['Campaign']}**")
            col_a, col_b = st.columns(2)
            
            with col_a:
                # فحص الكرييتف
                if row['CTR%'] < 1.5:
                    st.error(f"⚠️ **مشكلة في المحتوى:** معدل النقر {row['CTR%']:.2f}% ضعيف جداً. (الهوك) مش جذاب أو الإعلان محروق.")
                else:
                    st.success(f"✅ **الكرييتف قوي:** معدل النقر {row['CTR%']:.2f}% ممتاز، استمر في نفس التوجه.")
            
            with col_b:
                # فحص المبيعات والمودريتور
                if row['CR% (Sales)'] < 10:
                    st.warning(f"⚠️ **خلل في الإغلاق:** معدل التحويل {row['CR% (Sales)']:.2f}% قليل. العيب في المودريتور أو السعر مش مناسب للجمهور.")
                else:
                    st.success(f"✅ **كفاءة تشغيل عالية:** المودريتور بيقفل أوردرات بنسبة {row['CR% (Sales)']:.2f}% وهذا معدل صحي.")
            
            if row['Net Profit'] < 0:
                st.markdown(f"🚩 **قرار نهائي:** هذه الحملة **تنزف ميزانية**. الإيقاف الفوري هو الحل الوحيد لتجنب خسارة {abs(row['Net_Profit'])} جنيه.")
            st.markdown("---")

    # 4. زر التحميل (تحويل الجدول لـ CSV كتقرير مبدئي لحين تطوير الـ PDF المعقد)
    st.download_button("📥 تحميل التقرير التفصيلي (CSV)", df.to_csv().encode('utf-8-sig'), "Full_Audit_Report.csv", "text/csv")
