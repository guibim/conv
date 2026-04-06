Feature: Smoke coverage for deployed Conv surfaces

  As a QA engineer
  I want to confirm the main public surfaces are reachable
  So that I can quickly detect deployment regressions

  Scenario: Main API v2 health endpoint responds
    Given the Render deployment for api-v2 is active
    When I send a request to "/health"
    Then the response status should be 200
    And the response should contain the service name
    And the response should contain the current version

  Scenario: Main API v2 conversions endpoint responds
    Given the Render deployment for api-v2 is active
    When I send a request to "/conversions"
    Then the response status should be 200
    And the response should list supported conversion pairs

  Scenario: Frontend landing page loads
    Given the GitHub Pages frontend is published
    When I open the landing page
    Then the page should render without a fatal error
    And the user should see the project branding
    And the user should see at least one conversion-related CTA
