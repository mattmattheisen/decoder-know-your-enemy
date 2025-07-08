import streamlit as st
import pandas as pd
import numpy as np
import re
from datetime import datetime
import base64
from io import BytesIO
import json

# Page configuration
st.set_page_config(
    page_title="Know Your Enemy | Decoder Universe",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling (matching existing Decoder apps)
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .alert-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sales training book database
TRAINING_BOOKS = {
    "customer_centered_selling": {
        "title": "Customer Centered Selling",
        "author": "Robert Miller & Stephen Heiman",
        "status": "EXPOSED",
        "description": "Mandatory reading at major financial firms. Learn the exact manipulation tactics disguised as 'customer care.'",
        "tactics": [
            "The 'Pain Funnel' - Exploiting Customer Fears",
            "Objection Reframing - Turning 'No' into 'Maybe'",
            "The Assumptive Close - Acting Like You've Already Decided",
            "Creating False Scarcity - 'This Offer Expires Today'"
        ],
        "insider_quote": "This was mandatory reading at major financial firms. Advisors have to role-play these techniques for weeks. What they call 'customer-centered' is actually sales-centered with a friendly mask."
    },
    "spin_selling": {
        "title": "SPIN Selling",
        "author": "Neil Rackham",
        "status": "COMING SOON",
        "description": "The questioning technique that makes you feel like the salesperson really cares about your needs. Spoiler: they're just following the SPIN formula.",
        "tactics": [
            "The SPIN questioning sequence",
            "How to make customers sell themselves", 
            "Implied vs. explicit needs manipulation"
        ]
    },
    "challenger_sale": {
        "title": "The Challenger Sale",
        "author": "Matthew Dixon & Brent Adamson",
        "status": "COMING SOON",
        "description": "Teaches salespeople to 'challenge' your thinking and position themselves as the expert who knows better than you do.",
        "tactics": [
            "The 'insight' that's really a sales pitch",
            "How to reframe your priorities",
            "Creating constructive tension"
        ]
    },
    "influence": {
        "title": "Influence: The Psychology of Persuasion",
        "author": "Robert Cialdini",
        "status": "COMING SOON", 
        "description": "The psychological principles that every sales training program references. Good science, questionable application.",
        "tactics": [
            "Weaponized reciprocity",
            "False social proof",
            "Authority manipulation",
            "Artificial scarcity"
        ]
    }
}

# Script examples from actual training
ACTUAL_SCRIPTS = {
    "pain_discovery": [
        "What keeps you up at night about your retirement?",
        "How would you feel if you outlived your money?",
        "What's your biggest financial regret?",
        "What would happen if you couldn't work tomorrow?"
    ],
    "objection_handling": [
        "When you say it's too expensive, help me understand what that means to you...",
        "I hear you saying you want to think about it. What specifically do you need to think about?",
        "Many of my clients felt the same way initially. What they found was...",
        "Let me ask you this: if I could address that concern, would you move forward today?"
    ],
    "false_urgency": [
        "This rate is only guaranteed until market close today...",
        "I can only offer this if you decide today...",
        "Other clients who waited wished they hadn't...",
        "This opportunity won't be available next week..."
    ],
    "assumptive_close": [
        "When we set up your account next week...",
        "After we get this started for you...",
        "Once you're enrolled in this program...",
        "I'll need your signature here to begin..."
    ]
}

def main():
    st.markdown('<h1 class="main-header">🎯 Know Your Enemy</h1>', unsafe_allow_html=True)
    st.markdown("**Exposing the sales training playbooks used against everyday consumers**")
    
    # Sidebar navigation with session state
    st.sidebar.title("Navigation")
    
    # Initialize session state for page navigation
    if 'page' not in st.session_state:
        st.session_state.page = "🏠 Overview"
    
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["🏠 Overview", "📖 Customer Centered Selling", "📚 Book Pipeline", "🎭 Script Database", "🕵️ Submit Intel", "🧠 Training Techniques"],
        index=["🏠 Overview", "📖 Customer Centered Selling", "📚 Book Pipeline", "🎭 Script Database", "🕵️ Submit Intel", "🧠 Training Techniques"].index(st.session_state.page) if st.session_state.page in ["🏠 Overview", "📖 Customer Centered Selling", "📚 Book Pipeline", "🎭 Script Database", "🕵️ Submit Intel", "🧠 Training Techniques"] else 0
    )
    
    # Update session state when sidebar selection changes
    st.session_state.page = page
    
    if page == "🏠 Overview":
        overview_page()
    elif page == "📖 Customer Centered Selling":
        customer_centered_selling_page()
    elif page == "📚 Book Pipeline":
        book_pipeline_page()
    elif page == "🎭 Script Database":
        script_database_page()
    elif page == "🕵️ Submit Intel":
        submit_intel_page()
    elif page == "🧠 Training Techniques":
        training_techniques_page()

def overview_page():
    # Hero section matching Advisor Decoder style
    st.markdown("""
    <div style="background: linear-gradient(135deg, #c0392b 0%, #8b1e1e 100%); 
                padding: 3rem 2rem; 
                border-radius: 10px; 
                text-align: center; 
                margin-bottom: 2rem;">
        <h1 style="color: white; font-size: 3rem; margin-bottom: 1rem; font-weight: bold;">
            🎯 Know Your Enemy
        </h1>
        <h2 style="color: #f0f8ff; font-size: 1.4rem; margin-bottom: 0.5rem; font-weight: normal;">
            Exposing the sales training playbooks used against consumers
        </h2>
        <p style="color: #e6f3ff; font-size: 1.1rem; font-style: italic; margin: 0;">
            "Don't Get Sold - Get Decoded"
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content in two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style="background: #fff3cd; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #ffc107;">
            <h3 style="color: #856404; margin-top: 0;">📚 The Hidden Training Library</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("**The scripts aren't accidental.** Companies spend millions training sales teams using specific books and psychological techniques:")
        
        training_facts = [
            "**Mandatory role-playing** for weeks after reading sales books",
            "**Pre-fabricated scripts** designed to handle every objection",
            "**Psychological manipulation** techniques disguised as 'customer care'",
            "**McDonald's-style training** - anyone can follow the playbook",
            "**Revenue-based compensation** that biases every recommendation",
            "**Ongoing coaching** to perfect manipulation techniques"
        ]
        
        for fact in training_facts:
            st.markdown(f"• {fact}")
    
    with col2:
        st.markdown("""
        <div style="background: #d1ecf1; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #17a2b8;">
            <h3 style="color: #0c5460; margin-top: 0;">🛡️ Your Intelligence Advantage</h3>
        </div>
        """, unsafe_allow_html=True)
        
        intelligence_features = [
            ("📖 **Book Exposés**", "Chapter-by-chapter breakdowns of actual training materials"),
            ("🎭 **Script Database**", "Real phrases and responses taught to salespeople"),
            ("🧠 **Technique Analysis**", "Psychological methods used to influence decisions"),
            ("🕵️ **Intel Collection**", "Submit sales tactics you've encountered"),
            ("🚨 **Red Flag Alerts**", "Warning signs of manipulation in progress"),
            ("📋 **Counter-Scripts**", "What to say when they use these tactics")
        ]
        
        for icon_title, description in intelligence_features:
            st.markdown(f"**{icon_title}** - {description}")
    

    
    # Quick action buttons
    st.subheader("🚀 Start Your Intelligence Briefing")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📖 Read First Exposé", use_container_width=True):
            st.session_state.page = "📖 Customer Centered Selling"
            st.rerun()
    
    with col2:
        if st.button("🎭 See Real Scripts", use_container_width=True):
            st.session_state.page = "🎭 Script Database"
            st.rerun()
    
    with col3:
        if st.button("🕵️ Submit Intel", use_container_width=True):
            st.session_state.page = "🕵️ Submit Intel"
            st.rerun()
    
    # Statistics section
    st.write("---")
    st.subheader("📊 Intelligence Database Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Training Books Analyzed", "4", "1 Complete")
    with col2:
        st.metric("Manipulation Tactics Exposed", "25+", "Growing")
    with col3:
        st.metric("Years Inside the Industry", "3", "Major Firms")
    with col4:
        st.metric("Scripts Memorized", "Dozens", "😤")
    
    # Featured exposure preview
    st.subheader("🚨 Latest Intelligence")
    
    book = TRAINING_BOOKS["customer_centered_selling"]
    
    st.markdown(f"""
    <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1.5rem; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <span style="background: #e74c3c; color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.8rem; font-weight: bold;">
            {book['status']}
        </span>
        <h3 style="margin: 1rem 0 0.5rem 0;">{book['title']}</h3>
        <p><strong>Author:</strong> {book['author']}</p>
        <p>{book['description']}</p>
        <div style="background: #ffe6e6; border-left: 4px solid #c0392b; padding: 1rem; margin: 1rem 0; border-radius: 5px;">
            <h4 style="margin-top: 0; color: #c0392b;">Key Tactics Exposed:</h4>
            <ul style="margin: 0;">
                {"".join([f"<li>{tactic}</li>" for tactic in book['tactics']])}
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem;">
        <p>Know Your Enemy v1.0 | Built from real sales training materials</p>
        <p><em>Disclaimer: This content is for educational purposes only. All information based on actual training materials from major firms.</em></p>
    </div>
    """, unsafe_allow_html=True)

def customer_centered_selling_page():
    book = TRAINING_BOOKS["customer_centered_selling"]
    
    # Status badge
    st.markdown(f'''
    <span style="background: #e74c3c; color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.8rem; font-weight: bold; display: inline-block; margin-bottom: 1rem;">
        {book['status']}
    </span>
    ''', unsafe_allow_html=True)
    
    st.title(book['title'])
    st.subheader(f"by {book['author']}")
    
    # Insider quote
    st.markdown(f'''
    <div style="background: #f8f9fa; border-left: 4px solid #34495e; padding: 1rem; margin: 1rem 0; font-style: italic; border-radius: 5px;">
        "{book['insider_quote']}"
        <br><strong>— Former Financial Advisor</strong>
    </div>
    ''', unsafe_allow_html=True)
    
    # Book overview
    st.markdown("### What This Book Really Teaches")
    st.write("""
    Despite the name, this book isn't about helping customers—it's about controlling conversations 
    to maximize sales. Every major financial firm uses these techniques because they work. 
    Here's what your advisor learned:
    """)
    
    # Tactics breakdown using tabs
    st.markdown("### 🎭 Key Manipulation Tactics")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Pain Funnel", "🔄 Objection Reframing", "✅ Assumptive Close", "⏰ False Scarcity"])
    
    with tab1:
        st.write("**What they teach:** Ask probing questions to identify customer pain points.")
        st.write("**The reality:** Create anxiety about problems that may not even exist, then position your product as the only solution.")
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.write("**Script examples from training:**")
        for script in ACTUAL_SCRIPTS["pain_discovery"]:
            st.write(f"• \"{script}\"")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("**Your defense:** Ask yourself - was I worried about this before they brought it up?")
    
    with tab2:
        st.write("**What they teach:** Never accept objections at face value. Always dig deeper.")
        st.write("**The reality:** Wear down resistance until you give up or give in.")
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.write("**Script examples from training:**")
        for script in ACTUAL_SCRIPTS["objection_handling"]:
            st.write(f"• \"{script}\"")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("**Your defense:** Your 'no' is complete. You don't owe them an explanation.")
    
    with tab3:
        st.write("**What they teach:** Assume the sale and start talking about implementation.")
        st.write("**The reality:** Psychological pressure to go along with what seems already decided.")
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.write("**Script examples from training:**")
        for script in ACTUAL_SCRIPTS["assumptive_close"]:
            st.write(f"• \"{script}\"")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("**Your defense:** Stop them immediately - 'Hold on, I haven't decided anything yet.'")
    
    with tab4:
        st.write("**What they teach:** Create urgency to prevent 'think it over' responses.")
        st.write("**The reality:** Manufactured deadlines that often don't really exist.")
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.write("**Script examples from training:**")
        for script in ACTUAL_SCRIPTS["false_urgency"]:
            st.write(f"• \"{script}\"")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("**Your defense:** Good investments don't disappear overnight. Take time to research.")
    
    # Chapter breakdown section
    st.markdown("### 📖 Chapter-by-Chapter Intelligence")
    
    chapter_tab1, chapter_tab2, chapter_tab3 = st.tabs(["Chapters 1-3", "Chapters 4-6", "Coming Soon"])
    
    with chapter_tab1:
        st.markdown("#### Chapter 1: The Sales Funnel Illusion")
        st.write("**What they teach:** How to control the entire conversation flow from first contact to close.")
        st.write("**The reality:** A systematic process to manipulate your decision-making.")
        
        st.markdown("#### Chapter 2: Pain Discovery Techniques")
        st.write("**What they teach:** The systematic process for finding and amplifying customer fears.")
        st.write("**The reality:** Creating problems to sell solutions.")
        
        st.markdown("#### Chapter 3: Solution Positioning")
        st.write("**What they teach:** Making their product seem like the only logical choice.")
        st.write("**The reality:** Ignoring alternatives that might be better for you.")
    
    with chapter_tab2:
        st.write("📚 **Deep dive analysis in progress...**")
        st.write("Currently re-reading these chapters with fresh (decoded) eyes.")
        st.write("Focus areas:")
        st.write("• Advanced objection handling techniques")
        st.write("• Emotional manipulation strategies")
        st.write("• Closing technique variations")
    
    with chapter_tab3:
        st.write("🔄 **Full book breakdown coming soon...**")
        st.write("The complete playbook exposure is in development.")
        
        progress_bar = st.progress(0.3)
        st.write("Progress: 30% complete")
    
    # Counter-intelligence section
    st.markdown("### 🛡️ Your Counter-Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**When they use Pain Funnel tactics:**")
        st.write("• Ask: 'Why are you asking me this?'")
        st.write("• Say: 'I'll evaluate my own concerns.'")
        st.write("• Remember: They're creating urgency, not helping.")
    
    with col2:
        st.write("**When they use Assumptive Close:**")
        st.write("• Stop them: 'I haven't decided anything.'")
        st.write("• Ask: 'What's the rush?'")
        st.write("• Take control: 'I'll let you know when I'm ready.'")
    
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.write("**💡 Remember:** Knowledge is your best defense. Now that you know their playbook, you can stay in control.")
    st.markdown('</div>', unsafe_allow_html=True)

def book_pipeline_page():
    st.header("📚 Intelligence Pipeline")
    st.write("These are the next sales training books I'll be exposing:")
    
    # Filter options
    status_filter = st.selectbox("Filter by status:", ["All", "EXPOSED", "COMING SOON"])
    
    # Filter books based on selection
    if status_filter == "All":
        filtered_books = TRAINING_BOOKS
    else:
        filtered_books = {k: v for k, v in TRAINING_BOOKS.items() if v['status'] == status_filter}
    
    # Display books
    for book_id, book in filtered_books.items():
        # Determine badge style
        if book['status'] == "EXPOSED":
            badge_style = "background: #e74c3c; color: white;"
        else:
            badge_style = "background: #95a5a6; color: white;"
        
        st.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1.5rem; margin: 1rem 0; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <span style="{badge_style} padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.8rem; font-weight: bold;">
                {book['status']}
            </span>
            <h3 style="margin: 1rem 0 0.5rem 0;">{book['title']}</h3>
            <p><strong>Author:</strong> {book['author']}</p>
            <p>{book['description']}</p>
            <div style="background: #ffe6e6; border-left: 4px solid #c0392b; padding: 1rem; margin: 1rem 0; border-radius: 5px;">
                <h4 style="margin-top: 0; color: #c0392b;">🚨 Tactics We'll Expose:</h4>
                <ul style="margin: 0;">
                    {"".join([f"<li>⚠️ {tactic}</li>" for tactic in book['tactics']])}
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Submission for new books
    st.write("---")
    st.subheader("📖 Suggest a Book for Analysis")
    
    with st.form("suggest_book"):
        col1, col2 = st.columns(2)
        
        with col1:
            suggested_title = st.text_input("Book Title")
            suggested_author = st.text_input("Author")
        
        with col2:
            industry = st.selectbox("Industry", ["Financial Services", "Insurance", "Real Estate", "Automotive", "Other"])
            urgency = st.selectbox("Priority Level", ["High - Widely Used", "Medium - Common", "Low - Niche"])
        
        why_important = st.text_area("Why should this book be analyzed?", height=100)
        
        submit_suggestion = st.form_submit_button("📚 Submit Book Suggestion")
        
        if submit_suggestion:
            st.success("Book suggestion received! Thank you for helping build the intelligence database.")

def script_database_page():
    st.header("🎭 Script Database")
    st.write("**Real phrases and responses** taught to salespeople in training programs.")
    
    # Search functionality
    search_term = st.text_input("Search scripts:", placeholder="Enter a phrase or topic...")
    
    # Script categories
    script_category = st.selectbox("Category:", ["All", "Pain Discovery", "Objection Handling", "False Urgency", "Assumptive Close"])
    
    # Filter scripts based on category
    if script_category == "All":
        display_scripts = ACTUAL_SCRIPTS
    else:
        category_map = {
            "Pain Discovery": "pain_discovery",
            "Objection Handling": "objection_handling", 
            "False Urgency": "false_urgency",
            "Assumptive Close": "assumptive_close"
        }
        display_scripts = {category_map[script_category]: ACTUAL_SCRIPTS[category_map[script_category]]}
    
    # Display scripts
    for category, scripts in display_scripts.items():
        category_title = category.replace("_", " ").title()
        
        with st.expander(f"🎭 {category_title} Scripts"):
            for script in scripts:
                if not search_term or search_term.lower() in script.lower():
                    st.markdown(f"""
                    <div style="background: #f8f9fa; border-left: 4px solid #c0392b; padding: 1rem; margin: 0.5rem 0; border-radius: 5px;">
                        <strong>Script:</strong> "{script}"<br>
                        <strong>Purpose:</strong> {get_script_purpose(script)}<br>
                        <strong>Your Response:</strong> {get_counter_script(script)}
                    </div>
                    """, unsafe_allow_html=True)
    
    # Add new script section
    st.write("---")
    st.subheader("🎯 Submit a Script You've Heard")
    
    with st.form("submit_script"):
        heard_script = st.text_area("What exact phrase did you hear?", height=80)
        script_context = st.selectbox("When did they use this?", 
                                    ["First meeting", "When I objected", "During close", "Follow-up call", "Other"])
        script_effect = st.text_area("How did it make you feel? What was their goal?", height=80)
        
        submit_script = st.form_submit_button("🎭 Submit Script")
        
        if submit_script:
            st.success("Script submitted! This will help other consumers recognize these tactics.")

def get_script_purpose(script):
    """Return the purpose of a given script"""
    purpose_map = {
        "What keeps you up at night": "Create anxiety about retirement",
        "How would you feel if you outlived": "Fear-based motivation",
        "What's your biggest financial regret": "Find emotional triggers",
        "When you say it's too expensive": "Overcome price objections",
        "I hear you saying you want to think": "Prevent delay tactics",
        "This rate is only guaranteed": "Create artificial urgency",
        "When we set up your account": "Assume the sale is done"
    }
    
    for key, purpose in purpose_map.items():
        if key.lower() in script.lower():
            return purpose
    return "Manipulate decision-making"

def get_counter_script(script):
    """Return suggested response to a script"""
    counter_map = {
        "What keeps you up at night": "I'll share my concerns when I'm ready.",
        "How would you feel if you outlived": "Let's focus on facts, not fears.",
        "What's your biggest financial regret": "That's personal. Let's discuss your services.",
        "When you say it's too expensive": "Price is important to me. What are my alternatives?",
        "I hear you saying you want to think": "Yes, I need time to research independently.",
        "This rate is only guaranteed": "I don't make financial decisions under pressure.",
        "When we set up your account": "Stop. I haven't agreed to anything yet."
    }
    
    for key, counter in counter_map.items():
        if key.lower() in script.lower():
            return f'"{counter}"'
    return '"I need to think about this independently."'

def submit_intel_page():
    st.header("🕵️ Submit Sales Training Intel")
    st.write("Have you encountered sales training materials, scripts, or tactics that should be exposed? Share your intelligence here.")
    
    # Intel submission form
    intel_type = st.selectbox("What type of intelligence are you submitting?", 
                             ["Sales Training Book/Material", "Actual Script Used", "Training Program Info", "Company Policy", "Other"])
    
    if intel_type == "Sales Training Book/Material":
        with st.form("book_intel"):
            st.subheader("📖 Training Material Intelligence")
            
            col1, col2 = st.columns(2)
            
            with col1:
                book_title = st.text_input("Book/Material Title")
                author_company = st.text_input("Author/Company")
                industry = st.selectbox("Industry", ["Financial Services", "Insurance", "Real Estate", "Automotive", "Retail", "Other"])
            
            with col2:
                your_role = st.text_input("Your Role/Experience (optional)")
                company_used = st.text_input("Company That Used This (optional)")
                year_encountered = st.number_input("Year Encountered", min_value=2000, max_value=2025, value=2024)
            
            tactics_observed = st.text_area("What specific tactics or techniques were taught?", height=100)
            red_flags = st.text_area("What red flags should consumers watch for?", height=100)
            additional_context = st.text_area("Additional context or insider information", height=100)
            
            submit_book_intel = st.form_submit_button("🎯 Submit Training Material Intel")
            
            if submit_book_intel:
                st.success("Intelligence received! This will help expose these tactics to protect other consumers.")
                st.balloons()
    
    elif intel_type == "Actual Script Used":
        with st.form("script_intel"):
            st.subheader("🎭 Script Intelligence")
            
            actual_script = st.text_area("What was the exact phrase or script?", height=80)
            situation = st.selectbox("When was this used?", 
                                   ["First meeting", "When I said no", "During sales pitch", "Follow-up call", "Closing attempt"])
            
            col1, col2 = st.columns(2)
            with col1:
                salesperson_type = st.selectbox("Type of salesperson", ["Financial Advisor", "Insurance Agent", "Car Salesman", "Real Estate Agent", "Other"])
                company = st.text_input("Company (optional)")
            
            with col2:
                effectiveness = st.selectbox("How effective was it?", ["Very manipulative", "Somewhat effective", "I saw through it", "Backfired"])
                your_response = st.text_area("How did you respond?", height=60)
            
            submit_script_intel = st.form_submit_button("🎭 Submit Script Intel")
            
            if submit_script_intel:
                st.success("Script intelligence received! This helps build our defense database.")
    
    # Display recent intel stats
    st.write("---")
    st.subheader("📊 Intelligence Database Growth")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Books Identified", "47", "+3 this month")
    with col2:
        st.metric("Scripts Documented", "156", "+12 this month")
    with col3:
        st.metric("Companies Exposed", "23", "+2 this month")
    with col4:
        st.metric("Contributors", "89", "+7 this month")
    
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.write("**🎯 Your Intelligence Matters**")
    st.write("• Every submission helps protect other consumers")
    st.write("• All intel is verified before publication")
    st.write("• Contributors remain anonymous unless requested")
    st.write("• Building the most comprehensive database of sales manipulation tactics")
    st.markdown('</div>', unsafe_allow_html=True)

def training_techniques_page():
    st.header("🧠 Sales Training Techniques")
    st.write("The psychological methods taught to salespeople to influence your decisions.")
    
    # Technique categories
    technique_tabs = st.tabs(["🎯 5-Stage Process", "🧠 Psychological Tricks", "🚩 Warning Signs", "🛡️ Defense Strategies"])
    
    with technique_tabs[0]:
        st.subheader("The 5-Stage Influence Framework")
        st.write("Most professional sales training follows this systematic psychological process:")
        
        stages = [
            {
                "stage": "PREPARE",
                "title": "Setting the Psychological Trap",
                "description": "Planning how to 'influence your state of mind'",
                "tactics": [
                    "Research your psychological profile",
                    "Set primary objective (the sale) and backup plans",
                    "Choose meeting environment for maximum impact"
                ],
                "red_flags": [
                    "Advisor seems to know too much about you beforehand",
                    "Meeting feels overly structured or scripted",
                    "Questions designed to uncover vulnerabilities"
                ]
            },
            {
                "stage": "CONNECT", 
                "title": "Building False Intimacy",
                "description": "Creating artificial emotional connection",
                "tactics": [
                    "Rapport building through fake common interests",
                    "Managing impressions to appear trustworthy",
                    "Getting small commitments that lead to bigger ones"
                ],
                "red_flags": [
                    "'We have so much in common!'",
                    "'I understand exactly what you're going through'",
                    "'Do I have your permission to ask questions?'"
                ]
            }
        ]
        
        for stage in stages:
            with st.expander(f"**Stage {stage['stage']}: {stage['title']}**"):
                st.write(f"**What they're doing:** {stage['description']}")
                
                st.write("**Tactics:**")
                for tactic in stage['tactics']:
                    st.write(f"• {tactic}")
                
                st.write("**Red flags to watch for:**")
                for flag in stage['red_flags']:
                    st.write(f"• {flag}")
    
    with technique_tabs[1]:
        st.subheader("Psychological Manipulation Techniques")
        
        techniques = {
            "State Management": {
                "description": "Controlling your emotional state to make you more receptive",
                "examples": ["Using fear to create urgency", "Making you feel special or exclusive", "Creating artificial time pressure"],
                "defense": "Stay calm and logical. Ask for time to think independently."
            },
            "Anchoring": {
                "description": "Setting a high initial price to make other options seem reasonable",
                "examples": ["Showing expensive option first", "Mentioning worst-case scenarios", "Using high fee products as 'anchors'"],
                "defense": "Research typical costs beforehand. Don't let them set your price expectations."
            },
            "Social Proof": {
                "description": "Using others' behavior to influence your decisions",
                "examples": ["'Most of my clients choose this'", "'Everyone is doing this now'", "'Other people in your situation...'"],
                "defense": "Ask for verifiable references. Your situation is unique."
            }
        }
        
        for technique, details in techniques.items():
            with st.expander(f"**{technique}**"):
                st.write(f"**What it is:** {details['description']}")
                st.write("**Examples:**")
                for example in details['examples']:
                    st.write(f"• {example}")
                st.markdown(f'<div class="success-box"><strong>Your defense:</strong> {details["defense"]}</div>', unsafe_allow_html=True)
    
    with technique_tabs[2]:
        st.subheader("🚩 Warning Signs of Manipulation")
        
        warning_categories = {
            "Pressure Tactics": [
                "Must decide today",
                "This offer expires soon", 
                "I can only do this if you act now",
                "Other clients who waited regretted it"
            ],
            "Information Control": [
                "Reluctant to provide written details",
                "Won't explain fees clearly",
                "Dismisses your questions as 'complicated'",
                "Focuses on emotions over facts"
            ],
            "Relationship Manipulation": [
                "Asks personal questions too early",
                "Claims to use same products for their family",
                "Creates false urgency about your situation",
                "Makes you feel guilty for questioning them"
            ]
        }
        
        for category, warnings in warning_categories.items():
            st.write(f"**{category}:**")
            for warning in warnings:
                st.write(f"🚩 {warning}")
            st.write("")
    
    with technique_tabs[3]:
        st.subheader("🛡️ Your Defense Strategies")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Before Any Meeting:**")
            st.write("• Research the person and company independently")
            st.write("• Prepare your own questions list")
            st.write("• Set clear boundaries for yourself")
            st.write("• Bring a trusted friend if possible")
            
            st.write("**Questions That Give You Control:**")
            st.write("• How are you compensated?")
            st.write("• What are ALL the fees?")
            st.write("• Can I have this in writing?")
            st.write("• What happens if I want to leave?")
        
        with col2:
            st.write("**During the Meeting:**")
            st.write("• Take notes on everything")
            st.write("• Don't share unnecessary personal details")
            st.write("• Ask for information in writing")
            st.write("• Trust your instincts if something feels off")
            
            st.write("**Phrases That Stop Manipulation:**")
            st.write("• 'I need time to research this independently'")
            st.write("• 'I don't make financial decisions under pressure'")
            st.write("• 'Why are you asking me that?'")
            st.write("• 'I'll let you know when I'm ready'")
    
    st.markdown('<div class="alert-box">', unsafe_allow_html=True)
    st.write("**🎯 Remember: You're the Customer**")
    st.write("• You're interviewing them, not the other way around")
    st.write("• Good professionals welcome questions and don't pressure you")  
    st.write("• Your money, your timeline for decisions")
    st.write("• Trust is earned through transparency, not sales techniques")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
