import logging
import secrets
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.ext import CallbackContext, MessageHandler, Filters, ChatMemberHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram import Chat, ChatMember, ParseMode, ChatMemberUpdated
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
from lxml import html
import food_recipes
import json
import requests
import time
import random
import pytz
from datetime import datetime
import os


############################### Logging ########################################

# get the heroku port
PORT = int(os.environ.get('PORT', 8443) )

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
################################ Variables ######################################
username = ''
food_list =''
curr_time = time.localtime()
hr = int(time.strftime("%H", curr_time))
daytime= (hr < 12 and 'morning') or (hr < 16 and 'afternoon') or 'evening'
TOKEN = '1877580174:AAEd0xkWtccSDFmr4bo0VSbdP2yI7CI-I40'
fauna_secret ="fnAEkaidvrACTDwNzMlmjdXXCwYSKeNNh8FQcUMN"
################################### Variable defs ##############################
def randomizer_male() :
    mrand = ["dude", "bro", "man", "guy", "boss😂", "chairman", "Oga😂", "OG", "chairman😂"]
    return random.choice(mrand)

def randomizer_female() :
    frand = ["girl", "babygirl", "bestie", "Queen", "cutiepie", "Bae"]
    return random.choice(frand)

################################### Main Bot ###################################

############################# Work Functions ###################################
def split_ingredients(ingreList):
    ingre = ingrelist.toLower()
    ingre_norm_json = ingre.split()
    if "oil" in ingre_norm_json:
        oilIndex = ingre_norm_json.index('oil')
        preKey = oilIndex - 1
        whatOil = (preKey == 'groundnut' and 'groundnut oil') or (preKey == 'red' or 'palm' and 'palm oil')
        ingre_norm_json.remove('oil','groundnut','red','palm')
        ingre_norm_json.append(whatOil)
        return str(ingre_norm_json)
    else:
        return str(ingre_norm_json)

def get_food(ingre_list):
    food = open(food_recipes.json)
    recipe = json.loads(food)
    #get food from json string 
    #search ingredients list and compare to recipe
    #find three close enough 
    #return three as list or tuple
    #conclude get food function


################################# Commands #####################################
def start(update: Update, context: CallbackContext) -> str:
  chat_id = update.effective_chat.id
  malerand = randomizer_male()
  femalerand = randomizer_female()
  try:
    user = client.query(q.create(q.ref(q.collection("User_Login"), chat_id), {
            "data": {
                "id": chat_id,
                "username": "",
                "sex": "",
                "last_command": "newUsername",
                "list": [],
                "last_meal": [],
                "date": datetime.now(pytz.UTC)
            }
        }))
    context.bot.send_message(chat_id = chat_id, text =("Well hello there,\nHow are you today,\nOkay don't answer that i wont know how to reply you😂😂\n\n My name is Food Bot What's Yours??"))

    client.query(q.update(q.ref(q.collection("User_Login"), chat_id), {"data": {"last_command": "newUsername"}}))
  except:
    user = client.query(q.get(q.match(q.index("userData"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("User_Login"), user["ref"].id())))
    username=using["data"]["username"]
    sex=using["data"]["sex"]
    nickname = malerand if sex == "male" else femalerand
    context.bot.send_message(chat_id = chat_id, text =(username+"!!!!!!!!,\nMy newly acquired old friend\nWhat's up "+nickname+", don't know what to eat this "+daytime+"??\nOr you just don't know how to cook it😂😂\n\nCome on tell me...."),
                           reply_markup=main_keyboard())

        
def help(update: Update, context: CallbackContext) -> str:
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("userData"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("User_Login"), user["ref"].id())))
    username=using["data"]["username"]

    context.bot.send_message(chat_id = chat_id, text = "Hey "+randInsult+", looks like you got a little lost 😂😂\nNot a problem here though, I'll just direct you\n Food Bot at your service\n\n I'm basically just a bot that tells you what to cook or how to cook it, you don't need to worry about how i have so much information though, I'm lowkey a Genius😂😂\n\n Okay I'm done tooting my own horn just write /start and 'start' (pun intended😂😂) using some of my features")

def echo(update, context):
    """Handle direct user messages"""
    chat_id = update.effective_chat.id
    chat = update.effective_chat
    message = update.message.text
    user = client.query(q.get(q.match(q.index("userData"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("User_Login"), user["ref"].id())))
    username=using["data"]["username"]
    sex=using["data"]["sex"]
    last_command = using["data"]["last_command"]
    ingre_json_list = ""

    if last_command == "newUsername":
        context.bot.send_message(chat_id=update.effective_chat.id, text=("WOW "+message+" that's a really wonderful name.\n Now I know this is a little intrusive "+message+", but I need just one more information.\nAre you male or female"),reply_markup=gender_keyboard())
        client.query(q.update(q.ref(q.collection("User_Login"), chat_id), {"data": {"username": message}}))
        client.query(q.update(q.ref(q.collection("User_Login"), chat_id), {"data": {"last_command": ""}}))
    
    elif last_command == "collectIngredients":
        ingre_json_list = split_ingredients(message)

        context.bot.send_message(chat_id=update.effective_chat.id, text=("Okay so bacically you have:\n"+ingre_json_list),reply_markup=confirm_ingredients())
        client.query(q.update(q.ref(q.collection("User_Login"), chat_id), {"data": {"last_command": ""}}))
        client.query(q.update(q.ref(q.collection("User_Login"), chat_id), {"data": {"list": ingre_json_list}}))
    
    elif last_command == "addIngredients":
        addition = split_ingredients(message)
        ingre_json_list += addition
        context.bot.send_message(chat_id=update.effective_chat.id, text=("You added:\n"+addition+" to your previous list.\n Well i can reccommend a few things for you to eat\n Wanna see"),reply_markup=complete_ingredients())
        client.query(q.update(q.ref(q.collection("User_Login"), chat_id), {"data": {"last_command": ""}}))
        client.query(q.update(q.ref(q.collection("User_Login"), chat_id), {"data": {"list": ingre_json_list}}))


def error(update, context):
    print(f'I just get one nonsense error just now (hahaha) see am {context.error}')

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Okay this might sound a little funny cause I have a great sense of humour, but the DOC who created me and wrote my code..... well he did not tell me what that word means\nHow about you say something else, soomething i might understand.....like /start")

############################# Callbacks ########################################

def male_gender(update, context):
    chat_id = update.effective_chat.id
    chat = update.effective_chat
    user = client.query(q.get(q.match(q.index("userData"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("User_Login"), user["ref"].id())))
    username=using["data"]["username"]
    context.bot.send_message(chat_id=update.effective_chat.id, text=("Boss "+username+", My newly acquired friend\nWhat's up my G, don't know what to eat this"+daytime+"??\n Or you just don't know how to cook it😂😂\n\nCome on tell me...."),reply_markup=main_keyboard())
    client.query(q.update(q.ref(q.collection("User_Login"), chat_id), {"data": {"sex": "male"}}))

def female_gender(update, context):
    chat_id = update.effective_chat.id
    chat = update.effective_chat
    user = client.query(q.get(q.match(q.index("userData"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("User_Login"), user["ref"].id())))
    username=using["data"]["username"]
    context.bot.send_message(chat_id=update.effective_chat.id, text=("Okay "+username+", My newly acquired friend\nWhat's up Baby Girl, don't know what to eat this"+daytime+"??\n Or you just don't know how to cook it😂😂\n\nCome on tell me...."),reply_markup=main_keyboard())
    client.query(q.update(q.ref(q.collection("User_Login"), chat_id), {"data": {"sex": "female"}}))

def collect_ingredients(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("userData"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("User_Login"), user["ref"].id())))
    username=using["data"]["username"]
    sex=using["data"]["sex"]
    malerand = randomizer_male()
    femalerand = randomizer_female()
    nickname = malerand if sex == 'male' else femalerand
    context.bot.send_message(chat_id=update.effective_chat.id, text=("So...."+nickname+"......!!!\vYou don't know what you'd like to eat today😂😂.\nThat's cool though, that's why I'm here.\n\n Gimme a list of the ingredients you've got and I'll think of something."))
    client.query(q.update(q.ref(q.collection("User_Login"), chat_id), {"data": {"last_command": "colletIngredients"}}))

def re_collect_ingredients(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("userData"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("User_Login"), user["ref"].id())))
    username=using["data"]["username"]
    sex=using["data"]["sex"]
    malerand = randomizer_male()
    femalerand = randomizer_female()
    nickname = malerand if sex == 'male' else femalerand
    context.bot.send_message(chat_id=update.effective_chat.id, text=("Sorry "+nickname+" What ingredients did i miss??"))
    client.query(q.update(q.ref(q.collection("User_Login"), chat_id), {"data": {"last_command": "addIngredients"}}))


def suggest_food():
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("userData"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("User_Login"), user["ref"].id())))
    username=using["data"]["username"]
    sex=using["data"]["sex"]
    ingre_list= using["data"]["list"]
    food_list = get_food(ingre_list)
    meal = iter(food_list)
    context.bot.send_message(chat_id=update.effective_chat.id, text=("Okay "+nickname+"\nHere's what I've got,\nYou could eat "+next(meal)+", or you could have "+next(meal)+" the last suggestion I've got would be "+next(meal)+"\nWhat do you think you'd like to eat??"),reply_markup=suggested_keyboard(food_list))

def say_goodbye():
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("userData"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("User_Login"), user["ref"].id())))
    username=using["data"]["username"]
    sex=using["data"]["sex"]
    malerand = randomizer_male()
    femalerand = randomizer_female()
    nickname = malerand if sex == 'male' else femalerand
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=update.effective_chat.id, text=("Okay "+nickname+"\nI guess you found somrthing else to eat.\n We'll talk later "+username+" byeeee"))
############################# Keyboard #########################################

def main_keyboard():
    keyboard = [[InlineKeyboardButton('Wondering what to cook', callback_data='collect_list')],
                [InlineKeyboardButton('Find Recipe', callback_data='give recipe')],
                [InlineKeyboardButton('Talk Later', callback_data='end_talk')]]
    return InlineKeyboardMarkup(keyboard)

def gender_keyboard():
    keyboard = [[InlineKeyboardButton('Male', callback_data='male'), InlineKeyboardButton('Female', callback_data='female')]]
    return InlineKeyboardMarkup(keyboard)

def confirm_ingredients():
    keyboard = [
        [InlineKeyboardButton('Yeah those are the things I have', callback_data="ingredients_confirm")], [InlineKeyboardButton('No i think you missed a few', callback_data="re_list")], [InlineKeybardButton('Nevermind, Talk later', callback_data="end_talk")]]

def complete_ingredients():
    keyboard = [
        [InlineKeyboardButton('Show Me', callback_data="ingredients_confirm"), InlineKeybardButton('Nevemind', callback_data="end_talk")]]

def suggested_keyboard(food_list):
    meal = iter(food_list)
    keyboard = [[InlineKeyboardButton(next(meal), callback_data='food_select')],
                [InlineKeyboardButton(next(meal), callback_data='food_select')],
                [InlineKeyboardButton(next(meal), callback_data='food_select')],
                [InlineKeyboardButton('Main Menu', callback_data='re_main')]]
    return InlineKeyboardMarkup(keyboard)

def food_given_keyboard():
    keyboard = [[InlineKeyboardButton('Take me to a recipe', callback_data= recipeUrl )],
              [InlineKeyboardButton('Nevermind I know how to cook it', callback_data='end_talk')],[InlineKeyboardButton('Go Back', callback_data='re_suggest')]]
    return InlineKeyboardMarkup(keyboard)

############################# Handlers #########################################
client = FaunaClient(secret=fauna_secret)

updater = Updater(TOKEN, use_context="natrue")

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))

unknown_handler = MessageHandler(Filters.command, unknown)
########################## Callback Handlers ###################################
updater.dispatcher.add_handler(CallbackQueryHandler(male_gender, pattern='male'))
updater.dispatcher.add_handler(CallbackQueryHandler(female_gender, pattern='female'))
updater.dispatcher.add_handler(CallbackQueryHandler(collect_ingredients, pattern='collect_list'))
updater.dispatcher.add_handler(CallbackQueryHandler(suggest_food, pattern='ingredients_confirm'))
updater.dispatcher.add_handler(CallbackQueryHandler(re_collect_ingredients, pattern='re_list'))
updater.dispatcher.add_handler(CallbackQueryHandler(suggest_food, pattern='give_food'))
#updater.dispatcher.add_handler(CallbackQueryHandler(take_food, pattern='give_recipe'))
#updater.dispatcher.add_handler(CallbackQueryHandler(food_taken, pattern='food_chosen'))
#updater.dispatcher.add_handler(CallbackQueryHandler(food_resplice, pattern='food_reject'))
#updater.dispatcher.add_handler(CallbackQueryHandler(re_main, pattern='re_main'))
#updater.dispatcher.add_handler(CallbackQueryHandler(re_resplice, pattern='re_suggest'))
updater.dispatcher.add_handler(CallbackQueryHandler(say_goodbye, pattern='end_talk'))

updater.dispatcher.add_error_handler(error)
updater.dispatcher.add_handler(unknown_handler)
# Get the dispatcher to register handlers
dp = updater.dispatcher

# on noncommand i.e message - echo the message on Telegram
dp.add_handler(MessageHandler(Filters.text, echo))

# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C and will stop the bot gracefully.
updater.idle()
################################################################################