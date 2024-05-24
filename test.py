import base64
import os
import openai

from openai import OpenAI

client = OpenAI(api_key='sk-proj-iqIenJ2D7p99oMUc5wj4T3BlbkFJE5U3pmE8PquPiTcAt4v3')

# Set your OpenAI API key here
openai.api_key = os.getenv('OPENAI_API_KEY')

prompt_template = """
A detailed cartoon image in a black and white style with red accents. The image is titled "{title}" and portrays {description}. 
The scene should include specific elements such as {specific_elements} and additional details like {additional_details}. 
The overall composition should maintain a satirical and humorous tone, similar to the style of an old newspaper/cartoon.
"""


def generate_and_save_image(title, description, specific_elements, additional_details, output_image_path):
    """Generates an image using DALL-E 3 and saves it to the specified path.

    Args:
        title (str): The title of the image.
        description (str): A description of the image.
        specific_elements (str): Specific elements to include in the image.
        additional_details (str): Additional details for the image.
        output_image_path (str): The path to save the generated image.
    """

    prompt = prompt_template.format(
        title=title,
        description=description,
        specific_elements=specific_elements,
        additional_details=additional_details
    )

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
        response_format="b64_json"
    )

    try:
        image_data = response.data[0].b64_json
        decoded_image = base64.b64decode(image_data)
        with open(output_image_path, 'wb') as f:
            f.write(decoded_image)
        print(f"Image saved as {output_image_path}")

    except KeyError:
        print(f"Error: 'b64_json' field not found in response. Response: {response}")


def generate_image_details(title, description=""):
    """Generates details for an image based on the title and description.

    Args:
        title (str): The title of the image.
        description (str): A description of the image (can be empty).

    Returns:
        tuple: A tuple containing the description, specific_elements, additional_details, file path, and database path.
    """

    # Default values
    specific_elements = generate_text(description,'specific elements')
    additional_details = generate_text(description,'additional details')
    file_path = f"static/images/{title.replace(' ', '_')}.jpg"
    database_path = f"images/{title.replace(' ', '_')}.jpg"

    # Generate a description if none is provided

    description_full = f"A depiction of the concept '{title}'. {description}"

    return description_full, specific_elements, additional_details, file_path, database_path


def generate_text(prompt,type):
    response = client.chat.completions.create(
        model="gpt-4o",  # or the engine you are using
        messages=[
            {"role": "system", "content": f'You describe {type} of a given scene. keep it short.'},
            {"role": "user", "content": prompt}
        ]
    )
    # Extract the text from the response
    text = response.choices[0].message.content
    return text


# Define your prompt

# Generate the text and store it in a variable
#generated_text = generate_text("Netflix Law","additional details")
#print(generated_text)


# print(generate_image_details(title, description))


# Example usage
title = "Netflix Law"
description = "a modern living room where people are browsing different legal letters on demand"
specific_elements = "a large TV screen displaying a menu of legal documents, a person using a remote to scroll through options, another person watching"
additional_details = "details of the living room like a couch, a coffee table with magazines, a potted plant, and wall art"

# generate_and_save_image(title, description, specific_elements, additional_details, "static/images/netflix_law.jpg")
