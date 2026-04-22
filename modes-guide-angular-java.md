# AI Coding Agent Modes — Developer Guide
### IBM Bob & RooCode · Angular & Java Edition

---

## Table of Contents

0. [Modes vs Rules vs Skills — What's the Difference?](#0-modes-vs-rules-vs-skills)
1. [What Are Modes?](#1-what-are-modes)
2. [Built-in Modes — Overview & Comparison](#2-built-in-modes)
3. [How to Switch Modes](#3-how-to-switch-modes)
4. [Recommended Workflows for Angular & Java](#4-recommended-workflows)
5. [Custom Modes — Concepts & Configuration](#5-custom-modes)
6. [Creating Custom Modes — Step by Step](#6-creating-custom-modes)
7. [Custom Mode Examples for Angular & Java](#7-custom-mode-examples)
8. [Mode-Specific Instruction Files](#8-instruction-files)
9. [Overriding Default Modes](#9-overriding-default-modes)
10. [Configuration Precedence & File Locations](#10-configuration-precedence)
11. [Regex Cheat Sheet for File Restrictions](#11-regex-cheat-sheet)
12. [Best Practices](#12-best-practices)
13. [Community Libraries & Existing Modes](#13-community-libraries)

---

## 0. Modes vs Rules vs Skills — What's the Difference?

These three concepts all influence how the AI behaves, and they are often confused because they overlap in purpose. They are **not** the same thing — they operate at different levels of the system and serve distinct roles.

### The Core Mental Model

> **Modes** define *who* the AI is and *what it can touch*.
> **Rules** define *how* it must behave while in that role.
> **Skills** define *what it knows* for a specific task, loaded on demand.

Think of it like an employee joining a team:

| Concept | Analogy |
|---|---|
| **Mode** | The job title and access badge (Java Dev vs. Reviewer vs. Architect). Defines your role, your floor access, and your desk. Persistent for the whole session. |
| **Rules** | The employee handbook and team conventions. Always in your pocket — you must follow them regardless of what task you're doing. |
| **Skill** | The how-to guide you pull from the shelf when you hit a specific task. You don't carry all the guides at once — you grab the right one when you need it. |

---

### Modes — The Persona Layer

A **mode** is a persistent identity switch. When you activate a mode, the AI gets a new system prompt defining its role, expertise, and tool access. It stays in that mode until you explicitly switch.

What a mode controls:
- **Role definition** — who the AI is (e.g. "You are a senior Java DDD engineer…")
- **Tool access** — what it can do (`read`, `edit`, `command`, `mcp`)
- **File restrictions** — what files it's allowed to touch (`fileRegex`)
- **Sticky model** (RooCode) — which LLM is used for this mode

A mode does NOT automatically load detailed task instructions — that's what rules and skills are for.

**Files:** `.roomodes`, `.bob/custom_modes.yaml`, `custom_modes.yaml`

---

### Rules — The Always-On Constraints

**Rules** are instructions that are **always injected** into the active mode's context, automatically. They don't need to be invoked — they're loaded at session start.

There are two kinds:

**Global rules** (all modes): Stored in `.roo/rules/` or `.bob/rules/`. Apply to every mode in the project. Use for: commit message conventions, code formatting standards, language-of-response requirements, security baseline.

**Mode-specific rules**: Stored in `.roo/rules-{slug}/` or `.bob/rules-{slug}/`. Only loaded when that specific mode is active. Use for: mode-specific architectural constraints, testing conventions for a TDD mode, naming rules for a domain mode.

Rules are always loaded — the AI has no choice. They are the **mandatory operating procedures**.

```
.roo/
  rules/                    ← global, applies to ALL modes
    01-commit-conventions.md
    02-no-console-log.md
  rules-java-domain/        ← only loaded when java-domain mode is active
    01-hexagonal-layers.md
    02-naming.md
  rules-angular-dev/
    01-standalone-only.md
```

**Key property:** Rules are always consumed tokens. Keep them concise — overly long rules add context overhead to every single message.

---

### Skills — The On-Demand Knowledge Packages

**Skills** (RooCode) are self-contained instruction packages that the AI loads **only when needed**. They are NOT automatically injected — the AI reads a skill's description first (from `SKILL.md` frontmatter) and decides to load it when a task matches.

A skill is a directory containing:
- A `SKILL.md` with frontmatter (`name`, `description`) and step-by-step instructions
- Optional helper files: templates, scripts, reference docs, code snippets

```
.roo/
  skills/                          ← available to all modes
    spring-boot-hexagonal/
      SKILL.md                     ← instructions + file index
      templates/
        AggregateTemplate.java
        PortTemplate.java
  skills-code/                     ← only available in Code mode
    angular-standalone-scaffold/
      SKILL.md
      templates/
        component.template.ts
```

Skills use **progressive disclosure**: the AI reads only the `SKILL.md` description during discovery (cheap). It loads the full content only when it decides the skill is relevant to the current task. This makes skills much more token-efficient than rules for large bodies of knowledge.

As of **RooCode v3.47**, skills can also target multiple modes at once via a `modeSlugs` frontmatter array, in addition to the `skills-{mode}/` directory convention:

```markdown
---
name: spring-aggregate
description: Scaffold a Spring Boot DDD aggregate with ports and adapters
modeSlugs: [java-domain, code]   ← available in these two modes only
---
```

**IBM Bob** has a Skills feature as well, but with two key differences:
- Skills are stored in `.bob/skills/` (project) or `~/.bob/skills/` (global) — NOT in `.bob/rules-{slug}/`
- **Bob Skills are only available in Advanced mode** (`🛠️ Advanced`). You cannot use skills in Code, Ask, or Plan modes.

**External community library:** [agentskills.io](https://agentskills.io) — community-contributed skills compatible with RooCode, Bob, Claude Code, Gemini CLI, and others. The universal install path is `.agents/skills/` (cross-tool). Bob supports it via `~/.bob/settings.json`:

```json
{
  "context": {
    "includeDirectories": ["/Users/you/.agents/skills/"]
  }
}
```

---

### Side-by-Side Comparison

| | **Mode** | **Rules** | **Skills** |
|---|---|---|---|
| **Purpose** | Define role & tool access | Enforce behavior constraints | Provide task-specific know-how |
| **Loaded** | On mode switch | Always (automatically) | On demand (by the AI) |
| **Scope** | Whole session | While mode is active | For a specific task invocation |
| **Token cost** | System prompt overhead | Always consumed | Only when activated |
| **Editable by** | Developer (YAML/UI) | Developer (Markdown files) | Developer (SKILL.md + files) |
| **Versioned** | Yes (in `.roomodes`) | Yes (in `.roo/rules*/`) | Yes (in `.roo/skills*/`) |
| **Used by Orchestrator** | Yes (`whenToUse` field) | Indirectly | Indirectly |

---

### How They Compose Together

The three layers stack on top of each other:

```
┌─────────────────────────────────────────────────┐
│  MODE: java-domain                              │
│  → Role: DDD Java engineer                     │
│  → Tools: read + edit (.java only) + command   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │  RULES (always loaded)                  │   │
│  │  .roo/rules/            → global rules  │   │
│  │  .roo/rules-java-domain/→ mode rules    │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │  SKILL (loaded on demand)               │   │
│  │  "spring-boot-hexagonal" skill          │   │
│  │  → loaded when creating a new aggregate │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

**Practical design advice:**

- Put **team-wide conventions** (git commit format, response language) in global rules.
- Put **mode-specific architectural constraints** (layer boundaries, naming) in mode rules.
- Put **complex, reusable procedural knowledge** (how to scaffold a Spring aggregate, how to write an ADR) in skills — not in rules, because they're only needed occasionally.
- Don't duplicate the same instruction in both `customInstructions` (in the mode YAML) and a rules file — pick one. The YAML `customInstructions` is fine for short inline rules; files scale better for longer content.

---

### Can I Put Rules Inside a Mode? Can I Attach a Skill to a Mode?

Yes to both, with nuance. This is one of the most frequent questions.

#### Rules inside a mode — YES, natively, 3 ways

**1. Inline `customInstructions` in the mode YAML** — simplest, always loaded with the mode:

```yaml
customModes:
  - slug: java-domain
    name: ☕ Java Domain Engineer
    roleDefinition: You are a DDD Java engineer...
    customInstructions: |-
      - No Spring annotations in domain layer
      - Use records for Value Objects
      - Always write tests first
    groups:
      - read
      - - edit
        - fileRegex: ^src/main/java/.*\.java$
```

**2. Mode-specific rules directory** — external files, auto-loaded when the mode is active and only then (this IS the "rules in a mode" mechanism):

```
.roo/
  rules-java-domain/         ← injected ONLY when java-domain is active
    01-hexagonal.md
    02-naming.md
  rules/                     ← injected for ALL modes (global)
    01-commit-format.md
```

**3. Both together** — `customInstructions` is injected first, then rules files are appended. They stack, they don't replace each other.

> ⚠️ **Bob note:** Same pattern, but paths use `.bob/rules-{slug}/` and `.bob/rules/`.

---

#### Skills attached to a mode — no direct embed, but two ways to target

A skill cannot be "embedded" in a mode definition — by design, skills are loaded on-demand. But you can scope them to specific modes:

**1. Mode-specific directory** — the skill only appears in that mode's discovery list:

```
.roo/
  skills/                    ← visible in ALL modes
    openapi-design/
      SKILL.md
  skills-code/               ← visible ONLY in Code mode
    spring-aggregate/
      SKILL.md
      templates/Aggregate.java
  skills-architect/          ← visible ONLY in Architect mode
    adr-template/
      SKILL.md
```

**2. `modeSlugs` frontmatter array** (RooCode v3.47+) — target multiple modes from a single skill location:

```markdown
---
name: spring-aggregate
description: Scaffold a DDD aggregate with ports, adapters, and unit tests
modeSlugs: [java-domain, code]
---
# Steps
...
```

**3. Hint via `customInstructions`** — nudge the mode to use a specific skill for certain patterns (workaround for quasi-automatic loading):

```yaml
customInstructions: |-
  When asked to create a new domain aggregate, ALWAYS load and follow
  the "spring-aggregate" skill before writing any code.
  When designing a new REST endpoint, load the "openapi-design" skill first.
```

> ⚠️ **Bob note:** Bob Skills are **Advanced mode only**. You cannot use skills in Code, Ask, or Plan modes. Store them in `.bob/skills/` (project) or `~/.bob/skills/` (global).

---

#### Full picture — all three layers combined

```
MODE yaml (.roomodes / .bob/custom_modes.yaml)
├── roleDefinition          ← WHO the AI is       [always in system prompt]
├── customInstructions      ← inline rules         [always injected]
├── groups + fileRegex      ← WHAT it can touch
│
RULES files (auto-loaded)
├── .roo/rules/             ← global, ALL modes    [always injected]
└── .roo/rules-java-domain/ ← this mode only       [injected when active]
│     01-hexagonal.md
│     02-naming.md
│
SKILLS (on-demand)
├── .roo/skills/            ← all modes            [loaded when task matches]
├── .roo/skills-code/       ← Code mode only
│     spring-aggregate/
│       SKILL.md
└── .agents/skills/         ← cross-tool universal path (agentskills.io)
```

---

## 1. What Are Modes?

Modes are **specialized AI personas** that change how the assistant thinks, what tools it can use, and what files it can touch. Think of them as switching between different team roles:

| If you were talking to a person… | Mode equivalent |
|---|---|
| Senior dev who writes and changes code | **Code** |
| Tech lead who designs before building | **Architect / Plan** |
| QA expert tracking down a bug | **Debug** |
| Colleague explaining how something works | **Ask** |
| Project manager coordinating multiple experts | **Orchestrator** |

Modes give you **safety**, **focus**, and **workflow discipline** — you decide what the AI is allowed to do at every stage of development.

---

## 2. Built-in Modes

### IBM Bob — Built-in Modes

| Mode | Emoji | Tool Access | Best For |
|---|---|---|---|
| **Code** | 💻 | `read`, `edit`, `command` | Daily implementation, refactoring, bug fixes |
| **Ask** | ❓ | `read`, `browser`, `mcp` | Q&A, code explanation, no file changes |
| **Plan** | 📝 | `read`, `edit` (markdown only), `browser`, `mcp` | Architecture, TDD specs, sprint planning |
| **Advanced** | 🛠️ | All groups | Complex workflows needing MCP tools |
| **Orchestrator** | 🔀 | None (delegates only) | Multi-step, multi-domain projects |

### RooCode — Built-in Modes

| Mode | Emoji | Tool Access | Best For |
|---|---|---|---|
| **Code** | 💻 | All (`read`, `edit`, `command`, `mcp`) | Full implementation tasks |
| **Ask** | ❓ | `read`, `mcp` | Learning, analysis, no edits |
| **Architect** | 🏗️ | `read`, `mcp`, `edit` (markdown only) | System design, ADRs, API contracts |
| **Debug** | 🪲 | All | Systematic bug hunting with logging |
| **Orchestrator** | 🪃 | None (uses `new_task` to delegate) | Boomerang tasks, multi-mode pipelines |

### Key Differences Between Bob & RooCode

- Bob has **Plan** mode; RooCode has **Architect** mode — both restrict edits to markdown only, ideal for pre-implementation thinking.
- RooCode has a dedicated **Debug** mode with specific instructions to add logs before fixing; Bob's Code mode handles debugging.
- RooCode's **Orchestrator** uses the `new_task` tool (Boomerang Tasks) to spin up sub-agents per mode; Bob's Orchestrator similarly coordinates without holding tools itself.
- RooCode **Sticky Models**: each mode remembers the last model you used, so you can assign e.g. a large model to Architect and a fast cheap one to Code.

---

## 3. How to Switch Modes

All three methods work in both tools:

### Dropdown (GUI)
Click the mode selector to the left of the chat input.

### Slash Command (fastest)
Type at the start of your message — the input clears and switches mode immediately.

| Bob command | RooCode command | Mode |
|---|---|---|
| `/code` | `/code` | Code |
| `/ask` | `/ask` | Ask |
| `/plan` | `/architect` | Plan / Architect |
| `/advanced` | — | Advanced (Bob only) |
| `/orchestrator` | `/orchestrator` | Orchestrator |
| — | `/debug` | Debug (RooCode only) |

### Keyboard Shortcut
`Ctrl + .` (Windows/Linux) or `⌘ + .` (macOS) — cycles through all available modes.

### Accept Suggestions
The AI itself will suggest mode switches when appropriate (e.g., "Switch to Code mode to implement this plan?").

---

## 4. Recommended Workflows for Angular & Java

### Standard Feature Development Workflow

```
Plan/Architect → Code → Ask → Debug (if needed)
```

**Step-by-step example: adding a REST endpoint in Spring Boot**

```
1. /plan  →  "Design a POST /api/orders endpoint following DDD.
              Domain: Order aggregate. Port + Adapter pattern.
              Write the plan in docs/design/order-endpoint.md"

2. /code  →  "Implement the plan in docs/design/order-endpoint.md.
              Create OrderController, OrderApplicationService,
              OrderRepository interface, and JPA adapter."

3. /ask   →  "Explain the difference between @Transactional on
              the service vs on the repository layer in this code."

4. /code  →  "Write unit tests for OrderApplicationService
              using Mockito. Cover the happy path and
              validation error cases."
```

**Example: Angular feature with TDD**

```
1. /plan  →  "Design a CartComponent using Angular signals.
              List the public API (inputs/outputs), state shape,
              and service dependencies. Save to docs/cart-design.md"

2. /code  →  "Scaffold CartComponent as per docs/cart-design.md.
              Use standalone component, OnPush, inject CartService."

3. /code  →  "Write Jasmine/Jest specs for CartComponent.
              Cover: add item, remove item, empty cart state."

4. /debug →  "The addItem() spec fails: Expected 2 to be 1.
              Investigate the state mutation logic."
```

---

### Bug Investigation Workflow (RooCode Debug Mode)

```
/debug  →  "NullPointerException in OrderService.createOrder()
            in production logs. Here is the stack trace: [paste].
            Narrow down the cause and suggest a fix."
```

Debug mode will:
1. Read all relevant source files
2. Suggest adding targeted log statements
3. Ask you to confirm before modifying anything
4. Propose a minimal, focused fix

---

### Orchestrator Workflow (multi-domain tasks)

```
/orchestrator → "Refactor the entire user authentication module:
                 1. Plan the new JWT structure (Architect/Plan)
                 2. Update the Spring Security config (Code)
                 3. Update the Angular auth interceptor (Code)
                 4. Update integration tests (Code)
                 5. Update the README (Documentation mode)"
```

The Orchestrator breaks this into subtasks and routes each to the appropriate mode automatically.

---

## 5. Custom Modes — Concepts & Configuration

### What Makes a Custom Mode

| Property | Key | Required | Description |
|---|---|---|---|
| Slug | `slug` | ✅ | Internal ID. Only `a-z`, `0-9`, `-`. Used for instruction file directories. |
| Name | `name` | ✅ | Display name. Can include emoji. |
| Description | `description` | ✅ | Short UI label shown in mode selector. |
| Role Definition | `roleDefinition` | ✅ | The AI's identity — placed at the top of the system prompt. Be specific and opinionated. |
| Tool Groups | `groups` | ✅ | What the AI can do: `read`, `edit`, `command`, `mcp`, `browser`. |
| When To Use | `whenToUse` | — | Used by Orchestrator to auto-route tasks. Not shown in UI. |
| Custom Instructions | `customInstructions` | — | Behavioral rules appended to the system prompt. |

### Tool Groups

| Group | Capability |
|---|---|
| `read` | Read files, list directories, search code |
| `edit` | Create and modify files (can be restricted with `fileRegex`) |
| `command` | Run terminal commands (Maven, npm, ng CLI, etc.) |
| `mcp` | Call MCP servers (databases, APIs, cloud tools) |
| `browser` | Browse the web (RooCode/Bob with browser tool) |

### File Restriction with `fileRegex`

The `edit` group can be tuned to only allow specific files:

```yaml
groups:
  - read
  - - edit
    - fileRegex: \.(java|xml)$
      description: Java source and Maven POM files only
  - command
```

---

## 6. Creating Custom Modes — Step by Step

### Method 1: Ask the AI (easiest)

In Bob:
> "Create a new mode called 'Java Test Engineer'. It should only be able to read and edit Java test files. It must enforce TDD and use AssertJ."

In RooCode:
> "Create a custom mode for Angular development. Restrict edits to `.ts`, `.html`, `.scss` files under `src/`. Role: Angular expert following standalone component patterns and signals."

The AI creates the YAML config for you, which you can refine manually.

---

### Method 2: Settings UI

1. Open the AI panel → click the gear / settings icon
2. Go to **Modes** tab
3. Click **New Mode** (➕)
4. Fill in: Name, Slug, Role Definition, Tools, Instructions
5. Choose save location: **Global** (all projects) or **Project** (this project only)
6. Click **Save / Create Mode**

---

### Method 3: Manual YAML (most control)

**IBM Bob — project mode file:** `.bob/custom_modes.yaml`
**RooCode — project mode file:** `.roomodes`
**Global (both):** `custom_modes.yaml` in the global settings directory

```yaml
customModes:
  - slug: my-mode
    name: 🎯 My Mode
    description: Short description for the UI
    roleDefinition: >-
      You are a specialized assistant for...
    whenToUse: Use this mode when working on...
    customInstructions: |-
      Always do X.
      Never do Y.
    groups:
      - read
      - - edit
        - fileRegex: \.(ts|html|scss)$
          description: Angular source files only
      - command
```

---

## 7. Custom Mode Examples for Angular & Java

### 7.1 Angular Feature Developer

```yaml
# .roomodes or .bob/custom_modes.yaml
customModes:
  - slug: angular-dev
    name: 🅰️ Angular Developer
    description: Angular specialist — signals, standalone, strict typing
    roleDefinition: >-
      You are a senior Angular developer with deep expertise in Angular 17+.
      You always use standalone components, Angular signals for state management,
      typed reactive forms, and the inject() function instead of constructor
      injection. You enforce strict TypeScript, use OnPush change detection,
      and follow the Angular Style Guide. You prefer native fetch over HttpClient
      for simple requests, use @ngx-templates/shared components when available,
      and write SCSS with BEM-like selectors prefixed with ec-.
    whenToUse: >-
      Use for any Angular feature implementation, component scaffolding,
      service creation, routing configuration, or Angular-specific refactoring.
    customInstructions: |-
      - Always use standalone: true in component decorators
      - Use signal() and computed() for local state, never BehaviorSubject in components
      - Use inject() not constructor injection
      - Prefix component selectors with ec-
      - Use @ngx-templates/shared/* components when available
      - Write specs with Jasmine, use TestBed.configureTestingModule sparingly
      - Never use ngModel; use typed reactive forms
    groups:
      - read
      - - edit
        - fileRegex: ^src/.*\.(ts|html|scss|spec\.ts)$
          description: Angular source files only
      - command
```

**Usage examples:**
```
/angular-dev  Create a ProductListComponent that:
              - Is standalone with OnPush
              - Uses a signal<Product[]> for the list
              - Calls ProductService.getAll() on init
              - Uses ec- selector prefix
```

```
/angular-dev  Refactor CartService to replace all BehaviorSubject
              with Angular signals. Keep the public API compatible.
```

---

### 7.2 Java/Spring Boot Domain Engineer

```yaml
customModes:
  - slug: java-domain
    name: ☕ Java Domain Engineer
    description: DDD hexagonal architecture — domain, ports, adapters
    roleDefinition: >-
      You are a senior Java engineer specializing in Domain-Driven Design
      with hexagonal (ports & adapters) architecture. You enforce strict
      separation between domain, application, and infrastructure layers.
      Domain objects are pure Java with no framework annotations.
      Application services orchestrate domain logic through ports (interfaces).
      Adapters (JPA, REST) live in infrastructure. You use Java 17+ features:
      records, sealed classes, pattern matching. Tests use JUnit 5 + AssertJ +
      Mockito. Build tool is Maven.
    whenToUse: >-
      Use when implementing domain logic, application services, repository
      interfaces, or REST controllers in a Spring Boot hexagonal architecture.
    customInstructions: |-
      - Domain classes have ZERO Spring/JPA annotations
      - Use records for Value Objects
      - Ports are interfaces in the application layer
      - Adapters implement ports and live in infrastructure
      - Write unit tests FIRST (TDD), then implementation
      - Test names: given_when_then format
      - Use AssertJ assertThat(), not JUnit assertEquals()
      - Always add @DisplayName to tests
    groups:
      - read
      - - edit
        - fileRegex: ^src/(main|test)/java/.*\.(java|xml)$
          description: Java source files and POM
      - command
```

**Usage examples:**
```
/java-domain  Create an Order domain aggregate.
              Fields: orderId (UUID), customerId, items (List<OrderItem>),
              status (enum: PENDING, CONFIRMED, CANCELLED).
              Business rule: can't add items to a CONFIRMED order.
              Include unit tests.
```

```
/java-domain  Create the OrderRepository port interface and
              a JpaOrderRepository adapter using Spring Data JPA.
              Map Order to OrderJpaEntity using a separate mapper.
```

---

### 7.3 Java Test Engineer (TDD enforcer)

```yaml
customModes:
  - slug: java-tdd
    name: 🧪 Java TDD Engineer
    description: Write tests first — JUnit 5, AssertJ, Mockito
    roleDefinition: >-
      You are a Java test engineer who writes tests before implementation.
      You are an expert in JUnit 5, AssertJ, Mockito, and Spring Boot Test.
      You write readable, maintainable tests that document business behavior.
      You cover: happy path, edge cases, exception handling, boundary conditions.
    whenToUse: Use when writing or reviewing Java unit or integration tests.
    customInstructions: |-
      - Always write the test class BEFORE the implementation
      - Use @DisplayName with business-language descriptions
      - Group tests with @Nested classes per scenario
      - Use AssertJ for all assertions
      - Mock external dependencies with @Mock / @InjectMocks
      - For Spring Boot: use @WebMvcTest for controllers, @DataJpaTest for repos
      - Never use assertTrue(x.equals(y)) — use assertThat(x).isEqualTo(y)
      - Aim for 100% branch coverage of domain logic
    groups:
      - read
      - - edit
        - fileRegex: ^src/test/java/.*\.java$
          description: Test files only — cannot touch production code
```

**Usage example:**
```
/java-tdd  Write tests for OrderApplicationService.createOrder().
           Cover: successful creation, duplicate order ID,
           invalid customer ID, item list empty.
```

---

### 7.4 Angular Code Reviewer (read-only)

```yaml
customModes:
  - slug: angular-review
    name: 🔍 Angular Reviewer
    description: Read-only review — no file edits
    roleDefinition: >-
      You are a senior Angular code reviewer. You check for: performance issues
      (unnecessary subscriptions, missing OnPush, N+1 HTTP calls), security
      (XSS risks, unsafe HTML binding), code style (Angular Style Guide
      compliance), and architecture (proper service/component separation,
      smart vs dumb components). You produce structured review reports.
    whenToUse: Use for pre-PR Angular code reviews.
    customInstructions: |-
      - Output review as: CRITICAL / WARNING / SUGGESTION sections
      - Always reference the Angular Style Guide rule number if applicable
      - Suggest refactored code snippets inline
      - Never edit files — review only
    groups:
      - read
      - browser
```

**Usage example:**
```
/angular-review  Review @src/app/checkout for:
                 - Change detection strategy
                 - Signal usage vs observable
                 - Template safety
                 - Component size and responsibilities
```

---

### 7.5 Spring Boot API Designer (markdown + OpenAPI)

```yaml
customModes:
  - slug: api-designer
    name: 📐 API Designer
    description: Design REST APIs — OpenAPI specs, ADRs, markdown only
    roleDefinition: >-
      You are a REST API architect specializing in Spring Boot applications.
      You design APIs following REST best practices, Richardson Maturity Model
      level 2+, and OpenAPI 3.1. You produce: API contract YAML files,
      Architecture Decision Records (ADRs), and request/response examples.
      You never write implementation code — you only produce documentation
      and specifications.
    whenToUse: >-
      Use before implementation to design endpoints, request/response contracts,
      error codes, and pagination strategies.
    customInstructions: |-
      - Always include error response schemas (RFC 7807 Problem Details)
      - Version APIs under /api/v{n}/
      - Use kebab-case for URL segments
      - Document all status codes (200, 201, 400, 401, 403, 404, 422, 500)
      - Include curl examples for each endpoint
    groups:
      - read
      - - edit
        - fileRegex: \.(md|yaml|yml)$
          description: Markdown and OpenAPI YAML files only
```

---

### 7.6 Full-Stack Orchestrator

```yaml
customModes:
  - slug: fullstack-orchestrator
    name: 🔀 Full-Stack Orchestrator
    description: Coordinate Angular + Spring Boot feature implementation
    roleDefinition: >-
      You are a full-stack tech lead coordinating Angular frontend and
      Spring Boot backend development. You break features into: API design,
      backend domain implementation, backend REST layer, Angular service,
      Angular component, and tests. You delegate each to the right specialist
      and ensure consistency between frontend and backend contracts.
    whenToUse: >-
      Use for end-to-end feature implementation spanning both Angular and
      Spring Boot codebases. Ideal for new features that need API + UI.
    groups: []
```

---

## 8. Mode-Specific Instruction Files

For complex modes, put instructions in files instead of (or alongside) `customInstructions`. This is easier to maintain and version-control.

### IBM Bob — directory structure

```
.bob/
  rules-angular-dev/
    01-component-rules.md
    02-state-rules.md
    03-testing-rules.md
  rules-java-domain/
    01-architecture.md
    02-naming.md
```

### RooCode — directory structure

```
.roo/
  rules-angular-dev/
    01-component-rules.md
    02-state-rules.md
  rules-java-tdd/
    01-junit5-conventions.md
```

### Example instruction file: `.roo/rules-angular-dev/01-component-rules.md`

```markdown
# Angular Component Rules

## Always standalone
All components must have `standalone: true`. NgModule is forbidden.

## Change detection
Always use `ChangeDetectionStrategy.OnPush`.

## State management
- Use `signal<T>()` for mutable local state
- Use `computed()` for derived values
- Use `effect()` only for side-effects (logging, localStorage)
- Never use BehaviorSubject inside components

## Template safety
- Never use `[innerHTML]` with unsanitized data
- Always use the async pipe or explicit subscriptions — never subscribe in templates

## Selector convention
All component selectors must start with `ec-`.
```

### Example instruction file: `.bob/rules-java-domain/01-architecture.md`

```markdown
# Hexagonal Architecture Rules

## Layer boundaries

| Layer | Package | Allowed dependencies |
|---|---|---|
| Domain | `domain.*` | Nothing external |
| Application | `application.*` | Domain only |
| Infrastructure | `infrastructure.*` | Application + Spring/JPA |

## Domain rules
- No Spring annotations in `domain.*` packages
- No JPA annotations in `domain.*` packages
- Use primitive types or Value Objects — no raw String IDs
- All aggregate roots must have an ID value object

## Naming conventions
- Ports: `{Entity}Repository`, `{Action}Port`
- Adapters: `Jpa{Entity}Repository`, `Http{Service}Adapter`
- Application services: `{Entity}ApplicationService`
```

---

## 9. Overriding Default Modes

Override a built-in mode (same slug) to restrict it to your stack.

### Project-level override — Java-only Code mode

**`.bob/custom_modes.yaml` or `.roomodes`:**

```yaml
customModes:
  - slug: code
    name: 💻 Code (Java + Angular only)
    description: Code mode restricted to Java and Angular files
    roleDefinition: >-
      You are a senior full-stack engineer working on a Spring Boot + Angular
      codebase. You follow the team's DDD hexagonal architecture on the backend
      and standalone signal-based components on the frontend.
    customInstructions: |-
      - Backend: Java 17, Spring Boot 3.x, Maven
      - Frontend: Angular 17+, standalone, signals, SCSS
      - Never suggest adding new dependencies without approval
      - Always run `mvn verify` after backend changes
      - Always run `ng build` after frontend changes
    groups:
      - read
      - - edit
        - fileRegex: \.(java|ts|html|scss|xml|json|yaml|yml|md)$
          description: Full-stack project files
      - command
```

---

## 10. Configuration Precedence & File Locations

### Precedence (highest to lowest)

```
Project mode (.bob/custom_modes.yaml or .roomodes)
    ↓  overrides completely (no merging)
Global mode (custom_modes.yaml in settings dir)
    ↓  overrides completely
Default built-in modes
```

### File locations

| Tool | Scope | File |
|---|---|---|
| IBM Bob | Project | `.bob/custom_modes.yaml` |
| IBM Bob | Global | Settings → Edit Global Modes → `custom_modes.yaml` |
| RooCode | Project | `.roomodes` (YAML or JSON) |
| RooCode | Global | `~/.roo/` → `custom_modes.yaml` |

### Instruction file locations

| Tool | Scope | Path |
|---|---|---|
| IBM Bob | Project | `.bob/rules-{slug}/` |
| IBM Bob | Global | `~/.bob/rules-{slug}/` |
| RooCode | Project | `.roo/rules-{slug}/` |
| RooCode | Global | `~/.roo/rules-{slug}/` |

> ⚠️ Project modes **completely replace** global modes with the same slug — properties are not merged.

---

## 11. Regex Cheat Sheet for File Restrictions

All patterns apply to the **full relative path** from the workspace root.

| Pattern (YAML) | JSON `fileRegex` | What it matches |
|---|---|---|
| `\.java$` | `"\\.java$"` | All Java files |
| `^src/main/java/.*\.java$` | `"^src/main/java/.*\\.java$"` | Main Java sources only |
| `^src/test/java/.*\.java$` | `"^src/test/java/.*\\.java$"` | Test Java sources only |
| `\.(ts\|html\|scss)$` | `"\\.(ts\|html\|scss)$"` | Angular source files |
| `^src/app/.*\.(ts\|html)$` | `"^src/app/.*\\.(ts\|html)$"` | Angular app folder |
| `^(?!.*(spec\|test)).*\.ts$` | `"^(?!.*(spec\|test)).*\\.ts$"` | TS files excluding specs |
| `^src/test/.*spec\.ts$` | `"^src/test/.*spec\\.ts$"` | Angular spec files only |
| `\.(md\|yaml\|yml)$` | `"\\.(md\|yaml\|yml)$"` | Docs and config files |
| `pom\.xml$` | `"pom\\.xml$"` | Maven POM files |
| `application.*\.yaml$` | `"application.*\\.yaml$"` | Spring Boot config files |

> **YAML**: single backslash (`\.`)  
> **JSON**: double backslash (`\\.`)

---

## 12. Best Practices

### Mode selection

- **Always start with Plan/Architect** for any feature larger than a simple fix. Use it to write `docs/design/{feature}.md` before a single line of code is touched.
- **Use Ask mode** to understand an unfamiliar piece of code before modifying it — it cannot accidentally touch files.
- **Use Debug mode** (RooCode) or switch to Code mode with explicit instructions to only read and log first.
- **Never use Orchestrator for simple tasks** — the overhead isn't worth it for a single-file change.

### Custom mode design

- Keep `roleDefinition` focused and opinionated. Vague roles produce generic output.
- Put behavioral rules in `customInstructions` or instruction files, not in the `roleDefinition`.
- Use `fileRegex` to enforce layer boundaries — a Domain mode that can only touch `src/main/java/*/domain/**` literally cannot pollute the infrastructure layer.
- Use `whenToUse` so the Orchestrator can correctly delegate to your custom modes automatically.

### Team & project setup

- Commit `.bob/custom_modes.yaml` and `.roomodes` to version control — modes are part of your project's tooling.
- Commit `.bob/rules-{slug}/` and `.roo/rules-{slug}/` directories — instruction files should be reviewed like code.
- Name modes after roles, not tasks: `java-domain` not `create-java-service`. The Orchestrator needs role-based routing.
- Export modes (RooCode UI → Export Mode) before making big changes — it's a free backup.

### Safety

- Production-sensitive projects: create a **read-only Review mode** with only the `read` group. Use it for investigations on prod branches.
- Restrict `command` access in modes that don't need it — an LLM with unrestricted terminal access on a build server is a risk.
- For shared team modes, prefer project-level `.roomodes` / `.bob/custom_modes.yaml` over global settings to ensure everyone runs the same configuration.

### Angular-specific tips

- Create separate modes for **component scaffolding** (strict file pattern) and **testing** (test files only). Avoid one catch-all Angular mode.
- Include your component selector prefix (`ec-`) and your component library (`@ngx-templates`) in the role definition — the AI will use them consistently.

### Java-specific tips

- Use layer-restricted `fileRegex` patterns to enforce hexagonal boundaries at the tooling level.
- Include your testing conventions (AssertJ, `@DisplayName`, `given_when_then`) in `customInstructions` — without this, the AI defaults to generic JUnit 5.
- Add `mvn verify` to the custom instructions of your Java Code mode so the AI validates builds after changes.

---

## 13. Community Libraries & Existing Modes

### RooCode — Built-in Marketplace

The Roo Code Marketplace is available directly within the Roo Code extension in VS Code (marketplace icon in the top menu bar). One-click install of community modes and MCPs.

**Docs:** https://docs.roocode.com/features/marketplace  
**How to access:** RooCode panel → marketplace icon → filter "Modes" → search `java`, `spring`, `angular`

Java- and Angular-specific modes are sparse compared to JS/TS ones, but the collection grows continuously. When you install a mode: Project scope → `.roomodes`; Global scope → `custom_modes.yaml`.

---

### GitHub — jtgsystems/Custom-Modes-Roo-Code

171 specialized AI agents: Core Development (36), Language Specialists (23 — including Java/Spring Boot, Go, Python, TypeScript, Rust, C#), DevOps (14), Security (13), Meta-Orchestration (28).

**Repo:** https://github.com/jtgsystems/Custom-Modes-Roo-Code  
**Stars:** ~155 · **License:** MIT

```bash
git clone https://github.com/jtgsystems/Custom-Modes-Roo-Code.git
# Java agent at: agents/language-specialists/java/java-developer.yaml
```

> ⚠️ Uses a non-standard YAML structure (`role`, `capabilities`, `frameworks`). You'll need to adapt content into `roleDefinition` / `customInstructions` fields before using with RooCode.

---

### GitHub — jezweb/roo-commander

The best reference implementation of the **Mode + Rules + Skills** combined pattern. Ships an Orchestrator mode that discovers skills before delegating to Code/Architect/Debug, plus 60+ production-tested skills and a CLI.

**Repo:** https://github.com/jezweb/roo-commander

```bash
npx roocommander init        # bootstraps the whole system
roocommander search java     # find Java-related skills
```

---

### agentskills.io — Cross-Tool Community Skills Library

Compatible with RooCode, IBM Bob, Claude Code, Gemini CLI, Cline. Universal install path: `.agents/skills/`.

**Site:** https://agentskills.io  
**GitHub (skills collection):** https://github.com/wondelai/skills

**RooCode:** copy/symlink into `.roo/skills/` or use `.agents/skills/` directly.  
**IBM Bob:** add the path to `~/.bob/settings.json`:
```json
{ "context": { "includeDirectories": ["/Users/you/.agents/skills/"] } }
```

---

### IBM Bob — No Public Marketplace (Yet)

No mode marketplace. Sharing is manual: commit `.bob/custom_modes.yaml` and `.bob/rules-{slug}/` to Git, or export YAML files via the Export Mode button.

**Bob Modes docs:** https://bob.ibm.com/docs/ide/features/modes  
**Bob Custom Modes config:** https://bob.ibm.com/docs/ide/configuration/custom-modes  
**Bob Skills docs:** https://bob.ibm.com/docs/ide/features/skills *(Advanced mode only)*

---

### Summary Table

| Source | Tool | Coverage | URL |
|---|---|---|---|
| **RooCode Marketplace** | RooCode | React, Docs, Testing, Java (growing) | Built-in in extension |
| **jtgsystems/Custom-Modes-Roo-Code** | RooCode | 171 agents — Java, Go, Python, DevOps | https://github.com/jtgsystems/Custom-Modes-Roo-Code |
| **jezweb/roo-commander** | RooCode | Full-stack + 60 skills, Mode+Rules+Skills reference | https://github.com/jezweb/roo-commander |
| **agentskills.io** | RooCode + Bob + Claude Code | Cross-tool skills library | https://agentskills.io |
| **Manual team sharing** | Bob + RooCode | Your own team modes | Commit to git |

---

### Recommendation for Angular + Java Teams

**IBM Bob:** Build your own modes from the examples in section 7. Commit `.bob/custom_modes.yaml` and `.bob/rules-*/` to your monorepo. Use agentskills.io for skills (Advanced mode only).

**RooCode:** Start with the in-app Marketplace, then pull the Java specialist from `jtgsystems/Custom-Modes-Roo-Code`. Study `jezweb/roo-commander` for the complete Mode + Rules + Skills architecture pattern.
