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
st.sidebar.write("- Banker draws based on Player's third card and their total.")

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
    player_hand, banker_hand = [], []
    
    announcement = st.empty()
    announcement.markdown("<h3 style='text-align: center; color: gold;'>🃏 Dealing Cards... 🎴</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Reveal Player's first and second cards
    for i in range(2):
        sleep(5)
        announcement.markdown(f"<h3 style='text-align: center; color: blue;'>🔵 Dealer is drawing Player's card {i+1}...</h3>", unsafe_allow_html=True)
        player_hand.append(deal_card())
        sleep(5)
        announcement.empty()
        with col1:
            st.markdown(f"<h4 style='color:blue;'>🔵 Player's Card {i+1}: {display_card_icon(player_hand[-1])}</h4>", unsafe_allow_html=True)
    
    # Reveal Banker's first and second cards
    for i in range(2):
        sleep(5)
        announcement.markdown(f"<h3 style='text-align: center; color: orange;'>🟠 Dealer is drawing Banker's card {i+1}...</h3>", unsafe_allow_html=True)
        banker_hand.append(deal_card())
        sleep(5)
        announcement.empty()
        with col2:
            st.markdown(f"<h4 style='color:orange;'>🟠 Banker's Card {i+1}: {display_card_icon(banker_hand[-1])}</h4>", unsafe_allow_html=True)
    
    # Implement third card rule
    player_value = calculate_hand_value(player_hand)
    banker_value = calculate_hand_value(banker_hand)
    player_third_card = None
    if player_value < 6:
        announcement.markdown("<h3 style='text-align: center; color: blue;'>🔵 Dealer is drawing Player's third card...</h3>", unsafe_allow_html=True)
        sleep(5)
        player_third_card = deal_card()
        player_hand.append(player_third_card)
        with col1:
            st.markdown(f"<h4 style='color:blue;'>🔵 Player's Third Card: {display_card_icon(player_hand[-1])}</h4>", unsafe_allow_html=True)
    
    if banker_value < 6:
        announcement.markdown("<h3 style='text-align: center; color: orange;'>🟠 Dealer is drawing Banker's third card...</h3>", unsafe_allow_html=True)
        sleep(5)
        banker_hand.append(deal_card())
        with col2:
            st.markdown(f"<h4 style='color:orange;'>🟠 Banker's Third Card: {display_card_icon(banker_hand[-1])}</h4>", unsafe_allow_html=True)
    
    # Determine winner
    player_value = calculate_hand_value(player_hand)
    banker_value = calculate_hand_value(banker_hand)
    winner = "Player" if player_value > banker_value else "Banker" if banker_value > player_value else "Tie"
    result_color = "blue" if winner == "Player" else "orange" if winner == "Banker" else "green"
    
    # Final Outcome Display with Fanfare
    st.markdown("<h2 style='text-align: center; color: gold;'>🎊 Final Outcome 🎊</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: blue;'>🔵 Player's Hand: {' '.join([display_card_icon(c) for c in player_hand])}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: orange;'>🟠 Banker's Hand: {' '.join([display_card_icon(c) for c in banker_hand])}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color:{result_color}; text-shadow: 2px 2px 4px black;'>🎉 {winner} Wins! 🎉</h1>", unsafe_allow_html=True)
    
# Main Page Deal Button
st.markdown("<h2 style='text-align: center; color: gold;'>Welcome to Baccarat 🎲</h2>", unsafe_allow_html=True)
if st.button("🎴 Deal Baccarat Hand 🎲", key="main_deal_button"):
    play_baccarat()
