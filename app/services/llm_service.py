import google.generativeai as genai
import re

# 🔑 Configure with your API key
genai.configure(api_key="AIzaSyCLr53tXafAfkzbXNlV1y1cPdVkWoWXPdk")  # <-- replace with your actual key

# ✅ Use a supported Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

def question_to_sql(question: str) -> str:
    prompt = f"""
    You are an expert SQL generator for a SQLite database.

    The database has these tables:
    - product_ad_sales(date TEXT, item_id INTEGER, ad_sales REAL, impressions INTEGER, ad_spend REAL, clicks INTEGER, units_sold INTEGER)
    - product_total_sales(date TEXT, item_id INTEGER, total_sales REAL, total_units_ordered INTEGER)
    - product_eligibility(eligibility_datetime_utc TEXT, item_id INTEGER, eligibility BOOLEAN, message TEXT)

    VERY IMPORTANT RULES:
    - When the user asks for totals (like "total sales", "total ad spend"), return a SINGLE VALUE using SUM() with NO GROUP BY.
    - When the user asks for Return on Ad Spend (RoAS), calculate it as:
      SUM(ad_sales) / SUM(ad_spend) from product_ad_sales, and return a SINGLE VALUE.
    - When the user asks for highest CPC (Cost Per Click):
        Always calculate CPC as SUM(ad_spend)/SUM(clicks) from product_ad_sales
        Include WHERE clicks > 0
        GROUP BY item_id
        ORDER BY CPC DESC
        LIMIT 1 unless otherwise specified.
    - When joining tables, use consistent and valid aliases.
      • Use `pts` for product_total_sales.
      • Use `pe` for product_eligibility.
      • Use `pa` for product_ad_sales if needed.
    - Never use alias `p`. Only use the defined aliases above.
    - Always reference columns with their alias (e.g., pts.item_id, pe.message).
    - Only use GROUP BY when the question explicitly asks for a breakdown.
    - Only use the fields and tables listed above.
    - Return ONLY the SQL query, without markdown, without explanations, and without comments.

    User question: "{question}"
    """

    # 🔎 Call Gemini
    response = model.generate_content(prompt)
    raw_sql = response.text.strip()
    print("🔎 Raw Gemini output:\n", raw_sql)

    # ✅ Clean markdown fences if present
    cleaned_sql = re.sub(r"```.*?\n", "", raw_sql)
    cleaned_sql = cleaned_sql.replace("```", "").strip()

    # ✅ Fix invalid aliases that Gemini might hallucinate
    # Replace p. references with pts. for safety
    cleaned_sql = cleaned_sql.replace("p.item_id", "pts.item_id")
    cleaned_sql = cleaned_sql.replace("p.", "pts.")

    # ✅ Extra safeguard for unknown alias usage
    if "p." in cleaned_sql and "pts." in cleaned_sql:
        cleaned_sql = cleaned_sql.replace("p.", "pts.")

    print("✅ Cleaned SQL:\n", cleaned_sql)
    return cleaned_sql
