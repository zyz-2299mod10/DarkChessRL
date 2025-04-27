import random
from game import ChineseDarkChessEnv 

def random_test_dark_chess_env():
    env = ChineseDarkChessEnv()
    state = env.reset()
    done = False
    step_count = 0

    print("=== START ===")
    env.render()

    while not done:
        actions = env.get_legal_actions()

        if len(actions) == 0:
            print("No vaild action DRAW！")
            break

        action = random.choice(actions)

        print(f"Step {step_count+1}: Player {env.current_player} Choose action: {action}")

        state, reward, done, info = env.step(action)

        env.render()

        step_count += 1

        if done:
            if 'winner' in info:
                if info['winner'] == -1:
                    print("=== Draw ===")
                else:
                    print(f"=== player {info['winner']} WIN!===")
            else:
                print("=== GG ===")
            break

    print(f"total steps: {step_count}")


random_test_dark_chess_env()