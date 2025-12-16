# Analysis Responses

## Candidate Information

| Field | Value |
|-------|-------|
| **Name** | David Cermeño |
| **Date** | |

---

## Question 1: Performance Bottlenecks

> What are the two main performance bottlenecks in your implementation? How would you address them?

### Bottleneck 1

**What:**

All list endpoints (`GET /projects`, `GET /comments`) return complete datasets without pagination limits.

**Why it's a problem:**

- Large response payloads consume excessive bandwidth
- Memory pressure on both server and client
- Slow initial page load times
- Database queries load entire tables into memory

**Solution:**

- Add `limit` and `offset` query parameters
- Return pagination metadata (total count, has_next, has_prev)
- Set reasonable default limits (e.g., 20-50 items per page)
- Frontend: Implement infinite scroll or "Load More" buttons

### Bottleneck 2

**What:**

The queries maked by request

**Why it's a problem:**

With 100 projects, this results in 1 initial query + 100 additional queries = 101 total queries, causing significant latency.

**Solution:**

- Use SQL JOINs at the repository level to fetch related data in one query

---

## Question 2: Real-time Updates

> The client asks: "Can we add real-time updates so clients see new comments without refreshing?"

**Recommended approach:**

Use WebSockets to push new comments to clients in real-time.

**How it works:**

1. When a user opens a project page, the frontend connects to a WebSocket endpoint for that project
2. The backend keeps the connection open and groups connections by project_id
3. When someone creates a new comment, the backend sends it to all connected clients for that project
4. The frontend receives the message and updates the comment list automatically

**Why this approach:**

- WebSockets keep connection open, so updates are instant
- FastAPI has WebSocket support built-in, so it's straightforward to add
- More efficient than polling because server pushes data only when needed
  
**Trade-offs:**

- More complex than REST endpoints
- Need to handle connection errors and reconnection logic
- Uses more server resources (keeping connections open)
- Need to manage connection lifecycle (connect, disconnect, cleanup)