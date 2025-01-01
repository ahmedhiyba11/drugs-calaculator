import streamlit as st
import pandas as pd

# Load the drug database (replace with the actual path to your CSV file)
data = pd.read_csv(r"c:\Users\DELLL\OneDrive\Desktop\drugs project\DRUGs database - p2.csv", encoding='ISO-8859-1')

# User Interface with Streamlit
st.markdown(
    """
    <style>
        .main { background-color: #f2f7fa; color: #2c3e50; }
        .title { text-align: center; font-size: 32px; color: #16a085; font-weight: bold; }
        .footer { text-align: center; color: #7f8c8d; font-size: small; }
        .highlight { color: #e74c3c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True
)

# Title with a background color
st.markdown('<div class="title">Drug Price Calculator</div>', unsafe_allow_html=True)

# Drug selection and price update section
st.subheader("Update Drug Price and Code")
selected_drug = st.selectbox("Choose a Drug", data["Drug Name"])
 
# Filter selected drug information
drug_info = data[data["Drug Name"] == selected_drug]

if not drug_info.empty:
    # Display and modify the price
    default_price = drug_info.iloc[0]["Price"]
    original_price = st.number_input("Original Price (EGP)", min_value=0.0, value=float(default_price), step=0.1)

    # Display and modify the drug code
    default_code = drug_info.iloc[0]["No"]
    drug_code = st.text_input("Drug Code (EDA)", value=default_code)

    # Save button
    if st.button("Save Changes"):
        # Update the price and code in the DataFrame
        data.loc[data["Drug Name"] == selected_drug, "Price"] = original_price
        data.loc[data["Drug Name"] == selected_drug, "No"] = drug_code

        # Save the updated DataFrame back to the CSV file
        data.to_csv(r"C:\Users\DELLL\OneDrive\Desktop\drugs project\DRUGs database - p2.csv", index=False, encoding='ISO-8859-1')
        st.success(f"Details for {selected_drug} have been updated.")

    # Price calculations
    price_with_7_percent = original_price * 1.07
    st.write(f"Price + 7%: <span class='highlight'>{price_with_7_percent:.2f} EGP</span>", unsafe_allow_html=True)
    price_with_14_percent = price_with_7_percent * 1.07
    st.write(f"Price + 14%: <span class='highlight'>{price_with_14_percent:.2f} EGP</span>", unsafe_allow_html=True)
else:
    st.write("Drug not found in the database.")

# Section to add a new drug
st.subheader("Add a New Drug")

# Create a form for new drug entry
with st.form("new_drug_form"):
    new_drug_name = st.text_input("Drug Name")
    new_drug_price = st.number_input("Price (EGP)", min_value=0.0, step=0.1)
    new_drug_code = st.text_input("Drug Code (EDA)")
    submit_new_drug = st.form_submit_button("Save New Drug")

    if submit_new_drug:
        # Check if all fields are filled
        if new_drug_name and new_drug_price > 0 and new_drug_code:
            # Check if the drug already exists
            if new_drug_name not in data["Drug Name"].values:
                # Add the new drug entry to the DataFrame
                new_entry = pd.DataFrame({"Drug Name": [new_drug_name], "Price": [new_drug_price], "No": [new_drug_code]})
                data = pd.concat([data, new_entry], ignore_index=True)

                # Save the updated DataFrame back to the CSV file
                data.to_csv(r"C:\Users\DELLL\OneDrive\Desktop\drugs project\DRUGs database - p2.csv", index=False, encoding='ISO-8859-1')
                st.success(f"{new_drug_name} has been added to the database with a price of {new_drug_price:.2f} EGP and code {new_drug_code}.")
            else:
                st.warning(f"{new_drug_name} is already in the database. Please enter a unique drug name.")
        else:
            st.error("Please fill in all fields.")
