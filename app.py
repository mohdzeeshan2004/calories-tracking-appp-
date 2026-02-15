import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import os
import random

# Set page config
st.set_page_config(
    page_title="Calorie Tracker - Nutrition Leveling System",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .level-container {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
        transition: transform 0.3s ease;
    }
    .level-container:hover {
        transform: translateY(-5px);
    }
    .rank-container {
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.4);
        transition: transform 0.3s ease;
    }
    .rank-container:hover {
        transform: translateY(-5px);
    }
    .goal-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 5px 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    .on-track {
        background: linear-gradient(90deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
    }
    .over-calories {
        background: linear-gradient(90deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 4px solid #dc3545;
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
    }
    .achievement-badge {
        display: inline-block;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        padding: 10px 16px;
        border-radius: 20px;
        color: white;
        font-weight: bold;
        margin: 5px;
        box-shadow: 0 4px 12px rgba(255, 165, 0, 0.3);
    }
    .motivation-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        font-size: 18px;
        font-style: italic;
    }
    .macro-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 5px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(245, 87, 108, 0.3);
    }
    .food-item {
        background: #f8f9fa;
        padding: 12px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 4px solid #667eea;
    }
    </style>
""", unsafe_allow_html=True)

# Motivational quotes
NUTRITION_QUOTES = [
    "🥗 You are what you eat - make it count!",
    "💪 Fuel your body, fuel your dreams!",
    "🌟 Every healthy meal is a victory!",
    "🎯 Your body will thank you tomorrow!",
    "🔥 Progress over perfection!",
    "🌱 Small choices = Big changes!",
    "💚 Love your body, feed it well!",
    "⭐ You've got this! One meal at a time!",
    "🎪 Consistency builds health!",
    "🏆 Be the best version of yourself!",
    "✨ Nutrition is self-care!",
    "🚀 Your health is your wealth!",
    "💎 Invest in yourself - eat well!",
    "🌈 Balance is key, not perfection!",
    "👑 Own your nutrition journey!",
]

COMMON_FOODS = {
    "Breakfast": [
        {"name": "Oatmeal (1 cup)", "calories": 150, "protein": 5, "carbs": 27, "fat": 3},
        {"name": "Eggs (2)", "calories": 155, "protein": 13, "carbs": 1, "fat": 11},
        {"name": "Banana", "calories": 105, "protein": 1, "carbs": 27, "fat": 0},
        {"name": "Greek Yogurt (1 cup)", "calories": 130, "protein": 23, "carbs": 9, "fat": 0},
        {"name": "Toast with Butter", "calories": 200, "protein": 6, "carbs": 28, "fat": 9},
        {"name": "Smoothie (avg)", "calories": 250, "protein": 8, "carbs": 45, "fat": 6},
    ],
    "Lunch": [
        {"name": "Chicken Breast (100g)", "calories": 165, "protein": 31, "carbs": 0, "fat": 3},
        {"name": "Rice (1 cup)", "calories": 206, "protein": 4, "carbs": 45, "fat": 0},
        {"name": "Salmon (100g)", "calories": 206, "protein": 22, "carbs": 0, "fat": 13},
        {"name": "Salad (avg)", "calories": 150, "protein": 5, "carbs": 12, "fat": 8},
        {"name": "Pasta (1 cup)", "calories": 220, "protein": 8, "carbs": 43, "fat": 1},
        {"name": "Burger", "calories": 540, "protein": 30, "carbs": 40, "fat": 28},
    ],
    "Dinner": [
        {"name": "Grilled Fish (100g)", "calories": 180, "protein": 25, "carbs": 0, "fat": 8},
        {"name": "Broccoli (1 cup)", "calories": 55, "protein": 3, "carbs": 11, "fat": 0},
        {"name": "Sweet Potato", "calories": 103, "protein": 2, "carbs": 24, "fat": 0},
        {"name": "Steak (100g)", "calories": 250, "protein": 26, "carbs": 0, "fat": 15},
        {"name": "Spinach (1 cup)", "calories": 7, "protein": 1, "carbs": 1, "fat": 0},
        {"name": "Pizza (1 slice)", "calories": 285, "protein": 12, "carbs": 36, "fat": 10},
    ],
    "Snacks": [
        {"name": "Apple", "calories": 95, "protein": 0, "carbs": 25, "fat": 0},
        {"name": "Almonds (1 oz)", "calories": 164, "protein": 6, "carbs": 6, "fat": 14},
        {"name": "Protein Bar", "calories": 200, "protein": 20, "carbs": 22, "fat": 5},
        {"name": "Greek Yogurt (small)", "calories": 100, "protein": 17, "carbs": 7, "fat": 0},
        {"name": "Peanut Butter (2 tbsp)", "calories": 188, "protein": 8, "carbs": 7, "fat": 16},
        {"name": "Chips (1 oz)", "calories": 150, "protein": 2, "carbs": 15, "fat": 10},
    ],
    "Beverages": [
        {"name": "Water", "calories": 0, "protein": 0, "carbs": 0, "fat": 0},
        {"name": "Green Tea", "calories": 2, "protein": 0, "carbs": 0, "fat": 0},
        {"name": "Coffee (black)", "calories": 5, "protein": 0, "carbs": 0, "fat": 0},
        {"name": "Orange Juice (1 cup)", "calories": 112, "protein": 2, "carbs": 26, "fat": 0},
        {"name": "Soda (1 can)", "calories": 140, "protein": 0, "carbs": 39, "fat": 0},
        {"name": "Protein Shake", "calories": 180, "protein": 25, "carbs": 8, "fat": 2},
    ],
}

ACHIEVEMENTS = {
    "first_meal": {"name": "First Bite", "description": "Log your first meal", "emoji": "🍽️"},
    "five_meals": {"name": "Meal Logger", "description": "Log 5 meals", "emoji": "📝"},
    "on_target": {"name": "Perfect Day", "description": "Stay within calorie goal", "emoji": "🎯"},
    "week_on_track": {"name": "Consistency", "description": "7 days on target", "emoji": "📅"},
    "macro_master": {"name": "Macro Master", "description": "Hit macros within 10%", "emoji": "💪"},
    "high_protein": {"name": "Protein Powerhouse", "description": "100g+ protein in one day", "emoji": "🥚"},
    "veggie_warrior": {"name": "Veggie Warrior", "description": "200+ calories from veggies", "emoji": "🥬"},
    "water_warrior": {"name": "Hydration Hero", "description": "8+ glasses of water", "emoji": "💧"},
    "calorie_deficit": {"name": "Deficit Achiever", "description": "Maintain 500 cal deficit", "emoji": "📉"},
    "weight_milestone": {"name": "Milestone Reached", "description": "Reach weight goal", "emoji": "🏆"},
}

RANK_SYSTEM = [
    {"rank": "BEGINNER", "min_points": 0, "emoji": "🌱"},
    {"rank": "APPRENTICE", "min_points": 100, "emoji": "👨‍🍳"},
    {"rank": "CHEF", "min_points": 250, "emoji": "🍽️"},
    {"rank": "MASTER CHEF", "min_points": 500, "emoji": "👨‍🍳"},
    {"rank": "NUTRITION EXPERT", "min_points": 1000, "emoji": "💚"},
    {"rank": "HEALTH CHAMPION", "min_points": 2000, "emoji": "🏆"},
    {"rank": "LEGEND", "min_points": 5000, "emoji": "👑"},
]

# Data storage
DATA_DIR = "calorie_data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def save_data(filename="tracker.json"):
    """Save data to JSON"""
    try:
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'w') as f:
            json.dump(st.session_state.user_data, f, indent=4)
        return True
    except:
        return False

def load_data(filename="tracker.json"):
    """Load data from JSON"""
    try:
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return None
    except:
        return None

# Initialize session state
if "user_data" not in st.session_state:
    loaded = load_data()
    if loaded:
        st.session_state.user_data = loaded
    else:
        st.session_state.user_data = {
            "username": "Nutritionist",
            "level": 1,
            "experience": 0,
            "exp_needed": 100,
            "rank": "BEGINNER",
            "rank_points": 0,
            "daily_calorie_goal": 2000,
            "daily_protein_goal": 150,
            "daily_carbs_goal": 225,
            "daily_fat_goal": 65,
            "target_weight": 170,
            "current_weight": 180,
            "meals": {},
            "weight_log": {},
            "achievements": [],
            "last_saved": None,
            "total_meals_logged": 0,
            "best_streak": 0,
            "daily_bonus_claimed": False,
            "last_bonus_date": None,
        }

def get_current_rank(rank_points):
    """Get current rank"""
    for i in range(len(RANK_SYSTEM) - 1, -1, -1):
        if rank_points >= RANK_SYSTEM[i]["min_points"]:
            return RANK_SYSTEM[i]
    return RANK_SYSTEM[0]

def get_today_key():
    """Get today's date as key"""
    return datetime.now().strftime("%Y-%m-%d")

def add_experience(exp_amount):
    """Add experience"""
    user = st.session_state.user_data
    user["experience"] += exp_amount
    
    leveled_up = False
    while user["experience"] >= user["exp_needed"]:
        user["experience"] -= user["exp_needed"]
        user["level"] += 1
        user["rank_points"] += 20
        user["exp_needed"] = 100 + (user["level"] - 1) * 50
        leveled_up = True
    
    new_rank = get_current_rank(user["rank_points"])
    user["rank"] = new_rank["rank"]
    
    return leveled_up

def log_meal(meal_name, calories, protein, carbs, fat):
    """Log a meal"""
    today = get_today_key()
    if today not in st.session_state.user_data["meals"]:
        st.session_state.user_data["meals"][today] = []
    
    st.session_state.user_data["meals"][today].append({
        "name": meal_name,
        "calories": calories,
        "protein": protein,
        "carbs": carbs,
        "fat": fat,
        "time": datetime.now().strftime("%H:%M")
    })
    
    st.session_state.user_data["total_meals_logged"] += 1
    add_experience(10)
    save_data()

def get_today_meals():
    """Get today's meals"""
    today = get_today_key()
    return st.session_state.user_data["meals"].get(today, [])

def get_today_totals():
    """Get today's totals"""
    meals = get_today_meals()
    totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
    
    for meal in meals:
        totals["calories"] += meal["calories"]
        totals["protein"] += meal["protein"]
        totals["carbs"] += meal["carbs"]
        totals["fat"] += meal["fat"]
    
    return totals

def get_meal_streak():
    """Get meal streak"""
    today = datetime.now()
    streak = 0
    
    for i in range(100):
        check_date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        if check_date in st.session_state.user_data["meals"]:
            meals = st.session_state.user_data["meals"][check_date]
            if meals:
                streak += 1
            else:
                break
        else:
            break
    
    if streak > st.session_state.user_data.get("best_streak", 0):
        st.session_state.user_data["best_streak"] = streak
    
    return streak

def claim_daily_bonus():
    """Claim daily bonus"""
    today = get_today_key()
    last_claimed = st.session_state.user_data.get("last_bonus_date")
    
    if last_claimed != today:
        add_experience(25)
        st.session_state.user_data["daily_bonus_claimed"] = True
        st.session_state.user_data["last_bonus_date"] = today
        save_data()
        return True
    return False

# Sidebar
st.sidebar.title("🍎 Calorie Tracker")

col_save1, col_save2 = st.sidebar.columns(2)
with col_save1:
    if st.button("💾 Save", use_container_width=True):
        if save_data():
            st.session_state.user_data["last_saved"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.sidebar.success("✅ Saved!")

with col_save2:
    if st.button("📥 Load", use_container_width=True):
        loaded = load_data()
        if loaded:
            st.session_state.user_data = loaded
            st.sidebar.success("✅ Loaded!")
            st.rerun()

st.sidebar.divider()

# Daily bonus
today = get_today_key()
if st.session_state.user_data.get("last_bonus_date") != today:
    if st.sidebar.button("🎁 Daily Bonus (+25 XP)", use_container_width=True):
        if claim_daily_bonus():
            st.sidebar.success("🎉 Bonus claimed!")
            st.rerun()
else:
    st.sidebar.caption("✅ Bonus claimed!")

st.sidebar.divider()

page = st.sidebar.radio("Navigation", ["🏠 Home", "🍽️ Log Meal", "📊 Analytics", "⚖️ Weight", "🏆 Achievements", "⚙️ Settings"])

# Main Header
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    st.markdown(f"""
    <div class='level-container'>
        <h2>🍎 LEVEL {st.session_state.user_data['level']}</h2>
        <p>Experience: {st.session_state.user_data['experience']}/{st.session_state.user_data['exp_needed']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    progress = st.session_state.user_data['experience'] / st.session_state.user_data['exp_needed']
    st.progress(min(progress, 1.0))

with col2:
    rank_info = get_current_rank(st.session_state.user_data['rank_points'])
    st.markdown(f"""
    <div class='rank-container'>
        <h2>{rank_info['emoji']} {rank_info['rank']}</h2>
        <p>Rank Points: {st.session_state.user_data['rank_points']}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='goal-container'>
        <h4>🎯 Daily Goal</h4>
        <p style='margin: 5px 0;'>{st.session_state.user_data['daily_calorie_goal']} cal</p>
        <small>Weight: {st.session_state.user_data['current_weight']} lbs</small>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Daily motivation
st.markdown(f"""
<div class='motivation-card'>
🌟 {random.choice(NUTRITION_QUOTES)} 🌟
</div>
""", unsafe_allow_html=True)

# PAGE: Home
if page == "🏠 Home":
    today_meals = get_today_meals()
    today_totals = get_today_totals()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        remaining = st.session_state.user_data["daily_calorie_goal"] - today_totals["calories"]
        color = "🟢" if remaining >= 0 else "🔴"
        st.metric(f"{color} Remaining", f"{max(0, remaining)} cal")
    
    with col2:
        st.metric("📝 Meals", len(today_meals))
    
    with col3:
        streak = get_meal_streak()
        st.metric("📅 Streak", f"{streak} days")
    
    with col4:
        st.metric("⭐ Total Logged", st.session_state.user_data["total_meals_logged"])
    
    st.divider()
    
    # Today's calories status
    goal = st.session_state.user_data["daily_calorie_goal"]
    consumed = today_totals["calories"]
    
    if consumed == 0:
        st.info("📝 No meals logged yet. Start by logging a meal!")
    elif consumed <= goal:
        status = "✅ ON TRACK!"
        st.markdown(f"""
        <div class='on-track'>
            <b>{status}</b> You're doing great! {goal - consumed} calories remaining.
        </div>
        """, unsafe_allow_html=True)
    else:
        excess = consumed - goal
        st.markdown(f"""
        <div class='over-calories'>
            <b>⚠️ OVER GOAL</b> You've consumed {excess} extra calories. Time to get moving!
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Macros
    st.subheader("💪 Macronutrients")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        protein_percent = (today_totals["protein"] / st.session_state.user_data["daily_protein_goal"]) * 100
        st.markdown(f"""
        <div class='macro-card'>
            <h3>🥚 Protein</h3>
            <h2>{today_totals["protein"]}g</h2>
            <p>Goal: {st.session_state.user_data["daily_protein_goal"]}g ({protein_percent:.0f}%)</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(min(protein_percent / 100, 1.0))
    
    with col2:
        carbs_percent = (today_totals["carbs"] / st.session_state.user_data["daily_carbs_goal"]) * 100
        st.markdown(f"""
        <div class='macro-card'>
            <h3>🍞 Carbs</h3>
            <h2>{today_totals["carbs"]}g</h2>
            <p>Goal: {st.session_state.user_data["daily_carbs_goal"]}g ({carbs_percent:.0f}%)</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(min(carbs_percent / 100, 1.0))
    
    with col3:
        fat_percent = (today_totals["fat"] / st.session_state.user_data["daily_fat_goal"]) * 100
        st.markdown(f"""
        <div class='macro-card'>
            <h3>🥑 Fat</h3>
            <h2>{today_totals["fat"]}g</h2>
            <p>Goal: {st.session_state.user_data["daily_fat_goal"]}g ({fat_percent:.0f}%)</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(min(fat_percent / 100, 1.0))
    
    st.divider()
    
    # Today's meals
    st.subheader("🍽️ Today's Meals")
    if today_meals:
        for i, meal in enumerate(today_meals):
            st.markdown(f"""
            <div class='food-item'>
                <b>{meal['name']}</b> ({meal['time']})
                <br>
                {meal['calories']} cal | P:{meal['protein']}g | C:{meal['carbs']}g | F:{meal['fat']}g
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No meals logged yet. Log your first meal to start!")

# PAGE: Log Meal
elif page == "🍽️ Log Meal":
    st.subheader("🍽️ Log a Meal")
    
    tab1, tab2 = st.tabs(["Quick Select", "Custom Entry"])
    
    with tab1:
        st.write("### Select from common foods")
        
        category = st.selectbox("Food Category", list(COMMON_FOODS.keys()))
        foods = COMMON_FOODS[category]
        
        food_option = st.selectbox("Food", [f"{food['name']} ({food['calories']} cal)" for food in foods])
        
        selected_idx = [f"{food['name']} ({food['calories']} cal)" for food in foods].index(food_option)
        selected_food = foods[selected_idx]
        
        if st.button("✅ Log This Food", type="primary", key="log_quick"):
            log_meal(selected_food["name"], selected_food["calories"], selected_food["protein"], selected_food["carbs"], selected_food["fat"])
            st.success(f"✅ Logged {selected_food['name']}!")
            st.balloons()
            st.rerun()
    
    with tab2:
        st.write("### Enter custom food")
        
        col1, col2 = st.columns(2)
        with col1:
            food_name = st.text_input("Food Name")
            calories = st.number_input("Calories", min_value=0, max_value=5000, value=100)
        
        with col2:
            protein = st.number_input("Protein (g)", min_value=0, max_value=500, value=10)
            carbs = st.number_input("Carbs (g)", min_value=0, max_value=500, value=20)
        
        fat = st.number_input("Fat (g)", min_value=0, max_value=200, value=5)
        
        if st.button("✅ Log Custom Food", type="primary", key="log_custom"):
            if food_name:
                log_meal(food_name, calories, protein, carbs, fat)
                st.success(f"✅ Logged {food_name}!")
                st.balloons()
                st.rerun()
            else:
                st.error("Please enter a food name")

# PAGE: Analytics
elif page == "📊 Analytics":
    st.subheader("📊 Analytics & Trends")
    
    if not st.session_state.user_data["meals"]:
        st.info("Log some meals to see analytics!")
    else:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📝 Total Meals", st.session_state.user_data["total_meals_logged"])
        
        with col2:
            days_logged = len(st.session_state.user_data["meals"])
            st.metric("📅 Days Logged", days_logged)
        
        with col3:
            streak = get_meal_streak()
            st.metric("🔥 Streak", f"{streak} days")
        
        with col4:
            st.metric("🏆 Best Streak", st.session_state.user_data["best_streak"])
        
        st.divider()
        
        # Simple table of last 7 days
        st.subheader("📅 Last 7 Days Summary")
        
        summary_data = []
        today = datetime.now()
        
        for i in range(6, -1, -1):
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            date_display = (today - timedelta(days=i)).strftime("%a, %b %d")
            meals = st.session_state.user_data["meals"].get(date, [])
            
            total_cal = sum(m["calories"] for m in meals)
            total_protein = sum(m["protein"] for m in meals)
            total_carbs = sum(m["carbs"] for m in meals)
            total_fat = sum(m["fat"] for m in meals)
            
            summary_data.append({
                "Date": date_display,
                "Calories": total_cal,
                "Protein": total_protein,
                "Carbs": total_carbs,
                "Fat": total_fat,
                "Meals": len(meals)
            })
        
        df = pd.DataFrame(summary_data)
        st.dataframe(df, use_container_width=True)

# PAGE: Weight
elif page == "⚖️ Weight":
    st.subheader("⚖️ Weight Tracking")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Current Weight", f"{st.session_state.user_data['current_weight']} lbs")
    
    with col2:
        st.metric("🎯 Target Weight", f"{st.session_state.user_data['target_weight']} lbs")
    
    with col3:
        difference = st.session_state.user_data["current_weight"] - st.session_state.user_data["target_weight"]
        st.metric("📈 To Go", f"{difference} lbs")
    
    st.divider()
    
    st.write("### Update Weight")
    col1, col2 = st.columns(2)
    
    with col1:
        new_weight = st.number_input("Current Weight (lbs)", value=st.session_state.user_data["current_weight"], min_value=50, max_value=500)
    
    with col2:
        target_weight = st.number_input("Target Weight (lbs)", value=st.session_state.user_data["target_weight"], min_value=50, max_value=500)
    
    if st.button("💾 Save Weight", type="primary"):
        today = get_today_key()
        st.session_state.user_data["current_weight"] = new_weight
        st.session_state.user_data["target_weight"] = target_weight
        st.session_state.user_data["weight_log"][today] = new_weight
        save_data()
        st.success("✅ Weight saved!")
        st.rerun()
    
    st.divider()
    
    # Weight history table
    if st.session_state.user_data["weight_log"]:
        st.subheader("📉 Weight History")
        
        weight_data = []
        for date in sorted(st.session_state.user_data["weight_log"].keys(), reverse=True)[:10]:
            weight_data.append({
                "Date": date,
                "Weight": st.session_state.user_data["weight_log"][date]
            })
        
        df_weight = pd.DataFrame(weight_data)
        st.dataframe(df_weight, use_container_width=True)

# PAGE: Achievements
elif page == "🏆 Achievements":
    st.subheader("🏆 Achievements")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📝 Meals Logged", st.session_state.user_data["total_meals_logged"])
    
    with col2:
        st.metric("🏅 Achievements", f"{len(st.session_state.user_data['achievements'])}/{len(ACHIEVEMENTS)}")
    
    with col3:
        st.metric("📅 Streak", f"{get_meal_streak()} days")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 🎖️ Earned Achievements")
        if st.session_state.user_data["achievements"]:
            for ach_id in st.session_state.user_data["achievements"]:
                ach = ACHIEVEMENTS.get(ach_id)
                if ach:
                    st.markdown(f"<div class='achievement-badge'>{ach['emoji']} {ach['name']}</div>", unsafe_allow_html=True)
                    st.caption(ach["description"])
        else:
            st.info("🚀 Start logging meals!")
    
    with col2:
        st.write("### 🎯 Next Achievements")
        count = 0
        for ach_id, ach in ACHIEVEMENTS.items():
            if ach_id not in st.session_state.user_data["achievements"] and count < 5:
                st.write(f"**{ach['emoji']} {ach['name']}**")
                st.caption(ach["description"])
                count += 1

# PAGE: Settings
elif page == "⚙️ Settings":
    st.subheader("⚙️ Settings")
    
    tab1, tab2 = st.tabs(["Goals", "Advanced"])
    
    with tab1:
        st.write("### Nutrition Goals")
        
        col1, col2 = st.columns(2)
        
        with col1:
            calorie_goal = st.number_input("Daily Calorie Goal", value=st.session_state.user_data["daily_calorie_goal"], min_value=500, max_value=5000, step=100)
            protein_goal = st.number_input("Daily Protein Goal (g)", value=st.session_state.user_data["daily_protein_goal"], min_value=20, max_value=500, step=5)
        
        with col2:
            carbs_goal = st.number_input("Daily Carbs Goal (g)", value=st.session_state.user_data["daily_carbs_goal"], min_value=50, max_value=500, step=10)
            fat_goal = st.number_input("Daily Fat Goal (g)", value=st.session_state.user_data["daily_fat_goal"], min_value=20, max_value=200, step=5)
        
        if st.button("💾 Save Goals", type="primary"):
            st.session_state.user_data["daily_calorie_goal"] = calorie_goal
            st.session_state.user_data["daily_protein_goal"] = protein_goal
            st.session_state.user_data["daily_carbs_goal"] = carbs_goal
            st.session_state.user_data["daily_fat_goal"] = fat_goal
            save_data()
            st.success("✅ Goals saved!")
    
    with tab2:
        if st.button("🔄 Reset All Data", type="secondary"):
            if st.checkbox("I'm sure"):
                st.session_state.user_data = {
                    "username": "Nutritionist",
                    "level": 1,
                    "experience": 0,
                    "exp_needed": 100,
                    "rank": "BEGINNER",
                    "rank_points": 0,
                    "daily_calorie_goal": 2000,
                    "daily_protein_goal": 150,
                    "daily_carbs_goal": 225,
                    "daily_fat_goal": 65,
                    "target_weight": 170,
                    "current_weight": 180,
                    "meals": {},
                    "weight_log": {},
                    "achievements": [],
                    "last_saved": None,
                    "total_meals_logged": 0,
                    "best_streak": 0,
                }
                save_data()
                st.rerun()
        
        st.divider()
        st.info("""
        **Calorie Tracker v1.0** 🍎
        
        ✨ Features:
        - 🎮 Leveling System
        - 📝 Meal Logging
        - 💪 Macro Tracking
        - ⚖️ Weight Tracking
        - 🏆 Achievements
        - 💾 Auto-Save
        - 🎁 Daily Bonus
        """)

st.sidebar.divider()
st.sidebar.write("**Made with 💚 for Nutrition Goals**")
