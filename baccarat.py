import os
import random
import csv
import html
import base64
import streamlit as st
import pandas as pd
from time import sleep

# Page Configuration with sidebar starting collapsed
st.set_page_config(
    page_title="Welcome to El Dorado Lounge's Baccarat", 
    page_icon="🎲", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Set background using a hack for later Streamlit versions
def set_bg_hack(main_bg):
    '''
    Unpacks an image from the root folder and sets it as the background.
    '''
    main_bg_ext = "png"
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True,
     )

# Call the function with your background file
set_bg_hack("EL-DORADO_bck.png")

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

# Sidebar Information (New-Player Friendly)
st.sidebar.title("📜 Baccarat Basics & Odds")
st.sidebar.write("Welcome to Baccarat! Here’s what you need to know:")
st.sidebar.write("🔢 **Decks in Play:** 8 decks")
st.sidebar.write("🎲 **Game Odds:**")
st.sidebar.write("- **Player Wins:** About 44.62% chance")
st.sidebar.write("- **Banker Wins:** About 45.86% chance")
st.sidebar.write("- **Tie:** About 9.52% chance")
st.sidebar.write("\n**Basic Rules:**")
st.sidebar.write("- Your goal is to have a hand with a total value closest to 9.")
st.sidebar.write("- Cards 2–9 are worth their face value, 10s and face cards (J, Q, K) are worth 0, and Aces are worth 1.")
st.sidebar.write("- If the sum is 10 or more, only the last digit counts (e.g., 15 becomes 5).")
st.sidebar.write("- The Player gets a third card if their total is between 0 and 5.")
st.sidebar.write("- The Banker’s drawing rules depend on both their total and the Player’s third card:")
st.sidebar.write("   • If the Player doesn’t draw a third card, the Banker draws if their total is 0–5.")
st.sidebar.write("   • If the Player does draw a third card, the Banker:")
st.sidebar.write("     - Draws if their total is 0, 1, or 2.")
st.sidebar.write("     - Draws if their total is 3 (unless the Player’s third card is 8).")
st.sidebar.write("     - Draws if their total is 4 and the Player’s third card is 2–7.")
st.sidebar.write("     - Draws if their total is 5 and the Player’s third card is 4–7.")
st.sidebar.write("     - Draws if their total is 6 and the Player’s third card is 6 or 7.")
st.sidebar.write("     - Stands if they have 7 or more.")

# Sidebar pill selection for manipulation mode.
manipulation_mode = st.sidebar.radio(
    "Choose Game Odds:",
    options=["Default", "Stack against Player", "Stack against Banker"],
    index=0,
    horizontal=True
)

# Initialize deck in session_state if not already present
if "deck" not in st.session_state:
    st.session_state.deck = list(card_values.keys()) * 8
    random.shuffle(st.session_state.deck)

# Reshuffle Deck button in the sidebar
if st.sidebar.button("🔄 Reshuffle Deck"):
    st.session_state.deck = list(card_values.keys()) * 8
    random.shuffle(st.session_state.deck)
    st.sidebar.success("The deck has been reshuffled!")

def deal_card():
    if len(st.session_state.deck) <= 10:
        st.warning("Almost out of cards! The deck will be reshuffled soon.")
        st.session_state.deck = list(card_values.keys()) * 8
        random.shuffle(st.session_state.deck)
    return st.session_state.deck.pop()

def calculate_hand_value(hand):
    return sum(card_values[card][0] for card in hand) % 10

def play_baccarat():
    # Set up Banker's hand placeholders using a five-column layout for centering.
    st.markdown("<h2 style='text-align: center; color: gold;'>Banker's Hand</h2>", unsafe_allow_html=True)
    banker_cols = st.columns([1, 2, 2, 2, 1])
    banker_placeholders = [banker_cols[1].empty(), banker_cols[2].empty(), banker_cols[3].empty()]
    for ph in banker_placeholders:
        ph.image("Cards/cardBack_red4.png", use_container_width=False, width=200)
    
    # Set up Player's hand placeholders using a five-column layout for centering.
    st.markdown("<h2 style='text-align: center; color: gold;'>Player's Hand</h2>", unsafe_allow_html=True)
    player_cols = st.columns([1, 2, 2, 2, 1])
    player_placeholders = [player_cols[1].empty(), player_cols[2].empty(), player_cols[3].empty()]
    for ph in player_placeholders:
        ph.image("Cards/cardBack_red4.png", use_container_width=False, width=200)
    
    announcement = st.empty()
    player_hand = []
    banker_hand = []
    
    # Slowly deal two cards each with delays
    for i in range(2):
        ordinal = "First" if i == 0 else "Second"
        
        sleep(5)
        announcement.markdown(f"<h2 style='text-align: center; color: blue;'>Dealing Player's {ordinal} card... Please wait!</h2>", unsafe_allow_html=True)
        card = deal_card()
        player_hand.append(card)
        player_placeholders[i].image(get_card_image_path(card), use_container_width=False, width=200)
        sleep(5)
        announcement.empty()
        
        sleep(5)
        announcement.markdown(f"<h2 style='text-align: center; color: orange;'>Dealing Banker's {ordinal} card... Hold tight!</h2>", unsafe_allow_html=True)
        card = deal_card()
        banker_hand.append(card)
        banker_placeholders[i].image(get_card_image_path(card), use_container_width=False, width=200)
        sleep(5)
        announcement.empty()
    
    # Check for third card draws following standard rules
    player_value = calculate_hand_value(player_hand)
    player_third_card = None
    if player_value < 6:
        announcement.markdown("<h2 style='text-align: center; color: blue;'>Player gets a third card...</h2>", unsafe_allow_html=True)
        sleep(5)
        player_third_card = deal_card()
        player_hand.append(player_third_card)
        player_placeholders[2].image(get_card_image_path(player_third_card), use_container_width=False, width=200)
        sleep(5)
        announcement.empty()
    
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
        announcement.markdown("<h2 style='text-align: center; color: orange;'>Banker draws a third card...</h2>", unsafe_allow_html=True)
        sleep(5)
        banker_third = deal_card()
        banker_hand.append(banker_third)
        banker_placeholders[2].image(get_card_image_path(banker_third), use_container_width=False, width=200)
        sleep(5)
        announcement.empty()
        
    player_final = calculate_hand_value(player_hand)
    banker_final = calculate_hand_value(banker_hand)
    
    st.markdown(f"<h3 style='text-align: center; color: blue;'>Player Hand Value: {player_final}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: orange;'>Banker Hand Value: {banker_final}</h3>", unsafe_allow_html=True)
    
    if player_final > banker_final:
        winner = "Player Wins!"
        result_color = "blue"
    elif banker_final > player_final:
        winner = "Banker Wins!"
        result_color = "orange"
    else:
        winner = "It's a Tie!"
        result_color = "green"
    
    st.markdown("<h2 style='text-align: center; color: gold;'>Final Outcome</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color:{result_color}; text-shadow: 2px 2px 4px black;'>🎉 {winner} 🎉</h1>", unsafe_allow_html=True)

def play_baccarat_manipulated(manipulation):
    # Define multiple predetermined combinations.
    # For a winning two-card hand (total 9) choose from these:
    winning_combos = [
        ("9♣", "J♦"),  # 9 + 0 = 9
        ("8♠", "A♥"),  # 8 + 1 = 9
        ("7♥", "2♣"),  # 7 + 2 = 9
        ("6♦", "3♠"),  # 6 + 3 = 9
        ("5♣", "4♥")   # 5 + 4 = 9
    ]
    # For a losing two-card hand (total 7, for example) choose from these:
    losing_combos = [
        ("4♣", "3♣"),  # 4 + 3 = 7
        ("7♠", "J♣"),  # 7 + 0 = 7
        ("6♠", "A♦")   # 6 + 1 = 7
    ]
    
    # Depending on the manipulation mode, randomly pick the appropriate combination.
    if manipulation == "Stack against Player":
        # Banker wins: banker gets a winning combo (9), player gets a losing combo.
        banker_hand = list(random.choice(winning_combos))
        player_hand = list(random.choice(losing_combos))
    elif manipulation == "Stack against Banker":
        # Player wins: player gets a winning combo (9), banker gets a losing combo.
        player_hand = list(random.choice(winning_combos))
        banker_hand = list(random.choice(losing_combos))
    
    # Set up placeholders for both hands.
    st.markdown("<h2 style='text-align: center; color: gold;'>Banker's Hand</h2>", unsafe_allow_html=True)
    banker_cols = st.columns([1, 2, 2, 2, 1])
    banker_placeholders = [banker_cols[1].empty(), banker_cols[2].empty(), banker_cols[3].empty()]
    st.markdown("<h2 style='text-align: center; color: gold;'>Player's Hand</h2>", unsafe_allow_html=True)
    player_cols = st.columns([1, 2, 2, 2, 1])
    player_placeholders = [player_cols[1].empty(), player_cols[2].empty(), player_cols[3].empty()]
    
    # Initially, show the card backs to mimic the default game.
    for ph in player_placeholders:
         ph.image("Cards/cardBack_red4.png", use_container_width=False, width=200)
    for ph in banker_placeholders:
         ph.image("Cards/cardBack_red4.png", use_container_width=False, width=200)
    
    announcement = st.empty()
    
    # Slowly reveal the predetermined cards as if dealing them.
    for i in range(2):
        ordinal = "First" if i == 0 else "Second"
        
        sleep(5)
        announcement.markdown(f"<h2 style='text-align: center; color: blue;'>Revealing Player's {ordinal} card...</h2>", unsafe_allow_html=True)
        player_placeholders[i].image(get_card_image_path(player_hand[i]), use_container_width=False, width=200)
        sleep(5)
        announcement.empty()
        
        sleep(5)
        announcement.markdown(f"<h2 style='text-align: center; color: orange;'>Revealing Banker's {ordinal} card...</h2>", unsafe_allow_html=True)
        banker_placeholders[i].image(get_card_image_path(banker_hand[i]), use_container_width=False, width=200)
        sleep(5)
        announcement.empty()
    
    # For simplicity, no third card is drawn in manipulated mode.
    player_final = calculate_hand_value(player_hand)
    banker_final = calculate_hand_value(banker_hand)
    
    st.markdown(f"<h3 style='text-align: center; color: blue;'>Player Hand Value: {player_final}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: orange;'>Banker Hand Value: {banker_final}</h3>", unsafe_allow_html=True)
    
    if manipulation == "Stack against Player":
        winner = "Banker Wins!"
        result_color = "orange"
    elif manipulation == "Stack against Banker":
        winner = "Player Wins!"
        result_color = "blue"
    
    st.markdown("<h2 style='text-align: center; color: gold;'>Final Outcome</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color:{result_color}; text-shadow: 2px 2px 4px black;'>🎉 {winner} 🎉</h1>", unsafe_allow_html=True)

# Main Page Deal Button
st.markdown("<h2 style='text-align: center; color: gold;'>Welcome to El Dorado Lounge's Baccarat</h2>", unsafe_allow_html=True)
if st.button("🎴 Deal Baccarat Hand 🎲", key="main_deal_button"):
    if manipulation_mode == "Default":
        play_baccarat()
    else:
        play_baccarat_manipulated(manipulation_mode)
