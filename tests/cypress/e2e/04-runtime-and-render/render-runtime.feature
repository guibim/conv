Feature: Render Free Tier runtime behavior

  As a QA engineer
  I want environment-specific behavior to be visible and acceptable
  So that platform limitations are not mistaken for functional regressions

  Scenario: Cold start behavior is documented
    Given the application is hosted on Render Free Tier
    When I review project-facing documentation
    Then cold start behavior should be explicitly described
    And the user should be informed that the first request may take longer after inactivity

  Scenario: API recovers after idle period
    Given the Render service has been idle long enough to suspend
    When I send the first request after inactivity
    Then the service may respond more slowly
    But the request should still complete successfully once the instance wakes up

  Scenario: Subsequent requests are faster than the cold start request
    Given the first request after idle has completed
    When I send another request shortly after
    Then the response should be noticeably faster than the cold start request
