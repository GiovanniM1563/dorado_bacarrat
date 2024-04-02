import os
import io
import sys
import streamlit as st
import pandas as pd
import random
import csv
import html
# import altair as alt

# Define card values for all four suits
card_values = {
    '2♠️': (2, 'black'), '3♠️': (3, 'black'), '4♠️': (4, 'black'), '5♠️': (5, 'black'),
    '6♠️': (6, 'black'), '7♠️': (7, 'black'), '8♠️': (8, 'black'), '9♠️': (9, 'black'),
    '10♠️': (0, 'black'), 'J♠️': (0, 'black'), 'Q♠️': (0, 'black'), 'K♠️': (0, 'black'),
    'A♠️': (1, 'black'),
    '2♥️': (2, 'red'), '3♥️': (3, 'red'), '4♥️': (4, 'red'), '5♥️': (5, 'red'),
    '6♥️': (6, 'red'), '7♥️': (7, 'red'), '8♥️': (8, 'red'), '9♥️': (9, 'red'),
    '10♥️': (0, 'red'), 'J♥️': (0, 'red'), 'Q♥️': (0, 'red'), 'K♥️': (0, 'red'),
    'A♥️': (1, 'red'),
    '2♦️': (2, 'red'), '3♦️': (3, 'red'), '4♦️': (4, 'red'), '5♦️': (5, 'red'),
    '6♦️': (6, 'red'), '7♦️': (7, 'red'), '8♦️': (8, 'red'), '9♦️': (9, 'red'),
    '10♦️': (0, 'red'), 'J♦️': (0, 'red'), 'Q♦️': (0, 'red'), 'K♦️': (0, 'red'),
    'A♦️': (1, 'red'),
    '2♣️': (2, 'black'), '3♣️': (3, 'black'), '4♣️': (4, 'black'), '5♣️': (5, 'black'),
    '6♣️': (6, 'black'), '7♣️': (7, 'black'), '8♣️': (8, 'black'), '9♣️': (9, 'black'),
    '10♣️': (0, 'black'), 'J♣️': (0, 'black'), 'Q♣️': (0, 'black'), 'K♣️': (0, 'black'),
    'A♣️': (1, 'black'),
}

# Define global variable for the deck
deck = list(card_values.keys()) * 8
random.shuffle(deck)

# Function to deal a card from 8 decks without replacement
def deal_card():
    global deck
    if len(deck) <= 10:
        st.wtite("The deck is about to be exhausted. Next hand will be the last hand.")
        deck = list(card_values.keys()) * 8
        random.shuffle(deck)
    return deck.pop()


# # Function to deal a card
# def deal_card():
#     return random.choice(list(card_values.keys()))

# Function to calculate hand value
def calculate_hand_value(hand):
    value = sum(card_values[card][0] for card in hand) % 10
    return value

# Function to display card icon with color
def display_card_icon(card):
    value, color = card_values[card]
    if color == 'red':
        return f'<span style="color:red;">{card}</span>'
    else:
        return f'<span style="color:black;   text-shadow: -1px 0 white, 0 1px white, 1px 0 white, 0 -1px white;">{card}</span>'
    
# Function to display card icon with image
# def display_card_icon(card):
#     value, image_path = card_values[card]
#     return f'<img src="{image_path}.png" alt="{card}" width="100" height="150">'


# Function to record game results as (game_results.csv) data file
def record_game_result(player_hand, banker_hand, result):
    # Decode HTML entities in card symbols
    player_hand = [html.unescape(card) for card in player_hand]
    banker_hand = [html.unescape(card) for card in banker_hand]
    
    # Check if the file exists
    file_exists = os.path.exists('game_results.csv')
    
    with open('game_results.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # If the file doesn't exist, write the column headers
        if not file_exists:
            writer.writerow(['Player Hand', 'Banker Hand', 'Result'])
        
        # Write the current game result
        writer.writerow([', '.join(player_hand), ', '.join(banker_hand), result])

# Initialize score counters
player_wins = 0

if hasattr(st.session_state, "player_wins"):
    player_wins = st.session_state.player_wins

banker_wins = 0
if hasattr(st.session_state, "banker_wins"):
    banker_wins = st.session_state.banker_wins
    
ties = 0
if hasattr(st.session_state, "ties"):
    ties = st.session_state.ties

# Initialize lists to store game results for plotting
player_wins_history = []
banker_wins_history = []
ties_history = []
game_count = 0

def play_baccarat():
    global player_wins, banker_wins, ties, player_wins_history, banker_wins_history, ties_history, game_count

    player_hand = []
    banker_hand = []

# Deal two cards to player and banker
    for _ in range(2):  # The player receives 1st and 3rd cards and the Banker will have 2nd the 4th cards. 
        player_hand.append(deal_card())
        # st.write("Player Card:", *[display_card_icon(card) for card in player_hand], unsafe_allow_html=True)

        banker_hand.append(deal_card())
        # st.write("Banker Card", *[display_card_icon(card) for card in banker_hand], unsafe_allow_html=True)

     # Calculate initial hand values
    player_hand_value = int(calculate_hand_value(player_hand))
    banker_hand_value = int(calculate_hand_value(banker_hand))

    # Player hand is a natural 8 or 9
    player_natural = player_hand_value in [8, 9]

    # Banker hand is a natural 8 or 9
    banker_natural = banker_hand_value in [8, 9]


    if player_natural or banker_natural:
        col1, col2 = st.columns(2)
        with col1:
            st.write("##### Player's Cards: ", *[display_card_icon(card) for card in player_hand], unsafe_allow_html=True)
        with col2:
            st.write("##### Banker's Cards: ",  *[display_card_icon(card) for card in banker_hand], unsafe_allow_html=True)
        
        if player_natural > banker_natural:
            st.write("###### Player Wins :  Natural ", player_hand_value,"Over ", banker_hand_value)
            player_wins += 1
            record_game_result(player_hand, banker_hand, 'P')
            
        elif player_natural < banker_natural:
            st.write("###### Banker Wins :  Natural ", banker_hand_value, "Over ", player_hand_value)
            banker_wins += 1
            record_game_result(player_hand, banker_hand, 'B')
        else:
            st.write("###### It's a Natural Tie ! ", player_hand_value, "and ", banker_hand_value)
            ties += 1
            record_game_result(player_hand, banker_hand, 'T')
        
        # Append current game results to history
        player_wins_history.append(player_wins)
        banker_wins_history.append(banker_wins)
        ties_history.append(ties)
        game_count += 1
    
        return player_wins, banker_wins, ties

    last_player_card_value = ''
    # Draw third card for Player (values 0 through 5)
    if player_hand_value < 6:
        last_player_card = deal_card()
        last_player_card_value = calculate_hand_value([last_player_card])
        player_hand.append(last_player_card)
        player_hand_value = calculate_hand_value(player_hand)
    
    if banker_hand_value < 6 and (player_hand_value == 6 or player_hand_value == 7):
        banker_hand.append(deal_card())
    elif banker_hand_value < 3:
        banker_hand.append(deal_card())
        banker_hand_value = calculate_hand_value(banker_hand)
    elif banker_hand_value == 3 and last_player_card_value != 8:
        banker_hand.append(deal_card())
    elif banker_hand_value == 4 and last_player_card_value in [2, 3, 4, 5, 6, 7]:
        banker_hand.append(deal_card())
    elif banker_hand_value == 5 and last_player_card_value in [4, 5, 6, 7]:
        banker_hand.append(deal_card())
    elif banker_hand_value == 6 and last_player_card_value in [6, 7]:
        banker_hand.append(deal_card())

    # banker_hand_value = calculate_hand_value(banker_hand)

    # Recalculate hand values
    player_hand_value = calculate_hand_value(player_hand)
    banker_hand_value = calculate_hand_value(banker_hand)

    col1, col2 = st.columns(2)
    with col1:
        st.write("##### Player's Cards: ", *[display_card_icon(card) for card in player_hand], unsafe_allow_html=True)
    with col2:
        st.write("##### Banker's Cards: ", *[display_card_icon(card) for card in banker_hand], unsafe_allow_html=True)

    # Determine the winner based on hand values

    if player_hand_value > banker_hand_value:
        st.write("###### Player Wins ", player_hand_value, "over ", banker_hand_value)
        player_wins += 1
        record_game_result(player_hand, banker_hand, 'P')

    elif player_hand_value < banker_hand_value:
        st.write("###### Banker Wins ", banker_hand_value, "over ", player_hand_value)
        banker_wins += 1        
        record_game_result(player_hand, banker_hand, 'B')

    else:
        st.write("###### It's a Tie ! ", player_hand_value, "and ", banker_hand_value)
        ties += 1
        record_game_result(player_hand, banker_hand, 'T')

    # Append current game results to history
    player_wins_history.append(player_wins)
    banker_wins_history.append(banker_wins)
    ties_history.append(ties)
    game_count += 1

    return player_wins, banker_wins, ties


# Run the app
if __name__ == "__main__":
    st.sidebar.title("Casino Games")
    st.sidebar.text("Click the button to Play / Deal")

     # Add a "Play Again" button for Baccarat
    
    if st.sidebar.button("Baccarat"):
   
        st.title("Baccarat")
        st.write("##### Total Decks : 8")
        st.write("###### With No Replacement - dealt cards are not placing back to the shuffler")
        st.empty()

        # Play a new game of Baccarat
        player_wins, banker_wins, ties = play_baccarat()
        st.session_state.player_wins = player_wins
        st.session_state.banker_wins = banker_wins
        st.session_state.ties = ties


# Check if the lists are not empty before accessing the last element
if player_wins_history and banker_wins_history and ties_history:
    # Combine the data into a DataFrame
    data = {
        "Results": ["Player", "Banker", "Tie"],
        "Count": [player_wins_history[-1], banker_wins_history[-1], ties_history[-1]]
    }

    df = pd.DataFrame(data)

    # Set the "Result" column as index
    df.set_index("Results", inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        if not df.empty:
            # Define CSS style for the box
            box_style = """
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 20px;
                margin: 20px 0;
            """

            # Render the box with the chart inside
            with st.container(): 
                st.write("##### Game Results: ")  # Title inside the box
                st.bar_chart(df)  # Chart inside the box
        else:
            st.write("No game history yet.")
    
    # Calculate total count and percentage
    total_count = df['Count'].sum()
    df['Percentage'] = round((df['Count'] / total_count) * 100, 2)

    # # Add a row for total count and percentage
    # total_row = {'Count': total_count, 'Percentage': 100}
    # df = df.append(pd.Series(total_row, name='Total'))
    
    with col2:
    # Display the updated DataFrame in Streamlit
        st.write(df)
        # Download the number of win/loss or ties (Player, Banker, Tie )
        csv = df.to_csv(index = True).encode('utf-8')
        st.download_button('Results download', data = csv, file_name = "baccarat_output.csv",mime = "text/csv")

else:
    st.write("No game history yet.")

# Read the CSV file into a DataFrame
df_game_results = pd.read_csv('game_results.csv')

# Display the DataFrame
# st.write(df_game_results)

# Create a download button for the DataFrame
csv = df_game_results.to_csv(index=False).encode('utf-8')
st.write('If you are interested on cards outcome for each hand as .csv file, click the button below')
st.download_button('Download Cards data', data=csv, file_name='baccarat_hands.csv', mime='text/csv')


