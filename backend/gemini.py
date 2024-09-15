from pathlib import Path
import google.generativeai as genai
import yaml

def load_api_key():
    with open("key.yaml", "r") as file:
        key_data = yaml.safe_load(file)
        return key_data.get("API")

def analyze_image(image_path):
    api_key = load_api_key()

    genai.configure(api_key=api_key)

    # Set up the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 0.95,
        "top_k": 32,
        "max_output_tokens": 1024,
    }

    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                  generation_config=generation_config,
                                  )

    # Validate image presence
    if not (img := Path(image_path)).exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    # Prepare image data
    image_data = {
        "mime_type": "image/jpeg",
        "data": Path(image_path).read_bytes()
    }

    # Build prompt
    prompt_parts = [
        "Scan the image precisely, are there any deceptive or manipulative content(in context of commerce. ALso check for hidden fees, counterfeiting, tampering. And return a precise report result, exact keywords, short and precise, the format should be like the following:: Deceptive/Manipulative content: YES/NO ;; Reason : 'Write keyword reason for why or why not it's yes or no';; Tips: 'Give some relevant tips to user, the tip should be very very relevant to the image and response of YES/NO'. VERY IMPORTANT: All the response should be very very short, to the point, precise, use only keypoints.)",
        "Object: ",
        image_data,
        "Description: ",
    ]

    # Generate response
    response = model.generate_content(prompt_parts)
    return response.text

if __name__ == "__main__":
    image_path = "test01.jpg"   #### UPDATE THIS PATH WITH THE PATH IN FRONT-END
    try:
        analysis_result = analyze_image(image_path)
        print(analysis_result)
    except FileNotFoundError as e:
        print(e)
