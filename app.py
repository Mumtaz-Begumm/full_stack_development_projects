from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob  # For spell correction

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the frontend

# Define keywords for each category
category_keywords = {
    "apply_scholarship": ["how to apply for scholarship","apply scholarship","apply for scholarship"],
    "scholarship_details":["scholarship","available scholarships","available scholarship"],
    "aiml fees":["aiml fee","aiml fees","aiml course fee", "aiml course fees","fees for aiml","fees for artificial intelligence and machine learning","fees for artificial intelligence and machine learning engineering","fee for artificial intelligence and machie learning"],
    "hostel_rooms":["rooms available in hostel","number of rooms in hostel","no of rooms in hostel","how many rooms are there in hostel?","hostel rooms","rooms in hostel","rooms are available in hostel","rooms are present in hostel"],
    "greetings": ["hello", "hi", "hii"],
    "leave taking": ["bye", "goodbye"],
    "gratitude": ["thank you", "thanks", "thank you so much", "really thank you"],
    "documents": ["document", "documents needed for admission", "what things i need for admission", "things need to be submitted?"],
    "admission process": ["admission", "apply", "process", "how to apply", "apply for admission", "application"],
    "eligibility": ["eligibility", "criteria", "requirements", "who can apply", "qualification", "eligible"],
    "course_fees": [ "course fees", "fee structure","fees structure","course fee","fees for courses","fee for courses"],
    "cse-ai fees":["cse-ai fee","cse-ai fees","cse-ai course fee", "cse-ai course fees","fees for cse-ai","fee for cse-ai","fees for cse-ai"],
    "cse-ds fees":["cse-ds fee","cse-ds fees","cse-ds course fee", "cse-ds course fees","fees for cse-ds","fee for cse-ds","fees for cse-ds"],
    "cse fees":["cse fee","cse fees","cse course fee", "cse course fees","fees for cse","fees for computer science and engineering","fee for computer science and engineering","fees for computer science","fee for computer science","fee for cse","fees for cse"],
    "ece fees":["ece fee","ece fees","ece course fee", "ece course fees","fees for ece","fees for electronics and communication engineering","fee for ece","fees for ece"],
    "eee fees":["eee fee","eee fees","eee course fee", "eee course fees","fees for eee","fees for electrical and electronics engineering","fee for eee","fees for ee"],
    "civil fees":["civil fee","civil fees","civil course fee", "civil course fees","fees for civil","fee for civil","fees for civil"],
    "me fees":["me fee","me fees","me course fee", "me course fees","fees for me","fees for mechanical engineering","fee for me","fees for me"],
    "deadline": ["deadline", "last date", "apply before", "final date", "submit by"],
    "courses":["courses offered","available courses","courses","course"],
    "hostel_fees":["hostel fee","hostel","hostel fees"],
    "transportation":["transport","transportation fees","transportation","transportation fee","bus fees","bus fee"],
    "contact_details":["contact details","phone number","phone no","how can i contact?","contact no","contact"],
    "email_id":["what is the email id?","email id","email address","website","website name","college website","BITM email id","bitm email id","bitm email","bitm website","email"],

}

# Responses for each category
responses = {
    "greetings": "Hello! What would you like to ask me?",
    "leave taking": "Bye! Have a nice day :)",
    "gratitude": "You're welcome! You can ask me if you need any further help.",
    "admission process": "The admission process involves filling out an application form, submitting required documents, and attending an interview.",
    "eligibility": "Eligibility depends on the program. Please provide details about the course you're interested in.",
    "course_fees": "CSE\t- 3,40,000\nAIML\t- 2,65,000\nCSE-AI\t- 2,65,000\nCSE-DS\t - 2,65,000\nECE\t - 1,90,000\nME\t - 1,50,000\nEEE\t - 1,50,000\nCivil\t - 1,50,000",
    # "deadline": "The admission deadline is June 30th for the upcoming academic year.",
    # "scholarship": "We offer scholarships based on academic performance and financial need. Please contact the admissions office for more details",
    "hostel_fees":"rent + mess (BITM campus) - 75,000 (p.a)",
    "transportation":"transportation fee for day scholars: 14,000 (p.a)",
    "cse fees":"Fees for CSE : 3,40,000",
    "aiml fees":"Fees for AIML : 2,65,000",
    "cse-ai fees":"Fees for CSE-AI : 2,65,000",
    "cse-ds fees":"Fees for CSE-DS : 2,65,000",
    "ece fees":"Fees for ECE : 1,90,000",
    "me fees":"Fees for ME : 1,50,000",
    "eee fees":"Fees for EEE :1,50,000",
    "civil fees":"Fees for CIVIL : 1,50,000",
    "contact_details":"addmission office contacts :\nphone : 08392-237167 / 237190\n Mobile : 91 99024 99388",
    "email_id":"bitmbly@gmail.com | info@bitm.edu.in",

}

# Default document response
default_documents = [
    "The candidate after getting allotment of seat through CET/COMED-K/Management he/she has to approach the Admission Section complete the admission formalities with the following;\n",
    "1) Allotment letter\n",
    "2) Original SSLC/SSC/10th/PUC/12th Marks Card and Transfer Certificate\n",
    "3) Original Study and Conduct Certificate\n",
    "4) Original Caste Certificate / Income Certificate, if applicable\n",
    "5) Original Migration Certificate, if applicable\n",
    "6) Two sets of photo copies of all the above along with 8 passport size photos, College Fees, as applicable.\n",
    "7) The candidate will be allotted a section, either in Chemistry Group or Physics Group and the same is notified on the Notice Board at the beginning of the semester\n",
    "8)The sections allotted to the students have to be followed and no change of sections is allowed under any circumstances.\n"
]
eligibility_criteria=[
    "Students who have passed Karnataka 2nd PUC/ 12th Std,/ 10+2 / Intermediate or equivalent exam with Physics & Mathematics along with Chemistry/ Computer Science /Biology and any other optional subject with English as one of the languages of study and should have obtained a minimum of 45% marks.\n",
    "For SC/ST & other backward classes of Karnataka students only, the minimum marks is   40% in aggregate in the optional subjects in the qualifying examination, irrespective of marks obtained in the Common Entrance Test / Comed-K/ AIEEE."
]
courses_offered=[
    "1) Computer Science Engineering\n",
    "2) Electronics and Communication Engineering\n",
    "3) Mechanical Engineering\n",
    "4) Electrical and Electronics Engineering\n",
    "5) Civil Engineering\n",
    "6) Artificial Intelligence and Machine Learning Engineering\n",
    "7) Computer Science Engineering(Data Science)\n",
    "8) Computer Science Engineering(Artificial Intelligence)\n"
]
apply_scholarship=[
    "1. The students eligible for scholarship are required to obtain the application from the Office after completion of admission process and Apply Online.\n",
    "2. The SC/ST students who have taken admission through CET must apply for the scholarship compulsorily within the stipulated time only.\n",
    "3. The newly admitted students are required to submit the duly filled application along with 02 copies of the CET Admission order, 10+2 marks card, Income Certificate, Caste Certificate to the Scholarship in-charge.\n",
    "4. The higher semester students are required to submit the duly filled application along with 02 copies of the CET Admission order, Income Certificate Caste Certificate and previous semester's marks card to the Scholarship in-charge\n",
    "5. Further the same applications will be forwarded to concerned authorities after completing all the formalities at the college end.\n",
    "6. Immediately after receiving the Scholarship from the concerned departments, directly amount will be transferred to students account (DBT).\n"
]
scholarship_details=[
    "1. Schedule Caste / Schedule Tribe (Parent income below Rs. 2.50 Lakhs) : Post Matric Scholarship\n",
    "2.	Schedule Caste / Schedule Tribe (Parent income above Rs. 2.50 Lakhs) : Post Matric Scholarship/Department of Technical Education, Palace Road, Bengaluru.\n",
    "3.	Category-2A (Minority, i.e., Muslim, Jain, Parsi, Christian, Sikhs) (Parent Income Limit Rs. 2.00 Lakhs) : Fee Concession, Arivu Loan & MOM ONLINE\n",
    "4.	Pratibha Purskar (Selected from Govt. of Karnataka)	: Merit Students\n",
    "5.	Post Matric Scholarship (ONLINE) : For Non-Karnataka Students (i.e., Jharkhand, Bihar,etc.)\n",
    "6.	Sitaram Jindal Foundation : Merit Scholarship\n",
    "7.	BITM also Provides Scholarships	: Merit Scholarship\n",
    "8.	National Scholarship Portal (Online) : For all the categories\n"
]

hostel_fees=[
     "1. Kaveri Block-attached (Girls)	Rs 75,000/-\n",
     "2. Nethravathi Block-attached (Girls)	Rs 75,000/-\n",
	 "3. Tunga Block-attached (Boys)	Rs 75,000/-\n",
     "4. Tunga Block Non-attached (Boys)	Rs 65,000/-\n",
     "5. Bhadra Block-attached (Boys)	Rs 75,000/-\n",
     "6. Krishna Block-attached (Boys)	Rs 75,000/-\n",
     "7.RR Block-attached	Rs 89,000/-\n",
     "\nNOTE: Each room is to be occupied by a maximum of 3 students"
]
rooms=[
    "Gents Hostel:\n",
    "Tunga Block-attached : 26 Rooms\n",
    "Tunga Block-Non-attached : 57 Rooms\n",
    "Bhadra Block-Attached : 32 Rooms\n",
    "Krishna Block-attached	: 130 Rooms\n"

    "ladies hostel:",
    "Kaveri Block-attached	: 154 Rooms\n",
    "Nethravathi Block-attached	: 60 Rooms\n",
    "RR Block-attached	: 95 Rooms\n",
    "Sharavathi : 80 Rooms\n"
]


# Function to predict the category and return a response based on keywords
def get_response(user_query):
    # Correct spelling mistakes using TextBlob
    corrected_query = str(TextBlob(user_query).correct())  # Spell correction
    # Check for matching keywords
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword.lower() in corrected_query.lower() or (keyword.lower() in user_query.lower()):  # Case-insensitive matching
                if category == "documents":
                    return "The documents required for admission are:\n\n" + "\n".join(default_documents)
                elif category == "eligibility":
                    return "The eligibility criteria is:\n\n" + "\n".join(eligibility_criteria)
                elif category == "apply_scholarship":
                    return "To apply for scholarship:\n\n"+ "\n".join(apply_scholarship)
                elif category == "scholarship_details":
                    return "Scholarship details:\n\n"+ "\n".join(scholarship_details)
                elif category == "courses":
                    return "The courses offered are:\n\n" + "\n".join(courses_offered)
                elif category == "hostel_fees":
                    return "Hostel Fee Structure for the Year 2024-2025:\n\n" + "\n".join(hostel_fees)
                elif category == "hostel_rooms":
                    return "Hostel room details:\n\n" + "\n".join(rooms)
                else:
                    return responses.get(category, "I'm sorry, I can only answer queries related to admissions.")

    # If no keyword is found, return a default message
    return "I'm sorry, I didn't understand your question. Can you please ask about admissions, eligibility, fees, deadlines, or scholarships?"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    # Get the response
    response = get_response(user_input)

    return jsonify({"reply": response})

if __name__ == '__main__':
    app.run(debug=True)