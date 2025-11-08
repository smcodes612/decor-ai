from flask import Flask, request, jsonify
from PIL import Image
import io
import base64
from google import genai
from google.genai import types
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key="AIzaSyAIle7RYg0khaaN-Oo-890eJroGndF9I7M")

@app.route("/decorate", methods=["POST"])
def decorate():
    try:
        room_size = request.form.get("room_size", "medium")
        occasion = request.form.get("occasion", "party")
        style = request.form.get("style", "modern")
        materials = request.form.getlist("materials[]")
        budget = request.form.get("budget", "1000")
        image_file = request.files["image"]

        img = Image.open(image_file.stream)

        materials_str = ", ".join(materials) if materials else "no specific materials"

        image_prompt = f"""
        Transform this interior photo for a {occasion} in a {style} style.
        Room size: {room_size}.
        Use materials: {materials_str}.
        Keep architecture, furniture, and walls realistic.
        Add thematic decor, party props, and natural lighting adjustments.
        Maintain realistic reflections, textures, and consistent perspective.
        Ultra-detailed, photorealistic 8K render.
        """

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format or 'PNG')
        img_byte_arr = img_byte_arr.getvalue()

        image_part = types.Part(
            inline_data=types.Blob(
                mime_type="image/png",
                data=img_byte_arr
            )
        )

        text_prompt = f"""
        You are an expert interior decorator.
        Create a detailed, step-by-step decoration plan for a {occasion} in a {style} style room.
        Room size: {room_size}.
        Budget: ${budget}.
        Available materials: {materials_str}.
        Ensure the plan fits within budget and includes DIY-friendly suggestions.
        Mention lighting, table decor, and spatial flow improvements.
        Do not use any markdown. I just want plain text and indents for new lines.
        """

        text_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=text_prompt,
        )

        text_plan = ""
        for part in text_response.candidates[0].content.parts:
            if getattr(part, "text", None):
                text_plan += part.text + "\n"

        image_response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[image_prompt, image_part],
        )

        generated_image_base64 = None
        for part in image_response.candidates[0].content.parts:
            if getattr(part, "inline_data", None):
                image_bytes = part.inline_data.data
                generated_image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        if not generated_image_base64:
            raise ValueError("No image returned from Gemini image model.")

        return jsonify({
            "status": "success",
            "text_plan": text_plan.strip(),
            "image_base64": generated_image_base64
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
