import re

async def extract_history(chat_history):

    try:
        
        # Extract the last 5 full occurrences of USER: and ASSISTANT:
        user_statements = re.findall(r'(USER:.*?)(?=, ?(?:USER|ASSISTANT)|$)', chat_history, re.DOTALL)
        assistant_statements = re.findall(r'(ASSISTANT:.*?)(?=, ?(?:USER|ASSISTANT)|$)', chat_history, re.DOTALL)

        # Get the last 5 of each
        last_5_user = user_statements[-5:]
        last_5_assistant = assistant_statements[-5:]

        # Combine them back and interleave
        result_full = []
        for user, assistant in zip(last_5_user, last_5_assistant):
            result_full.append(f'{assistant}, {user} ')

        # Join the result back into a string
        result_full_str = "\n".join(result_full)

        return {
            "error": None,
            "chat_history": result_full_str,
            "status": 200
        }
        
    
    except Exception as e:
        return {
            "error": str(e),
            "message": "Error en la respuesta",
            "status": 500
        }