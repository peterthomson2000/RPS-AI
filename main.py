import random
import yaml
import os
from collections import deque, Counter, defaultdict

STATS_FILE = "rps_stats.yaml"
ADAPTIVE_MEMORY_FILE = "adaptive_memory.yaml"

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
        self.pattern_counts = defaultdict(Counter)

        if self.personality == "adaptive":
            self.load_adaptive_memory()

    def record_round(self, my_move, opponent_move):
        self.my_moves.append(my_move)
        self.opponent_moves.append(opponent_move)

        if len(self.opponent_moves) >= 3:
            pattern = tuple(list(self.opponent_moves)[-3:-1])
            next_move = self.opponent_moves[-1]
            self.pattern_counts[pattern][next_move] += 1

    def next_move(self):
        if self.mode == "optimal":
            return self.yellow_hat_predict()
        return self.simulate_human_opponent()

    def evaluate_result(self, player, opponent):
        if self.beats[player] == opponent:
            return "win"
        elif self.beats[opponent] == player:
            return "loss"
        return "tie"

    def simulate_human_opponent(self):
        if not self.my_moves:
            return random.choice(self.moves)

        last_my = self.my_moves[-1]
        last_opp = self.opponent_moves[-1] if self.opponent_moves else None

        if self.personality == "aggressive":
            if last_opp and self.beats[last_opp] == last_my:
                if random.randint(1, 3) == 2 or 3:
                    return last_opp
                return random.choice(self.moves)
            return random.choice(self.moves)
        elif self.personality == "copycat":
            return last_my
        elif self.personality == "static":
            return "rock"
        elif self.personality == "adaptive":
            return self.loses_to.get(last_my, random.choice(self.moves))

        return random.choice(self.moves)

    def yellow_hat_predict(self):
        if len(self.opponent_moves) >= 2:
            recent = tuple(list(self.opponent_moves)[-2:])
            if recent in self.pattern_counts:
                predicted = self.pattern_counts[recent].most_common(1)[0][0]
                return self.beats[predicted]
        if self.opponent_moves:
            most_common = Counter(self.opponent_moves).most_common(1)[0][0]
            return self.beats[most_common]
        return random.choice(self.moves)

    def save_adaptive_memory(self):
        if self.personality != "adaptive":
            return
        serializable = {str(k): dict(v) for k, v in self.pattern_counts.items()}
        with open(ADAPTIVE_MEMORY_FILE, "w") as f:
            yaml.dump(serializable, f)

    def load_adaptive_memory(self):
        if not os.path.exists(ADAPTIVE_MEMORY_FILE):
            return
        with open(ADAPTIVE_MEMORY_FILE, "r") as f:
            data = yaml.safe_load(f) or {}
        for k, v in data.items():
            # Clean tuple string format and parse into a tuple
            pattern = tuple(k.strip("()").replace("'", "").split(", "))
            self.pattern_counts[pattern] = Counter(v)

# --- Persistent Stats ---

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return yaml.safe_load(f) or {"wins": 0, "losses": 0, "ties": 0}
    return {"wins": 0, "losses": 0, "ties": 0}

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        yaml.dump(stats, f)

def reset_stats():
    stats = {"wins": 0, "losses": 0, "ties": 0}
    save_stats(stats)
    return stats

# --- Match Logic ---

def run_match(ai, rounds, stats):
    player_score = 0
    ai_score = 0
    print(f"\nBest-of-{rounds} match. First to {rounds // 2 + 1} wins.")
    print("Type 'reset' to clear your stats and adaptive AI memory.\n")

    while player_score < rounds // 2 + 1 and ai_score < rounds // 2 + 1:
        move = input("Your move (rock/paper/scissors): ").strip().lower()
        if move == 'reset':
            stats = reset_stats()
            if ai.personality == "adaptive" and os.path.exists(ADAPTIVE_MEMORY_FILE):
                os.remove(ADAPTIVE_MEMORY_FILE)
                print("Adaptive AI memory has been cleared.")
            print("Statistics have been reset.")
            continue
        if move not in ai.moves:
            print("Invalid move. Please try again.")
            continue

        ai_move = ai.next_move()
        ai.record_round(move, ai_move)
        result = ai.evaluate_result(move, ai_move)

        if result == "win":
            player_score += 1
        elif result == "loss":
            ai_score += 1

        print(f"AI played: {ai_move} — Result: {result}")
        print(f"Current score: You {player_score} | AI {ai_score}")

    if player_score > ai_score:
        print("\nYou won the match.")
        stats["wins"] += 1
    else:
        print("\nThe AI won the match.")
        stats["losses"] += 1

    if ai.personality == "adaptive":
        ai.save_adaptive_memory()

    return stats

# --- Game Entry Point ---

def game():
    stats = load_stats()

    while True:
        print("\nChoose AI Type:\n[1] Human-like\n[2] Optimal")
        mode_choice = input("Enter 1 or 2: ").strip()
        mode = "human" if mode_choice == "1" else "optimal"

        personality = "adaptive"
        if mode == "human":
            print("Choose personality: aggressive, copycat, static, adaptive")
            personality_input = input("Enter personality: ").strip().lower()
            if personality_input in ["aggressive", "copycat", "static", "adaptive"]:
                personality = personality_input
            else:
                print("Invalid personality. Defaulting to adaptive.")

        ai = RPS_AI(mode=mode, personality=personality)

        while True:
            rounds_input = input("Choose match format (3 or 5 rounds): ").strip()
            if rounds_input in ["3", "5"]:
                rounds = int(rounds_input)
                break
            else:
                print("Please enter 3 or 5.")

        stats = run_match(ai, rounds, stats)

        if len(ai.opponent_moves) >= 2:
            save_stats(stats)
            print(f"\nCumulative Optimal AIStatistics:")
            print(f"Wins:   {stats['wins']}")
            print(f"Losses: {stats['losses']}")

        play_again = input("\nWould you like to play another match? (y/n): ").strip().lower()
        if play_again != 'y':
            break

if __name__ == "__main__":
    print("Yellow Hat Logic RPS AI")
    game()