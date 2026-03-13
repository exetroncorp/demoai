# Coding Agent Test Spec — Team & Task Manager WebApp

---

## VERSION 1 — SIMPLE

Build a Spring Boot web application to manage developers and their tasks.

**Stack:** Java 21, Spring Boot 3, Thymeleaf, Maven (pre-installed), H2 (dev), PostgreSQL (prod).  
**Port:** 8765  
**Login:** demo / demo (hardcoded in-memory)

**What to build:**
- A login page. On success, redirect to the dashboard.
- A **Developers** page: list, add, edit, delete developers (name, email, role).
- A **Tasks** page: list, add, edit, delete tasks (title, description, status, assigned developer).
- Use H2 in-memory DB for the `dev` profile. Wire PostgreSQL for `prod` (config via `application-prod.yml`).
- All DB schema must be handled by Hibernate (`ddl-auto=update` is fine for this spec).
- The app must start cleanly with `mvn spring-boot:run` on port 8765 and be fully usable in a browser.

**Acceptance:** App starts, login works, full CRUD on developers and tasks works, tasks can be assigned to a developer.

---

---

## VERSION 2 — NORMAL

### Goal
Build a production-grade Spring Boot web application for managing a development team and their assigned tasks, following Clean Architecture, DDD, and TDD principles.

---

### Tech Stack

| Layer | Technology |
|---|---|
| Language | Java 21 |
| Framework | Spring Boot 3.x |
| UI | Thymeleaf + Bootstrap 5 (CDN) |
| Build | Maven (pre-installed on machine) |
| DB — dev profile | H2 in-memory |
| DB — prod profile | PostgreSQL |
| Testing | JUnit 5, Mockito, Spring Boot Test |
| Port | **8765** |

---

### Architecture

Follow a **layered Clean Architecture** with DDD building blocks:

```
src/main/java/com/example/teammanager/
├── domain/
│   ├── model/          # Entities & Value Objects (Developer, Task, TaskStatus)
│   └── repository/     # Repository interfaces (ports)
├── application/
│   └── service/        # Use-case services (DeveloperService, TaskService)
├── infrastructure/
│   ├── persistence/    # JPA entities, Spring Data repos (adapters)
│   └── security/       # Spring Security config
└── presentation/
    └── web/            # Thymeleaf controllers (DeveloperController, TaskController)
```

- Domain layer has **zero** Spring/JPA dependencies.
- Application services depend only on domain interfaces.
- Infrastructure adapters implement domain repository interfaces.
- Controllers are thin — delegate everything to application services.

---

### Domain Model

**Developer**
- `id` (UUID)
- `name` (required, non-blank)
- `email` (required, unique, valid format)
- `role` (enum: `FRONTEND`, `BACKEND`, `FULLSTACK`, `DEVOPS`, `QA`)

**Task**
- `id` (UUID)
- `title` (required, non-blank)
- `description` (optional)
- `status` (enum: `TODO`, `IN_PROGRESS`, `DONE`)
- `assignedDeveloper` (nullable FK → Developer)
- `createdAt` (auto-set)

---

### Features & CRUD

#### Authentication
- Spring Security with a single in-memory user: **login `demo` / password `demo`**.
- All routes except `/login` require authentication.
- On logout, redirect to `/login`.

#### Developer Management (`/developers`)
- List all developers in a table.
- Add new developer (form with validation).
- Edit existing developer.
- Delete developer (with confirmation; unassign their tasks first, do not cascade-delete tasks).

#### Task Management (`/tasks`)
- List all tasks with developer name shown.
- Filter tasks by status and/or assigned developer (optional dropdowns, submitted via GET).
- Add new task (form; developer assignment is optional).
- Edit task (change title, description, status, reassign developer).
- Delete task.

#### Dashboard (`/`)
- Summary cards: total developers, total tasks, tasks by status counts.

---

### Configuration

**`application.yml` (default / dev)**
```yaml
server:
  port: 8765
spring:
  profiles:
    active: dev
  security:
    user:
      name: demo
      password: demo
```

**`application-dev.yml`**
```yaml
spring:
  datasource:
    url: jdbc:h2:mem:teamdb;DB_CLOSE_DELAY=-1
    driver-class-name: org.h2.Driver
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true
  h2:
    console:
      enabled: true
      path: /h2-console
```

**`application-prod.yml`**
```yaml
spring:
  datasource:
    url: ${DB_URL}
    username: ${DB_USER}
    password: ${DB_PASS}
    driver-class-name: org.postgresql.Driver
  jpa:
    hibernate:
      ddl-auto: update
    database-platform: org.hibernate.dialect.PostgreSQLDialect
```

---

### TDD Requirements

Write tests **before** or alongside implementation. Minimum coverage targets:

| Layer | Test Type | Examples |
|---|---|---|
| Domain model | Unit | Value object validation, enum transitions |
| Application services | Unit (Mockito) | `DeveloperService`: create, update, delete logic |
| Controllers | Spring MVC Test (`@WebMvcTest`) | Form submission, redirects, model attributes |
| Repository | `@DataJpaTest` (H2) | Custom queries, constraints |
| Integration | `@SpringBootTest` | Full flow: login → create dev → create task → assign |

Tests live under `src/test/java` mirroring the main package structure.

---

### UI / Thymeleaf

- Shared layout fragment (`layout.html`) with navbar (links: Dashboard, Developers, Tasks, Logout).
- Inline form validation error messages using `th:errors`.
- Flash messages (success/error) on redirect using `RedirectAttributes`.
- Bootstrap 5 loaded from CDN — no local asset pipeline needed.
- All forms use CSRF tokens (Spring Security default).

---

### Maven `pom.xml` — Required Dependencies

```xml
spring-boot-starter-web
spring-boot-starter-thymeleaf
spring-boot-starter-data-jpa
spring-boot-starter-security
spring-boot-starter-validation
spring-boot-devtools (scope: runtime, optional)
h2 (scope: runtime)
postgresql (scope: runtime)
spring-boot-starter-test (scope: test)
thymeleaf-extras-springsecurity6
```

Use `spring-boot-starter-parent` as parent POM. Java version: 21.

---

### Run Instructions

```bash
# Dev mode (H2, no external DB needed)
mvn spring-boot:run

# Prod mode
mvn spring-boot:run -Dspring-boot.run.profiles=prod

# Run tests
mvn test
```

App must be reachable at: **http://localhost:8765**

---

### Acceptance Criteria

- [ ] `mvn spring-boot:run` starts the app on port **8765** with zero errors.
- [ ] Navigating to `http://localhost:8765` redirects to `/login`.
- [ ] Login with `demo` / `demo` succeeds and shows the dashboard.
- [ ] Full CRUD works for Developers (create, read, update, delete).
- [ ] Full CRUD works for Tasks (create, read, update, delete).
- [ ] A task can be assigned / reassigned to a developer.
- [ ] Deleting a developer does not delete their tasks (tasks become unassigned).
- [ ] Form validation errors are shown inline.
- [ ] `mvn test` passes with no failures.
- [ ] Switching to `prod` profile connects to PostgreSQL (env vars provided).
