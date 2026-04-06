# Test Matrix

## Coverage Categories

| Area | Objective | Priority | Notes |
| --- | --- | --- | --- |
| API availability | Validate `/`, `/health`, `/conversions`, `/docs` | High | Main API v2 baseline |
| Core conversions | Validate stable `api-v2` conversions | High | Direct business value |
| Validation rules | Enforce extension and payload checks | High | Prevent invalid request acceptance |
| Error responses | Verify controlled failure behavior | High | Important for public API reliability |
| Metadata extractor | Validate secondary API health and extraction flow | Medium | Separate service surface |
| Render behavior | Capture cold start expectations | Medium | Operational quality concern |
| Frontend consistency | Compare published frontend against live backend | High | Current known drift |

## Core Conversion Matrix

| From | To | Status in api-v2 | Priority | Notes |
| --- | --- | --- | --- | --- |
| txt | csv | Stable | High | One line becomes one row |
| csv | txt | Stable | High | Delimited text rendering |
| csv | json | Stable | High | Header row required |
| json | csv | Stable | High | Must be list of objects |
| csv | xml | Stable | High | XML-safe column sanitization |
| xml | csv | Stable | High | Simple repetitive structures only |
| csv | html | Stable | High | Output must escape HTML cells |
| html | txt | Stable | High | Lightweight extraction only |
| txt | json | Stable | Medium | One line per item |
| json | txt | Stable | Medium | Linearized list values |
| txt | xml | Stable | Medium | Line-based XML |
| json | xml | Beta | Medium | Structure-sensitive |
| xml | json | Beta | Medium | Structure-sensitive |

## Validation and Error Matrix

| Scenario | Expected Result | Priority |
| --- | --- | --- |
| Unsupported conversion pair | `400` | High |
| Extension does not match declared format | `400` | High |
| Payload exceeds max upload size | `413` | High |
| Invalid JSON payload | `400` or `422` depending on handler | High |
| Invalid XML payload | `400` | High |
| Unsupported XML shape for CSV conversion | `422` | High |
| Empty CSV payload | controlled error | High |
| Empty upload filename | `400` | Medium |

## Frontend Consistency Matrix

| Check | Expected Result | Current Risk |
| --- | --- | --- |
| Branding | Frontend naming aligned with repo naming | High |
| Supported conversions | Frontend options match `api-v2` registry | High |
| Cold start messaging | Frontend explains Render Free Tier behavior | Medium |
| Metadata flow | Frontend distinguishes metadata API from conversion API | Medium |
| About page | Frontend architecture text matches current backend | High |

## Suggested Regression Gate

Before considering a release acceptable:

1. `/health` must respond successfully.
2. `/conversions` must reflect the intended production registry.
3. Every stable conversion must have one happy-path scenario documented and verified.
4. High-priority negative-path scenarios must be covered.
5. Frontend must not advertise unsupported production conversions.
