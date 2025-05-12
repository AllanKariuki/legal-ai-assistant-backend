import os
import anthropic
from app.core.config import settings
# from google.generativeai import genai
from google import genai
from google.genai.types import GenerationConfig, GenerateContentConfig

async def get_llm_response(query: str) -> str:
    """
        Get a response from th eLLM based on the provided configured settings
    """

    if settings.LLM_PROVIDER == "claude":
        return await get_claude_response(query)
    elif settings.LLM_PROVIDER == 'gemini':
        return await get_gemini_response(query)
    else:
        raise NotImplementedError(f"LLM provider {settings.LLM_PROVIDER} not implemented")
    
async def get_claude_response(query: str) -> str:
    """
        Get a response from Claude API
    """

    try:
        client = anthropic.Anthropic(api_key=settings.LLM_API_KEY)

        system_prompt="""You are a helpful legal assistant AI that provides information about legal concepts, procedures, and documents in accordance to Kenya's laws. 
        Provide a clear, concise and accurate information. Format your response with markdown for readability. 
        Include relevant sections with headins when appropriate. 
        Always clarify that you are providing general information and not legal advice."""

        # Call the Claude API
        response = client.messages.create(
            model=settings.LLM_MODEL,
            system=system_prompt,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": query}
            ]
        )

        return response.content[0].text
    
    except Exception as e:
        # Log the error and return a generic error message
        print(f"Error getting claude response: {e}")
        raise Exception("Failed to get response from LLM service")
    

async def get_gemini_response(query: str) -> str:
    """
        Get a response from Gemini API
    """

    try:
        # Configure gemini
        client = genai.Client(api_key=settings.LLM_API_KEY)
    

        # System instructions
        system_instructions = (
            "You are a helpful legal assistant AI that provides information about legal "
            "concepts, procedures, and documents in accordance with Kenya's laws.\n\n"
            "Provide clear, concise, and accurate information. Format your response with markdown for readability.\n\n"
            "Include relevant sections with headings when appropriate.\n\n"
            "Always clarify that you are providing general information and not legal advice."
        )

        prompt = f"System: {system_instructions}\n\nUser: {query}"

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=1024,
                top_p=0.8,
                top_k=40,
            )
        )

        return response.candidates[0].content.parts[0].text
    
    except Exception as e:
        # Log the error and return a generic error message
        print(f"Error getting gemini response: {e}")
        raise Exception("Failed to get response from LLM service")