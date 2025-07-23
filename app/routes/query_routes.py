from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.services import llm_service, db_service
import google.generativeai as genai  # ✅ import Gemini client (assuming configured in llm_service or configure here)

# ✅ Define the router
router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_question(payload: QuestionRequest):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        # ✅ Get SQL from LLM
        sql_query = llm_service.question_to_sql(question)
        print(f"📝 Running SQL: {sql_query}")

        # ✅ Execute SQL
        rows = db_service.run_query(sql_query)
        print(f"📦 Raw DB rows: {rows}")

        # ✅ Handle no rows
        if not rows or len(rows) == 0:
            return {"answer": "No data found."}

        # ✅ Single row & single column
        if len(rows) == 1 and len(rows[0]) == 1:
            value = rows[0][0]

            # ✅ ✨ NEW: Use Gemini to phrase the answer naturally
            try:
                prompt = f"""
                You are a helpful assistant.
                The user asked: "{question}"
                The database result is: "{value}"

                Write a friendly, clear sentence that directly answers the user's question.
                """
                gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")  # or your chosen model
                phrased = gemini_model.generate_content(prompt)
                natural_answer = phrased.text.strip()
                return {"answer": natural_answer}
            except Exception as llm_error:
                print("⚠️ Gemini phrasing failed, falling back to raw value:", llm_error)
                # fallback to previous behavior
                if isinstance(value, (int, float)):
                    return {"answer": f"Result: {value:,.2f}"}
                else:
                    return {"answer": f"Result: {value}"}

        # ✅ Single row & multiple columns
        if len(rows) == 1 and len(rows[0]) > 1:
            return {"answer": ", ".join([str(col) for col in rows[0]])}

        # ✅ Multiple rows (grouped or joined results)
        columns = db_service.get_last_columns()
        table_data = [list(row) for row in rows]
        return JSONResponse(content={"table": table_data, "columns": columns})

    except Exception as e:
        print("❌ Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
