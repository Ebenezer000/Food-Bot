############################ Keyboards #########################################
def main_keyboard():
    keyboard = [[InlineKeyboardButton('Sign up', callback_data='')],
                [InlineKeyboardButton('Find Recipe', callback_data='')],
                [InlineKeyboardButton('Talk Later', callback_data='')]]
    return InlineKeyboardMarkup(keyboard)
def gender_keyboard():
    keyboard = [[InlineKeyboardButton('Male', callback_data='')],
                [InlineKeyboardButton('Female', callback_data='')]]
    return InlineKeyboardMarkup(keyboard)
def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Account', callback_data='m1')],
              [InlineKeyboardButton('Finances', callback_data='m2')],
              [InlineKeyboardButton('See Prices', callback_data='Prices')],
              [InlineKeyboardButton('Contact Us', callback_data='Contact')]]
  return InlineKeyboardMarkup(keyboard)
def first_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Sign up', callback_data='Signup')],
                [InlineKeyboardButton('View Private Key', callback_data='ViewKey')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
def second_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Balance', callback_data='balance')],
                [InlineKeyboardButton('Deposit', callback_data='Deposit'),
                InlineKeyboardButton('Transfer', callback_data='Transfer')],
                [InlineKeyboardButton('Rain', callback_data='Rain'),
                InlineKeyboardButton('Swap (Coming Soon)', callback_data='ksi')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
def back_to_main():
    keyboard = [[InlineKeyboardButton('Go Back', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
