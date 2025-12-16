# Technical Decisions

## Candidate Information

| Field | Value |
|-------|-------|
| **Name** | David Cermeño Moranchel|
| **Date Started** | 14/12/2025 |
| **Date Completed** | 16/12/2025 |
| **Total Time Spent** | 8 hours |

---

## Summary

A frontend web app with the aforementioned specifications, making use of libraries such as:
- React Hook Forms for form handling
- Tamstack/React-query for HTTP request state management
- Feature-driven architecture
- React Router DOM v7

For the backend, I decided to use Fast API because it allows for very fast development and provides documentation with automatic Swagger integration.

I also chose to use Hexagonal Architecture, attempting to adhere to SOLID principles (though I didn't have much time).

---

## Technology Stack

### Backend

| Component | Choice | Why? |
|-----------|--------|------|
| Framework | Fast API | Automatic Documentation |
| Database | PostgreSQL | requested |
| ORM | sqlalchemy | Top Rated, practicity |

### Frontend

| Component | Choice | Why? |
|-----------|--------|------|
| Framework | No framework, pure React | simplicity for the test |
| State Management | LocalStorage and Tamstack | The app doesn't not need something more complex like redux or Recoil, etc. |
| Styling | TailwindCSS | Requested |

---

## Architecture Decisions

### Backend Structure

Hexagonal Architecture, see backend/Readme.md

### Frontend Structure

Feature Base, see frontend/Readme.md

### Database Design

**Schema Overview:**

Three main tables with UUID primary keys:

- **users**: Stores authentication and user data
  - `id` (UUID, primary key)
  - `email` (unique, indexed)
  - `name`, `hashed_password`
  - `role` (enum: ADMIN | CLIENT)
  - `created_at`, `updated_at` (timestamps)

- **projects**: Project management
  - `id` (UUID, primary key)
  - `title`, `description` (Text)
  - `status` (enum: active | completed | on-hold)
  - `client_id` (UUID, FK to users, nullable)
  - `created_at`, `updated_at`

- **comments**: Project comments
  - `id` (UUID, primary key)
  - `project_id` (UUID, FK to projects)
  - `user_id` (UUID, FK to users)
  - `content` (Text)
  - `created_at`, `updated_at`

**Design Decisions:**

1. **UUIDs instead of integers**: Better for distributed systems, avoids ID enumeration
2. **Nullable client_id**: Projects can exist without assignment
3. **Enum types**: Status and roles enforced at database level
4. **Timestamps**: Automatic tracking of creation/updates
5. **Foreign keys**: Referential integrity for relationships
6. **Indexes**: Email indexed for fast lookups
7. **Text type**: Description and content use TEXT for longer content
8. 
---

## Security

### Security

**Authentication:**

- **JWT tokens**: Using `python-jose` with HS256 algorithm
- **Token expiration**: 30 minutes (configurable)
- **Password hashing**: bcrypt with automatic salt generation
- **Token storage**: Frontend stores in localStorage
- **Token validation**: Middleware validates on each request via `get_current_user` dependency

**Authorization:**

- **Role-based access control (RBAC)**: Two roles (ADMIN, CLIENT)
- **Endpoint protection**: All endpoints require authentication via `Depends(get_current_user)`
- **Role checks**: 
  - Admin-only endpoints: Project CRUD operations, user listing
  - Client restrictions: Can only access their assigned projects
  - Project access: Clients verified against `project.client_id`
- **Service layer filtering**: `ProjectService.get_all_projects()` filters by role automatically

**Input Validation:**

**Backend:**
- **Pydantic schemas**: All request/response models validated automatically
- **Email validation**: `EmailStr` type ensures valid email format
- **Type safety**: Enums (UserRole, ProjectStatus) prevent invalid values
- **Optional fields**: Properly handled with `Optional[str]` types

**Frontend:**
- **Zod schemas**: Client-side validation before API calls
- **React Hook Form**: Integrated with Zod for form validation
- **Type safety**: TypeScript interfaces match backend schemas
- **Error handling**: API errors caught and displayed to users

**Security Best Practices:**
- Passwords never stored in plain text
- Tokens include user ID, email, and role
- 401 errors automatically clear invalid tokens
- SQL injection prevented via SQLAlchemy ORM
- CORS configured for specific origins

---

## Challenges

## Challenges

**Time Constraint:**

The main challenge was implementing a full-stack application with multiple features (authentication, project management, comments, role-based access) within a limited timeframe.

**How I solved it:**

1. **Prioritized core features**: Focused on MVP functionality first (auth, CRUD operations) before enhancements
2. **Leveraged modern tooling**: FastAPI for rapid backend development, React + Vite for fast frontend iteration
3. **Architectural decisions**: Used hexagonal architecture patterns but kept implementations pragmatic rather than over-engineered
4. **Code reuse**: Created reusable components (Button, Input, Card) and hooks (useAuth, API hooks) to avoid repetition
5. **Incremental development**: Built and tested features one at a time rather than trying to build everything at once
6. **Docker Compose**: Used containerization to avoid environment setup overhead

**Specific technical challenges:**

- **React re-render loops**: Fixed by properly memoizing context values and using Navigate components instead of useEffect with navigate()
- **Backend/backend data mismatch**: Resolved snake_case vs camelCase inconsistencies between API responses and frontend types
- **Test coverage**: Focused on business logic (services) rather than infrastructure to maximize value with limited time
---

## Trade-offs

## Trade-offs

**What would you do differently with more time?**

1. **Microservices Architecture**: Extract user management into a dedicated microservice for better scalability and separation of concerns

2. **Design System**: Build a more polished, comprehensive design system with consistent components, spacing, and visual hierarchy

3. **Test-Driven Development (TDD)**: Write tests first to ensure better coverage and catch issues earlier in development

4. **Infrastructure as Code**: Use Terraform or Pulumi to define and version infrastructure, enabling reproducible deployments

5. **Search Functionality**: Add full-text search for projects and comments using PostgreSQL's full-text search or Elasticsearch

6. **Real-time Updates**: Implement WebSockets or Server-Sent Events (SSE) so clients see new comments and project updates without refreshing

**Additional improvements:**

- **Error boundaries**: Better error handling and user feedback
- **Loading states**: More granular loading indicators
- **Optimistic updates**: Improve perceived performance
- **Pagination**: For large project lists
- **File uploads**: Allow attachments to projects/comments
- **Email notifications**: Notify clients of project updates
- **Audit logs**: Track changes for compliance

---

## Resources Used

## Resources Used

**Documentation:**
- FastAPI official documentation (https://fastapi.tiangolo.com/)
- React documentation (https://react.dev/)
- TanStack Query documentation (https://tanstack.com/query)
- SQLAlchemy documentation
- Docker Compose documentation

**Tools & Libraries:**
- Vite for frontend build tooling
- Tailwind CSS for styling
- React Hook Form + Zod for form validation
- Pydantic for backend validation
- Alembic for database migrations

**AI Assistance:**
- Used AI coding assistant (Cursor) for:
  - Code generation and boilerplate
  - Debugging assistance
  - Architecture guidance
  - Code review suggestions

**Development Environment:**
- Docker & Docker Compose for containerization
- PostgreSQL for database
- Git for version control
