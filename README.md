# helpdesk_ai

helpdesk_ai/
# FastAPI entrypoint                    -- main.py           
# Celery background tasks               -- tasks.py           
# Pydantic / SQLAlchemy models          -- models.py          
# PostgreSQL/MongoDB/Redis connection   -- db.py              
# LangChain RAG pipeline                -- langchain_rag.py   
#requirements                           -- requirements.txt
-----------------------------------------------------------

+-----------------------------+
|         User                |
| Voice / App / Kiosk / API   |
+-------------+---------------+
              |
              v
+-------------+----------------+
|       FastAPI Gateway        |  <-- Handles REST / WebSocket / gRPC
|  - Receives voice/text       |
|  - Validates input           |
+-------------+----------------+
              |
              v
+-------------+----------------+
|     LangChain RAG / LLM      | <-- GPU-enabled inference
|  - Embedding query to DB     |
|  - Context retrieval         |
|  - LLM response generation   |
+-------------+----------------+
              |
              v
+-------------+----------------+
|   Celery Worker Queue        | <-- Async tasks
|  - Process orders            |
|  - Send confirmation emails  |
|  - Update POS / CRM          |
+-------------+----------------+
              |
              v
+-------------+----------------+
| PostgreSQL / Redis / Cache   |
|  - Order history             |
|  - Menu, loyalty info        |
|  - Redis caching             |
+------------------------------+

