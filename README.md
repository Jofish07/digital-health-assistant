# Digital Health Assistant: A Data-Driven Well-being Intervention Project

## Project Overview
This project identifies and proposes a solution for high-risk social media users based on an analysis of 5,000 user behavior records. The goal is to design a non-intrusive, data-informed well-being plugin.

## Key Findings (Data-Driven Insight)
- **High-Risk Group Definition**: Usage > 231 min/day + Sleep < 6.7 hrs + Negative Interactions.
- **Significant Impact**: This group exhibits **2.66 points higher stress levels** (8.27 vs 5.61) compared to the low-risk group, with a very large effect size (Cohen‘s d = 5.39).
- **Strong Behavioral Correlations**:
  - **Usage-Stress Link**: Social media time shows a **strong positive correlation (r = 0.88)** with stress levels.
  - **Sleep-Stress Link**: Sleep duration shows a **strong negative correlation (r = -0.83)** with stress levels.
  - This confirms **“usage management” and “sleep promotion”** as the two most critical behavioral levers for intervention.

## Project Deliverables
1.  **Data Analysis**: Python script (`digital_health_assistant_analysis.py`) for data processing, statistical testing, and visualization.
2.  **Cleaned Dataset**: `cleaned_behavior_data.csv` containing the processed data.
3.  **Visualizations**: Four key charts illustrating stress comparison, anxiety comparison, user distribution, and behavior correlations.
4.  **Product Requirements Document (PRD)**: Complete product strategy, feature list, and success metrics. [View Portfolio PDF](./江雨萱_数字健康助手_数据分析×产品设计作品集.pdf)
5.  **High-Fidelity Prototype**: Interactive Axure prototype showcasing the user flow. [View Prototype](https://4yhos8.axshare.com/?g=4)

## Technology & Tools
- Python (Pandas, NumPy, SciPy, Matplotlib, Seaborn)
- Statistical Analysis (Independent t-test, Effect Size)
- Axure RP (Prototyping)
- GitHub (Version Control)

## How to Run the Analysis
1.  Ensure Python 3.7+ is installed.
2.  Install required libraries: `pip install pandas numpy scipy matplotlib seaborn`.
3.  Place `cleaned_behavior_data.csv` in the same directory as the Python script.
4.  Run: `python digital_health_assistant_analysis.py`

## About the Author
**Jiang Yuxuan (江雨萱)**
- Social Work major, aspiring Product Manager.
- Focus on leveraging data to design human-centric, ethical digital solutions.
- [View My Portfolio PDF](./江雨萱_数字健康助手_数据分析×产品设计作品集.pdf)

---
*This project is for academic and portfolio purposes.*
