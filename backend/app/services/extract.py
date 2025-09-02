import openai
from app.config import settings
from app.schemas import ExtractionResult
import json


class LLMService:
    """LLM service for text extraction and analysis"""

    def __init__(self):
        openai.api_key = settings.openai_api_key

    def extract_information(self, transcript_text: str) -> ExtractionResult:
        """Extract structured information from call transcript"""

        system_prompt = """
        את/ה ממלא/ת תפקיד של "סוכן הפקת מידע משיחות שירות".
        קלט: תמליל שיחה בעברית.
        פלט: JSON תקין בלבד לפי הסכמה המצורפת.
        אם שדה לא מופיע – החזר null.
        סיכום חופשי תמיד בעברית, קצר וברור לפעולה.
        אל תנחש מחירים/כתובות אם אין רמזים.
        אם יש "ביום חמישי ב-שלוש" והמועד עבר – הוסף שדה follow_up שדורש תיאום מחדש.
        """

        user_prompt = f"""
        הפק/י את המידע הבא מתוך הטקסט:
        - פרטי לקוח (שם, טלפון, אימייל, כתובת: רחוב/עיר/הערות)
        - מכשיר/סוג טיפול (קטגוריה, מותג, דגם, תיאור בעיה, דחיפות)
        - מחיר שסוכם (מספר, מטבע)
        - תיאום פגישה (תאריך, שעה, משך, אישור הלקוח)
        - Follow-up אם אין תיאום סופי
        - סיכום חופשי בעברית (2-3 שורות)
        החזר JSON בלבד לפי הסכמה.

        טקסט:
        ```{transcript_text}```
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                max_tokens=1000,
            )

            result_text = response.choices[0].message.content
            result_json = json.loads(result_text)

            return ExtractionResult(**result_json)

        except Exception as e:
            # Return default result with error info
            return ExtractionResult(
                free_text_summary_he=f"שגיאה בעיבוד: {str(e)}", confidence=0.0
            )


llm_service = LLMService()
