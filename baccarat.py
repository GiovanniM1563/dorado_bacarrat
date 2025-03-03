import os
import random
import csv
import html
import base64
import streamlit as st
import pandas as pd
from time import sleep

# Page Configuration
st.set_page_config(page_title="Baccarat Casino", page_icon="🎲", layout="wide", initial_sidebar_state="collapsed")

# Function to set page background color
def set_background_color():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #228B22; /* Felt green color */
        }
        .stButton>button {
            background-color: gold;
            color: black;
            font-size: 18px;
            border-radius: 10px;
            padding: 10px 20px;
        }
        .stMarkdown {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Apply background color
set_background_color()

# Sidebar Information
st.sidebar.title("📜 Baccarat Rules & Odds")
st.sidebar.write("🔢 **Number of Decks:** 8")
st.sidebar.write("🎲 **Game Odds:**")
st.sidebar.write("- **Player Win:** ~44.62%")
st.sidebar.write("- **Banker Win:** ~45.86%")
st.sidebar.write("- **Tie:** ~9.52%")

st.sidebar.write("\n**📜 Rules:**")
st.sidebar.write("- The goal is to get a hand closest to 9.")
st.sidebar.write("- Face cards and 10s are worth 0, Aces are worth 1.")
st.sidebar.write("- If the total is over 9, only the last digit counts.")
st.sidebar.write("- Player draws a third card if their total is 0-5.")
st.sidebar.write("- Banker draws based on the player's third card and their total, following traditional rules:")
st.sidebar.write("  - If the player stands (no third card), banker draws if total is less than 6.")
st.sidebar.write("  - If the player draws a third card:")
st.sidebar.write("    - Banker draws with a total of 0–2.")
st.sidebar.write("    - Banker draws with a total of 3 unless the player's third card is an 8.")
st.sidebar.write("    - Banker draws with a total of 4 if the player's third card is 2–7.")
st.sidebar.write("    - Banker draws with a total of 5 if the player's third card is 4–7.")
st.sidebar.write("    - Banker draws with a total of 6 if the player's third card is 6 or 7.")
st.sidebar.write("    - Banker stands with a total of 7 or more.")

# Define card values and colors
card_values = {
    **{f'{rank}{suit}': (0 if rank in ['J', 'Q', 'K', '10'] else 1 if rank == 'A' else int(rank), 'black' if suit in '♠♣' else 'red')
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

def play_baccarat():
    global deck
    player_hand, banker_hand = [], []
    
    announcement = st.empty()
    announcement.markdown("<h3 style='text-align: center; color: gold;'>🃏 Dealing Cards... 🎴</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Alternate dealing: one card for the player then one for the banker (two rounds)
    for i in range(2):
        ordinal = "First" if i == 0 else "Second"
        # Deal Player's card
        sleep(5)
        announcement.markdown(f"<h3 style='text-align: center; color: blue;'>🔵 Dealer is drawing Player's {ordinal} card...</h3>", unsafe_allow_html=True)
        player_hand.append(deal_card())
        sleep(5)
        announcement.empty()
        with col1:
            st.markdown(f"<h4 style='color:blue;'>🔵 Player's {ordinal} Card: {display_card_icon(player_hand[-1])}</h4>", unsafe_allow_html=True)
        
        # Deal Banker's card
        sleep(5)
        announcement.markdown(f"<h3 style='text-align: center; color: orange;'>🟠 Dealer is drawing Banker's {ordinal} card...</h3>", unsafe_allow_html=True)
        banker_hand.append(deal_card())
        sleep(5)
        announcement.empty()
        with col2:
            st.markdown(f"<h4 style='color:orange;'>🟠 Banker's {ordinal} Card: {display_card_icon(banker_hand[-1])}</h4>", unsafe_allow_html=True)
    
    # Determine if the Player draws a third card
    player_value = calculate_hand_value(player_hand)
    player_third_card = None
    if player_value < 6:
        announcement.markdown("<h3 style='text-align: center; color: blue;'>🔵 Dealer is drawing Player's third card...</h3>", unsafe_allow_html=True)
        sleep(5)
        player_third_card = deal_card()
        player_hand.append(player_third_card)
        with col1:
            st.markdown(f"<h4 style='color:blue;'>🔵 Player's Third Card: {display_card_icon(player_third_card)}</h4>", unsafe_allow_html=True)
    
    # Determine if the Banker draws a third card following traditional rules
    banker_value = calculate_hand_value(banker_hand)
    draw_banker = False
    if player_third_card is None:
        # Player stands; banker draws if total is less than 6
        if banker_value < 6:
            draw_banker = True
    else:
        # Player drew a third card; apply traditional rules
        pt_value = card_values[player_third_card][0]
        if banker_value <= 2:
            draw_banker = True
        elif banker_value == 3 and pt_value != 8:
            draw_banker = True
        elif banker_value == 4 and 2 <= pt_value <= 7:
            draw_banker = True
        elif banker_value == 5 and 4 <= pt_value <= 7:
            draw_banker = True
        elif banker_value == 6 and pt_value in [6, 7]:
            draw_banker = True
        # Banker stands on 7 or more
    
    if draw_banker:
        announcement.markdown("<h3 style='text-align: center; color: orange;'>🟠 Dealer is drawing Banker's third card...</h3>", unsafe_allow_html=True)
        sleep(5)
        banker_third = deal_card()
        banker_hand.append(banker_third)
        with col2:
            st.markdown(f"<h4 style='color:orange;'>🟠 Banker's Third Card: {display_card_icon(banker_third)}</h4>", unsafe_allow_html=True)
    
    # Determine final hand values and winner
    player_final = calculate_hand_value(player_hand)
    banker_final = calculate_hand_value(banker_hand)
    if player_final > banker_final:
        winner = "Player Wins!"
        result_color = "blue"
    elif banker_final > player_final:
        winner = "Banker Wins!"
        result_color = "orange"
    else:
        winner = "Tie"
        result_color = "green"
    
    # Final Outcome Display with Fanfare
    st.markdown("<h2 style='text-align: center; color: gold;'>🎊 Final Outcome 🎊</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: blue;'>🔵 Player's Hand: {' '.join([display_card_icon(c) for c in player_hand])}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: orange;'>🟠 Banker's Hand: {' '.join([display_card_icon(c) for c in banker_hand])}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color:{result_color}; text-shadow: 2px 2px 4px black;'>🎉 {winner} 🎉</h1>", unsafe_allow_html=True)
    
# Main Page Deal Button
st.markdown("<h2 style='text-align: center; color: gold;'>🎲 Welcome to El Dorado Lounge's Baccarat 🎲</h2>", unsafe_allow_html=True)
if st.button("🎴 Deal Baccarat Hand 🎲", key="main_deal_button"):
    play_baccarat()
