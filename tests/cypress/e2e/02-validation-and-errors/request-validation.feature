Feature: Request validation and negative-path handling

  As a QA engineer
  I want invalid requests to fail predictably
  So that the API remains safe and understandable

  Scenario: Unsupported conversion pair is rejected
    Given a valid CSV file
    When I submit the file to "/convert" with from_format "csv" and to_format "dta"
    Then the response status should be 400
    And the error message should state that the conversion is unsupported

  Scenario: File extension mismatch is rejected
    Given a file named "sample.txt" that contains CSV-like content
    When I submit the file to "/convert" with from_format "csv" and to_format "json"
    Then the response status should be 400
    And the error message should mention extension mismatch

  Scenario: Oversized upload is rejected
    Given a file larger than the configured MAX_UPLOAD_BYTES
    When I submit the file to "/convert"
    Then the response status should be 413
    And the request should not be processed as a conversion

  Scenario: Invalid JSON is rejected for json to csv
    Given a malformed JSON file
    When I submit the file to "/convert" with from_format "json" and to_format "csv"
    Then the response status should indicate invalid input

  Scenario: Invalid XML is rejected
    Given a malformed XML file
    When I submit the file to "/convert" with from_format "xml" and to_format "csv"
    Then the response status should indicate invalid input
