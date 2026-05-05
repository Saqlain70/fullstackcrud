import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="CRUD App", page_icon="📝", layout="wide")

st.title("📝 Full-Stack CRUD Application")
st.markdown("---")

menu = ["Create Item", "View Items", "Update Item", "Delete Item"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Create Item":
    st.subheader("➕ Create New Item")
    with st.form("create_form"):
        name = st.text_input("Item Name")
        price = st.number_input("Price", min_value=0.01, step=0.01)
        description = st.text_area("Description")
        submitted = st.form_submit_button("Create Item")
        
        if submitted and name:
            response = requests.post(f"{API_URL}/items", json={"name": name, "price": price, "description": description})
            if response.status_code == 201:
                st.success("Item created!")

elif choice == "View Items":
    st.subheader("📋 All Items")
    response = requests.get(f"{API_URL}/items")
    if response.status_code == 200:
        items = response.json()
        if items:
            df = pd.DataFrame(items)
            st.dataframe(df)
        else:
            st.info("No items found")

elif choice == "Update Item":
    st.subheader("✏️ Update Item")
    response = requests.get(f"{API_URL}/items")
    if response.status_code == 200:
        items = response.json()
        if items:
            item_ids = [item['id'] for item in items]
            selected_id = st.selectbox("Select Item ID", item_ids)
            if selected_id:
                item = requests.get(f"{API_URL}/items/{selected_id}").json()
                with st.form("update_form"):
                    name = st.text_input("Name", value=item['name'])
                    price = st.number_input("Price", value=float(item['price']))
                    if st.form_submit_button("Update"):
                        requests.put(f"{API_URL}/items/{selected_id}", json={"name": name, "price": price})
                        st.success("Updated!")

elif choice == "Delete Item":
    st.subheader("🗑️ Delete Item")
    response = requests.get(f"{API_URL}/items")
    if response.status_code == 200:
        items = response.json()
        if items:
            selected_id = st.selectbox("Select Item ID to Delete", [item['id'] for item in items])
            if st.button("Delete"):
                requests.delete(f"{API_URL}/items/{selected_id}")
                st.success("Deleted!")
                st.rerun()
