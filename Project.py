import streamlit as st

# Predefined list of medical items and their prices
ITEMS = {
    "Paracetamol ": 20,
    "Ibuprofen ": 50,
    "Cough Syrup ": 60,
    "Antiseptic Cream ": 40,
    "Bandages ": 30,
    "Thermometer": 150,
    "Hand Sanitizer ": 120,
    "Face Masks ": 100,
    "Vitamin C Tablets ": 30,
    "Antacid Syrup ": 70,
}

# Initialize session state for user details
if "users" not in st.session_state:  #it checks user 
    st.session_state["users"] = {}  
if "user_name" not in st.session_state:
    st.session_state["user_name"] = None   #check user is not log in
if "medical_cart" not in st.session_state:
    st.session_state["medical_cart"] = []
if "delivery_address" not in st.session_state:
    st.session_state["delivery_address"] = ""

# Main page for login and account creation   
if st.session_state["user_name"] is None:    
    st.title("Welcome To The Medical Shop")
    st.header("Please Login Or Create An Account To Continue")

    action = st.radio("Select an Option:", ["Login", "Create Account"], horizontal=True)

    if action == "Create Account":
        st.subheader("Create A New Account")
        new_user = st.text_input("Enter a usernaame:")
        new_password = st.text_input("Enter a password:", type="password")
        if st.button("Create Account"):
            if new_user and new_password: 
                if new_user in st.session_state["users"]: 
                    st.error("Username already exists. Choose a different username.")
                else:
                    st.session_state["users"][new_user] = new_password 
                    st.success("Account created successfully! Please log in.")
            else:
                st.warning("Please fill in both username and password.")

    if action == "Login":
        st.subheader("Login To Your Account")
        existing_user = st.text_input("Enter your username:") 
        existing_password = st.text_input("Enter your password:", type="password")
        if st.button("Login"): 
            if (
                existing_user in st.session_state["users"]  
                and st.session_state["users"][existing_user] == existing_password   
            ):
                st.session_state["user_name"] = existing_user
                st.success(f"Welcome back, {existing_user}!")
            else:
                st.error("Invalid username or password.")
else:
    # Shopping page
    st.title(f"Welcome {st.session_state['user_name']} To The Medical Shop")
    st.header("Thank You For Choosing Our Pharmacy")
    st.subheader("Select Items And Manage Your Medicines")

    # Add Items to Cart
    st.subheader("Add New Item")
    item_name = st.selectbox("Select an Item", ["Choose an option"] + list(ITEMS.keys())) 
    if item_name != "Choose an option": 
        item_price = ITEMS[item_name]  
        item_quantity = st.number_input("Enter Quantity", min_value=1, step=1)  
        st.write(f"The price of {item_name} is ₹{item_price} per unit.") 

        if st.button("Add to Cart"):  
            st.session_state["medical_cart"].append(
                {"Item": item_name, "Price": item_price, "Quantity": item_quantity} 
            )
            st.success(f"{item_quantity} x {item_name} added to the cart at ₹{item_price} per unit!")

    st.subheader("Your Shopping Cart")
    if st.session_state["medical_cart"]:
        total_amount = 0
        for idx, item in enumerate(st.session_state["medical_cart"]): 
            st.write(
                f"{idx + 1}. {item['Item']} - ₹{item['Price']} x {item['Quantity']} = ₹{item['Price'] * item['Quantity']}"   #paracetmol-20*2=40   
            )
            total_amount += item["Price"] * item["Quantity"]

        st.write(f"Total Amount: ₹{total_amount}")

        # Payment Methods
        st.subheader("Select Payment Method")
        payment_method = st.selectbox("Choose Payment Method", ["Credit/Debit Card", "Net Banking", "Cash on Delivery"])
        st.write(f"Selected Payment Method: {payment_method}") 

        # Delivery Methods
        st.subheader("Select Delivery Method")
        delivery_method = st.selectbox("Choose Delivery Method", ["Home Delivery", "Store Pickup"]) 
        if delivery_method == "Home Delivery":
            delivery_address = st.text_area("Enter Delivery Address") 
            st.session_state["delivery_address"] = delivery_address  

        st.write(f"Selected Delivery Method: {delivery_method}")  
        if delivery_method == "Home Delivery" and not st.session_state["delivery_address"]: 
            st.warning("Please provide a delivery address for Home Delivery.")

        if st.button("Checkout"): 
            if delivery_method == "Home Delivery" and not st.session_state["delivery_address"]:
                st.error("Delivery address is required for Home Delivery.")
            else:
                st.success("Your order has been placed successfully!") 
                st.session_state["medical_cart"] = []  # Clear the cart after checkout

        if st.button("Clear Cart"):
            st.session_state["medical_cart"] = [] 
            st.success("Cart cleared!") # cart clear ke bad msg show 
    else:
        st.info("Your cart is empty. Add items to get started!")

    st.markdown("---")
    st.markdown(" Thank you for visiting and get well soon❤️")