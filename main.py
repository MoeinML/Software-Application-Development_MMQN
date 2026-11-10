from train_operations import get_all_trains

print("Train Booking System")

trains = get_all_trains()

for train in trains:
    print(train)