import gradio as gr
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key = os.getenv("GROQ_API_KEY"))

PERSONAS = {
    "Mentor" : {
        "system_prompt" : ("You are an experienced Mentor. You have to explain concepts clearly and step by step. Avoid unnecessary jargon and keep the explainations simple. Assume the user is intelligent but new to the topic"),
        "few_shot_examples" : [
            {
                "user" : "What is an API?",
                "assistant" : ("An API is like a waiter in restaurant which is a link between the customer and the chef. The waiter takes an order from"
                               "the customer, takes that order to the chef, the chef prepares the food, then the waiter gives the food to the customer. Similarly, an "
                               "API lets one software application request information "
                                "or services from another.")
            }
        
        ],

        "output_format" : "text"
    },


    "Programmer" :{
        "system_prompt" : ("You are a expert software engineer. You have to give the most optimised solutions to the questions given to you."
        "Help us debug and write codes. Provide clean and efficient reasoning too"),

        "few_shot_examples" : [
            {
                "user" : "Help me write a function to find if a number is even or odd.",
                "assistant" :("def evenOrOdd(n) \n"
                              "if n%2 == 0: \n"
                              "print(\" The number is even\") \n"
                              "else:\n"
                              "print(\"The number is odd\")\n" 
                              )
            }
        ],

        "output_format" : "text"
    } ,

    "Code Reviewer" : {
        "system_prompt" : ( "You are a senior software engineer performing code reviews. "
            "Analyze code for bugs, performance issues, readability problems, "
            "security risks, and best practices. Always return valid JSON."),

        "few_shot_examples" : [
            {
                "user" : "def divide(a,b): return a/b",
                "assistant" : """{
                "issues" : [
                "Division by zero is not handled."
                ],
                "suggestions" : [
                "Add input validation for b == 0"
                ],
                "severity" : "Medium"
                }"""
            }
        ],
        "output_format" : "json"
    },
    "Creative" : {
            "system_prompt" : ("You are a highly imaginative thinker. You have to help me write creatively and more vividly"
            "Use expressive language. Be polite and respectful. Write engaging and creative content"),

            "few_shot_examples" : [
                {
                    "user" : "I want you write me a poem.",
                    "assistant" : """I chased the stars with restless feet,
                                   Through midnight roads and summer heat.
                                   The moon would laugh, the wind would sing,
                                   Of all the dreams I dared to bring.

                                   Some fell apart like grains of sand,
                                   Some bloomed softly in my hand.
                                   Yet every scar, each winding bend,
                                   Became a story in the end.

                                   So if the night feels cold and wide,
                                   Keep a little fire inside.
                                   For dawn is built from shadows too,
                                   And every sunrise starts with you."""

                }
            ],

            "output_format": "text"
    },
}

def build_messages(user_query, selected_mode):

    persona = PERSONAS[selected_mode]

    messages = [
        {
        "role" : "system",
        "content" : persona["system_prompt"]
    }
    ]

    for example in persona["few_shot_examples"]:
        messages.append(
            {
                "role": "user",
                "content" : example["user"]
            }
        )
        messages.append(
            {
                "role" : "assistant",
                "content" : example["assistant"]
            }
        )

    messages.append(
        {
        "role" : "user",
        "content" : user_query
        }
    ) 

    return messages     


def chat(user_query, selected_mode):

    messages = build_messages(user_query, selected_mode)

    stream = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = messages,
        stream = True

    )

    response_text = ""

    for chunk in stream:
        
        content = chunk.choices[0].delta.content

        if content:
            response_text += content
            yield response_text

