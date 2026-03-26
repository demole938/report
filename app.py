import streamlit as st
import pandas as pd
import numpy as np

# إعدادات الواجهة
st.set_page_config(page_title="Report Campaign", layout="wide")

st.markdown("""
<style>
.metric-box { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; box-shadow: 0 4px 8px rgba(0,0,0,0.1); direction: rtl; text-align: right;}
.campaign-card { background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); direction: rtl; text-align: right;}
.status-scale { color: #28a745; font-weight: bold; background-color: #e6f4ea; padding: 5px 10px; border-radius: 5px;}
.status-kill { color: #dc3545; font-weight: bold; background-color: #fce8e6; padding: 5px 10px; border-radius: 5px;}
.status-monitor { color: #ffc107; font-weight: bold; background-color: #fef7e0; padding: 5px 10px; border-radius: 5px;}
</style>
""", unsafe_allow_html=True)

st.title("لوحة تحكم خبير الكواليس - Report Campaign")

client_name = st.text_input("اسم العميل:", placeholder="أدخل اسم العميل هنا...")

st.write("### 📝 إدخال بيانات الكواليس (بالعربي)")
# تحويل الجدول بالكامل للغة العربية
init_data = pd.DataFrame([{
    "اسم الحملة": "حملة 1", "المصروف": 0.0, "الظهور": 0, 
    "النقرات": 0, "الرسائل": 0, "إجمالي الأوردرات": 0, "المرتجعات": 0, 
    "متوسط قيمة الأوردر": 0.0, "تكلفة المنتج": 0.0
}])

df_input = st.data_editor(init_data, num_rows="dynamic", use_container_width=True)

if st.button("تنفيذ التقرير واستخراج النتائج"):
    df = df_input.copy()
    
    # العمليات الحسابية بناءً على الأسماء العربية الجديدة
    df['صافي الأوردرات'] = df['إجمالي الأوردرات'] - df['المرتجعات']
    df['صافي المبيعات'] = df['صافي الأوردرات'] * df['متوسط قيمة الأوردر']
    df['إجمالي التكلفة'] = df['المصروف'] + (df['صافي الأوردرات'] * df['تكلفة المنتج'])
    df['صافي الربح'] = df['صافي المبيعات'] - df['إجمالي التكلفة']
    
    df['ROAS'] = np.where(df['المصروف'] > 0, df['صافي المبيعات'] / df['المصروف'], 0)
    df['CTR%'] = np.where(df['الظهور'] > 0, (df['النقرات'] / df['الظهور']) * 100, 0)
    df['CR%'] = np.where(df['الرسائل'] > 0, (df['إجمالي الأوردرات'] / df['الرسائل']) * 100, 0)
    df['CPA'] = np.where(df['صافي الأوردرات'] > 0, df['المصروف'] / df['صافي الأوردرات'], 0)

    st.write("---")
    st.write(f"### 📊 التقييم الإجمالي لحساب العميل: {client_name}")
    
    total_spend = df['المصروف'].sum()
    total_revenue = df['صافي المبيعات'].sum()
    total_profit = df['صافي الربح'].sum()
    total_roas = total_revenue / total_spend if total_spend > 0 else 0
    total_orders = df['صافي الأوردرات'].sum()
    
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="metric-box"><h4>المصروف الفعلي</h4><h2>{total_spend:,.0f} EGP</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-box"><h4>المبيعات المؤكدة</h4><h2>{total_revenue:,.0f} EGP</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-box"><h4>صافي الربح الحقيقي</h4><h2 style="color: {"#28a745" if total_profit > 0 else "#dc3545"};">{total_profit:,.0f} EGP</h2></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-box"><h4>عائد الإنفاق (ROAS)</h4><h2>{total_roas:.2f}x</h2></div>', unsafe_allow_html=True)

    st.write("---")
    st.write("### 🔍 توصيات الفترة القادمة")
    
    # بناء ملف الـ HTML الاحترافي للطباعة
    html_report = f"""
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>تقرير الحملات - {client_name}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 40px; color: #333; background-color: #f4f7f6; }}
            h1, h2, h3 {{ color: #2c3e50; }}
            .header-section {{ text-align: center; margin-bottom: 40px; border-bottom: 2px solid #ddd; padding-bottom: 20px; }}
            .dashboard-grid {{ display: flex; gap: 20px; margin-bottom: 40px; justify-content: space-between; }}
            .metric-card {{ background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 23%; text-align: center; border-bottom: 4px solid #007bff; }}
            .metric-card h4 {{ margin: 0 0 10px 0; color: #6c757d; font-size: 16px; }}
            .metric-card h2 {{ margin: 0; color: #2c3e50; font-size: 24px; }}
            .profit-positive {{ border-bottom-color: #28a745 !important; }}
            .profit-negative {{ border-bottom-color: #dc3545 !important; }}
            .campaign-box {{ background: #fff; border: 1px solid #e0e0e0; padding: 20px; border-radius: 10px; margin-bottom: 20px; page-break-inside: avoid; }}
            .kill {{ border-right: 6px solid #dc3545; }}
            .scale {{ border-right: 6px solid #28a745; }}
            .monitor {{ border-right: 6px solid #ffc107; }}
            .metrics-row {{ display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 15px; background: #f8f9fa; padding: 15px; border-radius: 5px; }}
            .metrics-row div {{ width: 30%; font-size: 14px; }}
            .advice-box {{ padding: 15px; border-top: 1px solid #eee; font-size: 15px; line-height: 1.6; }}
        </style>
    </head>
    <body>
        <div class="header-section">
            <h1>تقرير الأداء الإعلاني والمالي</h1>
            <h2>العميل: {client_name}</h2>
        </div>
        
        <h3>1. ملخص الكواليس (النتائج الإجمالية)</h3>
        <div class="dashboard-grid">
            <div class="metric-card">
                <h4>إجمالي المصروف</h4>
                <h2>{total_spend:,.0f} EGP</h2>
            </div>
            <div class="metric-card">
                <h4>المبيعات الصافية</h4>
                <h2>{total_revenue:,.0f} EGP</h2>
            </div>
            <div class="metric-card {'profit-positive' if total_profit > 0 else 'profit-negative'}">
                <h4>صافي الربح</h4>
                <h2 style="color: {'#28a745' if total_profit > 0 else '#dc3545'};">{total_profit:,.0f} EGP</h2>
            </div>
            <div class="metric-card">
                <h4>الـ ROAS الفعلي</h4>
                <h2>{total_roas:.2f}x</h2>
            </div>
        </div>
        
        <h3>2. تفصيل الحملات وتوصيات الفترة القادمة</h3>
    """

    for idx, row in df.iterrows():
        is_profitable = row['صافي الربح'] > 0
        if not is_profitable:
            status = "إيقاف فوري ❌"
            status_class = "status-kill"
            html_class = "kill"
        elif row['ROAS'] >= 3 and is_profitable:
            status = "زيادة ميزانية 🚀"
            status_class = "status-scale"
            html_class = "scale"
        else:
            status = "مراقبة وتعديل ⚠️"
            status_class = "status-monitor"
            html_class = "monitor"
            
        return_rate = (row['المرتجعات'] / row['إجمالي الأوردرات'] * 100) if row['إجمالي الأوردرات'] > 0 else 0
        
        st.markdown(f"""
        <div class="campaign-card">
            <h3 style="margin-top:0;">{row['اسم الحملة']} <span style="float:left; font-size: 16px;" class="{status_class}">{status}</span></h3>
            <hr style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                <div style="flex: 1; min-width: 150px;"><b>صافي الربح:</b> <span style="color: {"#28a745" if is_profitable else "#dc3545"}; font-size: 18px;"><b>{row['صافي الربح']:,.0f} EGP</b></span></div>
                <div style="flex: 1; min-width: 150px;"><b>ROAS (الصافي):</b> {row['ROAS']:.2f}x</div>
                <div style="flex: 1; min-width: 150px;"><b>تكلفة الاستحواذ:</b> {row['CPA']:,.0f} EGP</div>
                <div style="flex: 1; min-width: 150px;"><b>معدل النقر (CTR):</b> {row['CTR%']:.2f}%</div>
                <div style="flex: 1; min-width: 150px;"><b>نسبة الإغلاق (CR):</b> {row['CR%']:.1f}%</div>
            </div>
            <div style="margin-top: 15px; padding: 15px; background-color: #f8f9fa; border-radius: 5px; border-right: 4px solid #6c757d;">
                <b style="color:#333;">توصيات الفترة القادمة:</b><br>
                <span style="color: #dc3545;">▪</span> <b>المرتجعات:</b> تم استرجاع {row['المرتجعات']} أوردر بمعدل مرتجع: {return_rate:.1f}%.<br>
                <span style="color: #007bff;">▪</span> <b>الاستحواذ:</b> {"الهوك (Hook) ضعيف ومحتاجين نغير الكرييتف فوراً لرفع معدل النقر." if row['CTR%'] < 1.5 else "الكرييتف ممتاز ومعدل النقر صحي جداً."}<br>
                <span style="color: #28a745;">▪</span> <b>المبيعات:</b> {"فيه مشكلة في المبيعات، إما السعر عالي أو المودريتور بيحرق رسايل." if row['CR%'] < 10 else "فريق المبيعات شغال بكفاءة ومعدل الإغلاق ممتاز."}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # إضافة بيانات الحملة لملف الـ HTML
        html_report += f"""
        <div class="campaign-box {html_class}">
            <h3 style="margin-top: 0;">{row['اسم الحملة']} <span style="float: left; font-size: 16px;">{status}</span></h3>
            <div class="metrics-row">
                <div><b>صافي الربح:</b> <span style="color: {'#28a745' if is_profitable else '#dc3545'};">{row['صافي الربح']:,.0f} EGP</span></div>
                <div><b>الـ ROAS:</b> {row['ROAS']:.2f}x</div>
                <div><b>تكلفة العميل (CPA):</b> {row['CPA']:,.0f} EGP</div>
                <div><b>معدل النقر (CTR):</b> {row['CTR%']:.2f}%</div>
                <div><b>نسبة الإغلاق (CR):</b> {row['CR%']:.1f}%</div>
            </div>
            <div class="advice-box">
                <b>توصيات الفترة القادمة:</b><br>
                - نسبة المرتجعات لهذه الحملة هي {return_rate:.1f}%.<br>
                - {"الهوك فاشل ومحتاجين نغير الإعلان." if row['CTR%'] < 1.5 else "الإعلان جاذب للانتباه ومعدل النقر ممتاز."}<br>
                - {"توجد مشكلة في الرد على الرسائل أو تسعير المنتج." if row['CR%'] < 10 else "عملية الإغلاق داخل الرسائل ممتازة."}
            </div>
        </div>
        """
        
    html_report += "</body></html>"
    
    st.download_button(
        label="📥 تحميل التقرير للعميل (HTML - افتحه واطبعه كـ PDF)",
        data=html_report,
        file_name=f"Report_Campaign_{client_name}.html",
        mime="text/html"
    )
