<<<<<<< HEAD
﻿# 🎓 Smart Study Planner

An intelligent AI-powered study planner that helps students organize their study schedule, manage subjects, and get AI-powered explanations using RAG (Retrieval-Augmented Generation).

## 🚀 Features

- **📅 Smart Study Scheduling**: Generate personalized study plans based on exam dates and priorities
- **📚 Document Management**: Upload and process study materials (PDF, TXT, DOCX)
- **🤖 AI Study Assistant**: Get explanations for topics using RAG with Gemini AI
- **📊 Progress Tracking**: Monitor your study progress and upcoming exams
- **🎯 Priority-based Recommendations**: AI recommends what to study next

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: LangChain, Google Gemini, RAG
- **Database**: SQLite
- **Vector Store**: FAISS
- **Document Processing**: PyPDF, LangChain

## 📦 Installation

1. **Clone the repository**:
\\\ash
git clone https://github.com/your-username/smart-study-planner.git
cd smart-study-planner
\\\

2. **Create virtual environment**:
\\\ash
python -m venv venv
source venv/bin/activate  # On Windows: .\\venv\\Scripts\\Activate.ps1
\\\

3. **Install dependencies**:
\\\ash
pip install -r requirements.txt
\\\

4. **Set up environment variables**:
   - Copy \.env.example\ to \.env\
   - Add your Gemini API key from [Google AI Studio](https://aistudio.google.com/)

5. **Run the application**:
\\\ash
streamlit run app.py
\\\

## 🔧 Configuration

1. Get your free Gemini API key from [Google AI Studio](https://aistudio.google.com/)
2. Add it to the \.env\ file:
\\\
GEMINI_API_KEY=your_api_key_here
\\\

## 📁 Project Structure

\\\
smart-study-planner/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # Project documentation
├── data/                 # Data storage
│   ├── uploaded_docs/    # User uploaded documents
│   └── vector_store/     # FAISS vector indices
├── modules/              # Core application modules
│   ├── database.py       # Database operations
│   ├── rag_pipeline.py   # RAG document processing
│   └── recommender.py    # Study scheduling logic
└── utils/                # Utility functions
    └── helpers.py        # Common helpers
\\\

## 🎯 Usage

1. **Add Subjects**: Go to Study Planner → Manage Subjects to add your courses and exam dates
2. **Upload Materials**: Upload your syllabus, notes, or textbooks in Study Materials
3. **Generate Plan**: Create personalized study schedules based on your availability
4. **Get Help**: Use the Study Assistant for AI-powered explanations of difficult topics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- AI powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- RAG implementation using [LangChain](https://www.langchain.com/)
=======
# smart-study-planner
An AI-powered study planner with RAG and recommendation system
>>>>>>> e9a7a7cae3f6719ce474a443c6bdc8ae227f3aec
