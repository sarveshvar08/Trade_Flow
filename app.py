import streamlit as st
import pandas as pd

from order import Order
from order_book import OrderBook
from matching_engine import MatchingEngine


st.set_page_config(page_title="TradeFlow", layout="wide")

st.title("TradeFlow")
st.caption("Stock Order Book Simulator")

if "order_book" not in st.session_state:
    st.session_state.order_book = OrderBook()

if "engine" not in st.session_state:
    st.session_state.engine = MatchingEngine(st.session_state.order_book)

if "order_counter" not in st.session_state:
    st.session_state.order_counter = 1


with st.form("order_form"):
    st.subheader("Place Order")

    symbol = st.text_input("Stock Symbol", value="TCS").upper()
    side = st.selectbox("Order Type", ["BUY", "SELL"])
    price = st.number_input("Price", min_value=0.01, value=100.0)
    quantity = st.number_input("Quantity", min_value=1, value=10, step=1)

    submitted = st.form_submit_button("Place Order")

    if submitted:
        if not symbol.strip():
            st.error("Please enter a stock symbol.")
        else:
            order = Order(
                st.session_state.order_counter,
                symbol,
                side,
                price,
                quantity
            )

            st.session_state.order_counter += 1

            st.session_state.order_book.add_order(order)
            st.session_state.engine.match_orders()

            st.success("Order placed successfully!")


buy_orders = st.session_state.order_book.buy_orders
sell_orders = st.session_state.order_book.sell_orders
trades = st.session_state.engine.trades


def order_data(orders):
    return [
        {
            "Order ID": order.order_id,
            "Stock": order.symbol,
            "Price": order.price,
            "Quantity": order.quantity,
            "Remaining": order.remaining_quantity,
            "Status": order.status
        }
        for order in orders
    ]


def trade_data(trades):
    return [
        {
            "Trade ID": trade.trade_id,
            "Stock": trade.symbol,
            "Price": trade.price,
            "Quantity": trade.quantity,
            "BUY ID": trade.buy_order_id,
            "SELL ID": trade.sell_order_id
        }
        for trade in trades
    ]


st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("BUY Order Book")

    if buy_orders:
        st.dataframe(
            pd.DataFrame(order_data(buy_orders)),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No pending BUY orders.")

with col2:
    st.subheader("SELL Order Book")

    if sell_orders:
        st.dataframe(
            pd.DataFrame(order_data(sell_orders)),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No pending SELL orders.")


st.divider()

st.subheader("Executed Trades")

if trades:
    st.dataframe(
        pd.DataFrame(trade_data(trades)),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No trades executed yet.")