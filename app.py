import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
customers_df = pd.read_csv('customers_df_cleaned.csv')
geolocation_df = pd.read_csv('geolocation_df_cleaned.csv')
order_items_df = pd.read_csv('order_items_df_cleaned.csv')
order_payments_df = pd.read_csv('order_payments_df_cleaned.csv')
order_reviews_df = pd.read_csv('order_reviews_df_cleaned.csv')
orders_df = pd.read_csv('orders_df_cleaned.csv')
product_category_df = pd.read_csv('product_category_name_translation_df_cleaned.csv')
products_df = pd.read_csv('products_df_cleaned.csv')
sellers_df = pd.read_csv('sellers_df_cleaned.csv')

# Convert date columns
orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
order_reviews_df['review_creation_date'] = pd.to_datetime(order_reviews_df['review_creation_date'])

# Streamlit UI
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
st.title("📊 E-Commerce Dashboard")
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Lihat:", ["Orders Analysis", "Payments Analysis", "Reviews Analysis", "Top Categories", "Top Sellers"])

if page == "Orders Analysis":
    st.header("📦 Orders Analysis")
    
    # Filter Tanggal di Dalam Halaman
    st.subheader("📆 Filter Data Berdasarkan Rentang Waktu")
    start_date = st.date_input("Start Date", orders_df['order_purchase_timestamp'].min().date())
    end_date = st.date_input("End Date", orders_df['order_purchase_timestamp'].max().date())

    # Filter data
    filtered_orders = orders_df[(orders_df['order_purchase_timestamp'] >= pd.Timestamp(start_date)) &
                                (orders_df['order_purchase_timestamp'] <= pd.Timestamp(end_date))]
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Order Status Distribution")
        order_status_counts = filtered_orders['order_status'].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=order_status_counts.index, y=order_status_counts.values, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Order Trend Over Time")
        order_time_series = filtered_orders.resample('M', on='order_purchase_timestamp').size()
        fig, ax = plt.subplots()
        order_time_series.plot(ax=ax)
        st.pyplot(fig)

elif page == "Payments Analysis":
    st.header("💰 Payments Analysis")
    
    # Filter Tanggal di Dalam Halaman
    st.subheader("📆 Filter Data Berdasarkan Rentang Waktu")
    start_date = st.date_input("Start Date", orders_df['order_purchase_timestamp'].min().date(), key="pay_start")
    end_date = st.date_input("End Date", orders_df['order_purchase_timestamp'].max().date(), key="pay_end")

    # Filter data
    filtered_orders = orders_df[(orders_df['order_purchase_timestamp'] >= pd.Timestamp(start_date)) &
                                (orders_df['order_purchase_timestamp'] <= pd.Timestamp(end_date))]
    filtered_payments = order_payments_df.merge(filtered_orders[['order_id']], on='order_id')

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Payment Types Distribution")
        payment_counts = filtered_payments['payment_type'].value_counts()
        fig, ax = plt.subplots()
        payment_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Total Payment Value by Type")
        payment_sum = filtered_payments.groupby('payment_type')['payment_value'].sum()
        fig, ax = plt.subplots()
        sns.barplot(x=payment_sum.index, y=payment_sum.values, ax=ax)
        st.pyplot(fig)

elif page == "Reviews Analysis":
    st.header("⭐ Reviews Analysis")
    
    # Filter Tanggal di Dalam Halaman
    st.subheader("📆 Filter Data Berdasarkan Rentang Waktu")
    start_date = st.date_input("Start Date", order_reviews_df['review_creation_date'].min().date(), key="review_start")
    end_date = st.date_input("End Date", order_reviews_df['review_creation_date'].max().date(), key="review_end")

    # Filter data
    filtered_reviews = order_reviews_df[(order_reviews_df['review_creation_date'] >= pd.Timestamp(start_date)) &
                                        (order_reviews_df['review_creation_date'] <= pd.Timestamp(end_date))]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Review Score Distribution")
        review_counts = filtered_reviews['review_score'].value_counts().sort_index()
        fig, ax = plt.subplots()
        sns.barplot(x=review_counts.index, y=review_counts.values, ax=ax)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Average Review Score Over Time")
        review_time_series = filtered_reviews.resample('M', on='review_creation_date')['review_score'].mean()
        fig, ax = plt.subplots()
        review_time_series.plot(ax=ax)
        st.pyplot(fig)

elif page == "Top Categories":
    st.header("🏆 Top Product Categories")
    
    # Filter Tanggal di Dalam Halaman
    st.subheader("📆 Filter Data Berdasarkan Rentang Waktu")
    start_date = st.date_input("Start Date", orders_df['order_purchase_timestamp'].min().date(), key="cat_start")
    end_date = st.date_input("End Date", orders_df['order_purchase_timestamp'].max().date(), key="cat_end")

    # Filter data
    filtered_orders = orders_df[(orders_df['order_purchase_timestamp'] >= pd.Timestamp(start_date)) &
                                (orders_df['order_purchase_timestamp'] <= pd.Timestamp(end_date))]
    
    merged_df = order_items_df.merge(products_df, on='product_id').merge(product_category_df, on='product_category_name')
    merged_df = merged_df[merged_df['order_id'].isin(filtered_orders['order_id'])]

    top_n = st.slider("Pilih jumlah kategori yang ingin ditampilkan:", 5, 20, 10)
    top_categories = merged_df['product_category_name_english'].value_counts().nlargest(top_n)

    fig, ax = plt.subplots()
    sns.barplot(x=top_categories.values, y=top_categories.index, ax=ax, orient='h')
    st.pyplot(fig)

elif page == "Top Sellers":
    st.header("🏆 Top Sellers")
    
    # Filter Tanggal di Dalam Halaman
    st.subheader("📆 Filter Data Berdasarkan Rentang Waktu")
    start_date = st.date_input("Start Date", orders_df['order_purchase_timestamp'].min().date(), key="sell_start")
    end_date = st.date_input("End Date", orders_df['order_purchase_timestamp'].max().date(), key="sell_end")

    # Filter data
    filtered_orders = orders_df[(orders_df['order_purchase_timestamp'] >= pd.Timestamp(start_date)) &
                                (orders_df['order_purchase_timestamp'] <= pd.Timestamp(end_date))]

    top_n_sellers = st.slider("Pilih jumlah seller yang ingin ditampilkan:", 5, 20, 10)
    top_sellers = order_items_df[order_items_df['order_id'].isin(filtered_orders['order_id'])].groupby('seller_id')['order_id'].count().nlargest(top_n_sellers)

    fig, ax = plt.subplots()
    sns.barplot(x=top_sellers.values, y=top_sellers.index, ax=ax, orient='h')
    st.pyplot(fig)
