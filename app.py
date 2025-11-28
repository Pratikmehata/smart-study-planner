import streamlit as st
import os
import sqlite3
from datetime import datetime, timedelta
import tempfile
import base64

# Custom CSS for beautiful styling
def load_css():
    return """
    <style>
    /* Main styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header styling */
    .main-header {
        font-size: 3rem;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
    }
    
    /* Card styling */
    .study-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid;
        margin: 1rem 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .study-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }
    
    .card-high {
        border-left-color: #ff6b6b;
        background: linear-gradient(135deg, #fff5f5, #ffffff);
    }
    
    .card-medium {
        border-left-color: #ffa94d;
        background: linear-gradient(135deg, #fff4e6, #ffffff);
    }
    
    .card-low {
        border-left-color: #51cf66;
        background: linear-gradient(135deg, #ebfbee, #ffffff);
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-top: 4px solid;
    }
    
    .metric-1 { border-top-color: #667eea; }
    .metric-2 { border-top-color: #764ba2; }
    .metric-3 { border-top-color: #f093fb; }
    .metric-4 { border-top-color: #f5576c; }
    
    /* Button styling */
    .stButton button {
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(45deg, #667eea, #764ba2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Custom tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f8f9fa;
        border-radius: 10px 10px 0px 0px;
        gap: 1rem;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    
    /* Subject badges */
    .subject-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .badge-easy { background: #d3f9d8; color: #2b8a3e; }
    .badge-medium { background: #fff3bf; color: #e67700; }
    .badge-hard { background: #ffe3e3; color: #c92a2a; }
    </style>
    """

# Simple implementations that work without external modules
class UserDatabase:
    def __init__(self, db_path="data/study_planner.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                exam_date DATE,
                difficulty TEXT,
                color TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def add_subject(self, name, exam_date, difficulty, color):
        try:
            self.conn.execute(
                "INSERT INTO subjects (name, exam_date, difficulty, color) VALUES (?, ?, ?, ?)",
                (name, exam_date, difficulty, color)
            )
            self.conn.commit()
            return True
        except:
            return False
    
    def delete_subject(self, subject_name):
        try:
            self.conn.execute("DELETE FROM subjects WHERE name = ?", (subject_name,))
            self.conn.commit()
            return True
        except:
            return False

class RAGPipeline:
    def __init__(self):
        self.vector_store = None
    
    def process_document(self, file_path, subject):
        return True
    
    def explain_topic(self, topic):
        explanations = {
            "machine learning": "Machine Learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed. It's like teaching computers to recognize patterns and make predictions.",
            "neural networks": "Neural Networks are computing systems inspired by the human brain. They consist of interconnected nodes (neurons) that process information and learn to perform tasks by analyzing examples.",
            "database systems": "Database Systems are organized collections of data that allow efficient storage, retrieval, and manipulation of information. They use structured query language (SQL) for operations.",
            "linear algebra": "Linear Algebra is the branch of mathematics concerning linear equations, linear functions, and their representations through matrices and vector spaces.",
            "calculus": "Calculus is the mathematical study of continuous change, dealing with derivatives (rates of change) and integrals (accumulation of quantities)."
        }
        return explanations.get(topic.lower(), f"This is a comprehensive explanation for '{topic}'. In a full implementation, AI would analyze your study materials to provide personalized insights and examples.")

class StudyRecommender:
    def __init__(self, database):
        self.db = database
    
    def generate_daily_plan(self):
        return [
            {
                "subject": "Machine Learning",
                "topic": "Neural Networks",
                "duration": 90,
                "priority": 0.8,
                "reason": "High priority for upcoming exam"
            },
            {
                "subject": "Database Systems",
                "topic": "SQL Optimization", 
                "duration": 60,
                "priority": 0.6,
                "reason": "Important for practical applications"
            }
        ]

# Helper functions
def init_session_state():
    if 'db' not in st.session_state:
        st.session_state.db = UserDatabase()
    if 'rag' not in st.session_state:
        st.session_state.rag = RAGPipeline()
    if 'recommender' not in st.session_state:
        st.session_state.recommender = StudyRecommender(st.session_state.db)
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            'subjects': [],
            'uploaded_docs': [],
            'today_plan': [],
            'study_preferences': {
                'daily_goal': 4,
                'preferred_times': ['Morning', 'Evening'],
                'break_frequency': '45 min',
                'intensity': 'Moderate'
            }
        }

def format_duration(minutes):
    if minutes < 60:
        return f"{minutes} min"
    else:
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}h {mins}m"

def calculate_days_until(target_date):
    if isinstance(target_date, str):
        try:
            target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
        except:
            return 999
    today = datetime.now().date()
    return (target_date - today).days

def format_date_readable(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_str

def get_subject_color(subject_name):
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
    return colors[hash(subject_name) % len(colors)]

def get_difficulty_badge(difficulty):
    difficulty = difficulty.lower()
    if difficulty in ['easy', 'beginner']:
        return "🟢 Easy"
    elif difficulty in ['medium', 'intermediate']:
        return "🟡 Medium" 
    else:
        return "🔴 Hard"

def display_metric_card(title, value, subtitle, metric_class):
    st.markdown(f"""
    <div class="metric-card {metric_class}">
        <h3 style="margin:0; color: #495057; font-size: 0.9rem;">{title}</h3>
        <h1 style="margin:0; color: #212529; font-size: 2rem; font-weight: 800;">{value}</h1>
        <p style="margin:0; color: #6c757d; font-size: 0.8rem;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def display_study_task(task, task_num):
    priority_class = "card-high" if task['priority'] > 0.7 else "card-medium" if task['priority'] > 0.4 else "card-low"
    
    st.markdown(f"""
    <div class="study-card {priority_class}">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex: 1;">
                <h4 style="margin:0; color: #495057;">{task_num}. {task['subject']} - {task['topic']}</h4>
                <p style="margin:0.5rem 0; color: #6c757d; font-size: 0.9rem;">
                    ⏰ {format_duration(task['duration'])} • 🎯 Priority: {task['priority']:.1f}
                </p>
                <p style="margin:0; color: #868e96; font-size: 0.8rem;">{task.get('reason', '')}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Smart Study Planner",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Main header
    st.markdown('<h1 class="main-header">🎓 Smart Study Planner</h1>', unsafe_allow_html=True)
    
    init_session_state()
    
    # Sidebar navigation with better styling
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: white; margin-bottom: 2rem;">📚</h2>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.radio(
            "Navigate to:",
            ["🏠 Dashboard", "📅 Study Planner", "📚 Study Materials", "❓ Study Assistant", "⚙️ Settings"],
            label_visibility="collapsed"
        )
    
    # Display selected page
    if page == "🏠 Dashboard":
        dashboard_page()
    elif page == "📅 Study Planner":
        study_planner_page()
    elif page == "📚 Study Materials":
        study_materials_page()
    elif page == "❓ Study Assistant":
        study_assistant_page()
    elif page == "⚙️ Settings":
        settings_page()

def dashboard_page():
    st.markdown("## 📊 Study Dashboard")
    
    # Quick stats in beautiful cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        subjects_count = len(st.session_state.user_data['subjects'])
        display_metric_card("SUBJECTS", subjects_count, "Total enrolled", "metric-1")
    
    with col2:
        upcoming = sum(1 for s in st.session_state.user_data['subjects'] if calculate_days_until(s.get('exam_date', '')) <= 30)
        display_metric_card("UPCOMING EXAMS", upcoming, "Next 30 days", "metric-2")
    
    with col3:
        total_time = sum(t.get('duration', 0) for t in st.session_state.user_data['today_plan'])
        display_metric_card("TODAY'S STUDY", format_duration(total_time), "Planned time", "metric-3")
    
    with col4:
        docs_count = len(st.session_state.user_data['uploaded_docs'])
        display_metric_card("DOCUMENTS", docs_count, "Uploaded files", "metric-4")
    
    st.markdown("---")
    
    # Quick actions and upcoming exams
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🚀 Quick Actions")
        
        action_col1, action_col2 = st.columns(2)
        with action_col1:
            if st.button("🔄 Generate Plan", use_container_width=True, type="primary"):
                plan = st.session_state.recommender.generate_daily_plan()
                st.session_state.user_data['today_plan'] = plan
                st.success("✨ Study plan generated successfully!")
                
        with action_col2:
            if st.button("📖 Study Now", use_container_width=True):
                st.rerun()
        
        if st.button("📚 Upload Materials", use_container_width=True):
            st.rerun()
    
    with col2:
        st.markdown("### 📅 Upcoming Exams")
        upcoming = []
        for subject in st.session_state.user_data['subjects']:
            days = calculate_days_until(subject.get('exam_date', ''))
            if days <= 30:
                upcoming.append((subject['name'], days, subject.get('difficulty', 'Medium')))
        
        if upcoming:
            for name, days, difficulty in sorted(upcoming, key=lambda x: x[1]):
                badge = get_difficulty_badge(difficulty)
                st.write(f"**{name}** - {days} days {badge}")
        else:
            st.info("🎉 No upcoming exams in the next 30 days!")
    
    # Today's study plan
    st.markdown("### 📖 Today's Study Plan")
    if st.session_state.user_data['today_plan']:
        for i, task in enumerate(st.session_state.user_data['today_plan'], 1):
            display_study_task(task, i)
            
            # Action buttons for each task
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col2:
                if st.button("📝 Study", key=f"study_{i}", use_container_width=True):
                    st.info(f"Starting study session: {task['topic']}")
            with col3:
                if st.button("❓ Explain", key=f"explain_{i}", use_container_width=True):
                    st.session_state.current_topic = task['topic']
                    st.session_state.current_explanation = st.session_state.rag.explain_topic(task['topic'])
            with col4:
                if st.button("✅ Complete", key=f"complete_{i}", use_container_width=True):
                    st.success(f"Great job completing: {task['topic']}!")
            st.markdown("---")
    else:
        st.info("🌟 No study plan generated yet. Click 'Generate Plan' to get started!")

def study_planner_page():
    st.markdown("## 📅 Study Planner")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Generate Plan", "📝 Manage Subjects", "📊 Progress"])
    
    with tab1:
        st.markdown("### Create Your Study Plan")
        
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                available_hours = st.slider(
                    "🕐 Available study hours today:",
                    min_value=1, max_value=8, value=4,
                    help="How many hours can you dedicate to studying today?"
                )
                
                focus_subject = st.selectbox(
                    "🎯 Focus on subject:",
                    options=["All subjects"] + [s['name'] for s in st.session_state.user_data['subjects']],
                    help="Choose a specific subject or study all subjects"
                )
            
            with col2:
                study_intensity = st.select_slider(
                    "💪 Study intensity:",
                    options=["Light", "Moderate", "Intensive"],
                    value="Moderate",
                    help="Light: More breaks | Moderate: Balanced | Intensive: Focused deep work"
                )
                
                include_review = st.checkbox("🔄 Include review sessions", value=True)
                include_breaks = st.checkbox("☕ Include break times", value=True)
        
        if st.button("🚀 Generate Smart Plan", type="primary", use_container_width=True):
            if st.session_state.user_data['subjects']:
                with st.spinner("🎯 Generating your personalized study plan..."):
                    plan = []
                    for subject in st.session_state.user_data['subjects']:
                        if focus_subject != "All subjects" and subject['name'] != focus_subject:
                            continue
                        for topic in subject.get('topics', [])[:2]:
                            plan.append({
                                'subject': subject['name'],
                                'topic': topic,
                                'duration': 60,
                                'priority': 0.7,
                                'reason': f"Upcoming exam in {calculate_days_until(subject['exam_date'])} days"
                            })
                    st.session_state.user_data['today_plan'] = plan
                    st.success("✅ Study plan generated successfully!")
                    st.balloons()
            else:
                st.error("❌ Please add subjects first in the 'Manage Subjects' tab!")
    
    with tab2:
        st.markdown("### Manage Your Subjects")
        
        with st.form("add_subject_form", border=True):
            st.markdown("#### ➕ Add New Subject")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                subject_name = st.text_input(
                    "📚 Subject Name*",
                    placeholder="e.g., Machine Learning",
                    help="Enter the name of your subject"
                )
            
            with col2:
                exam_date = st.date_input(
                    "📅 Exam Date*",
                    min_value=datetime.now().date(),
                    help="When is your exam for this subject?"
                )
            
            with col3:
                difficulty = st.selectbox(
                    "🎯 Difficulty Level",
                    ["Beginner", "Intermediate", "Advanced"],
                    help="How challenging is this subject for you?"
                )
            
            # Topics input
            topics_input = st.text_area(
                "📖 Topics to Study",
                placeholder="Linear Regression, Neural Networks, Decision Trees...",
                help="Enter topics separated by commas",
                height=80
            )
            
            submitted = st.form_submit_button(
                "➕ Add Subject", 
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                if subject_name:
                    color = get_subject_color(subject_name)
                    new_subject = {
                        'name': subject_name,
                        'exam_date': exam_date.strftime('%Y-%m-%d'),
                        'difficulty': difficulty,
                        'color': color,
                        'topics': [t.strip() for t in topics_input.split(',') if t.strip()],
                        'added_date': datetime.now().strftime('%Y-%m-%d')
                    }
                    
                    success = st.session_state.db.add_subject(
                        subject_name, 
                        exam_date.strftime('%Y-%m-%d'), 
                        difficulty,
                        color
                    )
                    
                    if success:
                        st.session_state.user_data['subjects'].append(new_subject)
                        st.success(f"✅ Subject '{subject_name}' added successfully!")
                    else:
                        st.error("❌ Failed to add subject to database.")
                else:
                    st.error("❌ Please enter a subject name")
        
        # Display current subjects
        st.markdown("### 📚 Your Subjects")
        if st.session_state.user_data['subjects']:
            for i, subject in enumerate(st.session_state.user_data['subjects']):
                with st.expander(
                    f"📘 {subject['name']} - Exam: {format_date_readable(subject['exam_date'])} {get_difficulty_badge(subject['difficulty'])}",
                    expanded=False
                ):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        days_until = calculate_days_until(subject['exam_date'])
                        st.write(f"**Days until exam:** {days_until}")
                        
                        if subject.get('topics'):
                            st.write("**Topics to study:**")
                            for topic in subject['topics']:
                                st.write(f"• {topic}")
                    
                    with col2:
                        progress = st.slider(
                            "Progress",
                            min_value=0, max_value=100, value=0,
                            key=f"progress_{i}",
                            label_visibility="collapsed"
                        )
                        st.write(f"**Progress:** {progress}%")
                        
                        if st.button("🗑️ Delete", key=f"delete_{i}", use_container_width=True):
                            st.session_state.db.delete_subject(subject['name'])
                            st.session_state.user_data['subjects'].pop(i)
                            st.rerun()
        else:
            st.info("📝 No subjects added yet. Add your first subject above!")
    
    with tab3:
        st.markdown("### 📊 Study Progress")
        
        if st.session_state.user_data['subjects']:
            for subject in st.session_state.user_data['subjects']:
                days_until = calculate_days_until(subject['exam_date'])
                progress = max(0, min(100, 100 - (days_until / 30 * 100)))
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{subject['name']}**")
                    st.progress(progress / 100)
                with col2:
                    st.write(f"{days_until} days left")
        else:
            st.info("📈 Add subjects to track your progress!")

def study_materials_page():
    st.markdown("## 📚 Study Materials")
    
    tab1, tab2 = st.tabs(["📤 Upload Documents", "📂 Your Documents"])
    
    with tab1:
        st.markdown("### Upload Study Materials")
        
        st.info("""
        📖 **Upload your study materials** to enable smart topic explanations and better study recommendations.
        Supported formats: PDF, TXT, DOCX
        """)
        
        uploaded_file = st.file_uploader(
            "Choose a document",
            type=['pdf', 'txt', 'docx'],
            help="Upload your syllabus, notes, or textbook chapters"
        )
        
        if uploaded_file is not None:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**File:** {uploaded_file.name}")
            with col2:
                file_size = uploaded_file.size / 1024 / 1024
                st.write(f"**Size:** {file_size:.2f} MB")
            with col3:
                st.write(f"**Type:** {uploaded_file.type}")
            
            if st.button("📥 Process Document", type="primary", use_container_width=True):
                with st.spinner("🔄 Processing your document..."):
                    try:
                        file_path = save_uploaded_file(uploaded_file)
                        st.session_state.rag.process_document(file_path, "General")
                        st.session_state.user_data['uploaded_docs'].append({
                            'name': uploaded_file.name,
                            'path': file_path,
                            'upload_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                            'size': f"{file_size:.2f} MB"
                        })
                        st.success("✅ Document processed successfully!")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    with tab2:
        st.markdown("### Your Documents")
        
        if st.session_state.user_data['uploaded_docs']:
            for i, doc in enumerate(st.session_state.user_data['uploaded_docs']):
                with st.expander(f"📄 {doc['name']}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Uploaded:** {doc['upload_date']}")
                        st.write(f"**Size:** {doc['size']}")
                    with col2:
                        if st.button("🗑️ Remove", key=f"remove_{i}", use_container_width=True):
                            if os.path.exists(doc['path']):
                                os.remove(doc['path'])
                            st.session_state.user_data['uploaded_docs'].pop(i)
                            st.rerun()
        else:
            st.info("📭 No documents uploaded yet.")

def study_assistant_page():
    st.markdown("## ❓ Study Assistant")
    
    st.info("""
    🎓 **Ask questions about your study topics!** 
    The assistant will help you understand concepts and provide detailed explanations.
    """)
    
    # Quick topic buttons
    st.markdown("### 📚 Quick Explanations")
    
    # Get all unique topics
    all_topics = set()
    for subject in st.session_state.user_data.get('subjects', []):
        all_topics.update(subject.get('topics', []))
    
    if all_topics:
        cols = st.columns(4)
        topics_list = list(all_topics)[:8]  # Show first 8 topics
        for i, topic in enumerate(topics_list):
            with cols[i % 4]:
                if st.button(f"📖 {topic}", key=f"quick_{i}", use_container_width=True):
                    st.session_state.current_topic = topic
    
    # Manual topic input
    st.markdown("### 💬 Ask About Any Topic")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        topic_query = st.text_input(
            "Enter a topic:",
            placeholder="e.g., Neural Networks, SQL Optimization, Calculus...",
            value=st.session_state.get('current_topic', ''),
            label_visibility="collapsed"
        )
    with col2:
        explanation_depth = st.selectbox(
            "Depth:",
            ["Simple", "Detailed", "Comprehensive"],
            label_visibility="collapsed"
        )
    
    if st.button("🎓 Get Explanation", type="primary", use_container_width=True) and topic_query:
        with st.spinner(f"🔍 Researching '{topic_query}'..."):
            explanation = st.session_state.rag.explain_topic(topic_query)
            st.session_state.current_explanation = explanation
            st.session_state.current_topic = topic_query
    
    # Display explanation
    if st.session_state.get('current_explanation'):
        st.markdown("---")
        st.markdown(f"### 📖 Explanation: {st.session_state.get('current_topic', 'Topic')}")
        
        st.markdown(st.session_state.current_explanation)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📝 Add to Study Plan", use_container_width=True):
                st.success(f"Added '{st.session_state.current_topic}' to study plan!")
        with col2:
            if st.button("💾 Save Explanation", use_container_width=True):
                st.success("Explanation saved!")
        with col3:
            if st.button("🔄 New Question", use_container_width=True):
                st.session_state.current_explanation = None
                st.session_state.current_topic = ""
                st.rerun()

def settings_page():
    st.markdown("## ⚙️ Settings")
    
    tab1, tab2, tab3 = st.tabs(["Preferences", "Account", "About"])
    
    with tab1:
        st.markdown("### 🎯 Study Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            daily_goal = st.number_input(
                "Daily study goal (hours):",
                min_value=1, max_value=12, value=4,
                help="Your target study time per day"
            )
            
            preferred_study_times = st.multiselect(
                "Preferred study times:",
                ["🌅 Morning (6AM-12PM)", "🌞 Afternoon (12PM-6PM)", "🌇 Evening (6PM-10PM)", "🌙 Night (10PM-2AM)"],
                default=["🌅 Morning (6AM-12PM)", "🌇 Evening (6PM-10PM)"],
                help="When do you prefer to study?"
            )
        
        with col2:
            break_frequency = st.select_slider(
                "Break frequency:",
                options=["25 min", "45 min", "60 min", "90 min"],
                value="45 min",
                help="How long between breaks? (Pomodoro technique)"
            )
            
            study_intensity = st.select_slider(
                "Study intensity:",
                options=["Light 🐢", "Moderate 🚶", "Intensive 🏃"],
                value="Moderate 🚶"
            )
        
        if st.button("💾 Save Preferences", type="primary"):
            st.session_state.user_data['study_preferences'] = {
                'daily_goal': daily_goal,
                'preferred_times': preferred_study_times,
                'break_frequency': break_frequency,
                'intensity': study_intensity
            }
            st.success("✅ Preferences saved successfully!")
    
    with tab2:
        st.markdown("### 👤 Account Settings")
        st.info("🔄 Account features coming in future updates!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Name", value="Student", disabled=True)
        with col2:
            st.text_input("Email", value="student@example.com", disabled=True)
    
    with tab3:
        st.markdown("### ℹ️ About Smart Study Planner")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white;">
        <h3 style="color: white; text-align: center;">🎓 Smart Study Planner</h3>
        <p style="text-align: center; color: white;">Your intelligent study companion</p>
        </div>
        
        ### 🚀 What is Smart Study Planner?
        
        An AI-powered study assistant that helps you:
        
        - **📅 Plan** your study schedule based on exam dates and priorities
        - **🎯 Understand** topics using intelligent explanations
        - **📊 Track** your progress and adapt to your learning style
        - **📚 Organize** your study materials effectively
        
        ### 🛠️ How it Works
        
        1. **Add subjects** and exam dates
        2. **Upload study materials** (PDFs, notes, textbooks)
        3. **Generate smart study plans** based on urgency
        4. **Get AI-powered explanations** for difficult topics
        5. **Track progress** and adjust as needed
        
        ### 💫 Features
        
        - Beautiful, intuitive interface
        - Smart study recommendations
        - Progress tracking
        - Document management
        - AI-powered explanations
        
        <div style="text-align: center; margin-top: 2rem;">
            <p>Built with ❤️ using Streamlit, Python, and AI</p>
        </div>
        """, unsafe_allow_html=True)

def save_uploaded_file(uploaded_file):
    os.makedirs("data/uploaded_docs", exist_ok=True)
    file_path = os.path.join("data/uploaded_docs", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

if __name__ == "__main__":
    main()