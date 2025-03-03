import os
import random
import csv
import html
import streamlit as st
import pandas as pd
from time import sleep

# Page Configuration
st.set_page_config(page_title="Baccarat Casino", page_icon="🎲", layout="wide")

# Apply custom background color for a casino feel
def set_background_color():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #006400;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
set_background_color()

# Define card values and colors
card_values = {
    **{f'{rank}{suit}': (0 if rank in 'JQK10' else 1 if rank == 'A' else int(rank), 'black' if suit in '♠♣' else 'red')
       for rank in [str(n) for n in range(2, 11)] + ['J', 'Q', 'K', 'A'] for suit in '♠♥♦♣'}
}

# Deck of 8 shuffled decks
deck = list(card_values.keys()) * 8
random.shuffle(deck)

def deal_card():
    global deck
    if len(deck) <= 10:
        st.warning("🔄 The deck is nearly exhausted. Next hand will be the last hand before reshuffling.")
        deck = list(card_values.keys()) * 8
        random.shuffle(deck)
    return deck.pop()

def calculate_hand_value(hand):
    return sum(card_values[card][0] for card in hand) % 10

def display_card_icon(card):
    value, color = card_values[card]
    return f'<span style="color:{color}; font-size:28px;">{card}</span>'

def record_game_result(player_hand, banker_hand, result):
    player_hand = [html.unescape(card) for card in player_hand]
    banker_hand = [html.unescape(card) for card in banker_hand]
    file_exists = os.path.exists('game_results.csv')
    with open('game_results.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Player Hand', 'Banker Hand', 'Result'])
        writer.writerow([', '.join(player_hand), ', '.join(banker_hand), result])

# Initialize session states
for key in ['player_wins', 'banker_wins', 'ties', 'game_count']:
    if key not in st.session_state:
        st.session_state[key] = 0

def play_baccarat():
    global deck
    player_hand, banker_hand = [deal_card(), deal_card()], [deal_card(), deal_card()]
    player_value, banker_value = calculate_hand_value(player_hand), calculate_hand_value(banker_hand)
    
    player_natural, banker_natural = player_value in [8, 9], banker_value in [8, 9]
    
    st.markdown("""
        <h3 style='text-align: center;'>🃏 Dealing Cards... 🎴</h3>
    """, unsafe_allow_html=True)
    
    # Add a loading bar for anticipation
    progress_bar = st.progress(0)
    for i in range(100):
        sleep(0.02)
        progress_bar.progress(i + 1)
    sleep(0.5)
    progress_bar.empty()
    
    # Display player and banker hands visually
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h4 style='color:blue;'>Player's Cards:</h4> {' '.join([display_card_icon(c) for c in player_hand])}", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h4 style='color:orange;'>Banker's Cards:</h4> {' '.join([display_card_icon(c) for c in banker_hand])}", unsafe_allow_html=True)
    
    if player_natural or banker_natural:
        winner = "Player" if player_value > banker_value else "Banker" if banker_value > player_value else "Tie"
    else:
        if player_value < 6:
            player_hand.append(deal_card())
            player_value = calculate_hand_value(player_hand)
        if banker_value < 6:
            banker_hand.append(deal_card())
            banker_value = calculate_hand_value(banker_hand)
        winner = "Player" if player_value > banker_value else "Banker" if banker_value > player_value else "Tie"
    
    # Display final results
    result_color = "blue" if winner == "Player" else "orange" if winner == "Banker" else "green"
    st.markdown(f"""
        <h3 style='text-align: center; color:{result_color};'>🎉 {winner} Wins! ({player_value} - {banker_value}) 🎉</h3>
    """, unsafe_allow_html=True)
    
    # Update game stats
    if winner == "Player":
        st.session_state.player_wins += 1
        record_game_result(player_hand, banker_hand, 'P')
    elif winner == "Banker":
        st.session_state.banker_wins += 1
        record_game_result(player_hand, banker_hand, 'B')
    else:
        st.session_state.ties += 1
        record_game_result(player_hand, banker_hand, 'T')
    
    st.session_state.game_count += 1
    
# Sidebar controls
st.sidebar.title("🎰 Casino Games")
st.sidebar.text("Click to Play Baccarat")
if st.sidebar.button("Play Baccarat 🎲"):
    st.title("Baccarat - Live Game")
    play_baccarat()
    
# Display game stats and chart
st.write("### 📊 Game Statistics")

data = pd.DataFrame({
    "Results": ["Player", "Banker", "Tie"],
    "Wins": [st.session_state.player_wins, st.session_state.banker_wins, st.session_state.ties]
})
data.set_index("Results", inplace=True)
st.bar_chart(data)

st.write("### 📜 Download Game History")
df_game_results = pd.read_csv('game_results.csv') if os.path.exists('game_results.csv') else pd.DataFrame()
if not df_game_results.empty:
    csv_data = df_game_results.to_csv(index=False).encode('utf-8')
    st.download_button(label='📥 Download Hands Data', data=csv_data, file_name='baccarat_results.csv', mime='text/csv')
else:
    st.write("No game data available yet.")

# Add Game Reset Button
if st.button("🔄 Reset Game Stats"):
    for key in ['player_wins', 'banker_wins', 'ties', 'game_count']:
        st.session_state[key] = 0
    st.write("Game statistics have been reset!")
