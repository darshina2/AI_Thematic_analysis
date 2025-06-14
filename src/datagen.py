import os
import google.generativeai as genai
import csv
import configparser

local_dir = os.path.abspath(os.path.join(__file__, "../../data/course_files"))
output_file = os.path.join(local_dir, "AI_Software_Development.txt")
Chat_history = os.path.join(local_dir, "Chain_of_thought.txt")

config = configparser.ConfigParser()
config.read("config.ini")

if "GEMINI" in config and "api_key" in config["GEMINI"]:
    api_key = config["GEMINI"]["api_key"]
else:
    api_key = None

genai.configure(api_key=api_key)

def load_chat_history(filename=Chat_history):
  try:
    with open(filename, "r") as f:
      history_str = f.read()
  except FileNotFoundError:
    return []  

  history = []
  for line in history_str.strip().split("\n"):
    if line.startswith("User:"):
      role = "user"
      content = line[5:] 
    elif line.startswith("Assistant:"):
      role = "assistant"
      content = line[10:]
    else:
      continue  
    history.append({"role": role, "content": content})
  return history


def generate_course_outline(prompt, history_file=Chat_history):

    generation_config = {
        "temperature": 0.7,  
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192, 
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    chat_history = load_chat_history(history_file)
    

    chat_session = model.start_chat(history=chat_history)

    full_prompt = f"""
    You are an experienced university professor with experience in teaching as mentioned in the given prompt. 
    You are tasked with creating a course outline for a university-level course taught at the university. 
    Using the following structured framework, 
    create a detailed course outline for a university-level course on the 
    application of Artificial Intelligence (AI) in a specific domain. 
    The course should be designed to equip learners with the necessary knowledge and skills to 
    effectively interact with AI in their field.

    **Framework:**
    Following is the structure of the course design framework.
        Section 1: AI in the Domain
        1.1 Domain:
        --Define the specific domain in which AI will be applied.
        --Example: Radiology, Mechanical Engineering, Finance, Education, etc.
        1.2 Potential AI Use Cases:
        --Identify current and future AI use cases relevant to the domain.
        --Describe how AI technology is impacting or could impact the domain.
        --Highlight domain-specific problems that AI can help solve.
        1.3 Data in the Domain:
        --Specify the types of data commonly used in the domain.
        --Explain the significance of this data for AI applications.
        --Discuss how understanding this data enables targeted AI techniques.
        1.4 Implications of Using AI:
        --Discuss ethical, legal, and social implications of AI use in the domain.
        --Provide examples of potential positive and negative impacts.
        --Address any domain-specific concerns or considerations.
        1.5 Additional Learning Resources:
        --List existing learning materials and resources that can support the course.
        --Include Open Educational Resources (OER), textbooks, online courses, articles, etc.
        Section 2: Learning Environment
        2.1 Learners and Their Interaction with AI:
        Describe the target learners:
        --Current level of AI knowledge and related skills (e.g., mathematics, programming).
        Background in the domain.
        --Expected role after completing the course regarding AI interaction (e.g., users, developers, decision-makers).
        2.2 Instructors:
        Detail the instructors' qualifications:
        --AI-related skills and competencies.
        Domain expertise.
        --Teaching experience and pedagogical skills.
        2.3 Internal Support:
        --Outline available resources and constraints:
        --Budget, personnel, and course duration.
        --Availability of domain-specific data.
        --Access to software and hardware (e.g., AI tools, computing resources).
        --Institutional support for interdisciplinary teaching.
        Section 3: Course Implementation
        3.1 Learning Outcomes:
        --Define clear and measurable learning objectives:
        --What should learners know or be able to do by the end of the course?
        --Align outcomes with the identified AI use cases and data types in the domain.
        3.2 Assessment:
        --Plan how to evaluate learners' achievement of learning outcomes:
        --Choose appropriate assessment methods (e.g., exams, projects, presentations).
        --Consider incorporating real-world applications and problem-solving tasks.
        --Ensure assessments are fair and account for learners' diverse backgrounds.
        3.3 Learning Activities:
        --Design engaging and effective learning experiences:
        --Incorporate the Merrill principles of instruction:
        --Problem-Centered: Engage learners with real-world problems.
        --Activation: Build on learners' prior knowledge.
        --Demonstration: Show examples of AI applications in the domain.
        --Application: Provide opportunities for learners to apply new knowledge.
        --Integration: Encourage learners to integrate new skills into their work.
        --Use a mix of teaching methods: Lectures, labs, discussions, and group work should be utilized to engage learners effectively.



    **Instructions:**
        1. Use concise and structured content generation, do not change the section headings name.
        2. Design the course outline very carefully, including all the components in the template. 
        3. Double-check the course outline that you generate. Based on these measures Correctness (Accuracy), Coherence, Relevance, Completeness, Originality, Instructive.

    

    **Example:**
    (Include a simple example of a course outline with the framework for better guidance)
    
        **Prompt:**  Please generate a detailed course outline for a university level bachelor introductory course titled 'Artificial Intelligence in Business Administration'. 
            Use the following information as guidance: 
                •	Domain: Business Administrator 
                •	Potential AI Use Cases: Forecasting sales of a company. Asset allocation. You can add more usecases. 
                •	Data in the Domain: Structured, text. You can add more. 
                •	Additional Learning Resources: Students can learn from popular youtube channels, Authentic blogs and courses from websites such as Udemy and Coursera. You can mention names of the courses. 
                •	Learners: These are bachelor students with a major in business administration, some of them have used AI but at a very high level. These learners are very new to AI. 
               •	Instructors: The instructor is a PhD professor in business administrator who has an overall 10 years of experience, with 4 years of industry experience in AI 
                
                Learning Outcomes: To equip learners with basic knowledge of AI of that they can understand the power of AI and start thinking of how to apply AI in their field.  

            Here is all the information I have now. But you can ask me for more info if that helps you in making the course outline even better.

        **Answer:**
        Course Outline: Artificial Intelligence in Business Administration
        ________________________________________
        Section 1: AI in the Domain
        1.1 Domain: Business Administration
        •	Definition: Business Administration involves planning, organizing, directing, and managing resources to achieve organizational goals. The integration of AI enhances decision-making, automates tasks, and provides insights into data-driven strategies.
        •	Relevance: AI is transforming traditional business processes by improving efficiency, providing real-time insights, and enabling smarter decisions in areas like operations, marketing, and finance.
        1.2 Potential AI Use Cases in Business Administration
        1.	Forecasting Sales: 
        o	Use AI models to predict future sales trends based on historical data and market conditions.
        2.	Asset Allocation: 
        o	Optimize resource allocation through predictive analytics and machine learning techniques.
        3.	Customer Relationship Management (CRM): 
        o	Enhance customer segmentation, personalize marketing, and improve customer service with AI chatbots.
        4.	Inventory Management: 
        o	Use AI to monitor and optimize stock levels to reduce overstocking or shortages.
        5.	Fraud Detection: 
        o	Employ AI for anomaly detection in financial transactions to prevent fraud.
        6.	Process Automation: 
        o	Automate routine tasks, such as data entry and report generation, to increase operational efficiency.
        1.3 Data in the Domain
        •	Types of Data: 
        o	Structured Data: Financial reports, sales records, customer demographics, and performance metrics.
        o	Text Data: Customer reviews, social media posts, emails, and business reports.
        o	Semi-Structured Data: Log files and JSON data from applications.
        •	Significance for AI Applications: 
        o	Structured data enables precise algorithm training and analytics for forecasting and optimization.
        o	Text data allows for natural language processing (NLP) applications, such as sentiment analysis.
        o	Data understanding enables targeted AI techniques like supervised learning for predictions and NLP for communication insights.
        1.4 Implications of Using AI in Business Administration
        •	Ethical Implications: Risk of bias in decision-making models, challenges with data privacy, and transparency concerns.
        •	Legal Implications: Compliance with data protection regulations like GDPR and ensuring fairness in AI algorithms.
        •	Social Implications: Changes in workforce dynamics due to automation, potential job displacement, and improving accessibility to business services.
        •	Examples: 
        o	Positive: Enhanced customer service through personalized interactions.
        o	Negative: AI misuse leading to unfair discrimination or unintended errors in decision-making.
        1.5 Additional Learning Resources
        •	YouTube Channels: 
        o	Simplilearn: “AI for Beginners.”
        o	Google Developers: “AI Basics with TensorFlow.”
        •	Online Courses: 
        o	Udemy: “Artificial Intelligence for Business” by 365 Careers.
        o	Coursera: “AI for Everyone” by Andrew Ng.
        o	EdX: “Introduction to Artificial Intelligence” by Microsoft.
        •	Blogs and Articles: 
        o	Towards Data Science: Articles on AI applications in business.
        o	Harvard Business Review: Insights on AI strategies for business leaders.
        ________________________________________
        Section 2: Learning Environment
        2.1 Learners and Their Interaction with AI
        •	Learners: 
        o	Bachelor students majoring in Business Administration.
        o	Minimal experience with AI, typically at a high level.
        •	Expected Role After Completion: 
        o	Gain foundational knowledge to understand AI’s capabilities and start applying AI concepts in decision-making, strategy, and operations.
        2.2 Instructors
        •	Qualifications: 
        o	PhD in Business Administration.
        o	10 years of academic experience, including 4 years of AI-related industry experience.
        •	Skills: 
        o	Strong grasp of business fundamentals and AI technologies.
        o	Ability to bridge technical AI concepts with practical business applications.
        o	Experience in interdisciplinary teaching and student engagement.
        2.3 Internal Support
        •	Resources: 
        o	Course duration: One semester (12–14 weeks).
        o	Access to software tools like Python, Excel, and Tableau for AI demonstrations.
        o	Availability of datasets for business applications (e.g., Kaggle, public business data repositories).
        o	Institutional support for interdisciplinary learning.
        ________________________________________
        Section 3: Course Implementation
        3.1 Learning Outcomes
        By the end of the course, students will:
        1.	Understand the basics of AI and its relevance to business administration.
        2.	Identify and evaluate AI applications in various business functions like marketing, finance, and operations.
        3.	Interpret business-related data for AI-driven decision-making.
        4.	Recognize ethical, legal, and societal considerations of using AI in business.
        5.	Apply foundational AI knowledge to propose solutions to domain-specific problems.
        3.2 Assessment
        1.	Individual Assignments: 
        o	Analyze case studies on AI in business (e.g., forecasting sales trends).
        2.	Group Project: 
        o	Design a business strategy incorporating AI (e.g., developing a CRM solution using AI insights).
        3.	Quizzes: 
        o	Weekly quizzes on key AI concepts and applications.
        4.	Final Presentation: 
        o	Present a business problem, propose an AI solution, and discuss implications.
        5.	Class Participation: 
        o	Active engagement in discussions and in-class activities.
        3.3 Learning Activities
        •	Problem-Centered: 
        o	Case studies on real-world AI applications, such as Amazon's inventory management or Netflix's recommendation system.
        •	Activation: 
        o	Reflect on personal experiences with technology in business and identify AI potential in known scenarios.
        •	Demonstration: 
        o	Live demonstrations of AI tools like Excel forecasting, Python for sales prediction, and chatbots in CRM.
        •	Application: 
        o	Hands-on labs for creating basic predictive models using business data.
        o	Group exercises to simulate business decision-making with AI insights.
        •	Integration: 
        o	Discuss how AI can complement traditional business practices.
        o	Encourage students to develop proposals for applying AI in their internship or workplace settings.

        **Your Turn:**
                    **Prompt:** Please generate a detailed course outline  as per the information given in the below prompt. Take help of the Chain of thought provided in the history:
                    
                    {prompt}

                    **Instruction:**
                    1. **Understand the text:** Read the text carefully and identify the main topic and key concepts.
                    2. **Identify key themes:** Determine the most important and relevant themes discussed in the text.
                    3. **Select minimum number of keywords:** Choose words or short phrases that best represent the key themes and provide a concise summary of the text.
                    4. **Do not add any additional text for heading or summary like **answer. Just provide keywords required.
                    5. Do not change the bullet number given in the prompt. 
                    
                    **Answer:** 
                    
       

    **Generate the course outline:** 
    """

    response = chat_session.send_message(full_prompt)
    course_outline = response.text

    return course_outline
 

if __name__ == "__main__":

  prompt = """
      * **Domain:** Software development
      * **Potential AI Use Cases:** automated code generation, code review, bug detection
      * **Data in the Domain:** Structured, codes. You can add more. 
      * **Additional Learning Resources:** Students can learn from Github, Youtube, Online courses -Udemy in addition to textbooks, blogs and forums. You can mention other resources if you know. 
      * **Learners:** These are bachelor students studying computer science, most of them know how to integrate AI. These learners know about tools such as ChatGPT. 
      * **Instructors:** The instructor is a professor of Software Programming who has an overall 25 years of experience. The professor has PhD in Computer Science- Software development. 
      * **Learning Outcomes:** To equip learners with practical knowledge of AI of that they can start thinking of how to apply AI in their field. 
  """


  course_outline = generate_course_outline(prompt)
  print(course_outline)
  with open(output_file, 'w') as file:
      file.write(course_outline)