'''
Import needed libraries
'''
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from random import randint


def card_name_set(URL):
    '''
    Uses BeautifulSoup object to extract card name and card set information from scryfall.com
    Args:
        URL (str): The string url for the scryfall website page to obtain card information from
    Return:
        Returns numpy arrays containing the card names and the sets the cards are from
    '''
    names_clean = []
    final_name1 = []
    final_name2 = []
    sets_clean = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    sleep(randint(1, 2))
    names = soup.find_all('div', class_='card-profile')
    sets = soup.find_all('span', class_='prints-current-set-name')

    for i, _ in enumerate(list(names)):
        names_clean.append(_.find_all('span', 'card-text-card-name'))

    for _ in names_clean:
        name1 = _[0].text.strip()

        if len(_) == 2:
            name2 = _[1].text.strip()

        else:
            name2 = np.nan

        final_name1.append(name1)
        final_name2.append(name2)

    for i, _ in enumerate(list(sets)):
        sets_clean.append(_.text.strip().split()[-1][1:4])

    return np.array(final_name1, dtype='object'), np.array(final_name2, dtype='object'), np.array(sets_clean,
                                                                                                  dtype='object')


def card_types(URL):
    '''
    Uses BeautifulSoup object to obtain card types from scryfall.com
    Args:
        URL (str): scryfall url in string form
    Return:
        Returns a numpy array of the card types for each cards type, and an array stating if the card is modal or not,
        and an array of the color indicator if present on the card
    '''
    ctypes = ['Land', 'Enchantment', 'Creature', 'Instant', 'Sorcery', 'Planeswalker', 'Artifact']
    types = []
    type1 = []
    type2 = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    sleep(randint(1, 2))
    cards = soup.find_all('div', class_='card-profile')

    for _ in cards:
        types.append(_.find_all('p', class_='card-text-type-line'))

    for _ in types:
        t1 = ''
        t2 = np.nan
        for i in _[0]:
            for j in ctypes:
                if j in i.text.strip().split(' '):
                    t1 = t1 + j + ' '

        if len(_) == 2:
            t2 = ''
            for i in _[1]:
                for j in ctypes:
                    if j in i.text.strip().split(' '):
                        t2 = t2 + j + ' '

            t2 = t2.strip()

        type1.append(t1.strip())
        type2.append(t2)

    return np.array(type1, dtype='object'), np.array(type2, dtype='object')


def mana_cost(URL):
    '''
    Uses BeautifulSoup object to obtain true mana cost of each card from scryfall.com
    Args:
        URL (str): scryfall url in string form
    Reutrn:
    Returns and array with all true mana costs, card overall converted mana cost, and whether it has phyrexian mana or not
    '''
    manas = []
    mc = []
    phyrexian = []
    cost1 = []
    cost2 = []
    MV1 = []
    MV2 = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    sleep(randint(1, 2))
    card = soup.find_all('div', class_='card-profile')

    for _ in card:
        manas.append(_.find_all('span', class_='card-text-mana-cost'))

    for _ in manas:
        if len(_) == 0:
            mana_c1 = np.nan
            mana_c2 = np.nan

        elif len(_) == 1:
            mana_c1 = _[0].text.strip().replace('{', '').replace('}', '')
            mana_c2 = np.nan

        elif len(_) == 2:
            mana_c1 = _[0].text.strip().replace('{', '').replace('}', '')
            mana_c2 = _[1].text.strip().replace('{', '').replace('}', '')

        cost1.append(mana_c1)
        cost2.append(mana_c2)

    for _ in cost1:
        Mana_value1 = 0
        if pd.isnull(_):
            Mana_value1 = 0
        else:
            for i in _:

                if i.isdigit():
                    Mana_value1 += float(i)

                elif i == 'X':
                    Mana_value1 += 0

                elif i in ['W', 'U', 'B', 'R', 'G']:
                    Mana_value1 += 1

        MV1.append(Mana_value1)

    for _ in cost2:
        Mana_value2 = 0
        if pd.isnull(_):
            Mana_value2 = 0
        else:
            for i in _:

                if i.isdigit():
                    Mana_value2 += float(i)

                elif i == 'X':
                    Mana_value2 += 0

                elif i in ['W', 'U', 'B', 'R', 'G']:
                    Mana_value2 += 1

        MV2.append(Mana_value2)

    return np.array(cost1, dtype='object'), np.array(cost2, dtype='object'), np.array(MV1, dtype='object'), np.array(
        MV2, dtype='object')


def color_ident(URL):
    '''
    Uses card mana costs and color indicators to determine the color identity of cards
    Args:
        castcost (array): array of true mana costs of cards (array elements are str type)
        colorinds (array): array of color indicators of each card if present (array elements are str type)
    Return:
        Returns and array containing the overall color identity of each card
    '''

    text = []
    symbols = []
    coloridentity = []
    alphabet = 'WUBRG'
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    sleep(randint(1, 2))
    card = soup.find_all('div', class_='card-profile')

    for _ in card:
        text.append(_.find_all('div', class_='card-text'))

    for _ in text:
        for i in _:
            unwanted = i.find('i')
            if unwanted != None and i.find('p',class_='card-text-type-line').text.find('Land') == -1:
                unwanted.extract()
            symbols.append(i.find_all('abbr'))

    for _ in symbols:
        colors = ''
        for i in _:
            i = i.text.strip().replace('{', '').replace('}', '').replace('/', '').replace('Color Indicator: ',
                                                                                          '').replace(',', '').replace(
                'White', 'W').replace('Blue', 'U').replace('Black', 'B').replace('Red', 'R').replace('Green',
                                                                                                     'G').replace('and',
                                                                                                                  '')
            for j in i:
                if j in ['W', 'U', 'B', 'R', 'G']:
                    colors += j
        if colors == '':
            coloridentity.append('C')
        else:
            coloridentity.append(''.join(sorted(set(colors), key=lambda word: [alphabet.index(c) for c in word])))

    return np.array(coloridentity)


def rarity(URL):
    '''
    Uses BeautifulSoup object to obtain card rarity from scrfall.com
    Args:
        URL (str): scryfall.com string url
    Return:
        Returns an array of rarities for each card
    '''
    rarity_clean = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    sleep(randint(1, 2))
    rarity = soup.find_all('span', class_='prints-current-set-details')

    for _ in rarity:
        rarity_clean.append(_.text.strip().split()[2][0])

    return np.array(rarity_clean)


def price(URL):
    '''
    Uses BeautifulSoup object to obtain price for each card on scrfall.com
    Args:
        URL (str): scryfall.com string url
    Return:
        Returns and array of prices for each card
    '''
    prices_clean = []
    cards = []
    pricer = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    sleep(randint(1, 2))
    cards = soup.find_all('div', class_='card-profile')

    for _ in cards:
        pricer.append(_.find_all('a', class_='currency-usd'))

    for _ in pricer:
        pholder = []
        for i in _:
            p = i.text.strip()
            pholder.append(float(p[p.find('$') + 1:]))

        if pholder == []:
            prices_clean.append(np.nan)
        else:
            prices_clean.append(round(np.array(pholder).mean(), 2))

    return np.array(prices_clean, dtype='object')


'''
Initialize driver and dummy variables
Run for loop to go through each page of scryfall site 
Calls each function to pull all card info
Combines all info into a pandas dataframe and save as a csv file
'''
driver = webdriver.Chrome()
URL = 'https://scryfall.com/search?as=full&order=name&page='

lastpage = 1211
names1 = []
names2 = []
sets1 = []
types1 = []
types2 = []
mana_cost1 = []
mana_cost2 = []
mana_value1 = []
mana_value2 = []
rarities = []
prices = []
coloridents = []

for i in range(1, lastpage):
    driver.get(URL + str(i) + '&q=legal%3Acommander&unique=cards')

    name1, name2, set1 = card_name_set(URL)
    names1.extend(name1)
    names2.extend(name2)
    sets1.extend(set1)

    card_type1, card_type2 = card_types(URL)
    types1.extend(card_type1)
    types2.extend(card_type2)

    cost1, cost2, mvalue1, mvalue2 = mana_cost(URL)
    mana_cost1.extend(cost1)
    mana_cost2.extend(cost2)
    mana_value1.extend(mvalue1)
    mana_value2.extend(mvalue2)

    card_rarity = rarity(URL)
    rarities.extend(card_rarity)

    card_price = price(URL)
    prices.extend(card_price)

    card_color = color_ident(URL)
    coloridents.extend(card_color)

df = pd.DataFrame({'Name1': names1, 'Name2': names2, 'Set': sets1, 'Card_type1': types1, 'Card_type2': types2,
                   'Mana_Cost1': mana_cost1, 'Mana_Cost2': mana_cost2, 'Mana_Value1': mana_value1,
                   'Mana_Value2': mana_value2, 'Color': coloridents, 'Rarity': rarities, 'Price': prices})
df.to_csv('card_data.csv', index=False)
driver.close()