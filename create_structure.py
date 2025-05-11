import os

for week in range(1, 17):  # Week1 to Week16
    week_folder = f"Week{week}"
    os.makedirs(week_folder, exist_ok=True)
    
    for day in range(1, 6):  # Day1 to Day5
        day_folder = os.path.join(week_folder, f"Day{day}")
        os.makedirs(os.path.join(day_folder, "ExerciseXP"), exist_ok=True)
        os.makedirs(os.path.join(day_folder, "DailyChallenge"), exist_ok=True)
