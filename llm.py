# from openai import OpenAI
# import tiktoken
import os
import sys
import google.generativeai as genai

# Try to load from Kaggle secrets first, then .env file
OPENAI_API_KEY = None
GEMINI_API_KEY = None

# Method 1: Try Kaggle secrets
try:
    from kaggle_secrets import UserSecretsClient
    user_secrets = UserSecretsClient()
    OPENAI_API_KEY = user_secrets.get_secret("OPENAI_API_KEY")
    GEMINI_API_KEY = user_secrets.get_secret("GEMINI_API_KEY")
    if OPENAI_API_KEY:
        print(f"✓ Loaded OPENAI_API_KEY from Kaggle Secrets (length: {len(OPENAI_API_KEY)})")
    elif GEMINI_API_KEY:
        print(f"✓ Loaded GEMINI_API_KEY from Kaggle Secrets (length: {len(GEMINI_API_KEY)})")
    else:
        print("⚠ Kaggle secret 'OPENAI_API_KEY' and 'GEMINI_API_KEY' returned None or empty")
except Exception as e:
    print(f"ℹ Kaggle secrets not available: {type(e).__name__}")
    
    # Method 2: Try environment variable (set directly in Kaggle)
    if not OPENAI_API_KEY:
        OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        if OPENAI_API_KEY:
            print(f"✓ Loaded OPENAI_API_KEY from environment variable (length: {len(OPENAI_API_KEY)})")
    
    # Method 3: Try .env file for local development
    if not OPENAI_API_KEY and not GEMINI_API_KEY:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
            GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
            if OPENAI_API_KEY:
                print(f"✓ Loaded OPENAI_API_KEY from .env file (length: {len(OPENAI_API_KEY)})")
            elif GEMINI_API_KEY:
                print(f"✓ Loaded GEMINI_API_KEY from .env file (length: {len(GEMINI_API_KEY)})")
            else:
                print("⚠ .env file found but OPENAI_API_KEY is empty")
        except Exception as e2:
            print(f"ℹ Could not load .env file: {type(e2).__name__}")

# Validate API key is available
if not OPENAI_API_KEY and not GEMINI_API_KEY:
    print("\n" + "="*60)
    print("ERROR: OPENAI_API_KEY not found!")
    print("="*60)
    print("\nFor Kaggle:")
    print("  1. Click 'Add-ons' → 'Secrets' in the right sidebar")
    print("  2. Add a new secret with label: OPENAI_API_KEY")
    print("  3. Paste your OpenAI API key as the value")
    print("  4. Make sure 'Secrets' is enabled in notebook settings")
    print("\nFor Local Development:")
    print("  1. Create a .env file in the project root")
    print("  2. Add: OPENAI_API_KEY=sk-proj-your-key-here")
    print("="*60 + "\n")
    sys.exit(1)
elif OPENAI_API_KEY:
    # Show confirmation that key is loaded
    print(f"✓ API key ready: {OPENAI_API_KEY[:15]}...{OPENAI_API_KEY[-4:]}")
else:
    print(f"✓ API key ready: {GEMINI_API_KEY[:15]}...{GEMINI_API_KEY[-4:]}")

# class Client:
#     def __init__(self) -> None:
#         self.call_cnt = 0
#         self.token_cost = 0
#         # GPT tokenizer
#         self.tokenizer = tiktoken.encoding_for_model("gpt-4o")

#     def call_llm(self, all_msgs, log_msgs, pipeline=None, openai_key=None):
#         self.call_cnt = self.call_cnt + 1
#         while len(str(all_msgs)) > 30000:
#             all_msgs = all_msgs[1:]
#         if pipeline != None:
#             terminators = [
#                 pipeline.tokenizer.eos_token_id,
#                 pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
#             ]
#             outputs = pipeline(
#                 all_msgs,
#                 max_new_tokens=2048,
#                 eos_token_id=terminators,
#                 do_sample=True,
#                 temperature=0.0,
#                 top_p=0.9,
#             )
#             reply = outputs[0]["generated_text"][-1]["content"]
#             log_msgs.append({"role": "assistant", "content": reply})
#             return reply
#         else:
            
#             tokens = self.tokenizer.encode(str(all_msgs))
#             self.token_cost = self.token_cost + len(tokens)
#             # GPT-4o-mini API configuration
#             client = OpenAI(
#                 api_key=OPENAI_API_KEY
#             )
#             completion = client.chat.completions.create(
#                 model="gpt-4o-mini",
#                 messages=all_msgs, 
#                 temperature=0.0
#             )
#             tokens = self.tokenizer.encode(completion.choices[0].message.content)
#             self.token_cost = self.token_cost + len(tokens)
#             return completion.choices[0].message.content

#     def get_call_cnt(self):
#         return self.call_cnt

class Client:
    def __init__(self) -> None:
        self.call_cnt = 0
        self.token_cost = 0
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def _convert_messages_to_gemini(self, all_msgs):
        """Convert OpenAI-style messages to Gemini format."""
        gemini_history = []
        system_prompt = None
        
        for msg in all_msgs:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                system_prompt = content  # handled separately
            elif role == "user":
                gemini_history.append({"role": "user", "parts": [content]})
            elif role == "assistant":
                gemini_history.append({"role": "model", "parts": [content]})
        
        return gemini_history, system_prompt

    def call_llm(self, all_msgs, log_msgs, pipeline=None, gemini_key=None):
        self.call_cnt += 1

        # Trim messages if too long
        while len(str(all_msgs)) > 30000:
            all_msgs = all_msgs[1:]

        if pipeline is not None:
            terminators = [
                pipeline.tokenizer.eos_token_id,
                pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
            ]
            outputs = pipeline(
                all_msgs,
                max_new_tokens=2048,
                eos_token_id=terminators,
                do_sample=True,
                temperature=0.0,
                top_p=0.9,
            )
            reply = outputs[0]["generated_text"][-1]["content"]
            log_msgs.append({"role": "assistant", "content": reply})
            return reply
        else:
            # Override API key if provided
            api_key = gemini_key or GEMINI_API_KEY
            genai.configure(api_key=api_key)

            gemini_history, system_prompt = self._convert_messages_to_gemini(all_msgs)

            # Reinitialize model with system prompt if present
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=system_prompt
            )

            # Separate history from the latest user message
            history = gemini_history[:-1]
            last_message = gemini_history[-1]["parts"][0] if gemini_history else ""

            # Count input tokens
            input_token_count = model.count_tokens(str(all_msgs)).total_tokens
            self.token_cost += input_token_count

            # Start chat session and send message
            chat = model.start_chat(history=history)
            response = chat.send_message(
                last_message,
                generation_config=genai.GenerationConfig(temperature=0.0)
            )

            reply = response.text

            # Count output tokens
            output_token_count = model.count_tokens(reply).total_tokens
            self.token_cost += output_token_count

            return reply

    def get_call_cnt(self):
        return self.call_cnt
