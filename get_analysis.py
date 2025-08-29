import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
openai_client = OpenAI(
    api_key=OPENAI_API_KEY
)


def get_call_analysis(transcribe: str):
    model = "gpt-4o-mini"
    instructions = """
Prompt for AI Call Analysis Agent - Diallo

You are a Call Quality Analyzer for Diallo.
You will receive a call transcription in JSON format where each item contains:
- start: start time of speech (seconds)
- end: end time of speech (seconds)
- text: exact spoken content
- speaker: "Agent" or "Customer" in sequence

Your task: Analyze the call strictly based on the transcript and generate a structured report.

OUTPUT FORMAT:
- Call Disposition (string)
- Call Summary (string)
- Purpose (string)
- Area of improvement (string or null)
- Scores (0–10 scale for key parameters):
    -- Greeting & Customer Identification
    -- Self Introduction & Reaching right party contact
    -- Purpose of call
    -- Complete & Correct information Minor Impact
    -- Effective Probing
    -- Objection Handling / Resolution
    -- Negotiation
    -- Urgency Creation
    -- Online Payment Pitching
    -- Active Listening
    -- Clarity of Speech & Rate of Speech
    -- Tone & Voice Modulation
    -- Empathy
    -- Confidence
    -- Language & Grammar
    -- Telephone Etiquettes & Hold Procedure
    -- Summarization
    -- Closing
- Reason for delay (string or null)
- Remark (string or null)
- Incomplete / Incorrect information / False Commitment (string)
- Rudeness / Unprofessionalism / Call Disconnection (string)
- CRM protocol - Disposition (string)
- Positives (array of strings)
- Improvements (array of strings)
- Marked Transcript (string with only problematic lines in markdown)

RULES:
- Use transcript only, no assumptions.
- Score every relevant field objectively from 0–10.
- Be specific in positives & improvements.
- Marked Transcript: list exact problematic lines with [Issue: ...].
- For GOOD calls, check:
    * Agent follows full protocol for taking online payments
    * Objection handling done effectively with solutions
    * Pitching extensions/payment options clearly (including debit card & alternatives)
    * Urgency created with consequences of non-payment + funding options from friends/family
    * Tone polite, energetic, with clear and customer-matched speech rate
- For BAD calls, check:
    * Greeting/self-introduction missing
    * Relationship with customer not confirmed
    * Amount/payment details missing
    * Alternate number not collected
    * Conference option not offered
    * Callback time not asked
    * Closing missing
    * Late opening or loan details missing
    * Negative probing (e.g., "how much can you pay")
    * No family/friend option for payment
    * Source of payment not asked
    * Lack of urgency creation
    * Dead air after disconnection
    * Rude/unprofessional closing
"""

    try:
        response = openai_client.responses.create(
            model=model,
            instructions=instructions,
            input=transcribe,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "diallo_call_analysis",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "call_disposition": {"type": "string"},
                            "call_summary": {"type": "string"},
                            "purpose": {"type": "string"},
                            "area_of_improvement": {"type": ["string", "null"]},
                            "scores": {
                                "type": "object",
                                "properties": {
                                    "greeting_customer_identification": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "self_introduction_reaching_party": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "purpose_of_call": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "complete_correct_info_minor_impact": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "effective_probing": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "objection_handling_resolution": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "negotiation": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "urgency_creation": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "online_payment_pitching": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "active_listening": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "clarity_speech_rate": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "tone_voice_modulation": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "empathy": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "confidence": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "language_grammar": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "telephone_etiquettes": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "summarization": {"type": "integer", "minimum": 0, "maximum": 10},
                                    "closing": {"type": "integer", "minimum": 0, "maximum": 10}
                                },
                                "required": [
                                    "greeting_customer_identification",
                                    "self_introduction_reaching_party",
                                    "purpose_of_call",
                                    "complete_correct_info_minor_impact",
                                    "effective_probing",
                                    "objection_handling_resolution",
                                    "negotiation",
                                    "urgency_creation",
                                    "online_payment_pitching",
                                    "active_listening",
                                    "clarity_speech_rate",
                                    "tone_voice_modulation",
                                    "empathy",
                                    "confidence",
                                    "language_grammar",
                                    "telephone_etiquettes",
                                    "summarization",
                                    "closing"
                                ],
                                "additionalProperties": False
                            },
                            "reason_for_delay": {"type": ["string", "null"]},
                            "remark": {"type": ["string", "null"]},
                            "incorrect_info_false_commitment": {"type": "string"},
                            "rudeness_unprofessionalism": {"type": "string"},
                            "crm_protocol_disposition": {"type": "string"},
                            "positives": {"type": "array", "items": {"type": "string"}},
                            "improvements": {"type": "array", "items": {"type": "string"}},
                            "marked_transcript": {"type": "string"}
                        },
                        "required": [
                            "call_disposition",
                            "call_summary",
                            "purpose",
                            "area_of_improvement",
                            "scores",
                            "reason_for_delay",
                            "remark",
                            "incorrect_info_false_commitment",
                            "rudeness_unprofessionalism",
                            "crm_protocol_disposition",
                            "positives",
                            "improvements",
                            "marked_transcript"
                        ],
                        "additionalProperties": False
                    }
                }
            }
        )

        return json.loads(response.output[0].content[0].text)
    except Exception as e:
        print(f"Analysis Error: {e}")
        raise e


if __name__ == "__main__":
    response = get_call_analysis(transcribe="""Speaker 0: Hello

Speaker 1: hello

Speaker 0: hello. जी बताइए sir.

Speaker 1: मेरी जनथम board से भी हो गए हैं क्या वापस?

Speaker 0: Sir इसके लिए हम आपको वहां के number share कर देते हैं. Sir. Same number आपको WhatsApp पर available है and यह जानकारी आपको कब मिली थी sir कि रनथम board, Seविकाs Hospital, सवाए माधवपुर बंद हो चुका है?

Speaker 1: Sir, मैं तो वहां पर तो शाम को discharge करना पड़ा है मुझे इसलिए urgent में.

Speaker 0: जी sir. यह आप बता पाएंगे sir approx कितनी पुरानी बात है?

Speaker 1: यह sir दो से तीन दो पुरानी बात है.

Speaker 0: जी हम आपको number share कर रहे हैं sir. वहां के reception का यह number है. आप एक बार इस पर बात करिएगा. जो भी जानकारी आप लेना चाह रहे हैं यह आपको उपलब्ध करवा देंगे.

Speaker 1: बता दो, चालू number बताना sir please?

Speaker 0: बिल्कुल sir, हम आपको WhatsApp पर share कर रहे हैं. आप इस पर call कर लीजिएगा.

Speaker 1: उन्होंने purchase कर दिया था, वह number बंद आ रहा है.

Speaker 0: जी sir, हम आपको जो restriction का number है, वह share कर रहे हैं, तो आप एक बार इस पर call कर लीजिए. Ok. जी, कोई और जानकारी इसके अलावा लेना चाहेंगे?

Speaker 1: मुझे भी एक पूछना है कि hospital चालू हो गया है क्या?

Speaker 0: जी, आप इस number पर call कर लीजिएगा sir. जानकारी आपको दे दी जाएगी. नाम जान सकते हैं patient का?

Speaker 1: हां.

Speaker 0: जी, बता दीजिए sir.

Speaker 1: आप WhatsApp share कर दो, मैं उसको call कर लूंगा, ok

Speaker 0: sir? बिल्कुल sir, हमने आपको WhatsApp पर share कर दिया है.

Speaker 1: ठीक है.""")
    print(json.dumps(response, indent=2))
