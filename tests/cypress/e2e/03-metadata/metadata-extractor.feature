Feature: Image metadata extraction

  As a QA engineer
  I want to validate the secondary metadata API
  So that the image extraction flow remains stable and separate from the core conversion API

  Scenario: Metadata health endpoint responds
    Given the metadata API is deployed
    When I request "/health"
    Then the response status should be 200
    And the response should indicate service health

  Scenario: Supported image upload returns metadata or a controlled empty result
    Given a valid image file with or without EXIF metadata
    When I upload the file to the metadata extraction endpoint
    Then the response status should be 200
    And the response should either include metadata or a controlled "no metadata found" message

  Scenario: Non-image upload is rejected
    Given a non-image file
    When I upload the file to the metadata extraction endpoint
    Then the response status should be 400
