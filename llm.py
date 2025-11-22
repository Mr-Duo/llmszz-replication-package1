from openai import OpenAI
import tiktoken
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Client:
    def __init__(self) -> None:
        self.call_cnt = 0
        self.token_cost = 0
        # GPT tokenizer
        self.tokenizer = tiktoken.encoding_for_model("gpt-4o")

    def call_llm(self, all_msgs, log_msgs, pipeline=None, openai_key=None):
        self.call_cnt = self.call_cnt + 1
        while len(str(all_msgs)) > 30000:
            all_msgs = all_msgs[1:]
        if pipeline != None:
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
            
            tokens = self.tokenizer.encode(str(all_msgs))
            self.token_cost = self.token_cost + len(tokens)
            # GPT-4o-mini API configuration
            client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=all_msgs, 
                temperature=0.0
            )
            tokens = self.tokenizer.encode(completion.choices[0].message.content)
            self.token_cost = self.token_cost + len(tokens)
            return completion.choices[0].message.content

    def get_call_cnt(self):
        return self.call_cnt
