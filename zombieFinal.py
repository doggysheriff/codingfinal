# Imports the operating system that will allow the user easy access to the game :p
import os
# Imports the AI model that will be used 
import openai

# Function to adjust the suspicion level based on player's input
def adjust_suspicion(response, suspicion_level):
    # Keywords that increase or decrease suspicion
    increase_keywords = ["bite", "starve", "infect", "hungry", "eat", "visiting", "hunger", "dying", "die"]
    decrease_keywords = ["friend", "business", "lover", "doctor", "medicine"]
    #Increase/lower suspicion based on keywords in the response
    words = response.lower().split()
    for word in words: # For loop that will be used to execute a group of statements as long as the condition is satisfied
        if word in increase_keywords: # If statement that is used to check the condition
            suspicion_level += 10  # Increase suspicion
        elif word in decrease_keywords: # Elif statement written proceeding the if statement to test the alternative condition
            suspicion_level -= 25  # Decrease suspicion
    return suspicion_level # Returns the output from the function



# Function to check if the game should end based on suspicion level
def check_game_end(suspicion_level):
    if suspicion_level >= 100: # If statement that is used to check the conditions of the princess' access the kingdom
        print("The princess is too suspicious! You are denied entry.") # The print that acknowledges the princess' decision to exile the player
        return True # Returns the output from the function
    elif suspicion_level <= 0: # Elif statement written to test the alternative decision - in this case the princess lets you in the kingdom walls
        print("The princess believes you are safe. You are allowed to enter!") # Print that acknowledges the princess' decision to let you in
        return True # Returns the ouput from the function
    return False # Returns the output if it has not successfully completed its intended task

# Stephen Sparkman and the openai github account were responsible for implementing the AI chatbot
# Function that will support the AI's response system
def get_ai_response(prompt): 
    try: # Try to check for errors
        openai_api_key = os.environ["OPENAI_API_KEY"] # Mapping that represents the user's OS environmental variables
    except KeyError: # Used to run block of code on the exception that the try block arouses an error
        print("ERROR: OPENAI_API_KEY environment variable not set.") # Print that defines the error witht the API key 
        exit(1)
    # Creating a client instance with API key
    client = openai.OpenAI(api_key=openai_api_key)
    # Create a chat completion
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # davinci model used to support AI chat bot
        messages=[ # The prompt for the AI to digest and assume the role of
            {"role": "system", "content": "You are a princess conversing with someone outside the gates. Your primary role is to carefully assess the visitor's intentions based on their answers without making immediate decisions about entry. Maintain a neutral, inquisitive stance and seek to uncover more about the visitor's reasons for wanting to enter. Do not decide to allow or deny entry until clearly directed by the game logic."}, # Be more specific + he sometimes talks narratively of himself and his environment
            {"role": "user", "content": prompt}
        ],
        max_tokens=150, # The limit of generated response that the model can produce
        temperature=0.9 # Gauges how much a new response produced by the AI is similar to another response it has already made
    )


    # Extracting the message content correctly
    return response.choices[0].message.content  


# Function that will print the system messages upon starting the game
def main():
    print("You are a partially transformed zombie approaching the gates of a small kingdom.") # Defining the role of the player
    print("Your goal is to convince the princess to let you in so you can infect the village.") # Defining the player's objectives
    print("What will you say to the princess?") # Give the player a motive to make the first move

    # Start at neutral suspicion level 
    suspicion_level = 50
    while True: # Used to execute a block of code repeatedly until the condition is evaluated to false
        player_input = input("You say: ") # The player input 
        if player_input.lower() in ['exit', 'quit']: # Player input that will remove the player from the game
            print("Exiting game.")
            break

        # Update suspicion level based on player's input
        suspicion_level = adjust_suspicion(player_input, suspicion_level)



        # Check if the game should end based on the suspicion level
        if check_game_end(suspicion_level): # If statement used to check the condition and execute it if the condition hold true
            break
        
        # Generate the prompt for the AI
        prompt = f"A mysterious figure says: '{player_input}'" # What the AI sees
        ai_response = get_ai_response(prompt) # Allows me to retrieve the value of another item associated with it
        print(f"The princess says: {ai_response}") # What the player sees to understand the princess has spoken


# Conditional statement that tells the Python interpreter under what conditions the main method should be executed
if __name__ == "__main__":
    main()