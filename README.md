# ForgeIQ

## AI-Powered Software Architecture & Static Code Analysis Platform

ForgeIQ is a full-stack software analysis platform designed to help
developers understand a Python project as a **system**, rather than as a
collection of isolated source files.

A user uploads a Python project as a ZIP archive. ForgeIQ scans the
project, parses Python source code into Abstract Syntax Trees (ASTs),
calculates source-code metrics, evaluates maintainability, detects code
smells, resolves internal and external dependencies, builds a dependency
graph, detects circular dependencies, estimates module impact, infers
architectural organization, calculates engineering priority, evaluates
project health, and generates engineering recommendations.

> **Important implementation note**
>
> The current ForgeIQ implementation is primarily a
> deterministic/static-analysis engine. The project is designed with an
> AI/LLM layer in mind, but the uploaded implementation does **not**
> currently send the analyzed project to an LLM. The term "AI-powered"
> describes the product vision and future intelligence layer; the
> current analysis results are produced by the implemented
> static-analysis services and rules.

------------------------------------------------------------------------

## Table of Contents

-   [1. What is ForgeIQ?](#1-what-is-forgeiq)
-   [2. The Problem ForgeIQ Solves](#2-the-problem-forgeiq-solves)
-   [3. What ForgeIQ Does](#3-what-forgeiq-does)
-   [4. Feature Overview](#4-feature-overview)
-   [5. End-to-End Analysis Pipeline](#5-end-to-end-analysis-pipeline)
-   [6. Detailed Analysis Features](#6-detailed-analysis-features)
    -   [6.1 Project File Scanning](#61-project-file-scanning)
    -   [6.2 AST Parsing](#62-ast-parsing)
    -   [6.3 Source-Code Metrics](#63-source-code-metrics)
    -   [6.4 Cyclomatic Complexity](#64-cyclomatic-complexity)
    -   [6.5 Maintainability Analysis](#65-maintainability-analysis)
    -   [6.6 Code Smell Detection](#66-code-smell-detection)
    -   [6.7 Dependency Analysis](#67-dependency-analysis)
    -   [6.8 Dependency Graph](#68-dependency-graph)
    -   [6.9 Graph Analysis](#69-graph-analysis)
    -   [6.10 Circular Dependency
        Detection](#610-circular-dependency-detection)
    -   [6.11 Module Impact Analysis](#611-module-impact-analysis)
    -   [6.12 Architecture Detection](#612-architecture-detection)
    -   [6.13 Project Health](#613-project-health)
    -   [6.14 Engineering Priority](#614-engineering-priority)
    -   [6.15 Recommendations](#615-recommendations)
    -   [6.16 Project Report](#616-project-report)
-   [7. Authentication and Account
    Features](#7-authentication-and-account-features)
-   [8. Upload and Analysis Lifecycle](#8-upload-and-analysis-lifecycle)
-   [9. System Architecture](#9-system-architecture)
-   [10. Backend Architecture](#10-backend-architecture)
-   [11. Frontend Architecture](#11-frontend-architecture)
-   [12. Database Design](#12-database-design)
-   [13. API Reference](#13-api-reference)
-   [14. Analysis Response Structure](#14-analysis-response-structure)
-   [15. Dashboard](#15-dashboard)
-   [16. Technology Stack](#16-technology-stack)
-   [17. Prerequisites](#17-prerequisites)
-   [18. Project Setup](#18-project-setup)
    -   [18.1 Clone the Repository](#181-clone-the-repository)
    -   [18.2 Python Environment](#182-python-environment)
    -   [18.3 Backend Dependencies](#183-backend-dependencies)
    -   [18.4 MySQL](#184-mysql)
    -   [18.5 Environment Variables](#185-environment-variables)
    -   [18.6 Frontend Dependencies](#186-frontend-dependencies)
-   [19. Running ForgeIQ Without
    Docker](#19-running-forgeiq-without-docker)
-   [20. Running ForgeIQ With Docker](#20-running-forgeiq-with-docker)
-   [21. Docker Architecture](#21-docker-architecture)
-   [22. Database and Alembic](#22-database-and-alembic)
-   [23. API Documentation with
    Swagger](#23-api-documentation-with-swagger)
-   [24. Example API Workflow](#24-example-api-workflow)
-   [25. Security Model](#25-security-model)
-   [26. Error Handling](#26-error-handling)
-   [27. Repository Structure](#27-repository-structure)
-   [28. Service-by-Service Backend
    Guide](#28-service-by-service-backend-guide)
-   [29. Frontend Component Guide](#29-frontend-component-guide)
-   [30. Configuration Reference](#30-configuration-reference)
-   [31. Testing and Verification](#31-testing-and-verification)
-   [32. Troubleshooting](#32-troubleshooting)
-   [33. Development Workflow](#33-development-workflow)
-   [34. Current Implementation
    Status](#34-current-implementation-status)
-   [35. Current Limitations](#35-current-limitations)
-   [36. Future AI / LLM Layer](#36-future-ai--llm-layer)
-   [37. Future Scope](#37-future-scope)
-   [38. Project Vision](#38-project-vision)
-   [39. License](#39-license)

------------------------------------------------------------------------

# 1. What is ForgeIQ?

ForgeIQ is a web application for **software architecture intelligence
and static code analysis**.

The core idea is:

``` text
Traditional AI Code Assistant

Source Code
     |
     v
    LLM
     |
     v
Generic Answer
```

ForgeIQ is designed around:

``` text
ForgeIQ

Source Code
     |
     v
File Scanner
     |
     v
AST Parser
     |
     +--------------------+
     |                    |
     v                    v
Code Metrics       Structural Analysis
     |                    |
     v                    v
Maintainability     Dependencies
Code Smells         Dependency Graph
Complexity          Module Impact
     |                    |
     +---------+----------+
               |
               v
       Architecture Analysis
               |
               v
        Project Health
               |
               v
      Engineering Priority
               |
               v
       Recommendations
               |
               v
          Dashboard
```

This architecture allows ForgeIQ to build a structured representation of
the project before any future AI/LLM reasoning layer is introduced.

------------------------------------------------------------------------

# 2. The Problem ForgeIQ Solves

Large software projects become difficult to understand because important
information is distributed across:

-   files
-   classes
-   functions
-   imports
-   modules
-   services
-   architectural layers
-   dependency relationships
-   code-quality problems

A developer may know that a project "works" while still having
difficulty answering questions such as:

-   Which files are the most complex?
-   Which modules have the largest impact?
-   Which modules depend on each other?
-   Are there circular dependencies?
-   Which files have poor maintainability?
-   Where are code smells concentrated?
-   Which modules are heavily depended upon?
-   What architectural layers exist?
-   What should the development team fix first?
-   What is the overall health of the project?

ForgeIQ converts source code into a structured set of engineering
signals intended to answer these questions.

------------------------------------------------------------------------

# 3. What ForgeIQ Does

The current implementation supports the following workflow:

1.  A user creates or accesses a ForgeIQ account.
2.  The user authenticates using email/password or Google
    authentication.
3.  The user uploads a Python project as a `.zip` file.
4.  ForgeIQ creates a project record associated with the authenticated
    user.
5.  The ZIP archive is stored and extracted.
6.  Python files are discovered recursively.
7.  Each Python file is parsed with Python's AST module.
8.  Structural information is extracted.
9.  Source-code metrics are calculated.
10. Maintainability is estimated.
11. Code smells are detected.
12. Internal and external dependencies are identified.
13. A module dependency graph is built.
14. Graph-level relationships are analyzed.
15. Circular dependencies are detected.
16. Fan-in/fan-out module impact is calculated.
17. Engineering priority is assigned to files.
18. Project health is calculated.
19. Architecture is inferred from project structure.
20. Engineering recommendations are generated.
21. A structured project report is generated.
22. Important results are persisted in MySQL.
23. The React dashboard presents the analysis.

------------------------------------------------------------------------

# 4. Feature Overview

  -----------------------------------------------------------------------
  Feature                             Purpose
  ----------------------------------- -----------------------------------
  User registration                   Creates a ForgeIQ account

  Email/password login                Authenticates users using JWT

  Google login                        Supports Google Identity
                                      authentication

  Password reset                      Uses an emailed six-digit OTP

  ZIP upload                          Accepts Python projects as ZIP
                                      archives

  File scanning                       Finds Python source files
                                      recursively

  AST parsing                         Understands Python source structure

  Code metrics                        Measures lines, imports, classes,
                                      functions and methods

  Complexity analysis                 Estimates cyclomatic complexity

  Maintainability                     Produces a 0--100 maintainability
                                      index

  Code smells                         Detects selected structural quality
                                      issues

  Dependency analysis                 Separates internal and external
                                      imports

  Dependency graph                    Represents module relationships

  Graph analysis                      Finds connected and orphan modules

  Cycle detection                     Finds circular module dependencies

  Module impact                       Calculates fan-in and fan-out

  Architecture detection              Infers common architectural
                                      organization

  Project health                      Produces a 0--100 project health
                                      score

  Engineering priority                Ranks files by engineering
                                      risk/attention

  Recommendations                     Converts detected issues into
                                      actions

  Project report                      Produces a consolidated
                                      project-level report

  Persistent analysis                 Stores project, source-file,
                                      analysis and recommendation data

  Web dashboard                       Presents project-level and
                                      file-level insights
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 5. End-to-End Analysis Pipeline

ForgeIQ's central processing pipeline is implemented by
`ProjectAnalyzer`.

``` text
                       ZIP PROJECT
                            |
                            v
                  +-------------------+
                  |   File Scanner    |
                  +-------------------+
                            |
                            v
                  Python source files
                            |
                            v
                  +-------------------+
                  |    AST Parser     |
                  +-------------------+
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
          Metrics       Complexity     Structure
             |              |              |
             +--------------+--------------+
                            |
                            v
                  +-------------------+
                  | Maintainability   |
                  +-------------------+
                            |
                            v
                  +-------------------+
                  |  Code Smells      |
                  +-------------------+
                            |
                            v
                  +-------------------+
                  | Dependencies      |
                  +-------------------+
                            |
                            v
                  +-------------------+
                  | Dependency Graph  |
                  +-------------------+
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
          Graph         Cycles        Module Impact
          Analysis      Detection
             |              |              |
             +--------------+--------------+
                            |
                            v
                  +-------------------+
                  | Architecture      |
                  +-------------------+
                            |
                            v
                  +-------------------+
                  | Engineering       |
                  | Priority          |
                  +-------------------+
                            |
                            v
                  +-------------------+
                  | Project Health    |
                  +-------------------+
                            |
                            v
                  +-------------------+
                  | Recommendations   |
                  +-------------------+
                            |
                            v
                  +-------------------+
                  | Project Report    |
                  +-------------------+
                            |
                            v
                       DASHBOARD
```

------------------------------------------------------------------------

# 6. Detailed Analysis Features

## 6.1 Project File Scanning

ForgeIQ recursively searches the extracted project directory for `.py`
files.

The scanner intentionally ignores:

-   `__MACOSX` metadata folders
-   AppleDouble files whose names begin with `._`

This is important because ZIP files created on macOS can contain
filesystem metadata that should not be interpreted as source code.

The scanner is implemented in:

``` text
app/services/file_scanner.py
```

------------------------------------------------------------------------

## 6.2 AST Parsing

ForgeIQ uses Python's built-in `ast` module to parse source files.

The AST parser extracts:

### Imports

Both:

``` python
import requests
```

and:

``` python
from app.services.foo import Foo
```

are represented as imports.

### Classes

For each top-level class, ForgeIQ extracts:

-   class name
-   source line number
-   base classes
-   class docstring
-   methods

### Methods

For each method:

-   name
-   parameters
-   decorators
-   async status
-   docstring
-   line number
-   cyclomatic complexity
-   complexity risk

### Functions

Module-level functions receive similar information:

-   name
-   parameters
-   decorators
-   async status
-   docstring
-   line number
-   cyclomatic complexity
-   complexity risk

The raw AST tree is used internally and removed before the API response
is assembled.

Implementation:

``` text
app/services/ast_parser.py
```

------------------------------------------------------------------------

## 6.3 Source-Code Metrics

ForgeIQ calculates per-file metrics.

  Metric            Meaning
  ----------------- --------------------------------------------
  `total_lines`     Total number of source lines
  `code_lines`      Lines that are not blank/comment lines
  `blank_lines`     Empty lines
  `comment_lines`   Lines beginning with `#`
  `imports`         Number of parsed import statements/modules
  `classes`         Number of top-level classes
  `functions`       Number of top-level functions
  `methods`         Number of methods inside detected classes

The project summary aggregates these metrics across all analyzed Python
files.

Implementation:

``` text
app/services/metrics_engine.py
app/services/project_summary.py
```

### Example

If a file contains:

``` python
# comment

import os

def hello():
    print("Hello")
```

the metric engine distinguishes:

``` text
Total lines
Code lines
Blank lines
Comment lines
Imports
Functions
```

This provides a simple quantitative view of source size and structure.

------------------------------------------------------------------------

## 6.4 Cyclomatic Complexity

ForgeIQ calculates a lightweight cyclomatic complexity score using an
AST visitor.

The starting complexity is:

``` text
1
```

The analyzer increases complexity for:

-   `if`
-   `for`
-   `while`
-   `try` handlers
-   boolean operations
-   `match` cases

Conceptually:

``` text
Complexity = 1 + decision points
```

### Complexity risk

The AST parser categorizes functions and methods as:

    Complexity Risk
  ------------ ----------
        `<= 5` Low
        `6–10` Moderate
       `11–20` High
        `> 20` Critical

Implementation:

``` text
app/services/complexity_analyzer.py
```

and the extracted complexity information is attached by:

``` text
app/services/ast_parser.py
```

> This is a project-specific complexity implementation. It should not be
> described as a full replacement for every industrial complexity
> metric.

------------------------------------------------------------------------

## 6.5 Maintainability Analysis

ForgeIQ calculates a project-specific maintainability index for each
file.

The calculation begins at:

``` text
100
```

and applies the implemented rules:

``` text
Penalty for code lines:
    code_lines // 5

Penalty for top-level functions:
    functions * 2

Penalty for methods:
    methods

Comment contribution:
    comment_lines // 2
```

The final score is clamped to:

``` text
0–100
```

### Rating

       Score Rating
  ---------- -----------
    `85–100` Excellent
     `70–84` Good
     `50–69` Fair
      `0–49` Poor

Implementation:

``` text
app/services/maintainability_analyzer.py
```

This score is intended as a practical project-specific indicator, not as
a claim of strict ISO-standard maintainability measurement.

------------------------------------------------------------------------

## 6.6 Code Smell Detection

ForgeIQ currently detects four main categories of structural code
smells.

### 1. Long Function

A function is flagged when it is longer than:

``` text
40 lines
```

Severity:

``` text
Medium
```

------------------------------------------------------------------------

### 2. Long Parameter List

A function is flagged when it has more than:

``` text
5 parameters
```

Severity:

``` text
Medium
```

------------------------------------------------------------------------

### 3. Missing Docstring

Classes and functions are checked for docstrings.

Constructors named:

``` python
__init__
```

are excluded from this check.

Severity:

``` text
Low
```

------------------------------------------------------------------------

### 4. Large Class

A class is flagged when it contains more than:

``` text
10 methods
```

Severity:

``` text
High
```

Implementation:

``` text
app/services/code_smell_analyzer.py
```

### Code smell output

Each detected smell contains information such as:

``` json
{
  "type": "Long Function",
  "severity": "Medium",
  "location": "calculate",
  "message": "Function 'calculate' contains 57 lines."
}
```

------------------------------------------------------------------------

## 6.7 Dependency Analysis

ForgeIQ distinguishes between:

``` text
Internal Dependencies
External Dependencies
```

For every import, the dependency analyzer attempts to determine whether
the imported module belongs to the analyzed project.

The resolver uses several matching strategies:

1.  exact module match
2.  short/local module matching
3.  package/parent matching
4.  external dependency fallback

Example:

``` text
Project

app.services.auth
app.services.email
app.models.user
```

If:

``` python
from app.models.user import User
```

is detected, ForgeIQ attempts to resolve it to an internal module.

If:

``` python
import requests
```

cannot be matched against project modules, it is treated as external.

Output:

``` json
{
  "internal": [
    "app.models.user"
  ],
  "external": [
    "requests"
  ],
  "total_internal": 1,
  "total_external": 1
}
```

Implementation:

``` text
app/services/dependency_analyzer.py
```

------------------------------------------------------------------------

## 6.8 Dependency Graph

After file-level dependency analysis, ForgeIQ converts the relationships
into a module graph.

A file such as:

``` text
app/services/auth.py
```

becomes:

``` text
app.services.auth
```

and the graph stores its internal dependencies.

Example:

``` text
app.api.routes.users
        |
        v
app.models.user

app.services.auth
        |
        +------> app.models.user
        |
        +------> app.core.security
```

Implementation:

``` text
app/services/dependency_graph_builder.py
```

------------------------------------------------------------------------

## 6.9 Graph Analysis

ForgeIQ performs additional analysis on the dependency graph.

### Most connected module

The graph analyzer identifies the module with the greatest number of
outgoing dependencies.

### Orphan modules

A module is considered orphaned when:

``` text
outgoing dependencies = 0
AND
incoming dependencies = 0
```

### Circular dependencies

The graph analyzer delegates cycle detection to `CycleDetector`.

Implementation:

``` text
app/services/graph_analyzer.py
app/services/graph_utils.py
```

------------------------------------------------------------------------

## 6.10 Circular Dependency Detection

ForgeIQ detects cycles in the module dependency graph.

Example:

``` text
A
|
v
B
|
v
C
|
v
A
```

This represents:

``` text
A → B → C → A
```

which is a circular dependency.

Circular dependencies can make:

-   refactoring harder
-   module ownership unclear
-   testing more difficult
-   changes propagate unpredictably
-   architecture more tightly coupled

The implementation uses a DFS-style traversal with a recursion stack.

Implementation:

``` text
app/services/cycle_detector.py
```

Circular dependencies also influence:

-   engineering priority
-   project health
-   recommendations
-   project report critical issues

------------------------------------------------------------------------

## 6.11 Module Impact Analysis

ForgeIQ calculates two dependency-impact measurements.

### Fan-out

Number of modules a module depends on.

``` text
A → B
A → C
A → D

fan-out(A) = 3
```

### Fan-in

Number of modules that depend on a module.

``` text
A → C
B → C
D → C

fan-in(C) = 3
```

The implementation also calculates:

``` text
importance_score = fan_in + fan_out
```

Modules with an importance score of at least `2` can be classified as
core modules by the architecture analyzer.

Implementation:

``` text
app/services/module_impact_analyzer.py
```

------------------------------------------------------------------------

## 6.12 Architecture Detection

ForgeIQ uses project structure and module relationships to infer
architecture.

The current implementation recognizes:

### Layered Architecture

Detected when the project contains evidence of:

-   presentation
-   application
-   domain

For example:

``` text
api/
services/
models/
```

### Modular Architecture

Detected when the project contains meaningful domain/application
organization but does not meet the layered-architecture condition.

### Unclassified

Returned when the structural signals do not match the implemented
architecture rules.

Implementation:

``` text
app/services/architecture_analyzer.py
```

### Detected layers

Files can be classified into:

``` text
Presentation
Application
Domain
Infrastructure
```

The classifier looks for directory patterns such as:

``` text
api/
routes/
controllers/

services/
usecases/
application/

models/
entities/
domain/
schemas/

database/
repositories/
infrastructure/
storage/
```

### Entry points

ForgeIQ checks for common Python entry-point filenames:

``` text
main.py
app.py
server.py
run.py
manage.py
wsgi.py
asgi.py
```

### Core modules

Core modules are selected using fan-in and fan-out impact.

### Architecture issues

The implementation currently checks for conditions including:

-   high coupling
-   high dependency
-   orphan modules

------------------------------------------------------------------------

## 6.13 Project Health

ForgeIQ combines several signals into a project health score from:

``` text
0–100
```

The calculation begins from the average maintainability score and
applies penalties.

### Starting value

``` text
average maintainability
```

### Code smell penalty

Up to `20` points:

``` text
2 points per smell
```

### Circular dependency penalty

Up to `20` points:

``` text
10 points per circular dependency
```

### High-priority file penalty

Up to `20` points:

``` text
5 points per High/Critical file
```

The final score is clamped to `0–100`.

### Status

       Score Status
  ---------- -----------
    `85–100` Excellent
     `70–84` Good
     `50–69` Fair
      `0–49` Poor

The health result also includes factors:

``` json
{
  "average_maintainability": 82.4,
  "total_code_smells": 7,
  "circular_dependencies": 1,
  "high_priority_files": 2
}
```

Implementation:

``` text
app/services/project_health_analyzer.py
```

------------------------------------------------------------------------

## 6.14 Engineering Priority

Engineering priority is calculated at the file/module level.

The score combines several implemented signals.

### Complexity

    Average complexity   Points
  -------------------- --------
                `> 20`       40
                `> 10`       25
                 `> 5`       10

### Maintainability

    Maintainability   Points
  ----------------- --------
             `< 50`       30
             `< 70`       15

### Code smells

``` text
5 points per smell
maximum 30 points
```

### Internal dependency count

    Dependencies   Points
  -------------- --------
         `>= 10`       20
          `>= 5`       10

### Circular dependency

``` text
25 points
```

### Fan-in / module impact

     Fan-in   Points
  --------- --------
    `>= 10`       20
     `>= 5`       10
     `>= 2`        5

The final score is capped at `100`.

### Priority

      Score Priority
  --------- ----------
    `>= 70` Critical
    `40–69` High
    `20–39` Medium
     `< 20` Low

ForgeIQ also records the factors that contributed to the score.

Example:

``` json
{
  "score": 55,
  "priority": "High",
  "factors": [
    {
      "name": "Code Smells",
      "points": 15,
      "details": "3 code smell(s) detected"
    },
    {
      "name": "Circular Dependency",
      "points": 25,
      "details": "Module is part of a circular dependency"
    }
  ]
}
```

Implementation:

``` text
app/services/engineering_priority.py
```

------------------------------------------------------------------------

## 6.15 Recommendations

ForgeIQ converts detected conditions into engineering recommendations.

Recommendation categories include:

``` text
Dependency
Code Quality
Engineering Priority
Architecture
Project Health
```

### Circular dependency recommendation

The analyzer recommends restructuring cyclic relationships and suggests
approaches such as:

-   extracting shared functionality
-   introducing dependency injection
-   restructuring dependencies

### Code quality recommendation

For missing docstrings, the system recommends documenting:

-   purpose
-   parameters
-   return values where applicable

Other smells receive a general refactoring recommendation.

### Engineering priority recommendation

High and Critical files are recommended for early review.

### Architecture recommendation

Examples include:

``` text
Reduce high coupling.
Review highly depended-on modules.
Check orphan modules.
Refactor architectural issues.
```

### Project health recommendation

Health determines project-level recommendation priority:

``` text
< 50  → Critical
< 70  → High
< 85  → Medium
>= 85 → no health warning
```

Recommendations are sorted by:

``` text
Critical
High
Medium
Low
```

Implementation:

``` text
app/services/recommendation_engine.py
```

------------------------------------------------------------------------

## 6.16 Project Report

The project report generator creates a consolidated report containing:

### Overview

-   health score
-   health status
-   architecture
-   total files
-   total lines
-   total code lines
-   total classes
-   total functions

### Strengths

The implementation can report strengths such as:

-   high maintainability
-   low code complexity
-   successful project analysis

### Critical issues

The report collects:

-   circular dependencies
-   medium/high architecture issues
-   high-priority recommendations

### Architecture summary

Contains:

-   architecture type
-   entry points
-   core modules
-   detected layers

### Recommended actions

Recommendations are deduplicated by title and ordered by priority.

### File summary

Each file summary contains:

-   file path
-   maintainability
-   engineering priority
-   code smell count
-   module impact

Implementation:

``` text
app/services/project_report_generator.py
```

------------------------------------------------------------------------

# 7. Authentication and Account Features

ForgeIQ contains a complete account/authentication layer.

## 7.1 Registration

Endpoint:

``` http
POST /auth/register
```

Registration accepts:

``` json
{
  "email": "developer@example.com",
  "password": "Password123",
  "full_name": "Developer"
}
```

Username is optional in the API schema.

If no username is supplied, ForgeIQ derives one from the email address
and ensures uniqueness.

Passwords are hashed with `bcrypt`.

------------------------------------------------------------------------

## 7.2 Email/Password Login

Endpoint:

``` http
POST /auth/login
```

The endpoint uses FastAPI's OAuth2 password form.

The frontend submits:

``` text
username = email
password = password
```

The backend treats the `username` field as the user's email.

Successful authentication returns:

``` json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

------------------------------------------------------------------------

## 7.3 JWT Authentication

ForgeIQ uses:

``` text
OAuth2PasswordBearer
+
JWT
```

The token contains the user's email in:

``` text
sub
```

Protected endpoints retrieve the current user from the database using
that email.

The token expiry is configurable through:

``` text
ACCESS_TOKEN_EXPIRE_MINUTES
```

------------------------------------------------------------------------

## 7.4 Google Authentication

Endpoint:

``` http
POST /auth/google
```

The frontend uses Google Identity Services to obtain a credential.

The backend verifies the Google ID token, checks:

-   token validity
-   issuer
-   email verification
-   email
-   Google subject

and then issues the normal ForgeIQ JWT.

Google authentication requires:

``` text
GOOGLE_CLIENT_ID
```

on the backend and:

``` text
VITE_GOOGLE_CLIENT_ID
```

on the frontend.

------------------------------------------------------------------------

## 7.5 Password Reset

ForgeIQ implements an OTP-based password reset flow.

### Step 1: Request OTP

``` http
POST /auth/forgot-password
```

### Step 2: Verify OTP

``` http
POST /auth/verify-otp
```

### Step 3: Reset password

``` http
POST /auth/reset-password
```

The OTP is:

-   six digits
-   generated using a secure random generator
-   SHA-256 hashed before database storage
-   valid for 3 minutes
-   limited to 5 verification attempts
-   invalidated after successful use

The forgot-password endpoint intentionally returns a generic message so
that the API does not reveal whether an email address is registered.

------------------------------------------------------------------------

## 7.6 Welcome Email

After registration, ForgeIQ schedules a welcome email through FastAPI
background tasks.

Email delivery is controlled by:

``` text
MAIL_ENABLED
```

If email is disabled, the application logs that email delivery was
skipped.

------------------------------------------------------------------------

# 8. Upload and Analysis Lifecycle

The main upload endpoint is:

``` http
POST /projects/upload
```

It requires a valid JWT.

## Step 1 --- Validate file type

Only files whose name ends with:

``` text
.zip
```

are accepted.

------------------------------------------------------------------------

## Step 2 --- Create project

A `Project` record is created for the authenticated user.

The project name is derived from the ZIP filename.

------------------------------------------------------------------------

## Step 3 --- Store upload

The upload is stored under a structure similar to:

``` text
uploads/
└── user_<user_id>/
    └── project_<project_id>/
        ├── project.zip
        └── extracted/
```

------------------------------------------------------------------------

## Step 4 --- Update status

The project moves through states such as:

``` text
Uploaded
   ↓
Analyzing
   ↓
Completed
```

If analysis fails:

``` text
Analyzing
   ↓
Failed
```

------------------------------------------------------------------------

## Step 5 --- Extract ZIP

Python's `zipfile` module extracts the archive.

------------------------------------------------------------------------

## Step 6 --- Analyze

The extracted project is passed to:

``` text
ProjectAnalyzer.analyze_project()
```

------------------------------------------------------------------------

## Step 7 --- Persist results

ForgeIQ stores:

-   project analysis summary
-   source-file metrics
-   recommendations

in MySQL.

------------------------------------------------------------------------

## Step 8 --- Return result

The upload endpoint returns project information together with the
analysis result.

------------------------------------------------------------------------

# 9. System Architecture

``` text
                         ┌──────────────────────┐
                         │      Developer       │
                         └──────────┬───────────┘
                                    │
                                    │ Browser
                                    ▼
                         ┌──────────────────────┐
                         │   React + Vite UI    │
                         │     Port 5173        │
                         └──────────┬───────────┘
                                    │
                              HTTP / JSON
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   FastAPI Backend    │
                         │     Port 8000        │
                         └──────────┬───────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
       Authentication        Project Upload          Analysis Engine
             │                      │                      │
             │                      │              ┌───────┴────────┐
             │                      │              │                │
             ▼                      ▼              ▼                ▼
          JWT/Jose              ZIP Store       AST/Metrics     Graph/Architecture
             │                      │              │                │
             └──────────────────────┼──────────────┴────────────────┘
                                    │
                                    ▼
                            ┌─────────────────┐
                            │      MySQL      │
                            │     Port 3307   │
                            └─────────────────┘
```

------------------------------------------------------------------------

# 10. Backend Architecture

The backend follows a layered service-oriented structure.

``` text
app/
├── api/
│   └── routes/
│       ├── auth.py
│       ├── users.py
│       └── projects.py
│
├── core/
│   ├── config.py
│   └── security.py
│
├── database/
│   ├── base.py
│   ├── engine.py
│   └── session.py
│
├── dependencies/
│   └── database.py
│
├── models/
│   ├── user.py
│   ├── project.py
│   ├── source_file.py
│   ├── project_analysis.py
│   ├── recommendation.py
│   └── password_reset_otp.py
│
├── schemas/
│   ├── user.py
│   ├── project.py
│   └── password_reset.py
│
└── services/
    ├── authentication
    ├── scanning
    ├── parsing
    ├── metrics
    ├── dependency analysis
    ├── graph analysis
    ├── architecture analysis
    ├── quality analysis
    ├── recommendation generation
    └── project persistence
```

------------------------------------------------------------------------

# 11. Frontend Architecture

The frontend is implemented using React and Vite.

The application has two major states:

``` text
Not authenticated
        |
        v
     Auth UI
        |
        | successful login
        v
Authenticated
        |
        v
   ForgeIQ Dashboard
```

Authentication state is currently persisted using:

``` text
localStorage["access_token"]
```

The main application:

``` text
frontend/src/App.jsx
```

checks whether an access token exists.

------------------------------------------------------------------------

# 12. Database Design

ForgeIQ uses MySQL with SQLAlchemy.

## 12.1 Users

Table:

``` text
users
```

Contains:

-   `id`
-   `username`
-   `email`
-   `hashed_password`
-   `full_name`
-   `created_at`
-   `updated_at`

Relationships:

``` text
User
 ├── Projects
 └── PasswordResetOTP records
```

------------------------------------------------------------------------

## 12.2 Projects

Table:

``` text
projects
```

Contains:

-   `id`
-   `project_name`
-   `upload_path`
-   `status`
-   `uploaded_at`
-   `user_id`

Relationships:

``` text
User
  |
  +---- Project
           |
           +---- SourceFiles
           +---- ProjectAnalysis
           +---- Recommendations
```

------------------------------------------------------------------------

## 12.3 Source Files

Table:

``` text
source_files
```

Stores:

-   file name
-   file path
-   file type
-   total lines
-   code lines
-   project association
-   creation timestamp

------------------------------------------------------------------------

## 12.4 Project Analysis

Table:

``` text
project_analyses
```

Stores high-level persisted analysis information:

-   health score
-   health status
-   architecture type
-   total dependencies
-   circular dependencies
-   analysis timestamp
-   project association

------------------------------------------------------------------------

## 12.5 Recommendations

Table:

``` text
recommendations
```

Stores:

-   priority
-   title
-   message
-   recommendation
-   creation timestamp
-   project association

------------------------------------------------------------------------

## 12.6 Password Reset OTPs

Table:

``` text
password_reset_otps
```

Stores:

-   user
-   hashed OTP
-   expiry
-   attempt count
-   used state
-   creation timestamp

The plaintext OTP is not stored.

------------------------------------------------------------------------

# 13. API Reference

The FastAPI backend exposes the following implemented routes.

## Root

``` http
GET /
```

Response:

``` json
{
  "message": "Welcome to ForgeIQ API!"
}
```

------------------------------------------------------------------------

## Health

``` http
GET /health
```

Response:

``` json
{
  "status": "healthy",
  "service": "ForgeIQ API"
}
```

This endpoint is also used by the Docker backend health check.

------------------------------------------------------------------------

## Authentication

### Register

``` http
POST /auth/register
```

Content type:

``` text
application/json
```

Example:

``` json
{
  "email": "developer@example.com",
  "password": "Password123",
  "full_name": "Developer"
}
```

------------------------------------------------------------------------

### Login

``` http
POST /auth/login
```

Content type:

``` text
application/x-www-form-urlencoded
```

Fields:

``` text
username=<email>
password=<password>
```

------------------------------------------------------------------------

### Google Login

``` http
POST /auth/google
```

Example:

``` json
{
  "credential": "<google-id-token>"
}
```

------------------------------------------------------------------------

### Forgot Password

``` http
POST /auth/forgot-password
```

Example:

``` json
{
  "email": "developer@example.com"
}
```

------------------------------------------------------------------------

### Verify OTP

``` http
POST /auth/verify-otp
```

Example:

``` json
{
  "email": "developer@example.com",
  "otp": "123456"
}
```

------------------------------------------------------------------------

### Reset Password

``` http
POST /auth/reset-password
```

Example:

``` json
{
  "email": "developer@example.com",
  "otp": "123456",
  "new_password": "NewPassword123"
}
```

------------------------------------------------------------------------

## Users

### Current User

``` http
GET /users/me
```

Requires:

``` http
Authorization: Bearer <JWT>
```

------------------------------------------------------------------------

## Projects

### Create Test Project

``` http
POST /projects/test
```

Requires JWT authentication.

This creates a project named:

``` text
Demo Project
```

for the authenticated user.

------------------------------------------------------------------------

### Upload Project

``` http
POST /projects/upload
```

Requires:

``` http
Authorization: Bearer <JWT>
```

Content type:

``` text
multipart/form-data
```

Form field:

``` text
file=<project.zip>
```

------------------------------------------------------------------------

### Recommendation Summary

``` http
GET /projects/{project_id}/recommendations/summary
```

Requires JWT authentication.

The endpoint verifies that the requested project belongs to the
authenticated user.

It returns:

-   project information
-   total recommendations
-   priority counts
-   top recommendations

------------------------------------------------------------------------

# 14. Analysis Response Structure

The upload response contains several layers of information.

Conceptually:

``` json
{
  "project": {},
  "analysis": {},
  "summary": {},
  "dependency_graph": {},
  "graph_analysis": {},
  "project_health": {},
  "architecture": {},
  "recommendations": [],
  "project_report": {},
  "files": []
}
```

## `project`

Contains persisted project information:

``` text
id
project_name
upload_path
status
uploaded_at
```

------------------------------------------------------------------------

## `analysis`

Contains persisted high-level analysis information:

``` text
id
health_score
health_status
architecture_type
total_dependencies
circular_dependencies
analyzed_at
```

------------------------------------------------------------------------

## `summary`

Contains aggregated project metrics:

``` text
total_files
total_lines
code_lines
blank_lines
comment_lines
total_imports
total_classes
total_functions
total_methods
```

------------------------------------------------------------------------

## `dependency_graph`

Maps modules to their internal dependencies.

Example:

``` json
{
  "app.services.auth": [
    "app.models.user",
    "app.core.security"
  ]
}
```

------------------------------------------------------------------------

## `graph_analysis`

Contains graph-level information such as:

``` text
most_connected_module
max_dependencies
orphan_modules
circular_dependencies
```

------------------------------------------------------------------------

## `project_health`

Contains:

``` text
score
status
factors
```

------------------------------------------------------------------------

## `architecture`

Contains:

``` text
architecture_type
entry_points
core_modules
layers
issues
```

------------------------------------------------------------------------

## `recommendations`

Each recommendation can contain:

``` text
category
priority
title
message
recommendation
```

Depending on the originating analysis, additional context such as file,
location, or module may also be included.

------------------------------------------------------------------------

## `files`

Each analyzed Python file contains information similar to:

``` json
{
  "file": "app/services/example.py",
  "ast": {
    "imports": [],
    "classes": [],
    "functions": []
  },
  "metrics": {},
  "maintainability": {},
  "dependencies": {},
  "code_smells": [],
  "engineering_priority": {},
  "module_impact": {}
}
```

------------------------------------------------------------------------

# 15. Dashboard

The React dashboard presents the returned analysis in sections.

## Project Health

Displays:

-   health status
-   health score out of 100

------------------------------------------------------------------------

## Project Overview

Displays:

-   total files
-   total lines
-   code lines
-   classes
-   functions
-   methods

------------------------------------------------------------------------

## Architecture

Displays:

-   detected architecture type
-   entry points
-   core modules
-   fan-in
-   fan-out
-   importance score

------------------------------------------------------------------------

## Dependency Analysis

Displays:

-   most connected module
-   maximum dependencies
-   circular dependencies

------------------------------------------------------------------------

## Recommendations

Displays recommendations with:

-   priority
-   title
-   message
-   recommended action

------------------------------------------------------------------------

## File-Level Analysis

The dashboard also expands individual file analysis.

The file view includes information such as:

-   file path
-   metrics
-   maintainability
-   code smells
-   internal dependencies

------------------------------------------------------------------------

# 16. Technology Stack

## Backend

  Technology          Role
  ------------------- ------------------------------
  Python 3.12         Backend language
  FastAPI             REST API
  Uvicorn             ASGI server
  SQLAlchemy 2        ORM
  MySQL 8             Relational database
  PyMySQL             MySQL driver
  Pydantic            Request/response validation
  Pydantic Settings   Environment configuration
  Alembic             Database migration tooling
  python-jose         JWT handling
  Passlib + bcrypt    Password hashing
  Python `ast`        Python source parsing
  Google Auth         Google ID-token verification
  SMTP                Email delivery

------------------------------------------------------------------------

## Frontend

  Technology   Role
  ------------ ------------------------------------
  React 19     UI
  Vite 8       Frontend development/build tooling
  JavaScript   Application logic
  CSS          Styling
  Fetch API    Backend communication

------------------------------------------------------------------------

## Infrastructure

  Technology       Role
  ---------------- -------------------------------
  Docker           Containerization
  Docker Compose   Multi-container orchestration
  MySQL volume     Persistent database storage

------------------------------------------------------------------------

# 17. Prerequisites

You can run ForgeIQ either directly on your machine or through Docker.

## Recommended for Docker setup

Install:

``` text
Docker
Docker Compose
Git
```

## For local development

Install:

``` text
Python 3.12+
Node.js 20+
npm
MySQL 8+
```

------------------------------------------------------------------------

# 18. Project Setup

## 18.1 Clone the Repository

``` bash
git clone <your-repository-url>
cd ForgeIQ
```

Replace `<your-repository-url>` with the actual repository URL.

------------------------------------------------------------------------

## 18.2 Python Environment

Create a virtual environment:

``` bash
python3 -m venv .venv
```

Activate on macOS/Linux:

``` bash
source .venv/bin/activate
```

Windows PowerShell:

``` powershell
.venv\Scripts\Activate.ps1
```

Windows CMD:

``` cmd
.venv\Scripts\activate
```

------------------------------------------------------------------------

## 18.3 Backend Dependencies

Install dependencies:

``` bash
pip install -r requirements.txt
```

The current backend requirements include the packages needed for:

-   FastAPI
-   SQLAlchemy
-   MySQL
-   JWT
-   bcrypt
-   Google authentication
-   environment configuration
-   Uvicorn
-   multipart uploads

------------------------------------------------------------------------

## 18.4 MySQL

ForgeIQ expects MySQL configuration through environment variables.

The backend configuration class defines:

``` text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

For a local MySQL installation, create the database and user according
to your environment.

For Docker, the included Compose configuration creates:

``` text
Database: forgeiq
User: forgeiq
Password: forgeiq_password
Root password: root_password
```

> These Compose credentials are development/demo credentials and should
> be replaced for real deployments.

------------------------------------------------------------------------

## 18.5 Environment Variables

The backend settings define these application variables:

``` env
APP_NAME=ForgeIQ
APP_VERSION=0.1.0
ENVIRONMENT=development

DB_HOST=localhost
DB_PORT=3306
DB_NAME=forgeiq
DB_USER=forgeiq
DB_PASSWORD=your_password

SECRET_KEY=replace_with_a_secure_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

MAIL_ENABLED=false
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_FROM_NAME=ForgeIQ

GOOGLE_CLIENT_ID=
```

The exact values should be adapted to the environment.

### Important

Never commit real secrets.

Do not put real:

``` text
database passwords
JWT secrets
SMTP passwords
Google credentials
API keys
tokens
```

into Git.

------------------------------------------------------------------------

## 18.6 Frontend Dependencies

Enter the frontend directory:

``` bash
cd frontend
```

Install:

``` bash
npm install
```

The frontend environment example supports:

``` env
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
```

Then return to the project root:

``` bash
cd ..
```

------------------------------------------------------------------------

# 19. Running ForgeIQ Without Docker

## Terminal 1 --- Backend

Activate the virtual environment:

``` bash
source .venv/bin/activate
```

Start FastAPI:

``` bash
uvicorn app.main:app --reload
```

Backend:

``` text
http://localhost:8000
```

Swagger:

``` text
http://localhost:8000/docs
```

Health:

``` text
http://localhost:8000/health
```

------------------------------------------------------------------------

## Terminal 2 --- Frontend

``` bash
cd frontend
npm run dev
```

Frontend:

``` text
http://localhost:5173
```

The frontend API base URL should point to:

``` text
http://localhost:8000
```

------------------------------------------------------------------------

# 20. Running ForgeIQ With Docker

Docker Compose runs three services:

``` text
db
backend
frontend
```

From the project root:

``` bash
docker compose up -d --build
```

Check:

``` bash
docker compose ps
```

Expected services:

``` text
forgeiq-db
forgeiq-backend
forgeiq-frontend
```

------------------------------------------------------------------------

## Stop the application

``` bash
docker compose down
```

------------------------------------------------------------------------

## Stop and remove database volume

Use this only when you intentionally want to delete the Docker MySQL
data:

``` bash
docker compose down -v
```

> This deletes the named MySQL volume and therefore the database data
> stored in it.

------------------------------------------------------------------------

## Rebuild

``` bash
docker compose up -d --build
```

------------------------------------------------------------------------

## View logs

Backend:

``` bash
docker compose logs -f backend
```

Frontend:

``` bash
docker compose logs -f frontend
```

Database:

``` bash
docker compose logs -f db
```

All services:

``` bash
docker compose logs -f
```

------------------------------------------------------------------------

# 21. Docker Architecture

The Compose configuration defines:

``` text
                         Docker Compose
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
   +-------------+     +-------------+     +-------------+
   |    MySQL    |     |   FastAPI   |     |    React    |
   | forgeiq-db  |<----| forgeiq-    |<----| forgeiq-    |
   |             |     | backend     |     | frontend    |
   +-------------+     +-------------+     +-------------+
         |                    |                   |
         |                    |                   |
      3307:3306          8000:8000          5173:5173
```

### Database

Container:

``` text
forgeiq-db
```

Host port:

``` text
3307
```

Container port:

``` text
3306
```

------------------------------------------------------------------------

### Backend

Container:

``` text
forgeiq-backend
```

Host:

``` text
8000
```

The backend health check calls:

``` text
/health
```

Docker Compose waits for the database health check before starting the
backend.

------------------------------------------------------------------------

### Frontend

Container:

``` text
forgeiq-frontend
```

Host:

``` text
5173
```

The frontend build receives:

``` text
VITE_API_BASE_URL=http://localhost:8000
```

as a Docker build argument.

------------------------------------------------------------------------

# 22. Database and Alembic

The project includes:

``` text
alembic.ini
```

and Alembic is included in the backend dependencies.

The ORM models are located under:

``` text
app/models/
```

The repository snapshot used for this README contains the Alembic
configuration, but the uploaded supporting files do not establish a
complete committed `alembic/versions/` migration history.

Therefore, do not assume that a fresh checkout has a complete migration
chain unless the repository contains those migration files.

For a repository where migration files are present, the standard
workflow is:

``` bash
alembic upgrade head
```

To create a new migration during development:

``` bash
alembic revision --autogenerate -m "describe change"
```

Then:

``` bash
alembic upgrade head
```

Always review autogenerated migrations before applying them.

------------------------------------------------------------------------

# 23. API Documentation with Swagger

FastAPI automatically exposes interactive API documentation.

Start the backend and open:

``` text
http://localhost:8000/docs
```

Swagger allows you to:

-   inspect endpoints
-   view request schemas
-   view response schemas
-   authenticate
-   send requests
-   inspect HTTP responses

A second OpenAPI interface is normally available through FastAPI's ReDoc
endpoint:

``` text
http://localhost:8000/redoc
```

------------------------------------------------------------------------

# 24. Example API Workflow

## Step 1 --- Register

``` bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "password": "Password123",
    "full_name": "Demo User"
  }'
```

------------------------------------------------------------------------

## Step 2 --- Login

The login endpoint uses form data:

``` bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@example.com&password=Password123"
```

Copy the returned:

``` text
access_token
```

------------------------------------------------------------------------

## Step 3 --- Test authentication

``` bash
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

------------------------------------------------------------------------

## Step 4 --- Upload a project

``` bash
curl -X POST http://localhost:8000/projects/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@sample-project.zip"
```

------------------------------------------------------------------------

## Step 5 --- Inspect the result

The response contains:

``` text
project
analysis
summary
dependency_graph
graph_analysis
project_health
architecture
recommendations
project_report
files
```

------------------------------------------------------------------------

# 25. Security Model

ForgeIQ includes several security-oriented mechanisms.

## Password hashing

Passwords are hashed using:

``` text
bcrypt
```

Plaintext passwords are not stored.

------------------------------------------------------------------------

## JWT authentication

Protected APIs require:

``` http
Authorization: Bearer <token>
```

------------------------------------------------------------------------

## Current-user resolution

The backend:

1.  extracts the bearer token
2.  decodes the JWT
3.  reads `sub`
4.  resolves the user from the database
5.  rejects invalid/expired tokens

------------------------------------------------------------------------

## Project ownership

Protected project operations use the authenticated user's identity.

For example, the recommendation-summary endpoint checks:

``` text
Project.id == requested project ID
AND
Project.user_id == current_user.id
```

This prevents a user from requesting the recommendation summary of
another user's project through that endpoint.

------------------------------------------------------------------------

## Password-reset OTP security

OTP values are:

-   randomly generated
-   hashed before storage
-   time limited
-   attempt limited
-   invalidated after use

------------------------------------------------------------------------

## Account enumeration protection

The forgot-password endpoint returns a generic message regardless of
whether an account exists.

This avoids exposing account-existence information through the response.

------------------------------------------------------------------------

## Email failure isolation

Email delivery is designed so that temporary SMTP failures do not
directly cause registration/password-reset operations to fail.

------------------------------------------------------------------------

# 26. Error Handling

The backend uses FastAPI `HTTPException` for API-level failures.

Examples include:

``` text
401 Unauthorized
400 Bad Request
404 Not Found
```

Common authentication errors:

``` json
{
  "detail": "Not authenticated"
}
```

or:

``` json
{
  "detail": "Invalid or expired token."
}
```

Invalid project access can return:

``` json
{
  "detail": "Project not found"
}
```

The upload service also updates a project's status to:

``` text
Failed
```

when an exception occurs after a project has been created.

------------------------------------------------------------------------

# 27. Repository Structure

A simplified source structure is:

``` text
ForgeIQ/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── projects.py
│   │       └── users.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   ├── engine.py
│   │   └── session.py
│   │
│   ├── dependencies/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── source_file.py
│   │   ├── project_analysis.py
│   │   ├── recommendation.py
│   │   └── password_reset_otp.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── project.py
│   │   └── password_reset.py
│   │
│   └── services/
│       ├── architecture_analyzer.py
│       ├── ast_parser.py
│       ├── auth_service.py
│       ├── code_smell_analyzer.py
│       ├── complexity_analyzer.py
│       ├── cycle_detector.py
│       ├── dependency_analyzer.py
│       ├── dependency_graph_builder.py
│       ├── email_service.py
│       ├── engineering_priority.py
│       ├── file_scanner.py
│       ├── google_auth_service.py
│       ├── graph_analyzer.py
│       ├── graph_utils.py
│       ├── maintainability_analyzer.py
│       ├── module_impact_analyzer.py
│       ├── module_indexer.py
│       ├── password_reset_service.py
│       ├── project_analysis_service.py
│       ├── project_analyzer.py
│       ├── project_health_analyzer.py
│       ├── project_quality_analyzer.py
│       ├── project_report_generator.py
│       ├── project_service.py
│       ├── project_summary.py
│       ├── recommendation_engine.py
│       ├── recommendation_service.py
│       ├── recommendation_summary.py
│       ├── source_file_service.py
│       └── upload_service.py
│
├── analysis/
│   ├── dependency/
│   ├── metrics/
│   ├── parser/
│   ├── security/
│   └── sql/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
├── .gitignore
├── .dockerignore
├── LICENSE
└── README.md
```

------------------------------------------------------------------------

# 28. Service-by-Service Backend Guide

This section explains the responsibility of the major backend services.

  -----------------------------------------------------------------------
  Service                             Responsibility
  ----------------------------------- -----------------------------------
  `file_scanner.py`                   Finds Python files

  `ast_parser.py`                     Parses Python and extracts
                                      structural information

  `complexity_analyzer.py`            Calculates AST-based cyclomatic
                                      complexity

  `metrics_engine.py`                 Calculates source metrics

  `maintainability_analyzer.py`       Calculates maintainability
                                      score/rating

  `code_smell_analyzer.py`            Detects implemented code smells

  `module_indexer.py`                 Converts Python file paths into
                                      project module names

  `dependency_analyzer.py`            Resolves internal/external
                                      dependencies

  `dependency_graph_builder.py`       Builds module dependency graph

  `graph_utils.py`                    Provides graph utility calculations

  `graph_analyzer.py`                 Finds graph-level insights

  `cycle_detector.py`                 Detects circular dependencies

  `module_impact_analyzer.py`         Calculates fan-in/fan-out

  `architecture_analyzer.py`          Infers architecture, layers and
                                      architectural issues

  `engineering_priority.py`           Calculates file-level engineering
                                      priority

  `project_health_analyzer.py`        Calculates project health

  `project_quality_analyzer.py`       Provides project quality analysis
                                      logic

  `recommendation_engine.py`          Generates recommendations

  `recommendation_summary.py`         Summarizes recommendation
                                      priorities

  `project_summary.py`                Aggregates project metrics

  `project_report_generator.py`       Produces consolidated project
                                      report

  `project_analyzer.py`               Orchestrates the complete
                                      static-analysis pipeline

  `upload_service.py`                 Handles ZIP upload, extraction,
                                      analysis and persistence

  `project_service.py`                Creates/updates project records

  `project_analysis_service.py`       Persists project-level analysis

  `source_file_service.py`            Persists source-file information

  `recommendation_service.py`         Persists recommendations

  `auth_service.py`                   Registration and normal login

  `google_auth_service.py`            Google token verification/login

  `password_reset_service.py`         OTP password reset

  `email_service.py`                  SMTP email delivery
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 29. Frontend Component Guide

## `App.jsx`

Controls the main authentication state.

If no token is found:

``` text
Auth
```

is displayed.

If authenticated:

``` text
Navbar
+
Home
```

is displayed.

------------------------------------------------------------------------

## `Auth.jsx`

Provides the combined authentication interface.

Modes include:

``` text
login
register
forgot
otp
reset
```

It also initializes Google Identity Services.

------------------------------------------------------------------------

## `Home.jsx`

Provides:

-   project upload
-   ZIP validation
-   loading state
-   error state
-   analysis result state
-   analysis dashboard

------------------------------------------------------------------------

## `Navbar.jsx`

Displays:

-   ForgeIQ branding
-   analyzer status
-   logout action

------------------------------------------------------------------------

## `AnalysisDashboard.jsx`

Displays:

-   project health
-   overview metrics
-   architecture
-   core modules
-   dependency analysis
-   recommendations
-   file-level analysis

------------------------------------------------------------------------

## `FileAnalysis.jsx`

Displays individual file analysis information including:

-   metrics
-   maintainability
-   code smells
-   internal dependencies

------------------------------------------------------------------------

## `api.js`

Centralizes frontend API communication.

It contains functions for:

``` text
registerUser()
loginUser()
googleLogin()
forgotPassword()
verifyOTP()
resetPassword()
uploadProject()
logoutUser()
isAuthenticated()
```

The API base URL comes from:

``` text
VITE_API_BASE_URL
```

with a localhost fallback.

------------------------------------------------------------------------

# 30. Configuration Reference

## Backend

  Variable                        Purpose
  ------------------------------- ---------------------------------
  `APP_NAME`                      Application name
  `APP_VERSION`                   Application version
  `ENVIRONMENT`                   Runtime environment
  `DB_HOST`                       MySQL host
  `DB_PORT`                       MySQL port
  `DB_NAME`                       Database name
  `DB_USER`                       Database user
  `DB_PASSWORD`                   Database password
  `SECRET_KEY`                    JWT signing secret
  `ALGORITHM`                     JWT algorithm
  `ACCESS_TOKEN_EXPIRE_MINUTES`   JWT lifetime
  `MAIL_ENABLED`                  Enables/disables SMTP
  `MAIL_SERVER`                   SMTP server
  `MAIL_PORT`                     SMTP port
  `MAIL_USERNAME`                 SMTP username
  `MAIL_PASSWORD`                 SMTP password
  `MAIL_FROM`                     Sender email
  `MAIL_FROM_NAME`                Sender display name
  `GOOGLE_CLIENT_ID`              Google OAuth/Identity client ID

------------------------------------------------------------------------

## Frontend

  Variable                  Purpose
  ------------------------- ---------------------------
  `VITE_API_BASE_URL`       FastAPI base URL
  `VITE_GOOGLE_CLIENT_ID`   Google Identity client ID

------------------------------------------------------------------------

# 31. Testing and Verification

A basic verification sequence is:

## 1. Check Docker

``` bash
docker compose ps
```

All required services should be running.

------------------------------------------------------------------------

## 2. Check backend

``` bash
curl http://localhost:8000/health
```

Expected:

``` json
{
  "status": "healthy",
  "service": "ForgeIQ API"
}
```

------------------------------------------------------------------------

## 3. Register

Use Swagger or:

``` bash
curl
```

against:

``` text
POST /auth/register
```

------------------------------------------------------------------------

## 4. Login

Authenticate through:

``` text
POST /auth/login
```

------------------------------------------------------------------------

## 5. Test protected endpoint without a token

``` bash
curl -X POST http://localhost:8000/projects/test
```

Expected behavior:

``` json
{
  "detail": "Not authenticated"
}
```

------------------------------------------------------------------------

## 6. Test protected endpoint with JWT

``` bash
curl -X POST http://localhost:8000/projects/test \
  -H "Authorization: Bearer YOUR_TOKEN"
```

The endpoint should create the authenticated user's demo project.

------------------------------------------------------------------------

## 7. Upload a Python ZIP

Use the dashboard or:

``` bash
curl -X POST http://localhost:8000/projects/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@sample-project.zip"
```

------------------------------------------------------------------------

## 8. Check the dashboard

After successful analysis, verify:

-   project health
-   metrics
-   architecture
-   dependency information
-   recommendations
-   file analysis

------------------------------------------------------------------------

# 32. Troubleshooting

## Backend does not start

Check:

``` bash
docker compose logs backend
```

For local execution:

``` bash
uvicorn app.main:app --reload
```

Check that:

-   Python environment is active
-   dependencies are installed
-   `.env` exists
-   database configuration is correct

------------------------------------------------------------------------

## Database connection failure

If using Docker:

``` bash
docker compose ps
```

The database should show a healthy state.

Check:

``` bash
docker compose logs db
```

If using local MySQL, verify:

``` text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

------------------------------------------------------------------------

## Frontend cannot reach backend

Check:

``` text
VITE_API_BASE_URL
```

For local development:

``` text
http://localhost:8000
```

Check backend:

``` bash
curl http://localhost:8000/health
```

------------------------------------------------------------------------

## Upload returns "Not authenticated"

The frontend needs a JWT in:

``` text
localStorage.access_token
```

Log in again.

For API testing, include:

``` http
Authorization: Bearer YOUR_TOKEN
```

------------------------------------------------------------------------

## Upload fails

Ensure the selected file ends with:

``` text
.zip
```

The current upload implementation only accepts ZIP archives.

------------------------------------------------------------------------

## ZIP analysis finds unexpected files

ForgeIQ intentionally ignores:

``` text
__MACOSX/
._*
```

during Python file scanning.

------------------------------------------------------------------------

## Google login fails

Verify:

``` text
VITE_GOOGLE_CLIENT_ID
GOOGLE_CLIENT_ID
```

and make sure the frontend and backend use the appropriate Google client
ID.

Also verify that the Google credential is being generated successfully
in the browser.

------------------------------------------------------------------------

## Password reset email is not received

Check:

``` text
MAIL_ENABLED=true
MAIL_USERNAME
MAIL_PASSWORD
MAIL_SERVER
MAIL_PORT
```

Also inspect backend logs.

For development without SMTP, keep:

``` text
MAIL_ENABLED=false
```

but password-reset emails will not be delivered.

------------------------------------------------------------------------

## Docker frontend changes do not appear

Rebuild:

``` bash
docker compose up -d --build
```

Because `VITE_*` variables are part of the frontend build process,
changes to frontend build-time configuration require a rebuild.

------------------------------------------------------------------------

# 33. Development Workflow

A recommended development loop is:

``` text
1. Start MySQL / Docker
        |
        v
2. Start FastAPI
        |
        v
3. Start React/Vite
        |
        v
4. Make backend/frontend change
        |
        v
5. Test endpoint/UI
        |
        v
6. Run project analysis against sample ZIP
        |
        v
7. Inspect dashboard
        |
        v
8. Check logs/errors
        |
        v
9. Commit changes
```

For backend changes:

``` bash
uvicorn app.main:app --reload
```

For frontend changes:

``` bash
npm run dev
```

For a production-style frontend build check:

``` bash
npm run build
```

For linting:

``` bash
npm run lint
```

------------------------------------------------------------------------

# 34. Current Implementation Status

The current repository implements a substantial static-analysis
foundation.

## Implemented

### Authentication

-   [x] Registration
-   [x] Password hashing
-   [x] Email/password login
-   [x] JWT access tokens
-   [x] Protected endpoints
-   [x] Current-user endpoint
-   [x] Google login
-   [x] Password-reset OTP
-   [x] SMTP email service
-   [x] Welcome email

### Project processing

-   [x] ZIP upload
-   [x] Project creation
-   [x] Project ownership
-   [x] ZIP extraction
-   [x] Project status tracking
-   [x] Python file scanning

### Static analysis

-   [x] AST parsing
-   [x] Import extraction
-   [x] Class extraction
-   [x] Method extraction
-   [x] Function extraction
-   [x] Complexity calculation
-   [x] Source metrics
-   [x] Maintainability
-   [x] Code smells

### Architecture and dependencies

-   [x] Internal dependency detection
-   [x] External dependency detection
-   [x] Dependency graph
-   [x] Graph analysis
-   [x] Circular dependency detection
-   [x] Fan-in/fan-out
-   [x] Module impact
-   [x] Architecture inference
-   [x] Layer detection
-   [x] Entry-point detection
-   [x] Core-module detection
-   [x] Architecture issues

### Engineering intelligence

-   [x] Engineering priority
-   [x] Project health
-   [x] Recommendation generation
-   [x] Recommendation summary
-   [x] Project report

### Persistence

-   [x] Users
-   [x] Projects
-   [x] Source files
-   [x] Project analyses
-   [x] Recommendations
-   [x] Password-reset OTPs

### Frontend

-   [x] Authentication UI
-   [x] Registration
-   [x] Login
-   [x] Google login
-   [x] Password reset flow
-   [x] ZIP upload
-   [x] Loading state
-   [x] Error handling
-   [x] Project dashboard
-   [x] File-level analysis

### Infrastructure

-   [x] Dockerfile
-   [x] Docker Compose
-   [x] MySQL container
-   [x] Backend health check
-   [x] Frontend container
-   [x] Persistent MySQL volume

------------------------------------------------------------------------

# 35. Current Limitations

ForgeIQ's current implementation should be understood accurately.

## Python-focused analysis

The scanner currently searches for:

``` text
*.py
```

Therefore, the implemented analysis engine is Python-oriented.

------------------------------------------------------------------------

## ZIP-only project input

The upload endpoint currently accepts:

``` text
.zip
```

archives.

------------------------------------------------------------------------

## Static/rule-based analysis

Current scores and recommendations are generated by deterministic code.

The project does not currently demonstrate an integrated LLM inference
pipeline in the uploaded implementation.

------------------------------------------------------------------------

## Simplified complexity model

The complexity analyzer handles a selected set of AST constructs.

It is useful for project-level signals but is not intended to replace
every industrial complexity-analysis implementation.

------------------------------------------------------------------------

## Simplified maintainability model

The maintainability index is a custom heuristic based on:

-   code size
-   functions
-   methods
-   comments

It should be described as a ForgeIQ metric rather than a formal
industry-standard metric.

------------------------------------------------------------------------

## Limited code-smell catalogue

The current smell detector focuses on:

``` text
Long Function
Long Parameter List
Missing Docstring
Large Class
```

It does not currently implement a complete catalogue of Fowler-style or
static-analysis-tool code smells.

------------------------------------------------------------------------

## Architecture inference is heuristic

Architecture is inferred primarily from:

-   directory names
-   file locations
-   dependency relationships

It does not currently understand architecture using semantic LLM
reasoning.

------------------------------------------------------------------------

## ZIP extraction considerations

The upload implementation extracts ZIP archives using Python's `zipfile`
module. A production deployment should add stronger archive validation
and resource limits, including protections against malicious archive
contents and excessive extraction size.

------------------------------------------------------------------------

# 36. Future AI / LLM Layer

The long-term ForgeIQ architecture is designed to place an intelligence
layer after deterministic analysis.

The intended architecture is:

``` text
                 Source Code
                     |
                     v
             Static Analysis
                     |
                     v
              AST + Metrics
                     |
                     v
          Dependency / Graph Model
                     |
                     v
             Architecture Model
                     |
                     v
             Quality Signals
                     |
                     v
              Project Context
                     |
                     v
                 LLM Layer
                     |
                     v
        Context-Aware Engineering
             Recommendations
```

The important design principle is:

> **Do not send raw code to an LLM and ask it to guess the architecture.
> Build project context first.**

The static-analysis engine provides structured context such as:

``` text
project metrics
file metrics
classes
functions
complexity
code smells
dependencies
dependency graph
cycles
fan-in
fan-out
architecture
project health
engineering priority
```

A future LLM could use this context to answer higher-level engineering
questions.

For example:

``` text
"Why is this module high risk?"
```

could combine:

``` text
High complexity
+
Low maintainability
+
Many dependencies
+
High fan-in
+
Circular dependency
```

and produce a context-aware explanation.

------------------------------------------------------------------------

# 37. Future Scope

Potential future capabilities include:

## Multi-language support

Extend parsing beyond Python:

``` text
Java
C++
JavaScript
TypeScript
Go
C#
```

------------------------------------------------------------------------

## Advanced AST analysis

Add:

-   inheritance analysis
-   call graphs
-   symbol resolution
-   dead-code detection
-   exception-flow analysis
-   async-flow analysis

------------------------------------------------------------------------

## Advanced dependency intelligence

Add:

-   package-level dependency graphs
-   external package risk
-   dependency version analysis
-   transitive dependency analysis
-   dependency hotspots

------------------------------------------------------------------------

## Better architecture intelligence

Add:

-   architectural rule validation
-   layer violation detection
-   architectural drift
-   design-pattern detection
-   service-boundary analysis

------------------------------------------------------------------------

## Richer code quality

Add:

-   duplicate code detection
-   dead code
-   naming analysis
-   excessive nesting
-   god classes
-   feature envy
-   shotgun surgery
-   large files
-   duplicated logic

------------------------------------------------------------------------

## LLM-powered software architect

A future LLM layer could provide:

-   natural-language architecture explanations
-   project-wide Q&A
-   refactoring plans
-   migration plans
-   prioritized engineering roadmaps
-   architectural trade-off explanations
-   contextual recommendations
-   change-impact explanations

------------------------------------------------------------------------

## Knowledge graph

A future graph model could represent:

``` text
User
 |
Project
 |
 +-- File
      |
      +-- Module
      |
      +-- Class
      |
      +-- Function
      |
      +-- Dependency
      |
      +-- Issue
      |
      +-- Recommendation
```

This would allow ForgeIQ to reason over a richer project graph.

------------------------------------------------------------------------

# 38. Project Vision

ForgeIQ is intended to evolve from:

``` text
Static Code Analyzer
```

into:

``` text
Software Architecture Intelligence Platform
```

and eventually:

``` text
AI Software Architect
```

The long-term product direction is:

``` text
             ┌─────────────────────────┐
             │       Source Code       │
             └────────────┬────────────┘
                          |
                          v
             ┌─────────────────────────┐
             │    Static Analysis      │
             └────────────┬────────────┘
                          |
                          v
             ┌─────────────────────────┐
             │   Project Knowledge     │
             │                         │
             │ AST                     │
             │ Metrics                 │
             │ Dependencies            │
             │ Architecture            │
             │ Quality                 │
             │ Impact                  │
             └────────────┬────────────┘
                          |
                          v
             ┌─────────────────────────┐
             │     AI Reasoning        │
             └────────────┬────────────┘
                          |
                          v
             ┌─────────────────────────┐
             │  Engineering Guidance   │
             │                         │
             │ Explain                 │
             │ Prioritize              │
             │ Recommend               │
             │ Refactor                │
             │ Predict Impact           │
             └─────────────────────────┘
```

The goal is not simply to answer:

> "What does this code do?"

The goal is to answer:

> **"How does this software system behave, how healthy is its
> architecture, what are its risks, and what should an engineer do
> next?"**

------------------------------------------------------------------------

# 39. License

See the repository's `LICENSE` file for the applicable license.

------------------------------------------------------------------------

## Quick Start

For the fastest Docker-based setup:

``` bash
git clone <your-repository-url>
cd ForgeIQ
docker compose up -d --build
docker compose ps
```

Then open:

``` text
Frontend:
http://localhost:5173

Backend:
http://localhost:8000

Swagger:
http://localhost:8000/docs

Health:
http://localhost:8000/health
```

Create an account, log in, upload a Python ZIP project, and ForgeIQ will
run the complete implemented analysis pipeline.

------------------------------------------------------------------------

## ForgeIQ in One Sentence

**ForgeIQ transforms a Python project from raw source code into
structured architectural, dependency, quality, health, impact, priority,
and engineering insights --- providing the foundation for a future
AI-powered software architect.**
