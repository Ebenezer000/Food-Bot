############################# Messages #########################################
def welcome_back_message():
  return "My newly acquired but kinda old friend\nWhat's up my "+sex+", don't know what to eat this"+daytime+"??\n Or you just don't know how to cook it😂😂\n\nCome on tell me...."

def first_menu_message():
  return 'Setup your Wallet'

def second_menu_message():
  return 'What would you like to do with your finances today:'
def Contact(bot, update):
    bot.callback_query.message.edit_text(('Want to make a complaint?, Or request for addition of your custom token?, Contact us at info@ttk.finance or visit our website '+website),
    reply_markup=back_to_main())
def Prices(update, context):
    chat_id = update.effective_chat.id
    bnbpage = requests.get('https://coinmarketcap.com/currencies/binance-coin/')
    btcpage = requests.get('https://www.coindesk.com/price/bitcoin')
    ethpage = requests.get('https://www.coindesk.com/price/ethereum')
    bnbtree = html.fromstring(bnbpage.content)
    btctree = html.fromstring(btcpage.content)
    ethtree = html.fromstring(ethpage.content)
    _bnbprice = str(bnbtree.xpath('//div[@class="priceValue___11gHJ "]/text()'))
    _btcprice = str(btctree.xpath('//div[@class="price-large"]/text()'))
    _ethprice = str(ethtree.xpath('//div[@class="price-large"]/text()'))
    bnb_price = _bnbprice.strip(" [''] ")
    btc_price = _btcprice.strip(" [''] ")
    eth_price = _ethprice.strip(" [''] ")
    context.bot.send_message(chat_id = chat_id, text =('Right now the prices are:\n'+btc_price+' per BTC\n'+eth_price+' per ETH\n'+bnb_price+' per BNB'),
    reply_markup=back_to_main())
