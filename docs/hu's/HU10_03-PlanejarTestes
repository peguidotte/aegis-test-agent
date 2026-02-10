> **AS:** System (Aegis Tests + Aegis Agent)
>
> **I WANT:** Transform project inputs into a structured test plan
>
> **SO THAT:** We clearly define what will be generated before writing code.

---

## Context

Planning is the phase where the agent analyzes the full context and produces a ScenarioPlan: a detailed plan of Features, Scenarios, and Steps that will be generated.

This phase is crucial because it:
- Defines test structure before generation
- Enables human review before spending generation budget
- Ensures adequate coverage of the defined scope
- Allows time and cost estimation

### What is a ScenarioPlan?

A ScenarioPlan is a structured representation of what the agent intends to generate:

```
ScenarioPlan
├── Feature: User Authentication
│   ├── Scenario: Login with valid credentials
│   │   ├── Step: Send login request
│   │   └── Step: Verify access token
│   ├── Scenario: Login with invalid password
│   │   ├── Step: Send login request
│   │   └── Step: Verify error response
│   └── Scenario: Login with missing credentials
│       ├── Step: Send login request
│       └── Step: Verify validation error
│
└── Feature: Customer Management
    ├── Scenario: Create customer with valid data
    │   ├── Step: Send create request
    │   └── Step: Verify customer created
    └── Scenario: Create customer with duplicate CPF
        ├── Step: Send create request
        └── Step: Verify conflict response
```

Important: no executable code is generated in this phase. Only the plan (features, scenarios, steps, outlines) is produced.

---

## Planning Flow

```
GenerationJob (PLANNING)
        |
        v
+-------------------+
|   Aegis Agent     |
|   (Python + LLM)  |
+-------------------+
        |
        | Analyzes:
        | - Specification / ApiDocs / Repo
        | - Project context
        | - Aegis patterns and guidelines
        v
+-------------------+
|   ScenarioPlan    |
|   (Features +     |
|    Scenarios +    |
|    Steps)         |
+-------------------+
        |
        v
Persist to DB
        |
        v
Status: PLANNED
```

---

## Topics (Agent -> Orchestrator)

- `test-generation-planning-started` (planning started)
- `test-generation-planning-completed` (planning completed)
- `test-generation-planning-failed` (planning failed)

---

## Input Event (Orchestrator -> Agent)

### Headers

Standard message headers (transport-agnostic):

| Field | Type | Description | Required |
| --- | --- | --- | --- |
| sender | String | System or service that sent the message | Yes |
| timestamp | ISO-8601 | UTC timestamp when message was produced | Yes |
| correlationId | String | Correlation ID for tracing | Yes |
| messageId | String | Message identifier | No |
| traceId | String | Trace identifier | No |

### Payload (TestGenerationRequest)

| Field | Type | Description | Required |
| --- | --- | --- | --- |
| specificationId | Integer | Specification ID | Yes |
| name | String | Specification name | Yes |
| description | String | Specification description | No |
| inputType | String | Source input type | Yes |
| method | String | Primary API method | Yes |
| path | String | Primary API path | Yes |
| testObjective | String | Objective of the tests | Yes |
| requestExample | String | Serialized request example | No |
| requiresAuth | Boolean | Whether endpoint requires auth | Yes |
| approveBeforeGeneration | Boolean | Whether plan requires approval before generation | Yes |
| testProject | Object | Test project reference | Yes |
| environment | Object | Environment reference | Yes |
| domain | Object | Domain reference | No |
| authProfile | Object | Auth profile reference | No |
| apiCall | Object | Primary API call specification | Yes |
| supportingApiCalls | List<Object> | Supporting API call references | No |
| traceId | String | Trace identifier | Yes |
| createdAt | ISO-8601 | Creation timestamp | Yes |

### apiCall (Primary API Call Specification)

The primary API call must include request and response schemas, status codes, and examples.

| Field | Type | Description | Required |
| --- | --- | --- | --- |
| id | Integer | API call ID | Yes |
| name | String | API call name | Yes |
| method | String | HTTP method | Yes |
| path | String | Endpoint path | Yes |
| description | String | API call description | No |
| requestSchema | Object | Request body schema | Yes |
| responseSchema | Object | Response body schema | Yes |
| responseStatusCodes | List<Integer> | Expected status codes | Yes |
| requestExamples | List<Object or String> | Request examples | No |
| responseExamples | List<Object or String> | Response examples | No |

### supportingApiCalls

Supporting API calls provide context for verification. They are not the planning scope. The plan must cover only the primary apiCall.

---

## Output Events (Agent -> Orchestrator)

### Planning Started

| Field | Type | Description | Required |
| --- | --- | --- | --- |
| traceId | String | Trace identifier | Yes |
| specificationId | Integer | Specification ID | Yes |

### Planning Progress

| Field | Type | Description | Required |
| --- | --- | --- | --- |
| traceId | String | Trace identifier | Yes |
| specificationId | Integer | Specification ID | Yes |
| percentage | Integer | 0-100 | Yes |
| message | String | Progress message | No |

### Planning Completed

| Field | Type | Description | Required |
| --- | --- | --- | --- |
| traceId | String | Trace identifier | Yes |
| specificationId | Integer | Specification ID | Yes |
| summary | String | Planning summary | Yes |
| requiresApproval | Boolean | Whether approval is required | Yes |
| features | List<FeaturePlan> | Planned features | Yes |
| coverageAnalysis | Object | Coverage analysis | No |
| metrics | Object | Planning metrics | No |

### Planning Failed

| Field | Type | Description | Required |
| --- | --- | --- | --- |
| traceId | String | Trace identifier | Yes |
| specificationId | Integer | Specification ID | Yes |
| errorType | String | Error category | Yes |
| message | String | Error message | Yes |

---

## FeaturePlan

| Field | Type | Description |
| --- | --- | --- |
| featureNumber | Integer | Order of the feature in the plan |
| featureName | String | Feature name |
| featureTags | List<String> | Optional tags |
| scenarios | List<ScenarioPlan> | Planned scenarios |

## ScenarioPlan

| Field | Type | Description |
| --- | --- | --- |
| scenarioNumber | Integer | Order of the scenario in the feature |
| name | String | Scenario name |
| description | String | Scenario intent | Optional |
| type | Enum | POSITIVE, NEGATIVE, EDGE_CASE, SECURITY, PERFORMANCE |
| priority | Enum | HIGH, MEDIUM, LOW |
| tags | List<String> | Optional tags |
| outlines | List<ScenarioOutline> | Optional outline configuration |
| steps | List<StepPlan> | Planned steps |

## StepPlan

| Field | Type | Description |
| --- | --- | --- |
| stepNumber | Integer | Order of the step |
| stepName | String | Step description |

---

## Business Rules

| Code | Rule | Rationale | ErrorCode |
| --- | --- | --- | --- |
| RN10.03.1 | Job must be PLANNING to accept a plan | Flow | JOB_INVALID_STATUS |
| RN10.03.2 | Plan must contain at least 1 Feature | Minimum viable | PLAN_EMPTY |
| RN10.03.3 | Each Feature must contain at least 1 Scenario | Consistency | FEATURE_EMPTY |
| RN10.03.4 | If requiresAuth is true, include auth failure scenarios | Security baseline | AUTH_SCENARIOS_REQUIRED |
| RN10.03.5 | Planning must include positive, negative, edge, and security scenarios when context allows | Coverage | SCENARIO_COVERAGE_INCOMPLETE |
| RN10.03.6 | Supporting API calls are context only, not primary scope | Scope | SUPPORT_API_SCOPE |

---

## Approval Flow

```
PLANNED ----------------------------------------------+
    |                                                   |
    | requiresApproval = true                           | requiresApproval = false
    v                                                   |
WAITING_APPROVAL                                       |
    |                                                   |
    +--> APPROVE ------------> APPROVED ---------------+
    |                                                   |
    +--> APPROVE_WITH_EDITS -> APPROVED_WITH_EDITS -----+
    |                                                   |
    +--> REJECT -------------> REJECTED --> PLANNING    |
                                                        |
                                                        v
                                                   GENERATING
```

Note: Rejection reasons should be stored for learning and future improvements.

---

## Expected Outcome

- ScenarioPlan created and persisted
- Features, Scenarios, and Steps planned
- Coverage analyzed
- Plan available for review (if required)
- No executable code generated in this phase
- No final test artifacts created yet