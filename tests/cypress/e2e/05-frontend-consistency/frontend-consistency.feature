Feature: Frontend and backend consistency

  As a QA engineer
  I want frontend messaging to match actual backend behavior
  So that users are not misled about supported capabilities

  Scenario: Frontend branding matches current project branding
    Given the repository documentation uses the current project name
    When I open the published frontend
    Then the branding should match the documented project naming

  Scenario: Frontend conversion catalog matches api-v2
    Given the live api-v2 registry is available at "/conversions"
    When I inspect the conversion options presented in the frontend
    Then the frontend should not advertise unsupported production conversions
    And the frontend should not omit stable api-v2 conversions without explanation

  Scenario: About page reflects the current architecture
    Given api-v2 is the primary supported backend
    When I read the frontend About page
    Then the architecture description should mention the current backend baseline
    And it should not present deprecated capabilities as active production scope

  Scenario: Metadata functionality is framed as a secondary service
    Given the metadata extractor is a separate API surface
    When I inspect the frontend flow for metadata extraction
    Then the UI copy should distinguish it from the core conversion API
