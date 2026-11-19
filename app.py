import streamlit as st
import pandas as pd

from order import Order
from order_book import OrderBook
from matching_engine import MatchingEngine


st.set_page_config(
    page_title="TradeFlow",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background-color: #161b22;
}

h1, h2, h3 {
    color: #f0f3f6;
}

.metric-card {
    background: #161b22;
    border: 1px solid #30363d;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.metric-label {
    color: #8b949e;
    font-size: 14px;
}

.metric-value {
    color: #f0f3f6;
    font-size: 28px;
    font-weight: 600;
}

.buy-title {
    color: #3fb950;
}

.sell-title {
    color: #f85149;
}

.trade-title {
    color: #58a6ff;
}

div.stButton > button {
    border-radius: 8px;
    height: 45px;
    font-weight: 600;
    border: 1px solid #30363d;
}

div.stButton > button:hover {
    border-color: #58a6ff;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #30363d;
    border-radius: 10px;
}

hr {
    border-color: #30363d;
}

</style>
""", unsafe_allow_html=True)


# Initialize application state
if "order_book" not in st.session_state:
    st.session_state.order_book = OrderBook()

if "engine" not in st.session_state:
    st.session_state.engine = MatchingEngine(st.session_state.order_book)

if "order_counter" not in st.session_state:
    st.session_state.order_counter = 1


order_book = st.session_state.order_book
engine = st.session_state.engine


# Header
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("# 📈 TradeFlow")
    st.caption("Stock Order Book Simulator")

with col2:
    st.markdown(
        """
        <div style="text-align:right; padding-top:25px;">
            <span style="color:#3fb950;">●</span>
            <span style="color:#8b949e;">Simulation Active</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()


# Statistics
total_orders = len(order_book.buy_orders) + len(order_book.sell_orders)
total_trades = len(engine.trades)

traded_volume = sum(trade.quantity for trade in engine.trades)

buy_value = sum(
    order.price * order.remaining_quantity
    for order in order_book.buy_orders
)

sell_value = sum(
    order.price * order.remaining_quantity
    for order in order_book.sell_orders
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Pending Orders", total_orders)
col2.metric("Executed Trades", total_trades)
col3.metric("Traded Volume", traded_volume)
col4.metric("Open Buy Value", f"₹{buy_value:,.2f}")

st.divider()


# Order placement
with st.expander("＋  Place a New Order", expanded=True):

    with st.form("order_form"):

        col1, col2 = st.columns(2)

        with col1:
            symbol = st.text_input(
                "Stock Symbol",
                value="TCS"
            ).strip().upper()

            side = st.selectbox(
                "Order Side",
                ["BUY", "SELL"]
            )

        with col2:
            price = st.number_input(
                "Price (₹)",
                min_value=0.01,
                value=100.0,
                step=1.0
            )

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=10,
                step=1
            )

        submitted = st.form_submit_button(
            "Submit Order",
            use_container_width=True
        )

        if submitted:

            if not symbol:
                st.error("Stock symbol cannot be empty.")

            else:
                order = Order(
                    st.session_state.order_counter,
                    symbol,
                    side,
                    price,
                    quantity
                )

                st.session_state.order_counter += 1

                order_book.add_order(order)
                engine.match_orders()

                st.success(
                    f"{side} order for {symbol} submitted successfully."
                )


st.divider()


# Data conversion functions
def order_data(orders):

    return [
        {
            "ID": order.order_id,
            "Stock": order.symbol,
            "Price (₹)": order.price,
            "Qty": order.quantity,
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
            "Price (₹)": trade.price,
            "Qty": trade.quantity,
            "Buyer": trade.buy_order_id,
            "Seller": trade.sell_order_id
        }
        for trade in trades
    ]


# Order books
buy_orders = order_book.buy_orders
sell_orders = order_book.sell_orders


col1, col2 = st.columns(2)

with col1:

    st.markdown(
        "<h3 class='buy-title'>🟢 BUY Order Book</h3>",
        unsafe_allow_html=True
    )

    if buy_orders:

        buy_df = pd.DataFrame(order_data(buy_orders))

        st.dataframe(
            buy_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No pending BUY orders.")


with col2:

    st.markdown(
        "<h3 class='sell-title'>🔴 SELL Order Book</h3>",
        unsafe_allow_html=True
    )

    if sell_orders:

        sell_df = pd.DataFrame(order_data(sell_orders))

        st.dataframe(
            sell_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No pending SELL orders.")


st.divider()


# Trade history
st.markdown(
    "<h3 class='trade-title'>📋 Executed Trade History</h3>",
    unsafe_allow_html=True
)

if engine.trades:

    trades_df = pd.DataFrame(trade_data(engine.trades))

    st.dataframe(
        trades_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("Trades will appear here once BUY and SELL orders are matched.")


st.divider()


# Footer
st.markdown(
    """
    <div style="text-align:center; color:#8b949e; font-size:13px;">
        TradeFlow · Stock Order Book Simulator<br>
        Educational simulation — no real market transactions
    </div>
    """,
    unsafe_allow_html=True
)