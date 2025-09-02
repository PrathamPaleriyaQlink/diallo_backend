import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from prompt.call_analysis_prompt import x_bucket_prompt, y_bucket_prompt

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
openai_client = OpenAI(
    api_key=OPENAI_API_KEY
)

bucket_prompt = {
    "x_bucket": x_bucket_prompt,
    "y_bucket": y_bucket_prompt
}


def get_call_analysis(transcribe: str, bucket: str):
    model = "gpt-4o-mini"
    instructions = bucket_prompt[bucket]

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
                            "Call_summary": { "type": "string" },
                            "Call_purpose": { "type": "string" },
                            "Sentiment_overall": { "type": "string", "enum": ["positive", "neutral", "negative"] },
                            "Sentiment_by_speaker": {
                            "type": "object",
                            "properties": {
                                "Agent_sentiment": { "type": "string", "enum": ["positive", "neutral", "negative"] },
                                "Customer_sentiment": { "type": "string", "enum": ["positive", "neutral", "negative"] }
                            },
                            "required": ["Agent_sentiment", "Customer_sentiment"],
                            "additionalProperties": False
                            },
                            "Payment_discussed": { "type": "boolean" },
                            "Payment_amount": { "type": ["string", "null"] },
                            "Payment_options_discussed": { "type": "array", "items": { "type": "string" } },
                            "Follow_up_required": { "type": "boolean" },
                            "Follow_up_details": { "type": ["string", "null"] },
                            "Agent_performance": { "type": "string" },
                            "Unresolved_issues": { "type": "array", "items": { "type": "string" } },
                            "Summary": { "type": "string" },
                            "Total_Score": { "type": "integer", "minimum": 0, "maximum": 10 },
                            "Individual_Scores": {
                            "type": "object",
                            "properties": {
                                "Greeting_&_Opening": { "type": "integer", "minimum": 0, "maximum": 10 },
                                "Objection_Handling": { "type": "integer", "minimum": 0, "maximum": 10 },
                                "Urgency_Creation": { "type": "integer", "minimum": 0, "maximum": 10 },
                                "Payment_Process_Clarity": { "type": "integer", "minimum": 0, "maximum": 10 },
                                "Empathy_&_Tonality": { "type": "integer", "minimum": 0, "maximum": 10 },
                                "Call_Management_&_Closing": { "type": "integer", "minimum": 0, "maximum": 10 }
                            },
                            "required": [
                                "Greeting_&_Opening",
                                "Objection_Handling",
                                "Urgency_Creation",
                                "Payment_Process_Clarity",
                                "Empathy_&_Tonality",
                                "Call_Management_&_Closing"
                            ],
                            "additionalProperties": False
                            },
                            "Positives": { "type": "array", "items": { "type": "string" } },
                            "Improvements": { "type": "array", "items": { "type": "string" } }
                        },
                        "required": [
                            "Call_summary",
                            "Call_purpose",
                            "Sentiment_overall",
                            "Sentiment_by_speaker",
                            "Payment_discussed",
                            "Payment_amount",
                            "Payment_options_discussed",
                            "Follow_up_required",
                            "Follow_up_details",
                            "Agent_performance",
                            "Unresolved_issues",
                            "Summary",
                            "Total_Score",
                            "Individual_Scores",
                            "Positives",
                            "Improvements"
                        ],
                        "additionalProperties": False
                    } 
                }
            }
        )

        print(response)
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
