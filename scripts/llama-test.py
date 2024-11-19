import ollama
import pdfplumber
import re

model = 'llama3.1'

pdf_text = ""

with pdfplumber.open(r"data\manuals\GOVPUB-D101-PURL-LPS37172.pdf") as pdf:
  # for page in pdf.pages:
  #   pdf_text += page.extract_text()

  for i in range(10, 12): # (10, 17) only extracting text from page 3 to 25 that has content headers and their resptive pages
    pdf_text += pdf.pages[i].extract_text()

cleaned_text = re.sub(r'\s+', ' ', pdf_text).strip().lower()

def full_prompt(prompt, knowledge):
  res = f"""

    ### Notes: Keep your answers simple, short and crisp
    1. Make sure your answer STRICTLY mentions the SECTION and the PAGE number.
    2. Ensure the chapter details have details on correct down to the subsections e.g "1.2.4"
    3. Keep the description of your answer short
    4. Return the response in JSON format
    5. If there is descrepency in the question or if there are multiple answers. Pick the mostly likely answer.


    <EXAMPLE>
      INPUT: Could you show me where the information on the Flight Control System is?
      OUTPUT:
      {{
        "description":"Flight Control system information is available in the contents",
        "section":"1.2.5",
        "page": "1-13"
      }}
    </EXAMPLE>

    <EXAMPLE>
      INPUT: Where can I find details about Hand-held Coil?
      OUTPUT:
      {{
        "description": "Hand-held Coil details are available",
        "section": "1.4.8.1.2",
        "page": "1-34"
      }}
    </EXAMPLE>

    <EXAMPLE>
      INPUT: Where is the information on Ultrasonic Method?
      OUTPUT:
      {{
        "description": "Information on Ultrasonic Method (UT) available",
        "section": "1.4.12",
        "page": "1-38"
      }}
    </EXAMPLE>

    ### Instruction: {prompt}

    ### Knowledge: {knowledge}


    # Context: You are a AI assistant meant to help maintenance personal working on critical systems. Provide a clear, correct and concise response.

    # Response:"""

  return res


modelfile='''
FROM llama3.2:1b
SYSTEM You are a mechanic assistant providing document assistance for the Cessna 150 1977 Maintenance Manual.
'''

# QA = "What precautions should be taken when applying Dow Corning DC7 to the tubular strut during main landing gear installation?"

# QA = "can i use Dow Corning DC7 to surfaces i will need to paint"

QA = input("[ENTER YOUR QUERY HERE:] ")
stream = ollama.chat(model=model, messages=[
  {
    'role': 'user',
    'content': full_prompt(QA, cleaned_text),
  },
], stream=True)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)

