Feature: Stable conversion flows in api-v2

  As a QA engineer
  I want stable conversions to behave consistently
  So that the production API remains trustworthy

  Scenario Outline: Stable conversion succeeds for supported pairs
    Given a valid "<from_format>" test file
    And the file extension matches "<from_format>"
    When I submit the file to "/convert" with from_format "<from_format>" and to_format "<to_format>"
    Then the response status should be 200
    And the response content type should match the expected output
    And the response body should not be empty

    Examples:
      | from_format | to_format |
      | txt         | csv       |
      | csv         | txt       |
      | csv         | json      |
      | json        | csv       |
      | csv         | xml       |
      | xml         | csv       |
      | csv         | html      |
      | html        | txt       |
      | txt         | json      |
      | json        | txt       |
      | txt         | xml       |

  Scenario: CSV to HTML escapes executable markup
    Given a CSV file containing a cell with "<script>alert(1)</script>"
    When I submit the file to "/convert" with from_format "csv" and to_format "html"
    Then the response status should be 200
    And the generated HTML should escape the script tag
    And the generated artifact should not contain executable inline script markup
