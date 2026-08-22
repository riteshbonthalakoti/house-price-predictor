import os
import sys
import json
import subprocess
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"

FORM_TITLE = "Session Feedback — Machine Learning & AI Basics"
FORM_DESCRIPTION = "Thanks for joining today! Your honest feedback helps me improve — this takes under a minute. Name is optional."

def create_form():
    if not CREDENTIALS_FILE.exists():
        print("\n" + "="*60)
        print("[!] credentials.json NOT FOUND!")
        print("="*60)
        print("\nTo allow Google Forms API authorization:")
        print("1. Go to Google Cloud Console: https://console.cloud.google.com/apis/credentials")
        print("2. Click 'Create Credentials' -> 'OAuth client ID' -> Application type: 'Desktop app'")
        print("3. Click 'Download JSON', rename the file to 'credentials.json', and save it in:")
        print(f"   {CREDENTIALS_FILE}")
        print("\nThen run this script again: python scripts/create_google_form.py")
        print("="*60 + "\n")
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
            print("Please click 'Allow' in the browser popup window.\n")
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    service = build('forms', 'v1', credentials=creds)

    # 1. Create empty form
    print("📝 Creating Google Form...")
    form_body = {
        "info": {
            "title": FORM_TITLE,
            "documentTitle": FORM_TITLE
        }
    }
    res = service.forms().create(body=form_body).execute()
    form_id = res['formId']
    print(f"✅ Form created! ID: {form_id}")

    # 2. Add description and questions
    print("📋 Adding fields and questions...")
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
            # Q1: Name (optional) - Short Answer
            {
                "createItem": {
                    "item": {
                        "title": "Name (optional)",
                        "questionItem": {
                            "question": {
                                "required": False,
                                "textQuestion": {}
                            }
                        }
                    },
                    "location": {"index": 0}
                }
            },
            # Q2: Overall Rating - Scale 1-5
            {
                "createItem": {
                    "item": {
                        "title": "How would you rate today's session overall?",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "scaleQuestion": {
                                    "low": 1,
                                    "high": 5,
                                    "lowLabel": "Poor",
                                    "highLabel": "Excellent"
                                }
                            }
                        }
                    },
                    "location": {"index": 1}
                }
            },
            # Q3: Concept Clarity - Scale 1-5
            {
                "createItem": {
                    "item": {
                        "title": "How clear was the explanation of ML concepts?",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "scaleQuestion": {
                                    "low": 1,
                                    "high": 5,
                                    "lowLabel": "Confusing",
                                    "highLabel": "Very Clear"
                                }
                            }
                        }
                    },
                    "location": {"index": 2}
                }
            },
            # Q4: Live Demo Usefulness - Choice
            {
                "createItem": {
                    "item": {
                        "title": "Did the live demo (house price prediction) help you understand the concepts better?",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [
                                        {"value": "Yes, a lot"},
                                        {"value": "Somewhat"},
                                        {"value": "Not really"}
                                    ]
                                }
                            }
                        }
                    },
                    "location": {"index": 3}
                }
            },
            # Q5: Audio/Session Quality - Choice
            {
                "createItem": {
                    "item": {
                        "title": "Was the audio/session quality okay throughout?",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [
                                        {"value": "Yes, no issues"},
                                        {"value": "Had some minor issues"},
                                        {"value": "Significant issues"}
                                    ]
                                }
                            }
                        }
                    },
                    "location": {"index": 4}
                }
            },
            # Q6: One thing to improve - Paragraph
            {
                "createItem": {
                    "item": {
                        "title": "What's one thing that could be improved?",
                        "questionItem": {
                            "question": {
                                "required": False,
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    "location": {"index": 5}
                }
            },
            # Q7: Future Topics - Paragraph
            {
                "createItem": {
                    "item": {
                        "title": "Any topics you'd like covered in a future session?",
                        "questionItem": {
                            "question": {
                                "required": False,
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    "location": {"index": 6}
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
    
    return responder_url

if __name__ == '__main__':
    create_form()
