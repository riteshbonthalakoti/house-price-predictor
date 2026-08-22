import os
import sys
import json
import subprocess
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"

FORM_TITLE = "LearnDepth™ — Session Feedback: Machine Learning & AI Basics"
FORM_DESCRIPTION = "Thank you for attending today's LearnDepth™ Live Workshop! Please take 30 seconds to share your quick feedback so we can keep delivering high-impact sessions."

def create_form():
    if not CREDENTIALS_FILE.exists():
        print("\n" + "="*60)
        print("[!] credentials.json NOT FOUND!")
        print("="*60)
        print("Please place credentials.json in the project root directory.")
        return None

    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        print("Installing required Google API packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "google-api-python-client", "google-auth-httplib2", "google-auth-oauthlib"])
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build

    SCOPES = ['https://www.googleapis.com/auth/forms.body']

    creds = None
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("\n[+] Opening browser for Google Forms authorization...")
            print("Please sign in and click 'Allow' in the browser window.\n")
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    service = build('forms', 'v1', credentials=creds)

    # 1. Create empty form
    print("[+] Creating LearnDepth Google Form...")
    form_body = {
        "info": {
            "title": FORM_TITLE,
            "documentTitle": FORM_TITLE
        }
    }
    res = service.forms().create(body=form_body).execute()
    form_id = res['formId']
    print(f"SUCCESS: Form created! ID: {form_id}")

    # 2. Add description and questions (Optimized for <30 sec response time)
    print("[+] Adding optimized MCQ questions...")
    update_body = {
        "requests": [
            # Update Form Description
            {
                "updateFormInfo": {
                    "info": {
                        "description": FORM_DESCRIPTION
                    },
                    "updateMask": "description"
                }
            },
            # Q1: Overall Session Rating - Scale 1-5
            {
                "createItem": {
                    "item": {
                        "title": "1. How would you rate today's LearnDepth™ session overall?",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "scaleQuestion": {
                                    "low": 1,
                                    "high": 5,
                                    "lowLabel": "Poor",
                                    "highLabel": "Outstanding ⭐"
                                }
                            }
                        }
                    },
                    "location": {"index": 0}
                }
            },
            # Q2: Concept Clarity - Scale 1-5
            {
                "createItem": {
                    "item": {
                        "title": "2. How clear was the explanation of Machine Learning concepts?",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "scaleQuestion": {
                                    "low": 1,
                                    "high": 5,
                                    "lowLabel": "Confusing",
                                    "highLabel": "Super Clear 💡"
                                }
                            }
                        }
                    },
                    "location": {"index": 1}
                }
            },
            # Q3: Session Pacing - MCQ
            {
                "createItem": {
                    "item": {
                        "title": "3. How was the pace of the workshop?",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [
                                        {"value": "Perfect speed — easy to follow"},
                                        {"value": "A bit fast in some parts"},
                                        {"value": "A bit slow — could move faster"}
                                    ]
                                }
                            }
                        }
                    },
                    "location": {"index": 2}
                }
            },
            # Q4: Live House Price Predictor Demo - MCQ
            {
                "createItem": {
                    "item": {
                        "title": "4. Did the live House Price Predictor demo help connect theory to real code?",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [
                                        {"value": "Loved it! Made concepts crystal clear"},
                                        {"value": "Helpful, but wanted to see more code detail"},
                                        {"value": "Needs more step-by-step explanation"}
                                    ]
                                }
                            }
                        }
                    },
                    "location": {"index": 3}
                }
            },
            # Q5: Audio/Session Quality - MCQ
            {
                "createItem": {
                    "item": {
                        "title": "5. Was the audio and stream quality acceptable throughout?",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [
                                        {"value": "Flawless audio & video"},
                                        {"value": "Had minor audio/lag glitches"},
                                        {"value": "Significant technical issues"}
                                    ]
                                }
                            }
                        }
                    },
                    "location": {"index": 4}
                }
            },
            # Q6: Future Topics - MCQ + Other
            {
                "createItem": {
                    "item": {
                        "title": "6. What topic would you like LearnDepth™ to cover in our next workshop?",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [
                                        {"value": "Deep Learning & Neural Networks"},
                                        {"value": "LLMs, RAG & AI Agents"},
                                        {"value": "Computer Vision & Image Processing"},
                                        {"value": "Deploying ML Models to Cloud Production (FastAPI/Docker)"},
                                        {"isOther": True}
                                    ]
                                }
                            }
                        }
                    },
                    "location": {"index": 5}
                }
            },
            # Q7: Open Feedback - Paragraph (Optional)
            {
                "createItem": {
                    "item": {
                        "title": "7. Any additional suggestions or thoughts for us? (Optional)",
                        "questionItem": {
                            "question": {
                                "required": False,
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    "location": {"index": 6}
                }
            },
            # Q8: Name & Contact - Short Answer (Optional)
            {
                "createItem": {
                    "item": {
                        "title": "Your Name or Email (Optional)",
                        "questionItem": {
                            "question": {
                                "required": False,
                                "textQuestion": {}
                            }
                        }
                    },
                    "location": {"index": 7}
                }
            }
        ]
    }

    service.forms().batchUpdate(formId=form_id, body=update_body).execute()
    
    # Get updated form info to retrieve responder URI
    updated_form = service.forms().get(formId=form_id).execute()
    responder_url = updated_form.get('responderUri')
    
    print("\n" + "="*60)
    print("SUCCESS: GOOGLE FORM CREATED SUCCESSFULLY!")
    print("="*60)
    print(f"Edit Form URL:  https://docs.google.com/forms/d/{form_id}/edit")
    print(f"Share Form URL: {responder_url}")
    print("="*60 + "\n")
    
    # Auto-update resources.html if available
    resources_file = BASE_DIR / "resources.html"
    frontend_resources_file = BASE_DIR / "frontend" / "resources.html"
    if responder_url and resources_file.exists():
        content = resources_file.read_text(encoding='utf-8')
        new_content = content.replace('href="#"', f'href="{responder_url}"')
        resources_file.write_text(new_content, encoding='utf-8')
        if frontend_resources_file.exists():
            frontend_resources_file.write_text(new_content, encoding='utf-8')
        print(f"[+] Automatically updated resources.html with share URL: {responder_url}")

    return responder_url

if __name__ == '__main__':
    create_form()
