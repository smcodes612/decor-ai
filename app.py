import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from PIL import Image
import io
import base64
from google import genai
from google.genai import types
from flask_cors import CORS

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in .env")

# ----------------------------
# Initialize Gemini client
# ----------------------------
client = genai.Client(api_key=API_KEY)

# ----------------------------
# Initialize Flask
# ----------------------------
app = Flask(__name__)
CORS(app)

# ----------------------------
# /decorate endpoint
# ----------------------------
@app.route("/decorate", methods=["POST"])
def decorate():
    try:
        # Get form data
        room_size = request.form.get("room_size", "medium")
        occasion = request.form.get("occasion", "party")
        style = request.form.get("style", "modern")
        materials = request.form.getlist("materials[]")
        budget = request.form.get("budget", "1000")
        image_file = request.files.get("image")

        if not image_file:
            return jsonify({"status": "error", "message": "No image uploaded."})

        # Open uploaded image and convert to PNG
        img = Image.open(image_file.stream).convert("RGBA")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_bytes = img_byte_arr.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        materials_str = ", ".join(materials) if materials else "no specific materials"

        # ----------------------------
        # Text prompt for decoration plan
        # ----------------------------
        text_prompt = f"""
        You are an expert interior decorator.
        Create a detailed, step-by-step decoration plan for a {occasion} in a {style} style room.
        Room size: {room_size}.
        Budget: ${budget}.
        Available materials: {materials_str}.
        Ensure the plan fits within budget and includes DIY-friendly suggestions.
        Mention lighting, table decor, and spatial flow improvements.
        Do not use any markdown. Only plain text.
        """

        # Generate text plan
        text_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=text_prompt
        )

        text_plan = ""
        for part in text_response.candidates[0].content.parts:
            if getattr(part, "text", None):
                text_plan += part.text + "\n"

        # ----------------------------
        # Image prompt for decoration
        # ----------------------------
        image_prompt = f"""
        Transform this interior photo for a {occasion} in a {style} style.
        Room size: {room_size}.
        Use materials: {materials_str}.
        Keep architecture, furniture, and walls realistic.
        Add thematic decor, props, and natural lighting adjustments.
        Maintain realistic reflections, textures, and perspective.
        Ultra-detailed, photorealistic render.
        """

        image_part = types.Part(
            inline_data=types.Blob(
                mime_type="image/png",
                data=img_base64
            )
        )

        # Generate decorated image
        image_response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[image_prompt, image_part]
        )

        generated_image_base64 = None
        for part in image_response.candidates[0].content.parts:
            if getattr(part, "inline_data", None):
                generated_image_base64 = base64.b64encode(part.inline_data.data).decode("utf-8")

        if not generated_image_base64:
            raise ValueError("No image returned from Gemini image model.")

        # ----------------------------
        # Return JSON response
        # ----------------------------
        return jsonify({
            "status": "success",
            "text_plan": text_plan.strip(),
            "image_base64": generated_image_base64
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ----------------------------
# Run Flask
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
    