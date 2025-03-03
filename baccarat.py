import os
import random
import csv
import html
import streamlit as st
import pandas as pd
from time import sleep

# Page Configuration
st.set_page_config(page_title="Baccarat Casino", page_icon="🎲", layout="wide", initial_sidebar_state="collapsed")

# Apply custom background color for a casino feel
def set_background_color():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #006400;
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

def play_baccarat():
    global deck
    player_hand, banker_hand = [deal_card(), deal_card()], [deal_card(), deal_card()]
    player_value, banker_value = calculate_hand_value(player_hand), calculate_hand_value(banker_hand)
    
    player_natural, banker_natural = player_value in [8, 9], banker_value in [8, 9]
    
    st.markdown("""
        <h3 style='text-align: center; color: gold;'>🃏 Dealing Cards... 🎴</h3>
    """, unsafe_allow_html=True)
    
    # Add a loading bar for anticipation
    progress_bar = st.progress(0)
    for i in range(100):
        sleep(0.02)
        progress_bar.progress(i + 1)
    sleep(0.5)
    progress_bar.empty()
    
    # Display player and banker hands visually with glowing effect
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h4 style='color:blue; text-shadow: 2px 2px 4px black;'>Player's Cards:</h4> {' '.join([display_card_icon(c) for c in player_hand])}", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h4 style='color:orange; text-shadow: 2px 2px 4px black;'>Banker's Cards:</h4> {' '.join([display_card_icon(c) for c in banker_hand])}", unsafe_allow_html=True)
    
    # Determine the winner
    winner = "Player" if player_value > banker_value else "Banker" if banker_value > player_value else "Tie"
    result_color = "blue" if winner == "Player" else "orange" if winner == "Banker" else "green"
    
    st.markdown(f"""
        <h3 style='text-align: center; color:{result_color}; text-shadow: 2px 2px 4px black;'>🎉 {winner} Wins! ({player_value} - {banker_value}) 🎉</h3>
    """, unsafe_allow_html=True)
    
# Main Page Deal Button
st.markdown("<h2 style='text-align: center; color: gold;'>Welcome to Baccarat 🎲</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Click below to deal a hand.</p>", unsafe_allow_html=True)
if st.button("🎴 Deal Baccarat Hand 🎲", key="main_deal_button"):
    play_baccarat()

# Sidebar Information
st.sidebar.title("📊 Game Information")
st.sidebar.write("🔢 Number of Decks: 8")
st.sidebar.write("🎲 Game Odds:")
st.sidebar.write("- Player Win: ~44.62%")
st.sidebar.write("- Banker Win: ~45.86%")
st.sidebar.write("- Tie: ~9.52%")
