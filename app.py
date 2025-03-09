import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

customers_df = pd.read_csv('customers_df_cleaned.csv')
geolocation_df = pd.read_csv('geolocation_df_cleaned.csv')
order_items_df = pd.read_csv('order_items_df_cleaned.csv')
order_payments_df = pd.read_csv('order_payments_df_cleaned.csv')
order_reviews_df = pd.read_csv('order_reviews_df_cleaned.csv')
orders_df = pd.read_csv('orders_df_cleaned.csv')
product_category_df = pd.read_csv('product_category_name_translation_df_cleaned.csv')
products_df = pd.read_csv('products_df_cleaned.csv')
sellers_df = pd.read_csv('sellers_df_cleaned.csv')

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
st.title("📊 E-Commerce Dashboard")
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Lihat:", ["Overview", "Orders Analysis", "Payments Analysis", "Reviews Analysis", "Top Categories", "Top Sellers"])

if page == "Overview":
    st.header("📌 Dataset Overview")
    dataset_options = st.selectbox("Pilih dataset yang ingin kamu lihat overview-nya", [
        "Customers", "Geolocation", "Order Items", "Order Payments", "Order Reviews",
        "Orders", "Product Category", "Products", "Sellers"])
    
    datasets = {
        "Customers": customers_df,
        "Geolocation": geolocation_df,
        "Order Items": order_items_df,
        "Order Payments": order_payments_df,
        "Order Reviews": order_reviews_df,
        "Orders": orders_df,
        "Product Category": product_category_df,
        "Products": products_df,
        "Sellers": sellers_df
    }
    
    st.write("**Shape:**", datasets[dataset_options].shape)
    st.write("**Preview:**")
    st.dataframe(datasets[dataset_options].head(10))

elif page == "Orders Analysis":
    st.header("📦 Orders Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Order Status Distribution")
        order_status_counts = orders_df['order_status'].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=order_status_counts.index, y=order_status_counts.values, ax=ax)
        ax.set_ylabel("Count")
        ax.set_xlabel("Order Status")
        plt.xticks(rotation=45) 
        st.pyplot(fig)
    
    with col2:
        st.subheader("Order Count by Purchase Timestamp")
        orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
        order_time_series = orders_df.resample('M', on='order_purchase_timestamp').size()
        fig, ax = plt.subplots()
        order_time_series.plot(ax=ax)
        ax.set_ylabel("Number of Orders")
        ax.set_xlabel("Month")
        st.pyplot(fig)

elif page == "Payments Analysis":
    st.header("💰 Payments Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Payment Types Distribution")
        payment_counts = order_payments_df['payment_type'].value_counts()
        fig, ax = plt.subplots()
        payment_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Total Payment Value by Type")
        payment_sum = order_payments_df.groupby('payment_type')['payment_value'].sum()
        fig, ax = plt.subplots()
        sns.barplot(x=payment_sum.index, y=payment_sum.values, ax=ax)
        ax.set_ylabel("Total Payment Value")
        ax.set_xlabel("Payment Type")
        st.pyplot(fig)

elif page == "Reviews Analysis":
    st.header("⭐ Reviews Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Review Score Distribution")
        review_counts = order_reviews_df['review_score'].value_counts().sort_index()
        fig, ax = plt.subplots()
        sns.barplot(x=review_counts.index, y=review_counts.values, ax=ax)
        ax.set_ylabel("Count")
        ax.set_xlabel("Review Score")
        st.pyplot(fig)
    
    with col2:
        st.subheader("Average Review Score Over Time")
        order_reviews_df['review_creation_date'] = pd.to_datetime(order_reviews_df['review_creation_date'])
        review_time_series = order_reviews_df.resample('M', on='review_creation_date')['review_score'].mean()
        fig, ax = plt.subplots()
        review_time_series.plot(ax=ax)
        ax.set_ylabel("Average Review Score")
        ax.set_xlabel("Month")
        st.pyplot(fig)
    
elif page == "Top Categories":
    st.header("🏆 Top Product Categories")
    st.subheader("Top 10 Most Popular Categories")
    merged_df = order_items_df.merge(products_df, on='product_id').merge(product_category_df, on='product_category_name')
    top_categories = merged_df['product_category_name_english'].value_counts().nlargest(10)
    fig, ax = plt.subplots()
    sns.barplot(x=top_categories.values, y=top_categories.index, ax=ax, orient='h')
    ax.set_xlabel("Number of Orders")
    ax.set_ylabel("Product Category")
    st.pyplot(fig)

elif page == "Top Sellers":
    st.header("🏆 Top Sellers")
    st.subheader("Top 10 Best-Selling Sellers")
    top_sellers = order_items_df.groupby('seller_id')['order_id'].count().nlargest(10)
    fig, ax = plt.subplots()
    sns.barplot(x=top_sellers.values, y=top_sellers.index, ax=ax, orient='h')
    ax.set_xlabel("Number of Orders")
    ax.set_ylabel("Seller ID")
    st.pyplot(fig)
