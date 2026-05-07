# LangGraph Trace Analyzer API - Implementation Guide

## Overview

This OpenAPI specification defines a comprehensive API for analyzing LangGraph execution traces from watsonx Orchestrate agents. The API allows you to upload trace JSON data, query it for insights, and integrate it as a custom tool in watsonx Orchestrate.

## Key Features

### 1. **Trace Management**
- Upload LangGraph trace JSON
- Store and index trace data
- Search and filter traces
- Retrieve complete trace details

### 2. **Analysis Capabilities**
- Get high-level summaries
- List agents used in execution
- List tools called during execution
- View chronological timeline
- Extract error information
- Analyze performance metrics

### 3. **Advanced Insights**
- Natural language querying
- Trace comparison
- Performance bottleneck identification
- Error pattern analysis

## API Endpoints

### Core Endpoints

#### Upload a Trace
```http
POST /traces/upload
Content-Type: application/json

{
  "trace_data": { /* LangGraph trace JSON */ },
  "trace_name": "Policy Lookup - Customer 12345",
  "metadata": {
    "agent_name": "SFBL Policy Assistant",
    "execution_date": "2024-01-15T10:30:00Z",
    "user_id": "agent_001"
  }
}
```

**Response:**
```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Trace uploaded and indexed successfully",
  "summary": {
    "total_steps": 15,
    "agents_used": 3,
    "tools_called": 8,
    "execution_time_ms": 2450
  }
}
```

#### Query Traces with Natural Language
```http
POST /traces/query
Content-Type: application/json

{
  "question": "Which agents were used in the last policy lookup?",
  "limit": 10
}
```

**Response:**
```json
{
  "question": "Which agents were used in the last policy lookup?",
  "answer": "The last policy lookup used 3 agents: Policy Document Agent, Underwriting Guidelines Agent, and Premium Calculator Agent.",
  "supporting_data": {
    "agents": [
      {
        "name": "Policy Document Agent",
        "invocation_count": 2,
        "duration_ms": 850
      },
      {
        "name": "Underwriting Guidelines Agent",
        "invocation_count": 1,
        "duration_ms": 1200
      },
      {
        "name": "Premium Calculator Agent",
        "invocation_count": 1,
        "duration_ms": 400
      }
    ]
  },
  "traces_analyzed": 1
}
```

#### Get Trace Summary
```http
GET /traces/{trace_id}/summary
```

**Response:**
```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "trace_name": "Policy Lookup - Customer 12345",
  "execution_start": "2024-01-15T10:30:00Z",
  "execution_end": "2024-01-15T10:30:02.450Z",
  "total_duration_ms": 2450,
  "total_steps": 15,
  "agents_count": 3,
  "tools_count": 8,
  "has_errors": false,
  "error_count": 0,
  "status": "completed"
}
```

#### List Agents Used
```http
GET /traces/{trace_id}/agents
```

**Response:**
```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "agents": [
    {
      "agent_id": "agent_001",
      "agent_name": "Policy Document Agent",
      "agent_type": "retrieval",
      "invocation_count": 2,
      "total_duration_ms": 850,
      "first_invoked_at": "2024-01-15T10:30:00.100Z",
      "last_invoked_at": "2024-01-15T10:30:01.500Z",
      "tools_used": ["document_search", "policy_lookup"]
    }
  ]
}
```

#### Get Performance Metrics
```http
GET /traces/{trace_id}/performance
```

**Response:**
```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_duration_ms": 2450,
  "agent_breakdown": [
    {
      "agent_name": "Underwriting Guidelines Agent",
      "duration_ms": 1200,
      "percentage": 48.98
    },
    {
      "agent_name": "Policy Document Agent",
      "duration_ms": 850,
      "percentage": 34.69
    },
    {
      "agent_name": "Premium Calculator Agent",
      "duration_ms": 400,
      "percentage": 16.33
    }
  ],
  "tool_breakdown": [
    {
      "tool_name": "document_search",
      "call_count": 3,
      "total_duration_ms": 600,
      "average_duration_ms": 200.0
    }
  ],
  "slowest_operations": [
    {
      "operation": "Underwriting Guidelines Agent - risk_assessment",
      "duration_ms": 1200,
      "timestamp": "2024-01-15T10:30:00.500Z"
    }
  ]
}
```

## Integration with watsonx Orchestrate

### Step 1: Deploy the API

You can implement this API using:
- **Python Flask/FastAPI** (recommended)
- **Node.js Express**
- **Java Spring Boot**

### Step 2: Import as Custom Tool

1. In watsonx Orchestrate, go to **Tools** → **Add Tool**
2. Select **OpenAPI Specification**
3. Upload the `langgraph-trace-analyzer-api.yaml` file
4. Configure authentication (API Key or Bearer Token)
5. Test the connection

### Step 3: Add to Your Agent

1. Open your SFBL Policy Assistant agent
2. Go to **Tools** section
3. Add the LangGraph Trace Analyzer tool
4. Configure which operations the agent can use

### Step 4: Use in Conversations

Your agent can now answer questions like:
- "Show me the trace from my last policy lookup"
- "Which agents were involved in that execution?"
- "Were there any errors in the underwriting process?"
- "How long did the premium calculation take?"
- "Compare this trace with the previous one"

## Example Use Cases

### Use Case 1: Debugging Agent Failures

**User:** "Why did my policy lookup fail?"

**Agent Actions:**
1. Calls `GET /traces/search?has_errors=true&limit=1`
2. Gets the most recent failed trace
3. Calls `GET /traces/{trace_id}/errors`
4. Analyzes error information
5. Responds with specific error details and affected components

### Use Case 2: Performance Analysis

**User:** "Why is the underwriting process so slow?"

**Agent Actions:**
1. Calls `GET /traces/search?agent_name=Underwriting%20Agent&limit=10`
2. Calls `GET /traces/{trace_id}/performance` for each trace
3. Identifies bottlenecks
4. Responds with performance insights and recommendations

### Use Case 3: Audit Trail

**User:** "What tools did the agent use to calculate that premium?"

**Agent Actions:**
1. Calls `GET /traces/{trace_id}/tools`
2. Filters for Premium Calculator Agent
3. Lists all tools and their inputs/outputs
4. Provides complete audit trail

## Implementation Recommendations

### Backend Technology Stack

**Recommended: Python FastAPI**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from datetime import datetime
import uuid

app = FastAPI(title="LangGraph Trace Analyzer")

# In-memory storage (use database in production)
traces_db = {}

@app.post("/traces/upload")
async def upload_trace(trace_data: dict, trace_name: str = None):
    trace_id = str(uuid.uuid4())
    
    # Parse and index the trace
    summary = analyze_trace(trace_data)
    
    traces_db[trace_id] = {
        "trace_id": trace_id,
        "trace_name": trace_name,
        "uploaded_at": datetime.utcnow().isoformat(),
        "raw_trace": trace_data,
        "summary": summary
    }
    
    return {
        "trace_id": trace_id,
        "message": "Trace uploaded and indexed successfully",
        "summary": summary
    }

def analyze_trace(trace_data: dict) -> dict:
    # Parse LangGraph trace structure
    # Extract agents, tools, timing, errors
    # Return summary
    pass
```

### Database Schema

**PostgreSQL with JSONB:**
```sql
CREATE TABLE traces (
    trace_id UUID PRIMARY KEY,
    trace_name VARCHAR(255),
    uploaded_at TIMESTAMP,
    execution_start TIMESTAMP,
    execution_end TIMESTAMP,
    total_duration_ms INTEGER,
    raw_trace JSONB,
    metadata JSONB,
    has_errors BOOLEAN,
    status VARCHAR(50)
);

CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    trace_id UUID REFERENCES traces(trace_id),
    agent_name VARCHAR(255),
    agent_type VARCHAR(100),
    invocation_count INTEGER,
    total_duration_ms INTEGER
);

CREATE TABLE tool_calls (
    id SERIAL PRIMARY KEY,
    trace_id UUID REFERENCES traces(trace_id),
    tool_name VARCHAR(255),
    invoked_by_agent VARCHAR(255),
    invoked_at TIMESTAMP,
    duration_ms INTEGER,
    status VARCHAR(50),
    input_params JSONB,
    output JSONB
);

CREATE INDEX idx_traces_uploaded ON traces(uploaded_at);
CREATE INDEX idx_traces_status ON traces(status);
CREATE INDEX idx_agents_name ON agents(agent_name);
CREATE INDEX idx_tools_name ON tool_calls(tool_name);
```

### Natural Language Query Processing

For the `/traces/query` endpoint, you can use:

1. **Simple Pattern Matching** (basic implementation)
2. **LLM-based Query Understanding** (recommended)
   - Use watsonx.ai or OpenAI to parse the question
   - Convert to structured queries
   - Execute against trace database
   - Generate natural language response

Example with watsonx.ai:
```python
async def process_natural_language_query(question: str, trace_ids: list = None):
    # Use LLM to understand the question
    prompt = f"""
    Given this question about LangGraph traces: "{question}"
    
    Determine:
    1. What information is being requested (agents, tools, errors, performance, etc.)
    2. What filters should be applied
    3. What API endpoints should be called
    
    Return as JSON.
    """
    
    # Call watsonx.ai to parse the question
    parsed_query = await call_watsonx_ai(prompt)
    
    # Execute the appropriate queries
    results = await execute_queries(parsed_query, trace_ids)
    
    # Generate natural language response
    answer = await generate_answer(question, results)
    
    return {
        "question": question,
        "answer": answer,
        "supporting_data": results
    }
```

## Security Considerations

1. **Authentication**: Use API keys or JWT tokens
2. **Authorization**: Implement role-based access control
3. **Data Privacy**: Sanitize sensitive information from traces
4. **Rate Limiting**: Prevent abuse
5. **Audit Logging**: Track all API access

## Testing the API

### Using cURL

```bash
# Upload a trace
curl -X POST http://localhost:8080/langgraph-trace/traces/upload \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d @sample-trace.json

# Query traces
curl -X POST http://localhost:8080/langgraph-trace/traces/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"question": "Which agents were used?", "limit": 5}'

# Get performance metrics
curl http://localhost:8080/langgraph-trace/traces/{trace_id}/performance \
  -H "X-API-Key: your-api-key"
```

### Using Python

```python
import requests

API_BASE = "http://localhost:8080/langgraph-trace"
API_KEY = "your-api-key"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Upload trace
with open("sample-trace.json") as f:
    trace_data = json.load(f)

response = requests.post(
    f"{API_BASE}/traces/upload",
    json={"trace_data": trace_data, "trace_name": "Test Trace"},
    headers=headers
)
trace_id = response.json()["trace_id"]

# Query the trace
response = requests.post(
    f"{API_BASE}/traces/query",
    json={"question": "What tools were called?"},
    headers=headers
)
print(response.json()["answer"])
```

## Next Steps

1. **Implement the API** using the provided OpenAPI spec
2. **Deploy to your infrastructure** (IBM Cloud, AWS, Azure, etc.)
3. **Import into watsonx Orchestrate** as a custom tool
4. **Add to your SFBL agent** for trace analysis capabilities
5. **Test with real LangGraph traces** from your policy assistant

## Support

For questions or issues:
- Email: support@sfbl.com
- Documentation: https://docs.sfbl.com/trace-analyzer
- GitHub: https://github.com/sfbl/langgraph-trace-analyzer

---

**Made with Bob** - AI-Powered Development Assistant