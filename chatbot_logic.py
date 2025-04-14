from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import sqlite3
from datetime import datetime

# Load pre-trained DialoGPT
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

chat_history_ids = None

def get_response(user_input):
    global chat_history_ids
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response

# ========== DATABASE FUNCTIONS ==========

def init_db():
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            message TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_message(role, message):
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (role, message, timestamp) VALUES (?, ?, ?)",
              (role, message, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def load_chat_history():
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute("SELECT role, message FROM messages ORDER BY id ASC")
    rows = c.fetchall()
    conn.close()
    return [{"user": m[1]} if m[0] == "user" else {"bot": m[1]} for m in rows]
