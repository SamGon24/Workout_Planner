from flask import Flask, render_template, request, session, redirect, url_for, send_file
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

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')
# Comment: Here we trace a route to index.html, which is the layout portion for our page
@app.route('/start', methods=['POST'])
def start():
    session['gender'] = request.form.get('gender')
    session['level'] = request.form.get('level')
    return redirect(url_for('select_split'))
# While being in index.html, we store the user´s decisions in that specific session
@app.route('/select_split')
def select_split():
    gender = session.get('gender')
    if gender == 'Male':
        routines = get_male_routines()
    elif gender == 'Female':
        routines = get_female_routines()
    else:
        return redirect(url_for('index'))
    
    return render_template('select_split.html', routines=routines.keys())
# While being in select_split.html, we store the user´s decisions in that specific session and
# drop it to select_split.html
@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    routine_name = request.form.get('routine')
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
    return render_template('plan.html', plan=final_plan)
# While being in select_split.html we store the user´s decisions in that specific session and
# drop it to plan.html, also making sure that the user has the possibility of saving their workout plan as a .txt
@app.route('/download')
def download():
    final_plan = session.get('final_plan', {})
    content = "Your Personalized Workout Plan\n\n"
    for day, exercises in final_plan.items():
        content += f"{day}:\n"
        for ex in exercises:
            content += f"  - {ex}\n"
        content += "\n"
    
    buffer = io.BytesIO()
    buffer.write(content.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name='workout_plan.txt',
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(debug=True)