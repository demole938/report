import streamlit as st
import pandas as pd
import numpy as np

# إعدادات الواجهة
st.set_page_config(page_title="Executive Audit Report", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
* { font-family: 'Tajawal', sans-serif; }
.metric-box { background-color: #ffffff; padding: 20px; border-radius: 12px; border-top: 5px solid #1a237e; box-shadow: 0 4px 10px rgba(0,0,0,0.05); direction: rtl; text-align: right;}
.metric-box h4 { color: #546e7a; font-size: 15px; margin-bottom: 5px; }
.metric-box h2 { color: #1a237e; font-size: 24px; font-weight: 700; margin: 0; }
.strategist-box { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6; margin-bottom: 20px; direction: rtl; text-align: right;}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ نظام التدقيق الاستراتيجي للوكالات (Agency Auditor)")

col_client, col_date = st.columns(2)
with col_client:
    client_name = st.text_input("اسم العميل / الشركة:", placeholder="أدخل اسم العلامة التجارية...")
with col_date:
    report_date = st.text_input("نطاق التقرير (التاريخ):", placeholder="مثال: مارس 2026")

st.write("### 1️⃣ المعطيات المالية والتشغيلية")
init_data = pd.DataFrame([{
    "اسم الحملة": "", "المصروف": 0.0, "الظهور": 0, "النقرات": 0, "الرسائل": 0, 
    "الأوردرات المسلمة": 0, "المرتجعات": 0, "المبيعات المحصلة": 0.0, "إجمالي تكلفة البضاعة": 0.0
}])

df_input = st.data_editor(init_data, num_rows="dynamic", use_container_width=True)

st.write("### 2️⃣ عقل الخبير (The Strategist Brain)")
st.info("البيانات هنا ستظهر للعميل كخريطة طريق للفترة القادمة.")
col_geo, col_prod = st.columns(2)
with col_geo:
    top_geo = st.text_input("📍 أفضل منطقة جغرافية للمبيعات:", placeholder="مثال: القاهرة والإسكندرية")
    top_age = st.text_input("👥 الفئة العمرية الأكثر شراءً:", placeholder="مثال: من 25 إلى 34 سنة")
with col_prod:
    winner_product = st.text_input("🏆 المنتج البطل (Winner):", placeholder="مثال: بجامات بريمارك الصيفي")
    loser_product = st.text_input("🔻 المنتج الخاسر (Loser):", placeholder="مثال: جواكت الجلد (يجب وقف الاستيراد)")
    
action_plan = st.text_area("🎯 خطة إعادة توزيع الميزانية (الأسبوع القادم):", placeholder="مثال: سيتم إيقاف حملة X تماماً لتوفير 500 جنيه يومياً، وسيتم ضخ هذا المبلغ في حملة Y لمضاعفة مبيعات المنتج البطل...")

if st.button("🔍 إصدار التقرير الاستراتيجي النهائي"):
    df = df_input.copy()
    
    # فلترة الصفوف الفارغة لمنع الأخطاء التقنية
    df = df[df['اسم الحملة'].notna() & (df['اسم الحملة'].str.strip() != '') & (df['المصروف'] > 0)]
    
    if df.empty:
        st.error("برجاء إدخال بيانات حملة واحدة على الأقل وبها مصروف أكبر من صفر.")
    else:
        df['إجمالي الأوردرات'] = df['الأوردرات المسلمة'] + df['المرتجعات']
        df['صافي الربح الحقيقي'] = df['المبيعات المحصلة'] - (df['المصروف'] + df['إجمالي تكلفة البضاعة'])
        df['ROAS (الصافي)'] = np.where(df['المصروف'] > 0, df['المبيعات المحصلة'] / df['المصروف'], 0)
        df['CTR%'] = np.where(df['الظهور'] > 0, (df['النقرات'] / df['الظهور']) * 100, 0)
        df['CR%'] = np.where(df['الرسائل'] > 0, (df['إجمالي الأوردرات'] / df['الرسائل']) * 100, 0)
        df['CPA'] = np.where(df['الأوردرات المسلمة'] > 0, df['المصروف'] / df['الأوردرات المسلمة'], 0)
        df['نسبة المرتجع%'] = np.where(df['إجمالي الأوردرات'] > 0, (df['المرتجعات'] / df['إجمالي الأوردرات']) * 100, 0)

        total_spend = df['المصروف'].sum()
        total_revenue = df['المبيعات المحصلة'].sum()
        total_profit = df['صافي الربح الحقيقي'].sum()
        total_roas = total_revenue / total_spend if total_spend > 0 else 0
        
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="metric-box"><h4>المصروف الإعلاني</h4><h2>{total_spend:,.0f} EGP</h2></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-box"><h4>المبيعات المحصلة</h4><h2>{total_revenue:,.0f} EGP</h2></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-box"><h4>صافي الربح</h4><h2 style="color: {"#2e7d32" if total_profit > 0 else "#c62828"};">{total_profit:,.0f} EGP</h2></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="metric-box"><h4>الـ ROAS</h4><h2>{total_roas:.2f}x</h2></div>', unsafe_allow_html=True)

        # بناء التقرير بصيغة HTML
        html_report = f"""
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <title>التقرير الاستراتيجي - {client_name}</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
                body {{ font-family: 'Tajawal', sans-serif; padding: 40px; color: #263238; background-color: #f9fafb; }}
                h1, h2, h3, h4 {{ color: #1a237e; }}
                .header {{ border-bottom: 3px solid #1a237e; padding-bottom: 15px; margin-bottom: 30px; text-align: center; }}
                .summary-grid {{ display: flex; justify-content: space-between; background: #fff; padding: 20px; border-radius: 10px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
                .summary-grid div {{ text-align: center; width: 24%; border-left: 1px solid #eee; }}
                .summary-grid div:last-child {{ border-left: none; }}
                .summary-grid p {{ margin: 0 0 5px 0; font-size: 14px; color: #546e7a; }}
                .summary-grid h3 {{ margin: 0; font-size: 22px; color: #263238; }}
                .strategy-section {{ background: #e3f2fd; border: 1px solid #bbdefb; padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
                .strategy-section ul {{ line-height: 1.8; color: #0d47a1; font-weight: bold; }}
                .campaign-box {{ background: #fff; border: 1px solid #cfd8dc; padding: 20px; border-radius: 10px; margin-bottom: 20px; page-break-inside: avoid; }}
                .c-metrics {{ display: flex; gap: 15px; margin: 15px 0; background: #f8f9fa; padding: 15px; border-radius: 5px; }}
                .c-metrics div {{ width: 25%; font-size: 14px; }}
                .verdict {{ background: #f1f8e9; padding: 15px; border-radius: 5px; font-size: 14px; line-height: 1.6; border: 1px solid #c5e1a5; }}
                .verdict.negative {{ background: #ffebee; border-color: #ffcdd2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1 style="margin:0;">التقرير الاستراتيجي الشامل للإعلانات والمبيعات</h1>
                <p style="margin:5px 0 0 0; font-size: 18px; color: #546e7a;">العميل: <b>{client_name}</b> | الفترة: <b>{report_date}</b></p>
            </div>
            
            <h2>1. الخلاصة المالية (Executive Summary)</h2>
            <div class="summary-grid">
                <div><p>المصروف الإعلاني</p><h3>{total_spend:,.0f} EGP</h3></div>
                <div><p>المبيعات المحصلة</p><h3>{total_revenue:,.0f} EGP</h3></div>
                <div><p>صافي الربح</p><h3 style="color: {'#2e7d32' if total_profit > 0 else '#c62828'};">{total_profit:,.0f} EGP</h3></div>
                <div><p>الـ ROAS الفعلي</p><h3>{total_roas:.2f}x</h3></div>
            </div>

            <h2>2. التوجيه الاستراتيجي وخريطة السوق (Market Insights)</h2>
            <div class="strategy-section">
                <p style="margin-top:0; color: #1565c0;">بناءً على تحليل البيانات العميقة للفترة المحددة، إليك خريطة السوق وتوجهات الميزانية:</p>
                <ul>
                    <li><b>أفضل منطقة جغرافية للمبيعات:</b> {top_geo}</li>
                    <li><b>الفئة العمرية الأكثر تفاعلاً وشراءً:</b> {top_age}</li>
                    <li><b>المنتج البطل (يجب زيادة مخزونه):</b> {winner_product}</li>
                    <li><b>المنتج الخاسر (يجب تصفيته أو إيقافه):</b> {loser_product}</li>
                </ul>
                <h4 style="margin-bottom: 5px; color: #000;">🎯 خطة إعادة توزيع الميزانية للأسبوع القادم:</h4>
                <p style="margin:0; color: #333; white-space: pre-wrap;">{action_plan}</p>
            </div>

            <h2>3. الأداء التقني للحملات (Campaign Diagnostics)</h2>
        """

        for idx, row in df.iterrows():
            is_profitable = row['صافي الربح الحقيقي'] > 0
            verdict_class = "" if is_profitable else "negative"
            
            html_report += f"""
            <div class="campaign-box">
                <h3 style="margin-top:0; border-bottom: 1px solid #eee; padding-bottom: 10px;">{row['اسم الحملة']} 
                    <span style="float:left; font-size: 14px; background: {'#e8f5e9' if is_profitable else '#ffebee'}; color: {'#2e7d32' if is_profitable else '#c62828'}; padding: 5px 10px; border-radius: 5px;">
                        {'زيادة ميزانية 🚀' if is_profitable else 'إيقاف فوري ❌'}
                    </span>
                </h3>
                <div class="c-metrics">
                    <div><b>صافي الربح:</b> <span style="color: {'#2e7d32' if is_profitable else '#c62828'};">{row['صافي الربح الحقيقي']:,.0f} EGP</span></div>
                    <div><b>الـ ROAS:</b> {row['ROAS (الصافي)']:.2f}x</div>
                    <div><b>تكلفة العميل (CPA):</b> {row['CPA']:,.0f} EGP</div>
                    <div><b>معدل المرتجع:</b> {row['نسبة المرتجع%']:.1f}%</div>
                </div>
                <div class="verdict {verdict_class}">
                    <b>تشخيص الخبير:</b><br>
                    - <b>الجذب (الإعلان):</b> {"المحتوى المرئي غير جذاب ويجب تغييره فوراً." if row['CTR%'] < 1.5 else "المحتوى الإعلاني ممتاز وينجح في لفت الانتباه."} (CTR: {row['CTR%']:.2f}%)<br>
                    - <b>الإغلاق (المبيعات):</b> {"يوجد خلل في المبيعات، إما بسبب السعر أو فريق الرد." if row['CR%'] < 10 else "فريق المبيعات يتعامل بكفاءة عالية ويغلق الصفقات بنجاح."} (CR: {row['CR%']:.1f}%)
                </div>
            </div>
            """
            
        html_report += "</body></html>"
        
        st.download_button(
            label="📥 تحميل التقرير الاستراتيجي المعتمد للعميل (PDF Ready)",
            data=html_report,
            file_name=f"Strategic_Report_{client_name}.html",
            mime="text/html"
        )
