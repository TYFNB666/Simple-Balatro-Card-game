from game import Game

def main():
    print("=" * 60)
    print("Simple Balatro Game!")
    print("=" * 60)
    print("\nGame rules:")
    print("- You have 5 chances to play a card and 4 chances to discard a card.")
    print("- Different card combinations will receive different scores based on their difficulty level.")
    print("- Objective: To achieve the highest possible total score!")
    print("=" * 60)

    g = Game()
    g.draw_cards(7)
    g.display_hand()

    while g.plays_left > 0:
        cmd = input("(p=play, d=discard, q=quit): ").strip().lower()
        if not cmd:
            continue
        c = cmd[0]

        if c == 'p':
            if not g.hand:
                print("No cards in hand.")
                continue
            try:
                raw = input("Enter indices (space separated, at least 1, at most 5): ")
                idx = [int(x) for x in raw.split()]
                if len(idx) == 0:
                    print("Please choose at least 1 card.")
                    continue
                if len(idx) > 5:
                    print("Please choose at most 5 cards.")
                    continue
                if len(set(idx)) != len(idx):
                    print("Duplicate indices are not allowed.")
                    continue
                if not all(0 <= i < len(g.hand) for i in idx):
                    print("Index out of range.")
                    continue
                g.play_cards(idx)
                g.display_hand()
            except ValueError:
                print("Input format error.")

        elif c == 'd':
            if g.discards_left <= 0:
                print("No discard left.")
                continue
            if not g.hand:
                print("No cards in hand.")
                continue
            try:
                raw = input("Enter indices to discard (space separated): ")
                idx = [int(x) for x in raw.split()]
                if len(idx) == 0:
                    print("Please choose at least one card.")
                    continue
                if not all(0 <= i < len(g.hand) for i in idx):
                    print("Index out of range.")
                    continue
                g.discard_cards(idx)
                g.display_hand()
            except ValueError:
                print("Input format error.")

        elif c == 'q':
            break

        else:
            print("Unknown command.")

    g.show_final_result()
    print("Thanks for playing.")

if __name__ == "__main__":
    main()
