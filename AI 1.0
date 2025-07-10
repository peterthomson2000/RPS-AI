import random
from collections import deque, Counter

class RPS_AI:
    def __init__(self, memory=5, mode="human", personality="adaptive"):
        self.memory = memory
        self.mode = mode
        self.personality = personality.lower()
        self.opponent_moves = deque(maxlen=memory)
        self.my_moves = deque(maxlen=memory)
        self.moves = ["rock", "paper", "scissors"]
        self.beats = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
        self.loses_to = {v: k for k, v in self.beats.items()}

    def record_round(self, my_move, opponent_move):
        self.my_moves.append(my_move)
        self.opponent_moves.append(opponent_move)

    def simulate_human_opponent(self):
        if not self.my_moves:
            return random.choice(self.moves)

        last_my = self.my_moves[-1]
        last_opp = self.opponent_moves[-1] if self.opponent_moves else None

        if self.personality == "aggressive":
            if last_opp and self.beats[last_opp] == last_my:
                return last_opp
            return "rock"

        elif self.personality == "copycat":
            return last_my

        elif self.personality == "static":
            return "rock"

        elif self.personality == "adaptive":
            return self.loses_to.get(last_my, random.choice(self.moves))

        return random.choice(self.moves)

    def yellow_hat_predict(self):
        if not self.opponent_moves:
            return random.choice(self.moves)

        most_common = Counter(self.opponent_moves).most_common(1)[0][0]
        missing = set(self.moves) - set(self.opponent_moves)

        if missing:
            likely = most_common
        else:
            last_opponent = self.opponent_moves[-1]
            last_mine = self.my_moves[-1] if self.my_moves else None
            if last_opponent == self.beats.get(last_mine):
                likely = last_opponent
            else:
                likely = self.beats.get(last_opponent)

        return self.beats[likely]

    def next_move(self):
        if self.mode == "optimal":
            return self.yellow_hat_predict()
        return self.simulate_human_opponent()

    def evaluate_result(self, player, opponent):
        if self.beats[player] == opponent:
            return "Player wins!"
        elif self.beats[opponent] == player:
            return "AI wins!"
        return "It's a tie!"

    def play_round(self, my_move):
        opponent_move = self.next_move()
        self.record_round(my_move, opponent_move)
        return opponent_move, self.evaluate_result(my_move, opponent_move)

def play_against_both():
    print("\nChoose human-like AI personality: [aggressive, copycat, static, adaptive]")
    personality_input = input("Enter personality: ").strip().lower()
    if personality_input not in ["aggressive", "copycat", "static", "adaptive"]:
        print("Invalid personality. Defaulting to adaptive.")
        personality_input = "adaptive"

    human_like_ai = RPS_AI(mode="human", personality=personality_input)
    optimal_ai = RPS_AI(mode="optimal")

    while True:
        player_move = input("\nYour move (rock/paper/scissors or q to quit): ").strip().lower()
        if player_move == 'q':
            print("Exiting game.")
            break
        if player_move not in human_like_ai.moves:
            print("Invalid move.")
            continue

        move_human_ai, result_human = human_like_ai.play_round(player_move)
        move_optimal_ai, result_optimal = optimal_ai.play_round(player_move)

        print(f"\nHuman-like AI ({personality_input}) played: {move_human_ai} => {result_human}")
        print(f"Optimal AI played: {move_optimal_ai} => {result_optimal}")

if __name__ == "__main__":
    print("Yellow Hat Logic RPS AI")
    print("[1] Play against one AI\n[2] Play against both AIs")
    mode_choice = input("Enter 1 or 2: ").strip()

    if mode_choice == "1":
        print("Choose AI type: [1] Human-like [2] Optimal")
        ai_type = input("Enter 1 or 2: ").strip()
        mode = "human" if ai_type == "1" else "optimal"

        personality = "adaptive"
        if mode == "human":
            print("Choose personality: [aggressive, copycat, static, adaptive]")
            personality_input = input("Enter personality: ").strip().lower()
            if personality_input in ["aggressive", "copycat", "static", "adaptive"]:
                personality = personality_input

        ai = RPS_AI(mode=mode, personality=personality)

        while True:
            player_move = input("\nYour move (rock/paper/scissors or q to quit): ").strip().lower()
            if player_move == 'q':
                break
            if player_move not in ai.moves:
                print("Invalid move.")
                continue

            opponent_move, result = ai.play_round(player_move)
            print(f"AI played: {opponent_move} => {result}")

    elif mode_choice == "2":
        play_against_both()
    else:
        print("Invalid selection.")
