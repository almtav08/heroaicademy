from typing import Union
import game_structure as gs

def check(subject: Union['gs.Card', 'gs.Unit', 'gs.Action']):
    cards = [gs.Card(gs.CardValue.ARCHER, gs.CardType.UNIT), gs.Card(gs.CardValue.KNIGHT, gs.CardType.UNIT)]
    units = [gs.Unit(gs.Card(gs.CardValue.ARCHER, gs.CardType.UNIT), 1, 1, 1, 1, 1, 1, (1, 1), []), gs.Unit(gs.Card(gs.CardValue.KNIGHT, gs.CardType.UNIT), 1, 1, 1, 1, 1, 1, (1, 1), [])]
    actions = [gs.Action(units[0], None, (1,2))]
    if type(subject) is gs.Unit:
        in_units = subject in units
        print('Unit')
        print(in_units)
    elif type(subject) is gs.Action:
        in_actions = subject in actions
        print('Action')
        print(in_actions)
    else:
        in_deck = subject in cards
        print('Card')
        print(in_deck)

#card = gs.Card(gs.CardValue.CLERIC, gs.CardType.UNIT)
#card_col = gs.CardCollection()
#card_col.add_card(card)
#card_col_d = card_col.clone()
#card.value = gs.CardValue.ARCHER
#print(card_col_d)
#print(card_col)

card = gs.Card(gs.CardValue.ARCHER, gs.CardType.UNIT)
unit = gs.Unit(gs.Card(gs.CardValue.ARCHER, gs.CardType.UNIT), 1, 1, 1, 1, 1, 1, (1, 1), [])
action = gs.Action(unit, None, (1,2))

check(card)

#state = gs.GameState(gs.GameParameters())
#observation = state.get_observation()
#new_observation = observation.clone()
#new_observation.player_0_cards.remove_card(new_observation.player_0_cards.get_cards()[0])
#print(observation.player_0_cards)
#print(new_observation.player_0_cards)
#observation.copy_into(new_observation)
#print(new_observation.player_0_cards)

