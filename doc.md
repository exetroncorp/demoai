LensIDE Clone: Documentation DiagramsThis document provides visual diagrams using Mermaid syntax to illustrate the application's architecture, data model, and key user flows.1. Entity Relationship Diagram (ERD)This diagram shows the main data entities and their relationships as defined in the JDL.erDiagram
    CLUSTER ||--o{ NAMESPACE : contains
    NAMESPACE ||--|{ JUPYTERHUB_INSTANCE : hosts
    NAMESPACE }o--o{ USER_PROFILE : accessed_by
    NAMESPACE_USER_ACCESS {
        Role role
    }
    NAMESPACE -- USER_PROFILE : (NamespaceUserAccess)

    CLUSTER {
        String name PK
        // other attributes
    }
    NAMESPACE {
        String name PK
        String vip
        String url
        // FK to CLUSTER
        // FK to JUPYTERHUB_INSTANCE
    }
    JUPYTERHUB_INSTANCE {
        String url PK
        String status
        // FK to NAMESPACE
    }
    USER_PROFILE {
        String username PK
        // other attributes from JHipster User + UserProfile
    }
    NAMESPACE_USER_ACCESS {
        // FK to NAMESPACE
        // FK to USER_PROFILE
        Role role
    }

A CLUSTER can contain one or more NAMESPACEs.A NAMESPACE hosts exactly one JUPYTERHUB_INSTANCE.A NAMESPACE can be accessed by many USER_PROFILEs, and a USER_PROFILE can access many NAMESPACEs. The relationship details (like the role) are stored in the NAMESPACE_USER_ACCESS association entity.2. High-Level Architecture DiagramThis diagram shows the main components of the system and how they interact.graph TD
    subgraph Browser
        A[Angular Frontend]
    end

    subgraph Server (Spring Boot)
        B(API Gateway / Controllers)
        C(WebSocket Handler)
        D(Application Services)
        E(Domain Layer)
        F(Infrastructure Layer)
    end

    subgraph Data Storage
        G[SQL Database (PostgreSQL/H2)]
    end

    subgraph External/Managed Systems
        H(JupyterHub Instances)
        I(Server-Side Terminal Process)
    end

    A -- HTTP REST --> B
    A -- WebSocket --> C

    B -- Calls --> D
    C -- Calls --> D

    D -- Uses --> E
    D -- Uses --> F

    F -- Accesses --> G
    F -- Interacts with --> H(Potentially via API/Scripts)
    F -- Manages/Connects to --> I

    %% Styling (optional)
    classDef browser fill:#f9f,stroke:#333,stroke-width:2px;
    classDef server fill:#ccf,stroke:#333,stroke-width:2px;
    classDef db fill:#cfc,stroke:#333,stroke-width:2px;
    classDef external fill:#fcc,stroke:#333,stroke-width:2px;

    class A browser;
    class B,C,D,E,F server;
    class G db;
    class H,I external;
The Angular Frontend communicates with the Spring Boot Backend via REST APIs and WebSockets.The Backend follows Clean Architecture: Controllers/WebSocket Handlers interact with Application Services, which orchestrate domain logic and interact with the Infrastructure Layer.The Infrastructure Layer handles database access, and potentially interacts with external JupyterHub instances or manages the server-side processes for the web terminal.3. Admin User Flow: Create Namespace & Assign UserThis sequence diagram illustrates the steps an administrator might take to create a new namespace and grant access to a user.sequenceDiagram
    participant Admin as Admin User
    participant FE as Angular Frontend
    participant BE as Spring Boot Backend (API)
    participant DB as Database

    Admin->>+FE: Navigates to Create Namespace page (selects Cluster)
    FE->>Admin: Displays Namespace creation form
    Admin->>+FE: Fills form (Name, URL, etc.) & Submits
    FE->>+BE: POST /api/namespaces (Namespace data)
    BE->>+DB: Persist new Namespace entity (associating with Cluster, creating JupyterHubInstance record)
    DB-->>-BE: Confirms Namespace creation
    BE-->>-FE: Returns success (201 Created) + new Namespace details
    FE-->>-Admin: Shows success message & updated Namespace list

    Admin->>+FE: Navigates to Namespace details / User Access page
    FE->>+BE: GET /api/namespaces/{id}/users (or similar)
    BE->>+DB: Fetch users associated with Namespace {id}
    DB-->>-BE: Returns user list (if any)
    BE-->>-FE: Returns user list
    FE->>Admin: Displays current user access list & Add User form

    Admin->>+FE: Selects User, selects Role (e.g., DEV), Submits
    FE->>+BE: POST /api/namespaces/{id}/users (or similar endpoint for access grant - User ID, Role)
    BE->>+DB: Create NamespaceUserAccess record linking Namespace {id}, User ID, and Role
    DB-->>-BE: Confirms access grant
    BE-->>-FE: Returns success (200 OK or 201 Created)
    FE-->>-Admin: Shows updated user access list for the Namespace
4. Developer User Flow: Access TerminalThis sequence diagram shows how a developer accesses the web terminal for a namespace they have permission for.sequenceDiagram
    participant Dev as Developer User
    participant FE as Angular Frontend (Xterm.js)
    participant BE_WS as Spring Boot Backend (WebSocket Handler)
    participant BE_SVC as Spring Boot Backend (Services/Auth)
    participant TermSrv as Server-Side Terminal Process

    Dev->>+FE: Navigates to Namespace details page
    FE->>Dev: Displays Namespace info, JupyterHub link, and "Launch Terminal" button
    Dev->>+FE: Clicks "Launch Terminal"
    FE->>+BE_WS: Initiates WebSocket connection (e.g., /websocket/terminal/{namespaceId}) with auth token
    BE_WS->>+BE_SVC: Validates Auth Token & User Permissions for Namespace {namespaceId}
    BE_SVC-->>-BE_WS: Confirms user is authorized
    BE_WS->>+TermSrv: Initiates/Connects to appropriate terminal process for user/namespace
    TermSrv-->>-BE_WS: Terminal process ready (e.g., PTY established)
    BE_WS-->>-FE: WebSocket connection established

    %% Terminal Interaction Loop
    loop Terminal Session
        Dev->>+FE: Types command (e.g., "ls -l") into Xterm.js
        FE->>BE_WS: Sends command input over WebSocket
        BE_WS->>TermSrv: Forwards command to terminal process stdin
        TermSrv->>BE_WS: Sends command output (stdout/stderr) back
        BE_WS->>FE: Forwards output over WebSocket
        FE->>Dev: Displays output in Xterm.js
    end

    Dev->>+FE: Closes terminal tab/window or disconnects
    FE->>BE_WS: WebSocket connection closed by client
    BE_WS->>TermSrv: Signals terminal process to terminate or disconnects
    TermSrv-->>-BE_WS: Acknowledges closure (optional)
    BE_WS-->>-FE: Confirms WebSocket closure
You can copy and paste the Mermaid code blocks into tools or documentation platforms that support Mermaid rendering (like GitLab, GitHub Markdown, Obsidian, dedicated online editors, etc.).
