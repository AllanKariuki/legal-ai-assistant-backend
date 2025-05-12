import os
import anthropic
from app.core.config import settings

async def get_llm_response(query: str) -> str:
    """
        Get a response from th eLLM based on the provided configured settings
    """

    if settings.LLM_PROVIDER == "claude":
        return await get_claude_response(query)
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