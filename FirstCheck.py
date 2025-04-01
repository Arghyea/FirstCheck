import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import webbrowser
import random

class MentalHealthChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Mental Health Support Chatbot")
        self.root.geometry("700x600")
        self.root.configure(bg="#121212") 

     
        self.style = ttk.Style()
        
        self.style.theme_use("clam")
        self.style.configure(
            "My.TButton",
            background="#4D4D4D",
            foreground="white",
            relief="flat",
            borderwidth=0,
            focusthickness=0,
            padding=6
        )
       
        self.style.map(
            "My.TButton",
            background=[("active", "#4D4D4D"), ("pressed", "#4D4D4D"), ("disabled", "#4D4D4D")],
            foreground=[("active", "white"), ("pressed", "white"), ("disabled", "white")]
        )

     
        self.link_count = 0

        self.conversation_started = False
        self.last_detected_issue = None

      
        self.setup_ui()

        self.crisis_resources = {
            "India": [
                "AASRA: 91-9820466726",
                "Mental Health Helpline: 1800-599-0019",
                "Vandrevala Foundation: 1860-2662-345",
                "iCall: +91-22-25521111"
            ],
            "Global": [
                "International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/"
            ]
        }

        
        self.display_bot_message("Hi, I'm here to help. What's troubling you today?")

        
        self.keywords = {
            # Headaches
            "headache": self.handle_headache,
            "migraine": self.handle_headache,  
            "pain in head": self.handle_headache,
            "head pain": self.handle_headache,

            # Depression
            "depress": self.handle_depression,
            "sad": self.handle_depression,
            "low mood": self.handle_depression,
            "hopeless": self.handle_depression,
            "feeling down": self.handle_depression,

            # Suicidal Thoughts
            "suicid": self.handle_suicidal_thoughts,
            "kill myself": self.handle_suicidal_thoughts,
            "end my life": self.handle_suicidal_thoughts,
            "don't want to live": self.handle_suicidal_thoughts,
            "self harm": self.handle_suicidal_thoughts,

            # Anxiety
            "anxiety": self.handle_anxiety,
            "anxious": self.handle_anxiety,
            "worry": self.handle_anxiety,
            "panic": self.handle_anxiety,
            "fear": self.handle_anxiety,

            # Sleep Issues
            "sleep": self.handle_sleep_issues,
            "insomnia": self.handle_sleep_issues,
            "can't sleep": self.handle_sleep_issues,
            "tired": self.handle_sleep_issues,
            "fatigue": self.handle_sleep_issues,

            # Stress
            "stress": self.handle_stress,
            "overwhelm": self.handle_stress,
            "pressure": self.handle_stress,
            "burnout": self.handle_stress,

            # Additional conditions
            "diabetes": self.handle_diabetes,
            "high blood sugar": self.handle_diabetes,
            "blood sugar": self.handle_diabetes,
            "hypertension": self.handle_hypertension,
            "high blood pressure": self.handle_hypertension,
            "asthma": self.handle_asthma,
            "allergy": self.handle_allergies,
            "arthritis": self.handle_arthritis,
            "back pain": self.handle_back_pain,
            "stomach pain": self.handle_digestive_issues,
            "acid reflux": self.handle_digestive_issues,

            # Menstrual/Period pains (multiple synonyms)
            "period pain": self.handle_menstrual_pain,
            "period pains": self.handle_menstrual_pain,
            "menstrual pain": self.handle_menstrual_pain,
            "menstrual pains": self.handle_menstrual_pain,
            "cramps": self.handle_menstrual_pain,
            "menstrual cramps": self.handle_menstrual_pain,
        }

    def setup_ui(self):
        # Chat display area
        self.chat_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame,
            bg="#2c2c2c",
            fg="white",
            font=("Arial", 11),
            wrap=tk.WORD
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        
        self.options_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        
        self.input_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.user_input = tk.Entry(
            self.input_frame,
            bg="#2c2c2c",
            fg="white",
            font=("Arial", 11),
            insertbackground="white"
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", self.process_input)
        
        
        self.send_button = ttk.Button(
            self.input_frame,
            text="Send",
            style="My.TButton",
            command=self.process_input
        )
        self.send_button.pack(side=tk.RIGHT, padx=(5, 0))

        
        self.reset_button = ttk.Button(
            self.input_frame,
            text="Reset",
            style="My.TButton",
            command=self.reset_chat
        )
        self.reset_button.pack(side=tk.RIGHT, padx=(5, 0))

        self.user_input.focus_set()

    def display_bot_message(self, message):
        """Displays the bot message and converts any URL to a clickable link (sky blue)."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "Bot: ", ("bot_label",))
        self.chat_display.tag_config("bot_label", foreground="white", font=("Arial", 11, "bold"))
        words = message.split()
        for word in words:
            if word.startswith("http://") or word.startswith("https://"):
                tag_name = f"link_{self.link_count}"
                self.link_count += 1
                self.chat_display.insert(tk.END, word, (tag_name,))
                self.chat_display.insert(tk.END, " ")
                self.chat_display.tag_config(tag_name, foreground="sky blue", underline=1)
                self.chat_display.tag_bind(tag_name, "<Button-1>", lambda e, url=word: webbrowser.open_new(url))
            else:
                self.chat_display.insert(tk.END, word + " ")
        self.chat_display.insert(tk.END, "\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def display_user_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "You: " + message + "\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def clear_options(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

    def add_option_button(self, text, command):
        option_button = ttk.Button(
            self.options_frame,
            text=text,
            style="My.TButton",
            command=command
        )
        option_button.pack(side=tk.LEFT, padx=5, pady=5)

    def process_input(self, event=None):
        user_text = self.user_input.get()
        if not user_text:
            return
        self.display_user_message(user_text)
        self.user_input.delete(0, tk.END)
        self.clear_options()
        found_keyword = False
        user_text_lower = user_text.lower()
        for keyword, handler in self.keywords.items():
            if keyword in user_text_lower:
                handler()
                self.last_detected_issue = keyword
                found_keyword = True
                break
        if not found_keyword:
            if "mild" in user_text_lower and self.last_detected_issue:
                self.handle_severity("mild", self.last_detected_issue)
            elif "moderate" in user_text_lower and self.last_detected_issue:
                self.handle_severity("moderate", self.last_detected_issue)
            elif "severe" in user_text_lower and self.last_detected_issue:
                self.handle_severity("severe", self.last_detected_issue)
            else:
                self.handle_unknown_input()

    def reset_chat(self):
        """Clears the chat display and restarts from the initial greeting."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.clear_options()
        self.conversation_started = False
        self.last_detected_issue = None
        self.display_bot_message("Hi, I'm here to help. What's troubling you today?")

    
    #Subcategories ahead

    def handle_headache(self):
        self.display_bot_message("I see you're experiencing headaches. How would you describe them?")
        self.add_option_button("Mild", lambda: self.handle_severity("mild", "headache"))
        self.add_option_button("Moderate", lambda: self.handle_severity("moderate", "headache"))
        self.add_option_button("Severe", lambda: self.handle_severity("severe", "headache"))

    def handle_depression(self):
        self.display_bot_message(
            "I'm sorry to hear you're feeling this way. Depression symptoms can be challenging. How would you rate your feelings right now?"
        )
        self.add_option_button("Mild", lambda: self.handle_severity("mild", "depression"))
        self.add_option_button("Moderate", lambda: self.handle_severity("moderate", "depression"))
        self.add_option_button("Severe", lambda: self.handle_severity("severe", "depression"))
        self.display_crisis_resources()

    def handle_suicidal_thoughts(self):
        self.display_bot_message(
            "I'm very concerned about what you've shared. Please remember you're not alone, and help is available. It's important to talk to a mental health professional immediately."
        )
        self.display_crisis_resources()
        self.add_option_button("Show Resources", self.show_immediate_help)
        self.add_option_button("Need Someone to Talk To", self.show_immediate_help)

    def handle_anxiety(self):
        self.display_bot_message("I understand you're feeling anxious. How would you describe the intensity of your anxiety?")
        self.add_option_button("Mild", lambda: self.handle_severity("mild", "anxiety"))
        self.add_option_button("Moderate", lambda: self.handle_severity("moderate", "anxiety"))
        self.add_option_button("Severe", lambda: self.handle_severity("severe", "anxiety"))

    def handle_sleep_issues(self):
        self.display_bot_message("Sleep problems can affect your overall well-being. How would you describe your sleep issues?")
        self.add_option_button("Trouble Falling Asleep", lambda: self.handle_specific_sleep_issue("falling asleep"))
        self.add_option_button("Waking Up Frequently", lambda: self.handle_specific_sleep_issue("waking up"))
        self.add_option_button("Poor Sleep Quality", lambda: self.handle_specific_sleep_issue("quality"))

    def handle_stress(self):
        self.display_bot_message("Dealing with stress can be challenging. How would you rate your current stress levels?")
        self.add_option_button("Mild", lambda: self.handle_severity("mild", "stress"))
        self.add_option_button("Moderate", lambda: self.handle_severity("moderate", "stress"))
        self.add_option_button("Severe", lambda: self.handle_severity("severe", "stress"))

    def handle_menstrual_pain(self):
        self.display_bot_message(
            "Menstrual or period pains can be uncomfortable. Are you experiencing mild, moderate, or severe cramps?"
        )
        self.add_option_button("Mild", lambda: self.handle_menstrual_severity("mild"))
        self.add_option_button("Moderate", lambda: self.handle_menstrual_severity("moderate"))
        self.add_option_button("Severe", lambda: self.handle_menstrual_severity("severe"))

    def handle_menstrual_severity(self, severity):
        if severity == "mild":
            self.display_bot_message(
                "For mild menstrual cramps:\n• Gentle exercises or stretching\n• Apply a warm compress\n• OTC pain relief (after consulting a pharmacist)\n\n"
                "Johns Hopkins: https://www.hopkinsmedicine.org/health/conditions-and-diseases/menstrual-cramps"
            )
        elif severity == "moderate":
            self.display_bot_message(
                "For moderate cramps:\n• NSAIDs or hormonal birth control (if recommended)\n• Rest and hydration can help\n\n"
                "Mayo Clinic: https://www.mayoclinic.org/diseases-conditions/menstrual-cramps/symptoms-causes/syc-20374938"
            )
        elif severity == "severe":
            self.display_bot_message(
                "Severe menstrual cramps can be debilitating:\n• Consider consulting a gynecologist\n• Prescription pain relief may be necessary\n\n"
                "AIIMS: https://www.aiims.edu/"
            )

    
    #Severity Handler for Headache, Depression, Anxiety, and Stress
    
    def handle_severity(self, severity, issue):
        responses = {
            "headache": {
                "mild": (
                    "For mild headaches, try these approaches:\n• Stay hydrated\n• Take short breaks from screens\n• Try relaxation techniques\n\n"
                    "Johns Hopkins Medicine: https://www.hopkinsmedicine.org/health/conditions-and-diseases/headache"
                ),
                "moderate": (
                    "For moderate headaches:\n• OTC pain relievers may help\n• Apply a cold or warm compress\n• Rest in a quiet, dark room\n\n"
                    "Mayo Clinic: https://www.mayoclinic.org/symptoms/headache/basics/when-to-see-doctor/sym-20050800"
                ),
                "severe": (
                    "Severe headaches require attention. Please consider:\n• Consulting a doctor if they persist\n• Seeking immediate help if accompanied by other symptoms\n\n"
                    "AIIMS: https://www.aiims.edu/en/departments-and-centers/departments.html"
                )
            },
            "depression": {
                "mild": (
                    "For mild depression symptoms:\n• Regular exercise can help\n• Maintain social connections\n• Consider mindfulness practices\n\n"
                    "NIMH: https://www.nimh.nih.gov/health/topics/depression"
                ),
                "moderate": (
                    "For moderate depression:\n• Consider speaking with a mental health professional\n• Support groups can be beneficial\n• Establish a healthy routine\n\n"
                    "WHO: https://www.who.int/news-room/fact-sheets/detail/depression"
                ),
                "severe": (
                    "Severe depression requires professional help:\n• Consult a mental health professional immediately\n• Consider crisis helplines\n\n"
                    "National Institute of Mental Health: https://www.nimh.nih.gov/health/topics/depression"
                )
            },
            "anxiety": {
                "mild": (
                    "For mild anxiety:\n• Deep breathing exercises\n• Regular physical activity\n• Mindfulness meditation\n\n"
                    "Harvard Health: https://www.health.harvard.edu/topics/anxiety"
                ),
                "moderate": (
                    "For moderate anxiety:\n• Consider talking to a therapist\n• Learn cognitive behavioral techniques\n• Practice regular relaxation\n\n"
                    "ADAA: https://adaa.org/"
                ),
                "severe": (
                    "For severe anxiety:\n• Consult a mental health professional\n• Consider therapy and medical advice\n\n"
                    "NIMH: https://www.nimh.nih.gov/health/topics/anxiety-disorders"
                )
            },
            "stress": {
                "mild": (
                    "For mild stress:\n• Regular exercise\n• Practice mindfulness\n• Ensure adequate sleep\n\n"
                    "APA: https://www.apa.org/topics/stress"
                ),
                "moderate": (
                    "For moderate stress:\n• Time management and setting boundaries\n• Regular relaxation practices\n\n"
                    "Mayo Clinic: https://www.mayoclinic.org/healthy-lifestyle/stress-management/basics/stress-basics/hlv-20049495"
                ),
                "severe": (
                    "For severe stress:\n• Consider professional help\n• Evaluate work-life balance\n\n"
                    "WHO: https://www.who.int/news-room/questions-and-answers/item/stress"
                )
            }
        }
        if issue in responses and severity in responses[issue]:
            self.display_bot_message(responses[issue][severity])
            self.add_option_button("Tell me more", self.show_additional_resources)
            if severity == "severe":
                self.add_option_button("Find Help Near Me", self.find_local_resources)
        else:
            self.handle_unknown_input()

    
    #New Subcategories for Sleep Issues
    
    def handle_specific_sleep_issue(self, issue_type):
        responses = {
            "falling asleep": (
                "Trouble falling asleep:\n• Establish a regular sleep schedule\n• Create a relaxing bedtime routine\n• Limit screen time before bed\n\n"
                "Sleep Foundation: https://www.sleepfoundation.org/insomnia"
            ),
            "waking up": (
                "Waking up frequently:\n• Keep your bedroom cool and dark\n• Avoid caffeine later in the day\n• Consult a doctor if persistent\n\n"
                "Mayo Clinic: https://www.mayoclinic.org/diseases-conditions/insomnia/symptoms-causes/syc-20355167"
            ),
            "quality": (
                "Poor sleep quality:\n• Regular exercise\n• Evaluate your sleep environment\n• Consider a consistent routine\n\n"
                "Harvard Sleep: https://healthysleep.med.harvard.edu/"
            )
        }
        
        if issue_type in responses:
            self.display_bot_message(responses[issue_type])
            self.add_option_button("Sleep Hygiene Tips", self.show_sleep_hygiene)
            self.add_option_button("When to See a Doctor", self.when_to_see_doctor_sleep)
        else:
            self.handle_unknown_input()

    def show_sleep_hygiene(self):
        self.display_bot_message(
            "Good sleep hygiene includes:\n• Keep a consistent sleep schedule\n• Create a relaxing bedtime routine\n• Make your bedroom dark and quiet\n"
            "• Limit screen exposure before bed\n• Avoid caffeine and heavy meals near bedtime\n\n"
            "Sleep Foundation: https://www.sleepfoundation.org/sleep-hygiene"
        )

    def when_to_see_doctor_sleep(self):
        self.display_bot_message(
            "See a doctor if:\n• Your sleep issues persist for weeks\n• They interfere with your daily activities\n• You experience excessive daytime sleepiness\n"
            "• You have breathing difficulties during sleep\n\n"
            "Mayo Clinic: https://www.mayoclinic.org/diseases-conditions/insomnia/symptoms-causes/syc-20355167"
        )

    def handle_unknown_input(self):
        responses = [
            "I'm not sure I understand completely. Could you tell me more?",
            "It seems you're going through something difficult. Please elaborate so I can help.",
            "I want to assist you better. Could you share more details?",
            "I'm here to listen. Could you explain what's troubling you?"
        ]
        self.display_bot_message(random.choice(responses))
        self.add_option_button("Stress", self.handle_stress)
        self.add_option_button("Anxiety", self.handle_anxiety)
        self.add_option_button("Depression", self.handle_depression)
        self.add_option_button("Sleep Issues", self.handle_sleep_issues)

    
    #New Subcategories for Migraines
    
    def handle_migraine(self):
        self.display_bot_message("It seems you're experiencing migraines. Please rate your migraine severity:")
        self.add_option_button("Mild", lambda: self.handle_migraine_severity("mild"))
        self.add_option_button("Moderate", lambda: self.handle_migraine_severity("moderate"))
        self.add_option_button("Severe", lambda: self.handle_migraine_severity("severe"))

    def handle_migraine_severity(self, severity):
        self.clear_options()
        self.display_bot_message(f"For {severity} migraines, please select a type:")
        self.add_option_button("With Aura", lambda: self.diagnose_migraine_with_aura(severity))
        self.add_option_button("Without Aura", lambda: self.diagnose_migraine_without_aura(severity))

    def diagnose_migraine_with_aura(self, severity):
        self.display_bot_message(
            f"{severity.capitalize()} migraine with aura diagnosis:\n• Consider preventive medications\n• Avoid known triggers\n• Seek advice if aura symptoms affect your vision\n\n"
            "More info: https://www.mayoclinic.org/diseases-conditions/migraine-headache"
        )

    def diagnose_migraine_without_aura(self, severity):
        self.display_bot_message(
            f"{severity.capitalize()} migraine without aura diagnosis:\n• OTC pain relievers may help\n• Maintain a headache diary\n• Consult a neurologist if headaches worsen\n\n"
            "More info: https://www.aaa.org/"
        )

    
    #New Subcategories for Menstrual/Period Pains
    
    def handle_menstrual_pain(self):
        self.display_bot_message(
            "It appears you're experiencing menstrual/period pains. Please select the severity:"
        )
        self.add_option_button("Mild", lambda: self.handle_menstrual_subcategories("mild"))
        self.add_option_button("Moderate", lambda: self.handle_menstrual_subcategories("moderate"))
        self.add_option_button("Severe", lambda: self.handle_menstrual_subcategories("severe"))

    def handle_menstrual_subcategories(self, severity):
        self.clear_options()
        self.display_bot_message(f"For {severity} menstrual pain, please choose the duration pattern:")
        self.add_option_button("Short Duration (<1 day)", lambda: self.diagnose_menstrual_short(severity))
        self.add_option_button("Long Duration (>1 day)", lambda: self.diagnose_menstrual_long(severity))

    def diagnose_menstrual_short(self, severity):
        self.display_bot_message(
            f"For {severity} menstrual pain lasting less than one day:\n• Consider OTC NSAIDs\n• Apply a warm compress\n• Keep a pain diary\n\n"
            "More info: https://www.sleepfoundation.org/articles/menstrual-cramps"
        )

    def diagnose_menstrual_long(self, severity):
        self.display_bot_message(
            f"For {severity} menstrual pain lasting more than one day:\n• It might indicate conditions like endometriosis\n• Consult a gynecologist\n• Consider hormonal treatments\n\n"
            "More info: https://www.endometriosis.org/"
        )

    
    #New Subcategories for Hypertension (Blood Pressure)
    
    def handle_hypertension(self):
        self.display_bot_message("You're concerned about hypertension. Please rate the severity:")
        self.add_option_button("Mild", lambda: self.handle_hypertension_subcategories("mild"))
        self.add_option_button("Moderate", lambda: self.handle_hypertension_subcategories("moderate"))
        self.add_option_button("Severe", lambda: self.handle_hypertension_subcategories("severe"))

    def handle_hypertension_subcategories(self, severity):
        self.clear_options()
        self.display_bot_message(f"For {severity} hypertension, please select a contributing factor:")
        self.add_option_button("Lifestyle-Related", lambda: self.diagnose_hypertension_lifestyle(severity))
        self.add_option_button("Genetic Factors", lambda: self.diagnose_hypertension_genetic(severity))

    def diagnose_hypertension_lifestyle(self, severity):
        self.display_bot_message(
            f"{severity.capitalize()} hypertension likely related to lifestyle:\n• Adopt a low-sodium diet and exercise\n• Monitor your blood pressure at home\n• Consult your doctor for lifestyle counseling\n\n"
            "More info: https://www.heart.org/en/health-topics/high-blood-pressure"
        )

    def diagnose_hypertension_genetic(self, severity):
        self.display_bot_message(
            f"{severity.capitalize()} hypertension with a genetic component:\n• Regular check-ups are essential\n• Discuss your family history with your doctor\n• Medication adjustments may be required\n\n"
            "More info: https://www.cdc.gov/bloodpressure/"
        )

    
    #New Subcategories for Back Pain
    
    def handle_back_pain(self):
        self.display_bot_message("Is your back pain in the lower or upper region?")
        self.add_option_button("Lower Back", lambda: self.handle_lower_back_subcategories())
        self.add_option_button("Upper Back", lambda: self.handle_upper_back_subcategories())

    def handle_lower_back_subcategories(self):
        self.clear_options()
        self.display_bot_message("For lower back pain, please choose a type:")
        self.add_option_button("Mechanical Pain", self.diagnose_lower_back_mechanical)
        self.add_option_button("Neuropathic Pain", self.diagnose_lower_back_neuropathic)

    def diagnose_lower_back_mechanical(self):
        self.display_bot_message(
            "Lower back mechanical pain:\n• Often due to poor posture or muscle strain\n• Engage in gentle stretches and strengthening exercises\n• Consider physiotherapy if pain persists\n\n"
            "More info: https://www.spine-health.com/conditions/lower-back-pain"
        )

    def diagnose_lower_back_neuropathic(self):
        self.display_bot_message(
            "Lower back neuropathic pain:\n• May be due to nerve compression or disc issues\n• Consult a specialist for imaging\n• Treatment may include medications and physical therapy\n\n"
            "More info: https://www.mayoclinic.org/diseases-conditions/herniated-disc"
        )

    def handle_upper_back_subcategories(self):
        self.clear_options()
        self.display_bot_message("For upper back pain, please choose a type:")
        self.add_option_button("Mechanical Pain", self.diagnose_upper_back_mechanical)
        self.add_option_button("Neuropathic Pain", self.diagnose_upper_back_neuropathic)

    def diagnose_upper_back_mechanical(self):
        self.display_bot_message(
            "Upper back mechanical pain:\n• Often due to poor ergonomics or muscle strain\n• Improve your workspace setup\n• Try targeted stretches\n\n"
            "More info: https://www.healthline.com/health/upper-back-pain"
        )

    def diagnose_upper_back_neuropathic(self):
        self.display_bot_message(
            "Upper back neuropathic pain:\n• May be related to nerve irritation\n• A thorough examination is advised\n• Treatment might include medication or therapy\n\n"
            "More info: https://www.spine-health.com/conditions/upper-back-pain"
        )

    
    #New Subcategories for Allergies
    
    def handle_allergies(self):
        self.display_bot_message("Are you dealing with seasonal, food, or other allergies?")
        self.add_option_button("Seasonal", lambda: self.handle_allergies_type("seasonal"))
        self.add_option_button("Food", lambda: self.handle_allergies_type("food"))
        self.add_option_button("Other", lambda: self.handle_allergies_type("other"))

    def handle_allergies_type(self, allergy_type):
        if allergy_type == "seasonal":
            self.clear_options()
            self.display_bot_message("For seasonal allergies, please choose your specific allergy type:")
            self.add_option_button("Dust Mite Allergy", lambda: self.handle_seasonal_allergy_detail("dust mite"))
            self.add_option_button("Pollen Allergy", lambda: self.handle_seasonal_allergy_detail("pollen"))
            self.add_option_button("Mold Allergy", lambda: self.handle_seasonal_allergy_detail("mold"))
            self.add_option_button("Pet Dander Allergy", lambda: self.handle_seasonal_allergy_detail("pet dander"))
        elif allergy_type == "food":
            self.handle_food_allergy_subcategories()
        elif allergy_type == "other":
            self.display_bot_message(
                "For other allergies:\n• Identify and avoid triggers\n• Consult with an allergist for testing and treatment\n\n"
                "More info: https://www.mayoclinic.org/diseases-conditions/allergies"
            )

    def handle_seasonal_allergy_detail(self, allergy):
        if allergy == "dust mite":
            self.display_bot_message(
                "Dust mite allergy diagnosis:\n• Symptoms: sneezing, itchy eyes\n• Use allergen-proof bedding and reduce humidity\n\n"
                "More info: https://www.aaaai.org/conditions-and-treatments/allergies/dust-mite-allergy"
            )
        elif allergy == "pollen":
            self.display_bot_message(
                "Pollen allergy diagnosis:\n• Symptoms: sneezing, nasal congestion, watery eyes\n• Keep windows closed during high pollen seasons\n\n"
                "More info: https://www.aaaai.org/conditions-and-treatments/allergies/pollen-allergy"
            )
        elif allergy == "mold":
            self.display_bot_message(
                "Mold allergy diagnosis:\n• Can cause respiratory issues\n• Reduce indoor moisture and remove visible mold\n\n"
                "More info: https://www.mayoclinic.org/diseases-conditions/mold-allergy"
            )
        elif allergy == "pet dander":
            self.display_bot_message(
                "Pet dander allergy diagnosis:\n• Symptoms: sneezing, respiratory issues\n• Regular cleaning and HEPA filters can help\n\n"
                "More info: https://www.aaaai.org/conditions-and-treatments/allergies/pet-allergy"
            )

    def handle_food_allergy_subcategories(self):
        self.clear_options()
        self.display_bot_message("For food allergies, please choose the specific allergen:")
        self.add_option_button("Dairy Allergy", self.diagnose_food_allergy_dairy)
        self.add_option_button("Nut Allergy", self.diagnose_food_allergy_nut)
        self.add_option_button("Seafood Allergy", self.diagnose_food_allergy_seafood)
        self.add_option_button("Egg Allergy", self.diagnose_food_allergy_egg)

    def diagnose_food_allergy_dairy(self):
        self.display_bot_message(
            "Dairy allergy diagnosis:\n• Symptoms: stomach upset, hives\n• Avoid dairy products and consult a nutritionist\n\n"
            "More info: https://www.foodallergy.org/dairy-allergy"
        )

    def diagnose_food_allergy_nut(self):
        self.display_bot_message(
            "Nut allergy diagnosis:\n• Can cause severe reactions, including anaphylaxis\n• Strict avoidance is key; carry epinephrine if prescribed\n\n"
            "More info: https://www.foodallergy.org/common-allergens/tree-nut-allergy"
        )

    def diagnose_food_allergy_seafood(self):
        self.display_bot_message(
            "Seafood allergy diagnosis:\n• Reactions can range from mild to severe\n• Avoid seafood and consult an allergist\n\n"
            "More info: https://www.foodallergy.org/common-allergens/seafood-allergy"
        )

    def diagnose_food_allergy_egg(self):
        self.display_bot_message(
            "Egg allergy diagnosis:\n• Often seen in children, but may persist\n• Avoid eggs and egg-containing products\n\n"
            "More info: https://www.foodallergy.org/common-allergens/egg-allergy"
        )

    
    #Remaining Existing Handlers
    
    def handle_digestive_issues(self):
        self.display_bot_message("Are you experiencing digestive issues such as stomach pain or acid reflux?")
        self.add_option_button("Stomach Pain", lambda: self.handle_digestive_issue_type("stomach"))
        self.add_option_button("Acid Reflux", lambda: self.handle_digestive_issue_type("reflux"))

    def handle_digestive_issue_type(self, issue_type):
        if issue_type == "stomach":
            self.display_bot_message(
                "For stomach pain:\n• Avoid irritating foods\n• Stay hydrated and try a bland diet\n• Consult a doctor if symptoms persist\n\n"
                "More info: https://www.mayoclinic.org/symptoms/abdominal-pain/basics/causes/sym-20050728"
            )
        elif issue_type == "reflux":
            self.display_bot_message(
                "For acid reflux:\n• Avoid trigger foods like spicy or fatty meals\n• Eat smaller, frequent meals\n• Consult a doctor if symptoms worsen\n\n"
                "More info: https://www.aaaai.org/conditions-and-treatments/allergies/acid-reflux"
            )

    def handle_arthritis(self):
        self.display_bot_message("Experiencing joint pain related to arthritis. How severe are your symptoms?")
        self.add_option_button("Mild", lambda: self.handle_arthritis_severity("mild"))
        self.add_option_button("Moderate", lambda: self.handle_arthritis_severity("moderate"))
        self.add_option_button("Severe", lambda: self.handle_arthritis_severity("severe"))

    def handle_arthritis_severity(self, severity):
        if severity == "mild":
            self.display_bot_message(
                "For mild arthritis symptoms:\n• Engage in low-impact exercise\n• Maintain a healthy weight\n• Consider OTC pain relief\n\n"
                "More info: https://www.arthritis.org/"
            )
        elif severity == "moderate":
            self.display_bot_message(
                "For moderate arthritis:\n• Consider physical therapy\n• Discuss pain management options with your doctor\n\n"
                "More info: https://www.cdc.gov/arthritis/"
            )
        elif severity == "severe":
            self.display_bot_message(
                "For severe arthritis:\n• Consult a healthcare professional for advanced treatment\n• Follow prescribed pain management strategies\n\n"
                "More info: https://www.arthritis.org/"
            )

    
    #Crisis Helpline
    
    def display_crisis_resources(self):
        crisis_message = "🚨 IMPORTANT: If you're in crisis or thinking about self-harm, please seek immediate help:\n\n"
        for country, resources in self.crisis_resources.items():
            crisis_message += f"{country} Resources:\n"
            for resource in resources:
                crisis_message += f"• {resource}\n"
            crisis_message += "\n"
        self.display_bot_message(crisis_message)

    def show_immediate_help(self):
        self.display_bot_message(
            "Please contact one of these resources immediately:\n• National Mental Health Helpline (India): 1800-599-0019\n"
            "• Contact a trusted friend or family member\n• Visit your nearest emergency room\n• In immediate danger, call local emergency services"
        )
        self.add_option_button("Safety Plan", self.show_safety_plan)

    def show_safety_plan(self):
        self.display_bot_message(
            "A safety plan can help during crisis:\n1. Recognize warning signs\n2. Use internal coping strategies\n3. Connect with supportive people\n"
            "4. Reach out to family or friends\n5. Consult a mental health professional\n6. Ensure a safe environment\n\n"
            "National Suicide Prevention Lifeline: https://suicidepreventionlifeline.org/wp-content/uploads/2016/08/Brown_StanleySafetyPlanTemplate.pdf"
        )

    def show_additional_resources(self):
        self.display_bot_message(
            "Additional resources:\n• WHO: https://www.who.int/health-topics/mental-health\n• Mental Health Foundation: https://www.mentalhealth.org.uk/\n"
            "• NIMH: https://www.nimh.nih.gov/\n• AIIMS: https://www.aiims.edu/en/departments-and-centers/departments.html\n• Mind: https://www.mind.org.uk/"
        )

    def find_local_resources(self):
        self.display_bot_message(
            "For mental health resources near you in India:\n• NIMHANS: https://nimhans.ac.in/\n• Indian Psychiatric Society: https://indianpsychiatricsociety.org/\n"
            "• The Live Love Laugh Foundation: https://thelivelovelaughfoundation.org/\n• AIIMS Psychiatry: https://www.aiims.edu/"
        )

    
    #Diabetes and Asthma
    
    def handle_diabetes(self):
        self.display_bot_message("Concerned about diabetes? Do you need help with high blood sugar or management tips?")
        self.add_option_button("High Blood Sugar", lambda: self.handle_diabetes_severity("high"))
        self.add_option_button("Management Tips", lambda: self.handle_diabetes_severity("management"))

    def handle_diabetes_severity(self, severity):
        if severity == "high":
            self.display_bot_message(
                "High blood sugar levels can be serious:\n• Monitor regularly\n• Follow dietary guidelines\n• Consult your healthcare provider\n\n"
                "American Diabetes Association: https://www.diabetes.org/"
            )
        elif severity == "management":
            self.display_bot_message(
                "Managing diabetes involves lifestyle changes:\n• Regular exercise\n• A balanced diet\n• Routine check-ups\n\n"
                "CDC Diabetes Info: https://www.cdc.gov/diabetes/"
            )

    def handle_asthma(self):
        self.display_bot_message("Are you experiencing asthma symptoms? How severe are they?")
        self.add_option_button("Mild", lambda: self.handle_asthma_severity("mild"))
        self.add_option_button("Moderate", lambda: self.handle_asthma_severity("moderate"))
        self.add_option_button("Severe", lambda: self.handle_asthma_severity("severe"))

    def handle_asthma_severity(self, severity):
        if severity == "mild":
            self.display_bot_message(
                "For mild asthma:\n• Avoid triggers\n• Use preventive inhalers if prescribed\n• Schedule regular check-ups\n\n"
                "Learn more: https://www.lung.org/lung-health-diseases/lung-disease-lookup/asthma"
            )
        elif severity == "moderate":
            self.display_bot_message(
                "For moderate asthma:\n• Follow your asthma action plan\n• Use rescue inhalers as needed\n• Monitor symptoms closely\n\n"
                "CDC Asthma Guidance: https://www.cdc.gov/asthma/"
            )
        elif severity == "severe":
            self.display_bot_message(
                "For severe asthma:\n• Seek immediate medical help if symptoms worsen\n• Strictly adhere to your doctor's advice\n\n"
                "More info: https://www.asthma.org.uk/"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = MentalHealthChatbot(root)
    root.mainloop()
