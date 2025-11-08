from flask import Flask, request, jsonify
from PIL import Image
import io
import base64
import openai  # replace later with Gemini client

app = Flask(__name__)

# Configure your API key
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.route("/decorate", methods=["POST"])
def decorate():
    try:
        # 1️⃣ Get inputs from frontend
        room_size = request.form.get("room_size")
        occasion = request.form.get("occasion")
        style = request.form.get("style")
        materials = request.form.getlist("materials[]")  # JS sends arrays as []
        budget = request.form.get("budget")
        image_file = request.files["image"]

        # 2️⃣ Open the image
        img = Image.open(image_file.stream)

        # 3️⃣ Build unified prompt
        materials_str = ", ".join(materials) if materials else "no specific materials"
        prompt = f"""
        Edit the uploaded room photo for a {occasion} in a {style} style.
        Room size: {room_size}.
        Use these materials: {materials_str}.
        Budget: ${budget}.
        - Keep existing furniture and walls unchanged.
        - Maintain realistic lighting and shadows.
        - Preserve consistent object style (balloons, flowers, furniture).
        """

        # 4️⃣ Generate Text Plan (GPT)
        text_prompt = f"""
        You are an expert interior decorator.
        Create a step-by-step decoration plan for a {occasion} in a {style} style room.
        Room size: {room_size}.
        Budget: ${budget}.
        Available materials: {materials_str}.
        Make sure suggestions fit within budget and are easy to DIY.
        """

        text_response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional interior decorator."},
                {"role": "user", "content": text_prompt},
            ],
            temperature=0.7
        )

        text_plan = text_response["choices"][0]["message"]["content"]

        # 5️⃣ Generate Edited Image (Gemini or OpenAI Image Editing placeholder)
        # Replace with Gemini 2.5 Flash Image call later
        image_output_url = "https://placehold.co/600x400?text=Decorated+Room"  # placeholder

        # 6️⃣ Return results to frontend
        return jsonify({
            "status": "success",
            "text_plan": text_plan,
            "image_url": image_output_url
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
