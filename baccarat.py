import os
import random
import csv
import html
import base64
import uuid
import streamlit as st
import pandas as pd
from time import sleep

# Page Configuration
st.set_page_config(page_title="Welcome to El Dorado Lounge's Baccarat", 
                   page_icon="🎲", layout="wide", initial_sidebar_state="collapsed")

# Set background color and hide audio controls via CSS
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
        /* Hide all audio elements */
        audio {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Apply background color and hide audio bar
set_background_color()

# Mapping for suit symbols to image folder names
suit_map = {'♣': 'Clubs', '♦': 'Diamonds', '♥': 'Hearts', '♠': 'Spades'}

def get_card_image_path(card):
    """
    Given a card code (e.g., "10♣", "A♥"), return the image path.
    """
    rank = card[:-1]
    suit_symbol = card[-1]
    suit_name = suit_map.get(suit_symbol, "")
    return f"Cards/card{suit_name}{rank}.png"

# Define card values and colors
card_values = {
    **{f'{rank}{suit}': (0 if rank in ['J', 'Q', 'K', '10'] 
                          else 1 if rank == 'A' else int(rank),
                           'black' if suit in '♠♣' else 'red')
       for rank in [str(n) for n in range(2, 11)] + ['J', 'Q', 'K', 'A']
       for suit in '♠♥♦♣'}
}

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

# Initialize deck in session_state if not already present
if "deck" not in st.session_state:
    st.session_state.deck = list(card_values.keys()) * 8
    random.shuffle(st.session_state.deck)

# Reshuffle Deck button in the sidebar
if st.sidebar.button("🔄 Reshuffle Deck"):
    st.session_state.deck = list(card_values.keys()) * 8
    random.shuffle(st.session_state.deck)
    st.sidebar.success("Deck reshuffled!")

def deal_card():
    if len(st.session_state.deck) <= 10:
        st.warning("🔄 The deck is nearly exhausted. Next hand will be the last hand before reshuffling.")
        st.session_state.deck = list(card_values.keys()) * 8
        random.shuffle(st.session_state.deck)
    return st.session_state.deck.pop()

def calculate_hand_value(hand):
    return sum(card_values[card][0] for card in hand) % 10

def play_baccarat():
    # Create a single audio placeholder to play sounds.
    audio_placeholder = st.empty()

    # Function to play the card mixing sound using a unique URL.
    def play_dealing_sound():
        unique_url = "card-mixing-48088.mp3?dummy=" + str(uuid.uuid4())
        audio_placeholder.audio(unique_url, format="audio/mp3", autoplay=True)
    
    # Set up player's hand placeholders using a five-column layout for centering.
    st.markdown("<h2 style='text-align: center; color: gold;'>Player's Hand</h2>", unsafe_allow_html=True)
    player_cols = st.columns([1, 2, 2, 2, 1])
    player_placeholders = [player_cols[1].empty(), player_cols[2].empty(), player_cols[3].empty()]
    for ph in player_placeholders:
        ph.image("Cards/cardBack_red4.png", use_container_width=False, width=100)
    
    # Set up banker's hand placeholders using a five-column layout for centering.
    st.markdown("<h2 style='text-align: center; color: gold;'>Banker's Hand</h2>", unsafe_allow_html=True)
    banker_cols = st.columns([1, 2, 2, 2, 1])
    banker_placeholders = [banker_cols[1].empty(), banker_cols[2].empty(), banker_cols[3].empty()]
    for ph in banker_placeholders:
        ph.image("Cards/cardBack_red4.png", use_container_width=False, width=100)
    
    announcement = st.empty()
    player_hand = []
    banker_hand = []

    # Deal two cards each (initial hands)
    for i in range(2):
        ordinal = "First" if i == 0 else "Second"
        
        # Deal Player's card
        sleep(5)
        announcement.markdown(f"<h3 style='text-align: center; color: blue;'>🔵 Dealing Player's {ordinal} card...</h3>", unsafe_allow_html=True)
        play_dealing_sound()
        card = deal_card()
        player_hand.append(card)
        player_placeholders[i].image(get_card_image_path(card), use_container_width=False, width=100)
        sleep(5)
        announcement.empty()
        
        # Deal Banker's card
        sleep(5)
        announcement.markdown(f"<h3 style='text-align: center; color: orange;'>🟠 Dealing Banker's {ordinal} card...</h3>", unsafe_allow_html=True)
        play_dealing_sound()
        card = deal_card()
        banker_hand.append(card)
        banker_placeholders[i].image(get_card_image_path(card), use_container_width=False, width=100)
        sleep(5)
        announcement.empty()
    
    # Check if Player draws a third card
    player_value = calculate_hand_value(player_hand)
    player_third_card = None
    if player_value < 6:
        announcement.markdown("<h3 style='text-align: center; color: blue;'>🔵 Dealing Player's third card...</h3>", unsafe_allow_html=True)
        sleep(5)
        play_dealing_sound()
        player_third_card = deal_card()
        player_hand.append(player_third_card)
        player_placeholders[2].image(get_card_image_path(player_third_card), use_container_width=False, width=100)
        sleep(5)
        announcement.empty()
    
    # Determine if Banker draws a third card
    banker_value = calculate_hand_value(banker_hand)
    draw_banker = False
    if player_third_card is None:
        if banker_value < 6:
            draw_banker = True
    else:
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
    if draw_banker:
        announcement.markdown("<h3 style='text-align: center; color: orange;'>🟠 Dealing Banker's third card...</h3>", unsafe_allow_html=True)
        sleep(5)
        play_dealing_sound()
        banker_third = deal_card()
        banker_hand.append(banker_third)
        banker_placeholders[2].image(get_card_image_path(banker_third), use_container_width=False, width=100)
        sleep(5)
        announcement.empty()
    
    # Calculate and display final hand values
    player_final = calculate_hand_value(player_hand)
    banker_final = calculate_hand_value(banker_hand)
    
    st.markdown(f"<h3 style='text-align: center; color: blue;'>Player Hand Value: {player_final}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: orange;'>Banker Hand Value: {banker_final}</h3>", unsafe_allow_html=True)
    
    # Determine and display the final outcome
    if player_final > banker_final:
        winner = "Player Wins!"
        result_color = "blue"
    elif banker_final > player_final:
        winner = "Banker Wins!"
        result_color = "orange"
    else:
        winner = "Tie"
        result_color = "green"
    
    st.markdown("<h2 style='text-align: center; color: gold;'>Final Outcome</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color:{result_color}; text-shadow: 2px 2px 4px black;'>🎉 {winner} 🎉</h1>", unsafe_allow_html=True)

# Main Page Deal Button
st.markdown("<h2 style='text-align: center; color: gold;'>🎲 Welcome to El Dorado Lounge's Baccarat 🎲</h2>", unsafe_allow_html=True)
if st.button("🎴 Deal Baccarat Hand 🎲", key="main_deal_button"):
    play_baccarat()
