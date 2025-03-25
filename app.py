from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        gender = request.form.get('gender')
        level = request.form.get('level')
        
        if gender not in ['Male', 'Female']:
            return render_template('index.html', error="Invalid gender selection")
        
        routines = get_male_routines() if gender == 'Male' else get_female_routines()
        routine_names = list(routines.keys())
        
        return render_template('index.html', 
                             gender=gender,
                             level=level,
                             routine_names=routine_names,
                             show_routines=True)
    
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    gender = request.form.get('gender')
    level = request.form.get('level')
    routine_name = request.form.get('routine')
    
    if gender == 'Male':
        routines = get_male_routines()
    else:
        routines = get_female_routines()
    
    workout_plan = routines.get(routine_name, {})
    sets_and_reps = get_sets_and_reps(level)
    
    final_plan = {}
    for day, exercises in workout_plan.items():
        final_plan[day] = [f"{exercise} - {sets_and_reps}" for exercise in exercises]
    
    return render_template('plan.html', 
                         plan=final_plan,
                         gender=gender,
                         level=level,
                         routine_name=routine_name)

if __name__ == '__main__':
    app.run(debug=True)