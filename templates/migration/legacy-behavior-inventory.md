# Legacy Behavior Inventory - <Feature Name>

Status: draft
Feature ID: <feature-id>
Related package index: `migration-package-index.md`
Sensitivity: public-safe-example | internal | confidential

## Purpose

Capture observable legacy behavior as the migration contract.

## Source Systems Inspected

| Source | Type | What Was Inspected | Evidence |
| --- | --- | --- | --- |
| <system/repo/doc> | code | <files/flows> | <path/reference> |

## Entry Points

| Type | Entry Point | Request / Trigger | Response / Result |
| --- | --- | --- | --- |
| API | <endpoint> | <request> | <response> |
| UI | <flow> | <action> | <result> |
| Job | <job> | <schedule/event> | <result> |
| Event | <event> | <producer> | <consumer/result> |

## Main Flow

1. <step>
2. <step>
3. <step>

## Alternate Flows

| Flow | Trigger | Legacy Behavior | Notes |
| --- | --- | --- | --- |
| <name> | <condition> | <behavior> | <notes> |

## Validation Rules

| Rule | Input / Condition | Legacy Result | Evidence |
| --- | --- | --- | --- |
| <rule> | <condition> | <result> | <path/reference> |

## Permissions And Roles

| Actor / Role | Allowed Behavior | Denied Behavior | Evidence |
| --- | --- | --- | --- |
| <role> | <allowed> | <denied> | <path/reference> |

## Data Behavior

- Reads:
- Writes:
- Updates:
- Deletes:
- Transactions:
- Idempotency:
- Concurrency:

## Error Behavior

| Scenario | Status / Error | Body / Message | Side Effect | Evidence |
| --- | --- | --- | --- | --- |
| <scenario> | <status/error> | <message> | <side-effect> | <path/reference> |

## Side Effects

- Events emitted:
- Notifications:
- Logs:
- Metrics:
- External calls:
- Persistence side effects:

## Existing Tests Or Fixtures

| Test / Fixture | What It Proves | Reuse For Parity |
| --- | --- | --- |
| <test> | <behavior> | yes / no / partial |

## Behavior Contract

| ID | Legacy Behavior | Must Preserve? | Notes |
| --- | --- | --- | --- |
| LB-01 | <behavior> | yes | <notes> |

## Unknowns And Gaps

| Gap | Why It Matters | Recommended Action |
| --- | --- | --- |
| <gap> | <impact> | Spike | ask owner | document risk |

## Search Anchors

Terms people might search for:

- <feature-name>
- <legacy-behavior>
- <error-term>
- <role-term>
