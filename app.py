import streamlit as st
import pandas as pd
import numpy as np

# إعدادات واجهة الوكالات (Agency Level)
st.set_page_config(page_title="Executive Audit Report", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
* { font-family: 'Tajawal', sans-serif; }
.metric-box { background-color: #ffffff; padding: 25px; border-radius: 12px; border-top: 5px solid #1a237e; box-shadow: 0 10px 20px rgba(0,0,0,0.05); direction: rtl; text-align: right;}
.metric-box h4 { color: #546e7a; font-size: 16px; margin-bottom: 10px; }
.metric-box h2 { color: #1a237e; font-size: 28px; font-weight: 700; margin: 0; }
.campaign-card { background-color: #ffffff; padding: 25px; border-radius: 12px; border: 1px solid #eceff1; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); direction: rtl; text-align: right;}
.status-badge { padding: 6px 12px; border-radius: 6px; font-weight: bold; font-size: 14px; float: left; }
.bg-scale { background-color: #e8f5e9; color: #2e7d32; }
.bg-kill { background-color: #ffebee; color: #c62828; }
.bg-monitor { background-color: #fff8e1; color: #f57f17; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ نظام التدقيق الاستراتيجي للوكالات (Agency Auditor)")

col_client, col_date = st.columns(2)
with col_client:
    client_name = st.text_input("اسم العميل / الشركة:", placeholder="أدخل اسم العلامة التجارية...")
with col_date:
    report_date = st.text_input("نطاق التقرير (التاريخ):", placeholder="مثال: مارس 2026")

st.write("### 📝 المعطيات المالية والتشغيلية (إدخال دقيق)")
# الجدول الجديد بيطلب المبيعات الفعلية والتكلفة الفعلية بالجنيه
init_data = pd.DataFrame([{
    "اسم الحملة": "حملة الشتوي", "المصروف": 0.0, "الظهور": 0, "النقرات": 0, "الرسائل": 0, 
    "الأوردرات المسلمة": 0, "المرتجعات": 0, "المبيعات المحصلة": 0.0, "إجمالي تكلفة البضاعة": 0.0
}])

df_input = st.data_editor(init_data, num_rows="dynamic", use_container_width=True)

if st.button("🔍 تنفيذ الفحص المالي والتقني"):
    df = df_input.copy()
    
    # العمليات الحسابية الصارمة بناءً على الأموال الحقيقية
    df['إجمالي الأوردرات (خرجت للشحن)'] = df['الأوردرات المسلمة'] + df['المرتجعات']
    df['صافي الربح الحقيقي'] = df['المبيعات المحصلة'] - (df['المصروف'] + df['إجمالي تكلفة البضاعة'])
    
    # المؤشرات التقنية
    df['ROAS (الصافي)'] = np.where(df['المصروف'] > 0, df['المبيعات المحصلة'] / df['المصروف'], 0)
    df['CTR% (جذب الإعلان)'] = np.where(df['الظهور'] > 0, (df['النقرات'] / df['الظهور']) * 100, 0)
    df['CR% (كفاءة المبيعات)'] = np.where(df['الرسائل'] > 0, (df['إجمالي الأوردرات (خرجت للشحن)'] / df['الرسائل']) * 100, 0)
    df['CPA (تكلفة العميل)'] = np.where(df['الأوردرات المسلمة'] > 0, df['المصروف'] / df['الأوردرات المسلمة'], 0)
    df['نسبة المرتجع%'] = np.where(df['إجمالي الأوردرات (خرجت للشحن)'] > 0, (df['المرتجعات'] / df['إجمالي الأوردرات (خرجت للشحن)']) * 100, 0)

    st.write("---")
    st.write(f"### 📊 الملخص التنفيذي للعميل: {client_name}")
    
    total_spend = df['المصروف'].sum()
    total_revenue = df['المبيعات المحصلة'].sum()
    total_profit = df['صافي الربح الحقيقي'].sum()
    total_roas = total_revenue / total_spend if total_spend > 0 else 0
    
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="metric-box"><h4>إجمالي المصروف الإعلاني</h4><h2>{total_spend:,.0f} EGP</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-box"><h4>إجمالي المبيعات المحصلة</h4><h2>{total_revenue:,.0f} EGP</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-box"><h4>صافي الربح (بعد خصم كل التكاليف)</h4><h2 style="color: {"#2e7d32" if total_profit > 0 else "#c62828"};">{total_profit:,.0f} EGP</h2></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-box"><h4>العائد على الاستثمار (ROAS)</h4><h2>{total_roas:.2f}x</h2></div>', unsafe_allow_html=True)

    st.write("---")
    
    # بناء ملف الـ HTML الاحترافي (Agency Grade)
    html_report = f"""
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>التقرير الاستراتيجي - {client_name}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
            body {{ font-family: 'Tajawal', sans-serif; padding: 50px; color: #263238; background-color: #f9fafb; }}
            .header {{ text-align: center; margin-bottom: 50px; padding-bottom: 20px; border-bottom: 3px solid #1a237e; }}
            .header h1 {{ color: #1a237e; font-weight: 900; letter-spacing: -1px; margin-bottom: 5px; }}
            .header h3 {{ color: #546e7a; font-weight: 400; margin-top: 0; }}
            .executive-summary {{ display: flex; justify-content: space-between; margin-bottom: 40px; background: #fff; padding: 30px; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}
            .sum-item {{ text-align: center; width: 23%; border-left: 1px solid #eceff1; }}
            .sum-item:last-child {{ border-left: none; }}
            .sum-item p {{ color: #78909c; font-size: 14px; font-weight: 700; margin-bottom: 5px; }}
            .sum-item h2 {{ color: #263238; font-size: 28px; margin: 0; }}
            .profit-positive {{ color: #2e7d32 !important; }}
            .profit-negative {{ color: #c62828 !important; }}
            .campaign-row {{ background: #fff; border: 1px solid #cfd8dc; border-radius: 12px; padding: 25px; margin-bottom: 25px; page-break-inside: avoid; }}
            .c-header {{ border-bottom: 1px solid #eceff1; padding-bottom: 15px; margin-bottom: 20px; }}
            .c-header h2 {{ margin: 0; color: #37474f; font-size: 22px; display: inline-block; }}
            .badge {{ float: left; padding: 6px 15px; border-radius: 20px; font-size: 13px; font-weight: bold; }}
            .badge.scale {{ background: #e8f5e9; color: #2e7d32; }}
            .badge.kill {{ background: #ffebee; color: #c62828; }}
            .badge.monitor {{ background: #fff8e1; color: #f57f17; }}
            .metrics-grid {{ display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 20px; }}
            .m-box {{ width: 30%; background: #f8f9fa; padding: 15px; border-radius: 8px; border-right: 4px solid #90a4ae; }}
            .m-box p {{ margin: 0 0 5px 0; font-size: 13px; color: #546e7a; }}
            .m-box h4 {{ margin: 0; font-size: 18px; color: #263238; }}
            .auditor-verdict {{ background: #f1f8e9; padding: 20px; border-radius: 8px; border: 1px solid #c5e1a5; }}
            .auditor-verdict.negative {{ background: #ffebee; border-color: #ffcdd2; }}
            .auditor-verdict h4 {{ margin: 0 0 10px 0; color: #33691e; }}
            .auditor-verdict.negative h4 {{ color: #b71c1c; }}
            .auditor-verdict ul {{ margin: 0; padding-right: 20px; color: #455a64; font-size: 14px; line-height: 1.8; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>تقرير التدقيق الإعلاني والمالي</h1>
            <h3>العميل: {client_name} | الفترة: {report_date}</h3>
        </div>
        
        <h2 style="color: #1a237e; font-size: 20px; margin-bottom: 15px;">1. الملخص المالي التنفيذي (Executive Summary)</h2>
        <div class="executive-summary">
            <div class="sum-item">
                <p>إجمالي المصروف</p>
                <h2>{total_spend:,.0f} EGP</h2>
            </div>
            <div class="sum-item">
                <p>المبيعات المحصلة</p>
                <h2>{total_revenue:,.0f} EGP</h2>
            </div>
            <div class="sum-item">
                <p>صافي الربح الحقيقي</p>
                <h2 class="{'profit-positive' if total_profit > 0 else 'profit-negative'}">{total_profit:,.0f} EGP</h2>
            </div>
            <div class="sum-item">
                <p>العائد على الاستثمار (ROAS)</p>
                <h2>{total_roas:.2f}x</h2>
            </div>
        </div>
        
        <h2 style="color: #1a237e; font-size: 20px; margin-bottom: 15px;">2. التحليل الدقيق للحملات وقرارات التوجيه</h2>
    """

    for idx, row in df.iterrows():
        is_profitable = row['صافي الربح الحقيقي'] > 0
        
        if not is_profitable:
            status = "إيقاف فوري وتغيير الاستراتيجية ❌"
            badge_class = "kill"
            verdict_class = "negative"
        elif row['ROAS (الصافي)'] >= 3 and is_profitable:
            status = "توسيع وزيادة الميزانية (Scale) 🚀"
            badge_class = "scale"
            verdict_class = ""
        else:
            status = "مراقبة وتحسين مستمر ⚠️"
            badge_class = "monitor"
            verdict_class = ""
            
        # إضافة الحملة لملف الـ HTML
        html_report += f"""
        <div class="campaign-row">
            <div class="c-header">
                <h2>{row['اسم الحملة']}</h2>
                <div class="badge {badge_class}">{status}</div>
            </div>
            
            <div class="metrics-grid">
                <div class="m-box" style="border-right-color: {'#2e7d32' if is_profitable else '#c62828'};">
                    <p>صافي الربح</p>
                    <h4 class="{'profit-positive' if is_profitable else 'profit-negative'}">{row['صافي الربح الحقيقي']:,.0f} EGP</h4>
                </div>
                <div class="m-box">
                    <p>عائد الحملة (ROAS)</p>
                    <h4>{row['ROAS (الصافي)']:.2f}x</h4>
                </div>
                <div class="m-box">
                    <p>تكلفة اكتساب العميل الصافي</p>
                    <h4>{row['CPA (تكلفة العميل)']:,.0f} EGP</h4>
                </div>
            </div>

            <div class="auditor-verdict {verdict_class}">
                <h4>تشخيص الخبير (Auditor Diagnostics):</h4>
                <ul>
                    <li><b>كفاءة الإعلان (جذب الجمهور):</b> {"المحتوى المرئي غير جذاب ولا يوقف العميل (الهوك ضعيف)، يجب تغييره." if row['CTR% (جذب الإعلان)'] < 1.5 else "المحتوى الإعلاني ممتاز وينجح في لفت انتباه الشريحة المستهدفة."} (معدل: {row['CTR% (جذب الإعلان)']:.2f}%)</li>
                    <li><b>كفاءة المبيعات (الرد والإغلاق):</b> {"توجد مشكلة حقيقية إما في تسعير المنتج أو في مهارات فريق المبيعات في إغلاق الرسائل." if row['CR% (كفاءة المبيعات)'] < 10 else "فريق المبيعات يتعامل بكفاءة عالية مع الرسائل الواردة."} (معدل: {row['CR% (كفاءة المبيعات)']:.1f}%)</li>
                    <li><b>تحليل الاسترجاع:</b> نسبة المرتجعات سجلت {row['نسبة المرتجع%']:.1f}%، {"وهو مؤشر خطر يستوجب مراجعة جودة المنتج أو شركة الشحن." if row['نسبة المرتجع%'] > 20 else "وهي ضمن المعدلات الطبيعية للتجارة الإلكترونية."}</li>
                </ul>
            </div>
        </div>
        """
        
    html_report += "</body></html>"
    
    st.download_button(
        label="📥 تحميل التقرير الرسمي للعميل (Agency PDF Version)",
        data=html_report,
        file_name=f"Executive_Audit_{client_name}.html",
        mime="text/html"
    )
    
    st.success("تم الفحص بنجاح. يمكنك الآن تحميل التقرير بصيغة HTML. افتحه في المتصفح واضغط (Ctrl+P) لحفظه كملف PDF احترافي وتصديره للعميل.")
