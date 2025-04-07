from flask import Flask, render_template, request, session, redirect, url_for, send_file, jsonify, session
import io

app = Flask(__name__)

app.secret_key = '8401c7344c4a9963e10ea612fd8336d47370975976a116d0a727819dc9504e4a'
# Helper functions from original code
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

@app.route('/api/start', methods=['POST'])
def api_start():
    session['gender'] = request.json.get('gender')
    session['level'] = request.json.get('level')
    return jsonify({"message": "Session started", "gender": session['gender'], "level": session['level']})

@app.route('/api/select_split', methods=['GET'])
def api_select_split():
    gender = session.get('gender')
    if gender == 'Male':
        routines = get_male_routines()
    elif gender == 'Female':
        routines = get_female_routines()
    else:
        return jsonify({"error": "Invalid gender"}), 400
    
    return jsonify({"routines": list(routines.keys())})

@app.route('/api/generate_plan', methods=['POST'])
def api_generate_plan():
    routine_name = request.json.get('routine')
    session['routine'] = routine_name

    gender = session.get('gender')
    level = session.get('level')
    
    if gender == 'Male':
        routines = get_male_routines()
    else:
        routines = get_female_routines()
    
    workout_plan = routines[routine_name]
    sets_reps = get_sets_and_reps(level)
    
    final_plan = {}
    for day, exercises in workout_plan.items():
        final_plan[day] = [f"{exercise} - {sets_reps}" for exercise in exercises]
    
    session['final_plan'] = final_plan
    return jsonify({"plan": final_plan})

@app.route('/api/download', methods=['GET'])
def api_download():
    final_plan = session.get('final_plan', {})
    content = "Your Personalized Workout Plan\n\n"
    for day, exercises in final_plan.items():
        content += f"{day}:\n"
        for ex in exercises:
            content += f"  - {ex}\n"
        content += "\n"
    
    return jsonify({"workout_plan": content})