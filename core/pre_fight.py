import time

def pre_fight_timer(seconds: int) -> None:
    print(f"Подготовка к бою ({seconds} секунд)...")
    for i in range(seconds, 0, -1):
        print(i)
        time.sleep(1)
    print("В бой!\n")
