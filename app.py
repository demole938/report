import streamlit as st
import pandas as pd
import numpy as np

# إعداد واجهة المستخدم
st.set_page_config(page_title="Strategic Ads Auditor", layout="wide")

st.markdown("""
    <style>
    .report-card { background-color: #ffffff; padding: 20px; border-radius: 15px; border-left: 5px solid #ff4b4b; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .success-card { border-left: 5px solid #28a745; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Meta Ads Auditor - Zero Tolerance")
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
    
    # الحسابات التقنية
    df['CTR%'] = (df['Clicks'] / df['Impressions']) * 100
    df['CR%'] = (df['Orders'] / df['Messages']) * 100
    df['CPA'] = df['Spend'] / df['Orders']
    df['ROAS'] = df['Revenue'] / df['Spend']
    df['Net_Profit'] = df['Revenue'] - (df['Spend'] + df['Prod_Cost'])
    
    df.replace([np.inf, -np.inf], 0, inplace=True)
    df.fillna(0, inplace=True)

    # 2. لوحة المؤشرات الرئيسية (Dashboard)
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    total_net = df['Net_Profit'].sum()
    c1.metric("صافي الربح الحقيقي", f"{total_net:,.2f} EGP")
    c2.metric("متوسط ROAS", f"{df['ROAS'].mean():.2f}x")
    c3.metric("إجمالي المبيعات", f"{df['Revenue'].sum():,.2f}")
    c4.metric("تكلفة الاستحواذ (CPA)", f"{df['CPA'].mean():.2f}")

    # 3. التقرير الاستراتيجي والتوصيات
    st.markdown("### 🔍 تقرير خبير الكواليس والتوصيات التكتيكية:")
    
    for _, row in df.iterrows():
        is_losing = row['Net_Profit'] < 0
        card_style = "report-card" if is_losing else "report-card success-card"
        
        with st.container():
            st.markdown(f"""
            <div class="{card_style}">
                <h4>الحملة: {row['Campaign']}</h4>
                <p><b>الوضع المالي:</b> صافي ربح {row['Net_Profit']:,.2f} EGP | ROAS: {row['ROAS']:.2f}x</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.write("**🛡️ تحليل المحتوى (Creative):**")
                if row['CTR%'] < 1.5:
                    st.error(f"⚠️ CTR {row['CTR%']:.2f}% (ضعيف). الهوك فاشل أو المحتوى لا يلمس نقطة ألم الجمهور. غير الكرييتف فوراً.")
                else:
                    st.success(f"✅ CTR {row['CTR%']:.2f}% (ممتاز). المحتوى جذاب ويحقق نقرات رخيصة.")
            
            with col_b:
                st.write("**🤝 تحليل المبيعات (Closing):**")
                if row['CR%'] < 10:
                    st.warning(f"⚠️ معدل تحويل {row['CR%']:.2f}% (منخفض). المودريتور بيضيع رسايل أو السعر فيه مشكلة.")
                else:
                    st.success(f"✅ معدل تحويل {row['CR%']:.2f}% (صحي). عملية البيع داخل الرسايل ممتازة.")
                    
            with col_c:
                st.write("**🚩 القرار الاستراتيجي:**")
                if is_losing:
                    st.error(f"إيقاف فوري (Kill It). الحملة تحرق رأس المال.")
                elif row['ROAS'] > 3:
                    st.success("زيادة ميزانية (Scale). الحملة رابحة وقابلة للتوسع.")
                else:
                    st.info("مراقبة (Monitor). الحملة في منطقة التعادل.")

    # 4. استخراج التقرير
    st.download_button("📥 تحميل التقرير التفصيلي (CSV)", df.to_csv().encode('utf-8-sig'), "Deep_Audit_Report.csv", "text/csv")
