from agents.agents import HumanAgent
from game_engine.game_models import TenThousandEngine


def main_loop(num_players: int):
    players = [HumanAgent(agent_id=f"Player {i}") for i in range(num_players)]

    ten_thousand_engine = TenThousandEngine(players)

    game_state = ten_thousand_engine.game_state

    while not ten_thousand_engine.is_done():
        roll = ten_thousand_engine.roll()
        current_player_id = ten_thousand_engine.current_player_id

        print(current_player_id)
        print(f"Roll: {roll}")
        indices = input("Which indices would you like to keep? (separate with spaces) ")
        end_turn = input("Would you like to end your turn? (y/n) ").lower() == "y"

        indices = [int(die) for die in indices.split()]

        game_state = ten_thousand_engine.choose(current_player_id, indices, end_turn)

if __name__ == '__main__':
    main_loop(1)