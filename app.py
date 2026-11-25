import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="APL Logistics | Delivery Intelligence", page_icon="🚚", layout="wide")
st.title("🚚 APL Logistics — Delivery Performance & Delay Risk")
st.caption("Operational diagnostic dashboard | Source dataset: 180,519 shipment records")

@st.cache_data
def load_data():
    d = pd.read_csv("apl_logistics_analysis_data.csv.zip", compression="zip", encoding="utf-8-sig")
    d["Days for shipping (real)"] = pd.to_numeric(d["Days for shipping (real)"], errors="coerce")
    d["Days for shipment (scheduled)"] = pd.to_numeric(d["Days for shipment (scheduled)"], errors="coerce")
    d["Late_delivery_risk"] = pd.to_numeric(d["Late_delivery_risk"], errors="coerce")
    d["Delay Gap"] = d["Days for shipping (real)"] - d["Days for shipment (scheduled)"]
    d["Delivery Classification"] = np.select([d["Delay Gap"]>0,d["Delay Gap"]<0],["Delayed","Early"],default="On-time")
    return d

df=load_data()
st.sidebar.header("Dashboard filters")
def options(col):
    return sorted(df[col].dropna().astype(str).unique().tolist())
mode=st.sidebar.multiselect("Shipping mode", options("Shipping Mode"), default=options("Shipping Mode"))
region=st.sidebar.multiselect("Order region", options("Order Region"), default=options("Order Region"))
market=st.sidebar.multiselect("Market", options("Market"), default=options("Market"))
segment=st.sidebar.multiselect("Customer segment", options("Customer Segment"), default=options("Customer Segment"))
status=st.sidebar.multiselect("Delivery status", options("Delivery Status"), default=options("Delivery Status"))
f=df[df["Shipping Mode"].astype(str).isin(mode)&df["Order Region"].astype(str).isin(region)&df["Market"].astype(str).isin(market)&df["Customer Segment"].astype(str).isin(segment)&df["Delivery Status"].astype(str).isin(status)]
if f.empty:
    st.warning("No records match the selected filters.")
    st.stop()

total=len(f); delayed=(f["Delay Gap"]>0).mean()*100; ontime=(f["Delay Gap"]==0).mean()*100
risk=f["Late_delivery_risk"].mean()*100; gap=f["Delay Gap"].mean()
c1,c2,c3,c4,c5=st.columns(5)
c1.metric("Shipments",f"{total:,}")
c2.metric("Delayed share",f"{delayed:.2f}%")
c3.metric("Exactly on-time",f"{ontime:.2f}%")
c4.metric("Late-risk flag",f"{risk:.2f}%")
c5.metric("Mean delay gap",f"{gap:.2f} days")
st.caption("Classification uses actual shipping days minus scheduled days. Positive = delayed; zero = on-time; negative = early. No date field exists in the supplied dataset, so a date filter is not available.")

tabs=st.tabs(["Overview","Shipping modes","Geography","Customer segments","Data quality"])
with tabs[0]:
    left,right=st.columns(2)
    with left:
        cl=f["Delivery Classification"].value_counts().rename_axis("Classification").reset_index(name="Shipments")
        st.plotly_chart(px.pie(cl,names="Classification",values="Shipments",title="Delivery classification"),use_container_width=True)
    with right:
        st.plotly_chart(px.histogram(f,x="Delay Gap",nbins=7,title="Delay-gap distribution"),use_container_width=True)
    st.subheader("Delivery status")
    st.dataframe(f["Delivery Status"].value_counts().rename_axis("Status").reset_index(name="Shipments"),use_container_width=True)
with tabs[1]:
    m=f.groupby("Shipping Mode").agg(Shipments=("Delay Gap","size"),Delayed_Share=("Delivery Classification",lambda s:(s=="Delayed").mean()*100),Mean_Gap=("Delay Gap","mean"),Risk_Share=("Late_delivery_risk","mean")).reset_index()
    st.plotly_chart(px.bar(m,x="Shipping Mode",y="Delayed_Share",text_auto=".1f",title="Delayed share by shipping mode (%)"),use_container_width=True)
    st.dataframe(m.round(3),use_container_width=True)
with tabs[2]:
    geo=f.groupby("Market").agg(Shipments=("Delay Gap","size"),Delayed_Share=("Delivery Classification",lambda s:(s=="Delayed").mean()*100),Mean_Gap=("Delay Gap","mean"),Risk_Share=("Late_delivery_risk","mean")).reset_index()
    st.plotly_chart(px.bar(geo,x="Market",y="Delayed_Share",color="Delayed_Share",title="Market-wise delayed share (%)"),use_container_width=True)
    reg=f.groupby("Order Region").agg(Shipments=("Delay Gap","size"),Delayed_Share=("Delivery Classification",lambda s:(s=="Delayed").mean()*100),Mean_Gap=("Delay Gap","mean")).reset_index().sort_values("Delayed_Share",ascending=False)
    st.dataframe(reg.round(3),use_container_width=True)
with tabs[3]:
    seg=f.groupby("Customer Segment").agg(Shipments=("Delay Gap","size"),Delayed_Share=("Delivery Classification",lambda s:(s=="Delayed").mean()*100),Mean_Gap=("Delay Gap","mean"),Risk_Share=("Late_delivery_risk","mean")).reset_index()
    st.plotly_chart(px.bar(seg,x="Customer Segment",y="Delayed_Share",title="Delayed share by customer segment (%)"),use_container_width=True)
    st.dataframe(seg.round(3),use_container_width=True)
with tabs[4]:
    st.write("The analysis-ready file excludes customer names, street addresses, postal codes and customer IDs.")
    st.write("Missing values:")
    st.dataframe(df.isna().sum().loc[lambda x:x>0].rename("Missing").reset_index(names="Field"),use_container_width=True)
    st.write("Risk flag versus delay-gap classification:")
    st.dataframe(pd.crosstab(f["Delivery Classification"],f["Late_delivery_risk"]),use_container_width=True)
    st.info("The CSV contains no order or delivery date. Cancelled shipments should be separated from completed-delivery SLA reporting. The supplied risk flag is not identical to a positive delay gap.")
st.download_button("Download filtered records",f.to_csv(index=False).encode("utf-8-sig"),"apl_filtered_shipments.csv","text/csv")
