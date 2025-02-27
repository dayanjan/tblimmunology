# Blueprint for Constructing an AI-Based Patient Simulation to Enhance the Integration of Foundational and Clinical Sciences in Didactic Immunology in A US Doctor of Pharmacy Program: A Step-By-Step Prompt Engineering and Coding Toolkit 

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Authors
Ashim Malhotra, Micah Buller, Kunal Modi, Karim Pajazetovic, and Dayanjan S. Wijesinghe

## About
This repository hosts the AI-Guided Pharmacy Education Tool, designed to facilitate team-based learning activities in pharmacy education. The tool leverages Socratic AI mentorship to engage students in interactive patient case analysis and dialogue-driven guidance, promoting the integration of foundational sciences with clinical decision-making.

## Features
* **Interactive AI Chatbot**: Engages students in Socratic-style conversations for in-depth patient case studies
* **Team-Based Learning**: Supports collaborative learning activities, enhancing critical thinking and decision-making skills
* **Customizable Case Studies**: Offers a variety of patient cases focusing on immunology, adaptable to different educational needs
* **Cost Tracking**: Monitors API usage and associated costs for educational budget management
* **Conversation Export**: Allows saving and downloading of learning sessions for assessment and review
* **Standardized Assessment**: Evaluates student performance using a comprehensive rubric focused on clinical competencies

## Getting Started

### Prerequisites
* Python 3.10 or later
* OpenAI API key with access to GPT-4o models
* Please refer to `requirements.txt` for a list of necessary libraries and dependencies

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/wijesingheds/ai-guided-pharmacy-education.git
   cd ai-guided-pharmacy-education
   ```

2. Set up a Python virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   * On Windows:
     ```
     .\venv\Scripts\activate
     ```
   * On Unix or MacOS:
     ```
     source venv/bin/activate
     ```

4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up your OpenAI API key:
   * Create a `.streamlit/secrets.toml` file with the following content:
     ```toml
     [openai]
     api_key = "your-openai-api-key"
     ```

## Usage
1. Run the application:
   ```bash
   streamlit run tblimmunology.py
   ```

2. Select an exercise from the sidebar dropdown menu
3. Engage with the AI facilitator in Socratic dialogue about the patient case
4. Progress through symptomatology analysis, laboratory interpretation, and pharmaceutical care planning
5. Receive comprehensive feedback based on the standardized assessment rubric
6. Export your completed conversation for submission or review

## Case Studies
The system currently includes three immunology-focused case studies:
1. **Splenomegaly and Potential Leukemia**: Focuses on post-splenectomy care and vaccination protocols
2. **Chronic Inflammation**: Emphasizes holistic treatment approaches and long-term disease management
3. **Acute Kidney Rejection**: Focuses on transplant immunology and complex pharmaceutical interventions

## Technical Architecture
The application is built with:
* Python and Streamlit for the web interface
* OpenAI's GPT-4o models for AI-facilitated Socratic dialogue
* Custom prompt engineering for educational scaffolding
* Comprehensive logging and error handling for reliability

## Contributing
Contributions to enhance the tool are welcome. Please follow the standard GitHub pull request process to propose changes.

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE.txt) file for details.

## Acknowledgements
* This project was funded in part through a grant from the VentureWell Foundation titled "Creating a Program to Train Healthcare Professional Students in Digital Health Application Development and Deployment"
* Virginia Commonwealth University School of Pharmacy
* California Northstate University College of Pharmacy

## Citation
If you use this software in academic, research, or commercial applications, please cite:

```
Malhotra, A., Buller, M., Modi, K., Pajazetovic, K., & Wijesinghe, D. S. (2025). 
Blueprint for Constructing an AI-Based Patient Simulation to Enhance the Integration 
of Foundational and Clinical Sciences in Didactic Immunology in A US Doctor of 
Pharmacy Program: A Step-By-Step Prompt Engineering and Coding Toolkit. Pharmacy, 13.
```

## Contact
For queries or feedback, please reach out to:
* Dayanjan S. Wijesinghe: wijesingheds@vcu.edu or shanaka@dayanjan.com
