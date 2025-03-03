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
page_bg_img = '''
<style>
body {
background-image: url("https://ranchroleplay.com/cdn-cgi/imagedelivery/Hgl-UO4Kg_kPptcXUHVOrA/8717957e-7245-47c0-4b90-01043e6b3700/public");
background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

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
    player_hand, banker_hand = [], []
    
    st.markdown("<h3 style='text-align: center; color: gold;'>🃏 Dealing Cards... 🎴</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Reveal Player's first card
    sleep(3)
    st.markdown("<h3 style='text-align: center; color: blue;'>🔵 Dealer is drawing Player's first card...</h3>", unsafe_allow_html=True)
    player_hand.append(deal_card())
    with col1:
        st.markdown(f"<h4 style='color:blue;'>🔵 Player's First Card: {display_card_icon(player_hand[-1])}</h4>", unsafe_allow_html=True)
    sleep(3)
    
    # Reveal Banker's first card
    st.markdown("<h3 style='text-align: center; color: orange;'>🟠 Dealer is drawing Banker's first card...</h3>", unsafe_allow_html=True)
    banker_hand.append(deal_card())
    with col2:
        st.markdown(f"<h4 style='color:orange;'>🟠 Banker's First Card: {display_card_icon(banker_hand[-1])}</h4>", unsafe_allow_html=True)
    sleep(3)
    
    # Reveal Player's second card
    st.markdown("<h3 style='text-align: center; color: blue;'>🔵 Dealer is drawing Player's second card...</h3>", unsafe_allow_html=True)
    player_hand.append(deal_card())
    with col1:
        st.markdown(f"<h4 style='color:blue;'>🔵 Player's Second Card: {display_card_icon(player_hand[-1])}</h4>", unsafe_allow_html=True)
    sleep(3)
    
    # Reveal Banker's second card
    st.markdown("<h3 style='text-align: center; color: orange;'>🟠 Dealer is drawing Banker's second card...</h3>", unsafe_allow_html=True)
    banker_hand.append(deal_card())
    with col2:
        st.markdown(f"<h4 style='color:orange;'>🟠 Banker's Second Card: {display_card_icon(banker_hand[-1])}</h4>", unsafe_allow_html=True)
    sleep(3)
    
    player_value, banker_value = calculate_hand_value(player_hand), calculate_hand_value(banker_hand)
    
    player_natural, banker_natural = player_value in [8, 9], banker_value in [8, 9]
    
    # Implement the third card rule
    player_draws = banker_draws = False
    if not player_natural and not banker_natural:
        if player_value < 6:
            st.markdown("<h3 style='text-align: center; color: blue;'>🔵 Dealer is drawing Player's third card...</h3>", unsafe_allow_html=True)
            sleep(3.5)
            player_hand.append(deal_card())
            with col1:
                st.markdown(f"<h4 style='color:blue;'>🔵 Player's Third Card: {display_card_icon(player_hand[-1])}</h4>", unsafe_allow_html=True)
            player_value = calculate_hand_value(player_hand)
            player_draws = True
        
        third_card_value = card_values[player_hand[-1]][0] if player_draws else None
        if banker_value < 3 or (banker_value == 3 and third_card_value != 8) or (banker_value == 4 and third_card_value in [2, 3, 4, 5, 6, 7]) or (banker_value == 5 and third_card_value in [4, 5, 6, 7]) or (banker_value == 6 and third_card_value in [6, 7]):
            st.markdown("<h3 style='text-align: center; color: orange;'>🟠 Dealer is drawing Banker's third card...</h3>", unsafe_allow_html=True)
            sleep(3.5)
            banker_hand.append(deal_card())
            with col2:
                st.markdown(f"<h4 style='color:orange;'>🟠 Banker's Third Card: {display_card_icon(banker_hand[-1])}</h4>", unsafe_allow_html=True)
            banker_value = calculate_hand_value(banker_hand)
            banker_draws = True
    
    sleep(3)
    
    # Final Outcome Display with Fanfare
    st.markdown("<h2 style='text-align: center; color: gold;'>🎊 Final Outcome 🎊</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: blue;'>🔵 Player's Hand: {' '.join([display_card_icon(c) for c in player_hand])} - {player_value}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: orange;'>🟠 Banker's Hand: {' '.join([display_card_icon(c) for c in banker_hand])} - {banker_value}</h3>", unsafe_allow_html=True)
    
    winner = "Player" if player_value > banker_value else "Banker" if banker_value > player_value else "Tie"
    result_color = "blue" if winner == "Player" else "orange" if winner == "Banker" else "green"
    
    st.markdown(f"<h1 style='text-align: center; color:{result_color}; text-shadow: 2px 2px 4px black;'>🎉 {winner} Wins! 🎉</h1>", unsafe_allow_html=True)
    
# Main Page Deal Button
st.markdown("<h2 style='text-align: center; color: gold;'>Welcome to Baccarat 🎲</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Click below to deal a hand.</p>", unsafe_allow_html=True)
if st.button("🎴 Deal Baccarat Hand 🎲", key="main_deal_button"):
    play_baccarat()
