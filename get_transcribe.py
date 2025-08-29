from groq import Groq
from openai import OpenAI
import os

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

groq_client = Groq(api_key=GROQ_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)
deepgram = DeepgramClient()

def transcribe_audio(file_path: str, model: str = "whisper-large-v3-turbo") -> str:
    try:
        with open(file_path, "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=(file_path, file.read()),
                model=model,
                language="",
                prompt="",
                response_format="verbose_json",
            )
            return transcription.text
    except Exception as e:
        print(f"Transcription Error: {e}")
        raise e
    
def transcribe_audio_openai(file_path: str, model: str = "whisper-1"):
    try:
        with open(file_path, "rb") as file:
            transcription = openai_client.audio.transcriptions.create(
                file=(file_path, file.read()),
                model=model
            )
            return transcription.text
    except Exception as e:
        print(f"Transcription Error: {e}")
        raise e
    
def transcribe_audio_deepgram(file_path: str, model: str = "nova-2"):
    options = PrerecordedOptions(
            model=model,
            language="hi",
            smart_format=True,
            punctuate=True,
            paragraphs=True,
            utterances=True,
            diarize=True,
    )
    try:
        with open(file_path, "rb") as file:
            payload: FileSource = {
                "buffer": file.read()
            }
            response = deepgram.listen.rest.v("1").transcribe_file(
                payload,
                options,
            )
            return response["results"]["channels"][0]["alternatives"][0]["paragraphs"]["transcript"]
    except Exception as e:
        print(f"Transcription Error: {e}")
        raise e

if __name__ == "__main__":  
    # print(
    #     transcribe_audio("apex2.mp3")
    # )
    print("\Deephram")
    print(
        transcribe_audio_deepgram(
            "apex2.mp3"
        )
    )

# नमस्कार एपेक्स ओस्पिटल्स. हलो. जी बताईए सर. हलो. आवाज आ रही है सर आपको मेरी? एपेक्स ओस्पिटल्स बोल रहे हो क्या? जी सर बताईए. हाँ जी वो ऐसे करें. वो क्या मतलब? वो क्या मतलब? आज लग जाएगी न? सर चीज़ की 30 तारीक डेट थी. आप थोड़ा एक्स्प्लेइन कर पाएंगे? क्या जानकारी आप लेना चाहें? वो क्या मतलब? वो क्या मतलब? जी. 30 तारीक थी. कल की. कल बारिश आने वाली है. बारिश आने वाली है. अब आज लग जाएगी न? सर इसके लिए आप एक बार लाइन से बने रहे हैं. हम चेक कर लेते हैं. तो लाइन से बने रहने के लिए धन्यवाद सर. हाँ जी. जी इसके लिए सर जो डॉक्टर के कोडिनेट हैं, उनको कि इनके नंबर आपको शेयर कर दिये गए हैं. आप एक बार आने से पहले इनके बात कर लीजियेगा. तो यह आपकी नौ बज़े के बात में भी आप इनको कॉल कर सकते हैं. सर जेस्ट करेंगे. नौ बज़े बाद हो गया है? जी सर आप इनको एक बार कॉल कर लीजियेगा या आपको जानकारी प्लप्स करवा देंगे. नंबर नहीं है सर. जी सर यह जो टीट्वेंट आप ले रहे हैं, एटेक्स ओस्पिटिल्स में किस ब्रांच से ले रहे हैं? यह मानसरोर में. मानसरोर ब्रांच. डॉक्टर के जो कोडिनेट हैं, इनके नंबर हम आपको वर्टसब पर शेयर कर देते हैं. आप एक बार इनके बात कर लीजियेगा, या आपको जानकारी प्लप्स करवा देंगे. हां जी, एक बार. जी सर, आप एक बार इनको कॉल कर लीजियेगा, नौ बज़े के एपरोप्स कॉल कर लीजियेगा. सर मैं भी इसका मैं आपकी बात नहीं हो पाएगी, तो आप एक बार इनसे बात कर लीजियेगा. हां जी, एक बार नौ बज़े तक तो हमारे वहाँ बुलाते हैं, फिर लेके जाएंगे आने में, तो उनको लेके दो ढ़ायेंगे जाएंगे. जी सर, सज़ेस्ट करेंगे सर, सि                                                                                                                                                                                        िंगल कॉल अबी आप कर सकते हैं, अगर कॉल रिसीव हो जाता है, तो किनकि डॉक्टर के जब ओपीडी रहती है, मोस्तली डॉक्टर के जो कोडिनेट रहते हैं, उसी समय अवेलेबल हो पाते हैं. बाकि आप एक बार कॉल कर लीजियेगा, अगर नौ तक आप विजिट करना चाहें, तो नंबर                       र आपको वेटसेब पर बेज़ दिये गए हैं. जी, नाम जान सकते हैं सर, पेशेंट का? चिकन वाले. जी, क्या कोई और जानकारी आप इसके लावा लेना चाहें? नहीं, नहीं, बस मुझे वो आज लग जाएगा, वो आज लग जाएगा. कल के लिए, 30 तारीक के लिए फोन आए था वहां से? ज                          जी सर. आज आजाएगी, मैं लेकर दूँगा. आज एक बार जो नंबर आपको भेजे गए हैं, आप इस नंबर पर कॉल कर लीजियेगा. ठीक है. धन्यवाद सर एपेक्स ओस्पिल्स सुनने के लिए, आपका दिन शुब है.


# Namaskar, Apex Hospitals. Hello? Yes sir, tell me. Hello? Sir, can you hear me? Are you calling from Apex Hospitals? Yes sir, tell me. Yes, I am. What do you mean? Our date was 30th, it will be today, right? Sir, what was the 30th date? Can you explain what information you want to get? What do you mean by 30th? The date was 30th, yesterday. It rained yesterday. It didn't rain today. It rained yesterday. It will rain today. Sir, can you stand in the queue for a moment? Sure. Okay. Sir, can you stand in the queue for a moment? Thank you for standing in the queue, sir. Hi. For this, the number of the doctor's coordinator has been shared with you. You can talk to him before coming. Or you can call him after 9 o'clock. Talk to him after 9 o'clock. Yes sir, you can call him once. He will give you the information. What is the number? Sir, the treatment you are taking is from Apex Hospitals. Yes, Mansroor. Mansroor, okay. We will share the number of the doctor's coordinator on WhatsApp. You can talk to him once. He will give you the information. Can I talk to him? Yes sir, you can call him once. Call him after 9 o'clock. Sir, I can't talk to you right now. You can talk to him once. Okay sir, I will call him after 9 o'clock. Two people are going to come. Two people and two doctors will come. Sir, we would suggest you to do single call if you can. If the call is received, because the doctor's coordinator is available at the moment. If you want to visit by 9 o'clock, you can call once. You are sending the number on WhatsApp. What is the patient's name? Sir, you can send the patient's name. Kitchen Lal. Do you want to take any other call? No, no. I will be busy today. That's why I am going. I got a call for 3 o'clock yesterday. Yes, sir. I will come today. I am at the office. Okay, sir. You can call on the number you have been sent. Okay. Thank you, sir. Thank you, sir. I wish you a good day. Thank you.

# नमश्कार अपेक्स ओफ़बिटल्स अलो जी बताईगे सर अलो आवाज आड़ी है सर आपको मेरी अपेक्स ओफ़बिटल्स के साथ बोर रहे हूँ क्या जी सर बताईगे वो ऐसे ही करें वो क्या मलग है सर इसके लिए आप एक बार लाइन भी बने रहे हैं हम चेक कर लेते हैं लाइन पर बने रहने के लिए धन्यवाद सर आज़े जी इसके लिए सर जो डॉक्टर के कोडिनेट हैं उनको के इनके नंबर आपको शेर कर दिये गए हैं आप एक बार आने से पहले इनके बात कर लीज़ेगा पर यह आपकी नो बज़े के बाद में भी आप इनको कॉल कर सकते हैं नो बज़े बात होगी यह? जी सर आप इनको एक बार कॉल कर लीजेगा यह आपको जानकरी कलब्ब्ट करवा देंगे नमबर नहीं है चुपर? जी सर यह एक जो टीट्मेंट आप ले रहे हैं एपिक्स आस्पुर्टीजी जिस गांच से ले रहे हैं या मांसरोर में? मांसरोर गांच से जी सर आप एक बार इनको कॉल कर लीजेगा नौ बज़े के एपरोक्स कॉल कर लीजेगा सर में भी इस समय आपकी बात नहीं हो पाएगी तो आप एक बार इनसे बात कर लीजेगा अनने एक नौ बज़े के बार में तर बॉलाते हैं तो नेटु जाएँ आने में पर 2-2.5 नहीं आनें जी जिसके लिए आप कॉल कर सकते हैं अगर खॉल कर लिजेगा थो तो क्योंकि डॉक्टर की लिए प्लीडि रहती हैं अपने डॉक्टर की को कीछन ला लें क्या कोई ओर अपकारी आप खेला ला लेना चाहरें नहीं नहीं बस मुझे आज लग जाएँ कि हम इसलिए जब वही बात हैं कॉल कर लेगा 30 आई के लिए खॉल आयेता हूँ आथे अगर मैं आज जाएँ माना जाएँ मैं लेकर बिरा अपिस माना जाएँ तो आप एक बार जो नंबर आपको भिज़े गए हैं आप इस नंबर पर कॉल कर लेगा ठीक है धन्यवाद सर्वाद टेक्ट आफ्ट केल सिनने के लिए आपका दिन शुबू धन्यवाद सर्वाद टेक्ट आफ्ट केल सिनने के लिए आपका दिन शुबू

# Speaker 0: नमस्कार, AX

# Speaker 1: Hospital. Hello.

# Speaker 0: जी, बताइए sir. Hello. आवाज़ आ रही है sir आपको मेरी? से बोल रहे हो क्या? जी sir, बताइए.

# Speaker 1: हां जी, वह ऐसे ही करे, वह क्या मतलब वह क्या date हमारी तीस तारीख, कल आज आज लग जाएगी ना?

# Speaker 0: Sir किस चीज़ की तीस तारीख date थी, आप थोड़ा explain कर पाएंगे क्या जानकारी आप लेना चाह रहे हैं?

# Speaker 1: नहीं वह क्या मतलब वह क्या मतलब वह क्या वह लगी थी demo? जी. तो क्या होगा कि तीस तारीख, तीस तारीख थी कल की. जी. कल कल बारिश आने हुआ.

# बारिश में ही आने में. बारिश आ रही थी कल. जी. अब आज लगवाना, आज का आज लग जाएगा, आज

# Speaker 0: जाएगा. Sir इसके लिए आप एक बार line पर बने रहें, हम check कर लेते हैं. Line पर बने रहने के लिए धन्यवाद sir.

# Speaker 1: हां जी.

# Speaker 0: जी इसके लिए sir जो doctor doctor के coordinate हैं उनको क्या इनके number आपको share कर दिए गए हैं. आप एक बार आने से पहले इनसे बात कर लीजिएगा sir या फिर नौ बजे के बाद में भी आप इनको call कर सकते हैं. तो suggest करेंगे क                     कि

# Speaker 1: नौ बजे बात हो गई है?

# Speaker 0: जी sir, आप इनको एक बार call कर लीजिएगा, यह आपको जानकारी उपलब्ध करवा देंगे.

# Speaker 1: Number number नहीं है ना

# Speaker 0: तो फिर. जी, sir यह जो treatment आप ले रहे हैं Ethics Opocities किस branch से ले रहे हैं?

# Speaker 1: यहां मांसरोर में.

# Speaker 0: मांसरोर branch से. जी. Doctor के जो co ordinate हैं इनके number हम आपको WhatsApp पर share कर देते हैं. आप एक बार इनसे बात कर लीजिएगा या आपको जानकारी उपलब्ध करवा देंगे sir.

# Speaker 1: कहां से हो जाएगी ना बात?

# Speaker 0: जी sir, आप एक बार इनको call कर लीजिएगा, नौ बजे के approx call कर लीजिएगा sir. Maybe इस समय आपकी बात नहीं हो पाएगी. तो आप एक बार इनसे बात कर लीजिएगा.

# Speaker 1: हां जी कैसा है मैं एक नौ बजे तक तो हमारे वहां बुलाते हैं फिर लेकर जाएंगे आने में. इसलिए दो घंटे लगते हैं दो ढाई दिन जाएंगे.

# Speaker 0: जी then suggest करेंगे sir single call अभी आप कर सकते हैं अगर call receive हो जाता है तो क्योंकि doctor की जब OPD रहती है mostly doctor के जो coordinate रहते हैं उसी समय available हो पाते हैं sir. बाकी आप एक बार call क                कर लीजिएगा अगर जैसे नौ तक आप visit करना चाह रहे हैं तो number आपको WhatsApp पर भेज दिए गए हैं sir.

# Speaker 1: भेज दो sir.

# Speaker 0: जी, नाम जान सकते हैं sir patient जी?

# Speaker 1: किशन लाल.

# Speaker 0: जी, क्या कोई और जानकारी

# Speaker 1: आप इसके अलावा आप लेना चाह रहे हैं? नहीं नहीं, बस मुझे वह है भाई, आज लग जाएगा नहीं कि हम इसलिए करवा चुके भाई बात है. कल के लिए, तीस तारीख के लिए तो phone आया था वहां से.

# Speaker 0: जी sir.

# Speaker 1: अब मैं आज आ जाएगी मान लो, मैं लेकर फिर office में आना था.

# Speaker 0: जी sir, तो आप एक बार जो number आपको भेजे गए हैं आप इस number पर call कर लीजिएगा sir.

# Speaker 1: ठीक है.

# Speaker 0: धन्यवाद sir आकाश hospital में जुडने के लिए. आपका दिन शुभ हो.