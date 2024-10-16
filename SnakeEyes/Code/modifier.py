class Modifier:
    def __init__(self, name, description, cost, apply_modifier):
        self.name = name
        self.description = description
        self.cost = cost
        self.apply_modifier = apply_modifier
        self.active = False  # Track if modifier is currently active
        self.duration = 0  # Tracks how many turns modifier is active

    def activate(self, duration=0):
        self.active = True
        self.duration = duration

    def deactivate(self):
        self.active = False

    def apply(self, player, dice_rolls, game):
        if self.active:
            self.apply_modifier(player, dice_rolls, game)
            if self.duration > 0:
                self.duration -= 1
                if self.duration == 0:
                    self.deactivate()

#Isaac mod ideas
# Raise all store rewards by one (max of 5)
# Lower all store rewards by one (min of 5)






# Score Enhancers
def lucky_streak_modifier(player, dice_rolls, game):
    if player.tmpScore >= 20:  # Example threshold
        player.tmpScore = int(player.tmpScore * 1.5)
        game.result = f'Lucky Streak activated for Player {player.playerNum}!'

def hot_dice_modifier(player, dice_rolls, game):
    if dice_rolls == (5, 5):
        player.hot_dice_buff = 2  # Buff lasts for two turns
        game.result = f'Hot Dice activated for Player {player.playerNum}! Rolls +1 for next two turns.'


def cumulative_boost_modifier(player, dice_rolls, game):
    if player.last_roll == dice_rolls:  # Assuming player.last_roll tracks previous roll
        player.matching_rolls += 1
        if player.matching_rolls >= 3:
            player.tmpScore = int(player.tmpScore * (1 + 0.5 * (player.matching_rolls - 2)))
            game.result = f'Cumulative Boost! Score multiplier for Player {player.playerNum}.'


def bonus_round_modifier(player, dice_rolls, game):
    if dice_rolls == (1, 1):  # Snake eyes
        player.bonus_rounds = 3
        game.result = f'Bonus Round activated! Triple score for next three turns for Player {player.playerNum}.'


# Protection Modifiers
def shield_modifier(player, dice_rolls, game):
    if dice_rolls == (1, 6):
        player.shielded = True
        game.result = f'Shield activated for Player {player.playerNum}! Protected from next penalty.'


def safe_cash_out_modifier(player, dice_rolls, game):
    if dice_rolls == (3, 3):
        player.safe_cash_out = True
        game.result = f'Safe Cash Out activated for Player {player.playerNum}!'


def second_chance_modifier(player, dice_rolls, game):
    if player.losing_combination:
        player.second_chance = True
        game.result = f'Second Chance activated for Player {player.playerNum}! Roll again.'


def reset_immunity_modifier(player, dice_rolls, game):
    if player.cashed_out_first_time:
        player.reset_immunity = True
        game.result = f'Reset Immunity activated for Player {player.playerNum}!'


def dice_swap_modifier(player, dice_rolls, game):
    if dice_rolls in [(2, 5), (3, 4)]:  # Example combinations
        player.dice_swap = True
        game.result = f'Dice Swap activated for Player {player.playerNum}!'


def roll_rewind_modifier(player, dice_rolls, game):
    if player.bad_roll:
        player.roll_rewind = True
        game.result = f'Roll Rewind activated for Player {player.playerNum}!'


# Creating modifier instances
lucky_streak = Modifier(
    name="Lucky Streak",
    description="After successful rolls, the next score gets a x1.5 multiplier.",
    cost=10,
    apply_modifier=lucky_streak_modifier,
)

hot_dice = Modifier(
    name="Hot Dice",
    description="Rolling a 5 and 5 grants a temporary buff that adds +1 to each die roll for the next two turns.",
    cost=8,
    apply_modifier=hot_dice_modifier,
)

cumulative_boost = Modifier(
    name="Cumulative Boost",
    description="If a player rolls the same number three times in a row, they gain an increasing score multiplier.",
    cost=12,
    apply_modifier=cumulative_boost_modifier,
)

bonus_round = Modifier(
    name="Bonus Round",
    description="If a player rolls 'snake eyes', they enter a bonus round with triple scores for three turns.",
    cost=15,
    apply_modifier=bonus_round_modifier,
)

shield = Modifier(
    name="Shield",
    description="Rolling certain numbers (1 and 6) gives protection against penalties.",
    cost=5,
    apply_modifier=shield_modifier,
)

safe_cash_out = Modifier(
    name="Safe Cash Out",
    description="Players rolling a pair of threes can cash out with no penalty.",
    cost=7,
    apply_modifier=safe_cash_out_modifier,
)

second_chance = Modifier(
    name="Second Chance",
    description="One chance to roll again before a penalty applies on a losing combination.",
    cost=9,
    apply_modifier=second_chance_modifier,
)

reset_immunity = Modifier(
    name="Reset Immunity",
    description="After cashing out once, player becomes immune to resets for the next round.",
    cost=6,
    apply_modifier=reset_immunity_modifier,
)

dice_swap = Modifier(
    name="Dice Swap",
    description="On certain rolls, the player can swap dice values to turn a bad roll into a good one.",
    cost=8,
    apply_modifier=dice_swap_modifier,
)

roll_rewind = Modifier(
    name="Roll Rewind",
    description="After a bad roll, player can rewind one turn and use the previous roll result.",
    cost=10,
    apply_modifier=roll_rewind_modifier,
)

# List of all available modifiers
available_modifiers = [
    lucky_streak,
    hot_dice,
    cumulative_boost,
    bonus_round,
    shield,
    safe_cash_out,
    second_chance,
    reset_immunity,
    dice_swap,
    roll_rewind
]
