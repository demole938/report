import streamlit as st
import pandas as pd
import numpy as np

# إعدادات الواجهة الاحترافية
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

st.title("Report Campaign")

client_name = st.text_input("اسم العميل:", placeholder="أدخل اسم العميل هنا...")

st.write("### إدخال بيانات الحملات")
init_data = pd.DataFrame([{
    "Campaign": "اسم الحملة", "Spend": 0.0, "Impressions": 0, 
    "Clicks": 0, "Messages": 0, "Gross_Orders": 0, "Returns": 0, 
    "Avg_Order_Value": 0.0, "Product_Cost": 0.0
}])

df_input = st.data_editor(init_data, num_rows="dynamic", use_container_width=True)

if st.button("تنفيذ التقرير"):
    df = df_input.copy()
    
    df['Net_Orders'] = df['Gross_Orders'] - df['Returns']
    df['Net_Revenue'] = df['Net_Orders'] * df['Avg_Order_Value']
    df['Total_Cost'] = df['Spend'] + (df['Net_Orders'] * df['Product_Cost'])
    df['Net_Profit'] = df['Net_Revenue'] - df['Total_Cost']
    
    df['ROAS'] = np.where(df['Spend'] > 0, df['Net_Revenue'] / df['Spend'], 0)
    df['CTR%'] = np.where(df['Impressions'] > 0, (df['Clicks'] / df['Impressions']) * 100, 0)
    df['CR%'] = np.where(df['Messages'] > 0, (df['Gross_Orders'] / df['Messages']) * 100, 0)
    df['CPA'] = np.where(df['Net_Orders'] > 0, df['Spend'] / df['Net_Orders'], 0)

    st.write("---")
    st.write(f"### 📊 التقييم الإجمالي لحساب العميل: {client_name}")
    
    total_spend = df['Spend'].sum()
    total_revenue = df['Net_Revenue'].sum()
    total_profit = df['Net_Profit'].sum()
    total_roas = total_revenue / total_spend if total_spend > 0 else 0
    
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="metric-box"><h4>إجمالي المصروف</h4><h2>{total_spend:,.0f} EGP</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-box"><h4>المبيعات الصافية</h4><h2>{total_revenue:,.0f} EGP</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-box"><h4>صافي الربح الحقيقي</h4><h2 style="color: {"#28a745" if total_profit > 0 else "#dc3545"};">{total_profit:,.0f} EGP</h2></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-box"><h4>عائد الإنفاق الإجمالي (ROAS)</h4><h2>{total_roas:.2f}x</h2></div>', unsafe_allow_html=True)

    st.write("---")
    st.write("### 🔍 توصيات الفترة القادمة")
    
    html_report = f"""
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>Report Campaign - {client_name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 40px; color: #333; }}
            h1, h2, h3 {{ color: #2c3e50; }}
            .summary {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
            .campaign {{ border: 1px solid #ddd; padding: 20px; border-radius: 8px; margin-bottom: 20px; page-break-inside: avoid; }}
            .kill {{ border-right: 5px solid #dc3545; }}
            .scale {{ border-right: 5px solid #28a745; }}
            .monitor {{ border-right: 5px solid #ffc107; }}
            .metrics span {{ display: inline-block; width: 30%; margin-bottom: 10px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>Report Campaign</h1>
        <h2>اسم العميل: {client_name}</h2>
        
        <div class="summary">
            <h3>الملخص المالي</h3>
            <p>إجمالي المصروف: <b>{total_spend:,.0f} EGP</b> | المبيعات الصافية: <b>{total_revenue:,.0f} EGP</b></p>
            <p>صافي الربح: <b>{total_profit:,.0f} EGP</b> | الـ ROAS الإجمالي: <b>{total_roas:.2f}x</b></p>
        </div>
        
        <h2>توصيات الفترة القادمة</h2>
    """

    for idx, row in df.iterrows():
        if row['Net_Profit'] < 0:
            status = "إيقاف فوري ❌"
            status_class = "status-kill"
            html_class = "kill"
        elif row['ROAS'] >= 3 and row['Net_Profit'] > 0:
            status = "زيادة ميزانية 🚀"
            status_class = "status-scale"
            html_class = "scale"
        else:
            status = "مراقبة وتعديل ⚠️"
            status_class = "status-monitor"
            html_class = "monitor"
            
        return_rate = (row['Returns'] / row['Gross_Orders'] * 100) if row['Gross_Orders'] > 0 else 0
        
        st.markdown(f"""
        <div class="campaign-card">
            <h3 style="margin-top:0;">{row['Campaign']} <span style="float:left; font-size: 16px;" class="{status_class}">{status}</span></h3>
            <hr style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                <div style="flex: 1; min-width: 150px;"><b>صافي الربح:</b> <span style="color: {"#28a745" if row['Net_Profit'] > 0 else "#dc3545"}; font-size: 18px;"><b>{row['Net_Profit']:,.0f} EGP</b></span></div>
                <div style="flex: 1; min-width: 150px;"><b>ROAS (الصافي):</b> {row['ROAS']:.2f}x</div>
                <div style="flex: 1; min-width: 150px;"><b>تكلفة الاستحواذ (CPA):</b> {row['CPA']:,.0f} EGP</div>
                <div style="flex: 1; min-width: 150px;"><b>معدل النقر (CTR):</b> {row['CTR%']:.2f}%</div>
                <div style="flex: 1; min-width: 150px;"><b>نسبة الإغلاق (CR):</b> {row['CR%']:.1f}%</div>
            </div>
            <div style="margin-top: 15px; padding: 15px; background-color: #f8f9fa; border-radius: 5px; border-right: 4px solid #6c757d;">
                <b style="color:#333;">توصيات الفترة القادمة:</b><br>
                <span style="color: #dc3545;">▪</span> <b>المرتجعات:</b> تم استرجاع {row['Returns']} أوردر من أصل {row['Gross_Orders']} (معدل المرتجع: {return_rate:.1f}%).<br>
                <span style="color: #007bff;">▪</span> <b>الاستحواذ:</b> {"الهوك فاشل ومعدل النقر ضعيف، يجب تغيير الكرييتف." if row['CTR%'] < 1.5 else "معدل النقر قوي، الكرييتف ينجح في جذب الانتباه."}<br>
                <span style="color: #28a745;">▪</span> <b>المبيعات:</b> {"المودريتور يفشل في الإغلاق، أو السعر غير مناسب للجمهور المستهدف." if row['CR%'] < 10 else "عملية الإغلاق داخل الرسائل تتم بكفاءة عالية."}
            </div>
        </div>
        """, unsafe_allow_html=True)

        html_report += f"""
        <div class="campaign {html_class}">
            <h3>{row['Campaign']} <span style="float:left;">{status}</span></h3>
            <div class="metrics">
                <span>صافي الربح: {row['Net_Profit']:,.0f} EGP</span>
                <span>ROAS: {row['ROAS']:.2f}x</span>
                <span>تكلفة الاستحواذ: {row['CPA']:,.0f} EGP</span><br>
                <span>معدل النقر: {row['CTR%']:.2f}%</span>
                <span>نسبة الإغلاق: {row['CR%']:.1f}%</span>
            </div>
            <p><b>التوصيات:</b><br>
            - معدل المرتجع: {return_rate:.1f}%<br>
            - الاستحواذ: {"الهوك فاشل ومعدل النقر ضعيف." if row['CTR%'] < 1.5 else "معدل النقر قوي."}<br>
            - المبيعات: {"المودريتور يفشل في الإغلاق." if row['CR%'] < 10 else "عملية الإغلاق ممتازة."}
            </p>
        </div>
        """
        
    html_report += "</body></html>"
    
    st.download_button(
        label="📥 تحميل التقرير (HTML - افتحه واطبعه كـ PDF)",
        data=html_report,
        file_name=f"Report_Campaign_{client_name}.html",
        mime="text/html"
    )
