def get_male_routines():
    return {
        "Push Pull Legs": {
            "Push Day": ["Bench Press", "Overhead Press", "Triceps Dips"],
            "Pull Day": ["Deadlift", "Pull-Ups", "Barbell Rows"],
            "Leg Day": ["Squats", "Leg Press", "Calf Raises"]
        },
        "Bro Split": {
            "Chest Day": ["Bench Press", "Incline Dumbbell Press", "Cable Flys"],
            "Back Day": ["Deadlift", "Lat Pulldown", "Seated Rows"],
            "Leg Day": ["Squats", "Leg Curl", "Leg Extension"],
            "Shoulder Day": ["Overhead Press", "Lateral Raises", "Face Pulls"],
            "Arms Day": ["Barbell Curls", "Skull Crushers", "Hammer Curls"]
        },
        "Upper Lower": {
            "Upper Day": ["Bench Press", "Pull-Ups", "Overhead Press"],
            "Lower Day": ["Squats", "Deadlifts", "Calf Raises"]
        }
    }

def get_female_routines():
    return {
        "Glutes & Legs Focus": {
            "Day 1": ["Hip Thrusts", "Bulgarian Split Squats", "Deadlifts"],
            "Day 2": ["Squats", "Glute Bridges", "Lunges"]
        },
        "Full Body": {
            "Day 1": ["Squats", "Deadlifts", "Push-Ups"],
            "Day 2": ["Pull-Ups", "Lunges", "Shoulder Press"]
        },
        "Upper Lower": {
            "Upper Day": ["Bench Press", "Pull-Ups", "Shoulder Press"],
            "Lower Day": ["Squats", "Hip Thrusts", "Calf Raises"]
        }
    }

def get_sets_and_reps(level):
    levels = {
        "Beginner": "3 sets of 10-12 reps",
        "Intermediate": "4 sets of 8-10 reps",
        "Advanced": "5 sets of 6-8 reps"
    }
    return levels.get(level, "3 sets of 10 reps")

def save_to_file(workout_plan):
    with open("workout_plan.txt", "w") as file:
        file.write("Your Personalized Workout Plan\n\n")
        for day, exercises in workout_plan.items():
            file.write(f"{day}:\n")
            for exercise in exercises:
                file.write(f"  - {exercise}\n")
            file.write("\n")
    print("Workout plan saved to workout_plan.txt!")

def main():
    gender = input("Enter your gender (Male/Female): ").strip().capitalize()
    level = input("Enter your gym experience level (Beginner/Intermediate/Advanced): ").strip().capitalize()
    
    if gender == "Male":
        routines = get_male_routines()
    elif gender == "Female":
        routines = get_female_routines()
    else:
        print("Invalid gender input.")
        return
    
    print("\nAvailable Workout Splits:")
    for idx, routine in enumerate(routines.keys(), start=1):
        print(f"{idx}. {routine}")
    
    choice = int(input("Select your workout split (Enter number): "))
    routine_name = list(routines.keys())[choice - 1]
    workout_plan = routines[routine_name]
    
    sets_and_reps = get_sets_and_reps(level)
    
    final_plan = {}
    for day, exercises in workout_plan.items():
        final_plan[day] = [f"{exercise} - {sets_and_reps}" for exercise in exercises]
    
    save_to_file(final_plan)
    print("Workout routine generated successfully!")

if __name__ == "__main__":
    main()
