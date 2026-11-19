import streamlit as st
import pandas as pd

from order import Order
from order_book import OrderBook
from matching_engine import MatchingEngine


# Page configuration
st.set_page_config(
    page_title="TradeFlow",
    page_icon="📈",
    layout="wide"
)


# Styling
st.markdown("""
<style>
.stApp {
    background: #0b0f19;
    color: #e6edf3;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.8rem;
    padding-bottom: 2rem;
}

[data-testid="stMetric"] {
    background: #141a27;
    border: 1px solid #252d3b;
    padding: 18px;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: #9aa4b2;
}

[data-testid="stMetricValue"] {
    color: #e6edf3;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #252d3b;
    border-radius: 10px;
}

div.stButton > button,
div.stFormSubmitButton > button {
    border-radius: 8px;
    min-height: 42px;
    font-weight: 600;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    border-color: #58a6ff;
}

.buy-heading {
    color: #3fb950;
    font-size: 22px;
    font-weight: 700;
}

.sell-heading {
    color: #f85149;
    font-size: 22px;
    font-weight: 700;
}

.trade-heading {
    color: #58a6ff;
    font-size: 22px;
    font-weight: 700;
}

.small-text {
    color: #8b949e;
    font-size: 13px;
}

div[data-testid="stExpander"] {
    background: #141a27;
    border: 1px solid #252d3b;
    border-radius: 12px;
}

hr {
    border-color: #252d3b;
}

</style>
""", unsafe_allow_html=True)


# Initialize session state
if "order_book" not in st.session_state:
    st.session_state.order_book = OrderBook()

if "engine" not in st.session_state:
    st.session_state.engine = MatchingEngine(st.session_state.order_book)

if "order_counter" not in st.session_state:
    st.session_state.order_counter = 1


order_book = st.session_state.order_book
engine = st.session_state.engine


# Header
col1, col2 = st.columns([4, 1])

with col1:
    st.markdown("# 📈 TradeFlow")
    st.caption("Stock Order Book Simulator")

with col2:
    st.markdown(
        """
        <div style="text-align:right;padding-top:25px;">
        <span style="color:#3fb950;">●</span>
        <span style="color:#8b949e;">Simulation Active</span>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# Dashboard statistics
pending_orders = order_book.buy_orders + order_book.sell_orders

total_pending = len(pending_orders)
total_trades = len(engine.trades)

traded_volume = sum(
    trade.quantity for trade in engine.trades
)

buy_value = sum(
    order.price * order.remaining_quantity
    for order in order_book.buy_orders
)

sell_value = sum(
    order.price * order.remaining_quantity
    for order in order_book.sell_orders
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Pending Orders", total_pending)
col2.metric("Executed Trades", total_trades)
col3.metric("Traded Volume", traded_volume)
col4.metric("Open Buy Value", f"₹{buy_value:,.2f}")


st.divider()


# Order placement
st.markdown("### Place an Order")

with st.expander("New Order", expanded=True):

    with st.form("order_form"):

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            symbol = st.text_input(
                "Stock Symbol",
                value="TCS"
            ).strip().upper()

        with col2:
            side = st.selectbox(
                "Order Side",
                ["BUY", "SELL"]
            )

        with col3:
            price = st.number_input(
                "Price (₹)",
                min_value=0.01,
                value=100.0,
                step=1.0
            )

        with col4:
            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=10,
                step=1
            )

        submitted = st.form_submit_button(
            "Place Order",
            use_container_width=True
        )

        if submitted:

            if not symbol:
                st.error("Enter a valid stock symbol.")

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
                    f"{side} order for {symbol} placed successfully."
                )


st.divider()


# Stock filter
available_symbols = sorted(
    set(
        order.symbol
        for order in order_book.buy_orders + order_book.sell_orders
    ) |
    set(
        trade.symbol
        for trade in engine.trades
    )
)

filter_options = ["ALL"] + available_symbols

selected_symbol = st.selectbox(
    "Filter by Stock",
    filter_options
)


# Filtering
if selected_symbol == "ALL":

    filtered_buy_orders = order_book.buy_orders
    filtered_sell_orders = order_book.sell_orders
    filtered_trades = engine.trades

else:

    filtered_buy_orders = [
        order for order in order_book.buy_orders
        if order.symbol == selected_symbol
    ]

    filtered_sell_orders = [
        order for order in order_book.sell_orders
        if order.symbol == selected_symbol
    ]

    filtered_trades = [
        trade for trade in engine.trades
        if trade.symbol == selected_symbol
    ]


# Order table conversion
def order_data(orders):

    return [
        {
            "Order ID": order.order_id,
            "Stock": order.symbol,
            "Price (₹)": order.price,
            "Quantity": order.quantity,
            "Remaining": order.remaining_quantity,
            "Status": order.status
        }
        for order in orders
    ]


# Trade table conversion
def trade_data(trades):

    return [
        {
            "Trade ID": trade.trade_id,
            "Stock": trade.symbol,
            "Price (₹)": trade.price,
            "Quantity": trade.quantity,
            "Buyer ID": trade.buy_order_id,
            "Seller ID": trade.sell_order_id
        }
        for trade in trades
    ]


# Order books
col1, col2 = st.columns(2)

with col1:

    st.markdown(
        '<p class="buy-heading">🟢 BUY Order Book</p>',
        unsafe_allow_html=True
    )

    if filtered_buy_orders:

        st.dataframe(
            pd.DataFrame(order_data(filtered_buy_orders)),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No pending BUY orders.")


with col2:

    st.markdown(
        '<p class="sell-heading">🔴 SELL Order Book</p>',
        unsafe_allow_html=True
    )

    if filtered_sell_orders:

        st.dataframe(
            pd.DataFrame(order_data(filtered_sell_orders)),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No pending SELL orders.")


st.divider()


# Trade history
st.markdown(
    '<p class="trade-heading">📊 Executed Trade History</p>',
    unsafe_allow_html=True
)

if filtered_trades:

    st.dataframe(
        pd.DataFrame(trade_data(filtered_trades)),
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No trades recorded yet.")


st.divider()


# Simulation information
col1, col2 = st.columns(2)

with col1:

    st.markdown("### Simulation Overview")

    st.write(f"**Active Stocks:** {len(available_symbols)}")
    st.write(f"**Pending BUY Orders:** {len(order_book.buy_orders)}")
    st.write(f"**Pending SELL Orders:** {len(order_book.sell_orders)}")
    st.write(f"**Total Trades:** {len(engine.trades)}")

with col2:

    st.markdown("### Order Book Values")

    st.write(f"**Open BUY Value:** ₹{buy_value:,.2f}")
    st.write(f"**Open SELL Value:** ₹{sell_value:,.2f}")
    st.write(f"**Executed Volume:** {traded_volume} shares")


st.divider()


# Reset simulation
with st.expander("Simulation Controls"):

    st.warning("Resetting clears all pending orders and trade history.")

    if st.button("Reset Simulation", type="secondary"):

        st.session_state.order_book = OrderBook()
        st.session_state.engine = MatchingEngine(
            st.session_state.order_book
        )
        st.session_state.order_counter = 1

        st.rerun()


# Footer
st.markdown(
    """
    <div style="text-align:center;color:#8b949e;font-size:13px;">
        <br>
        TradeFlow · Stock Order Book Simulator<br>
        Educational simulation · No real market transactions
    </div>
    """,
    unsafe_allow_html=True
)