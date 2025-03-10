**Error Handling**
==================

Overview
--------

The Aymara AI SDK uses a structured exception hierarchy to handle errors returned from the API. All exceptions raised by the SDK inherit from the base ``AymaraError`` class, making it easy to catch all SDK-related errors.

Exception Hierarchy
-------------------

- **AymaraError**: Base exception class for all Aymara SDK errors
    - **AuthError**: Authentication and authorization errors
    - **RateLimitError**: Rate limiting and quota errors
    - **ResourceError**: Errors related to accessing resources (tests, policies, etc.)
    - **ValidationError**: Input validation errors
    - **ServerError**: Internal server errors

Error Codes
-----------

Each error raised by the SDK includes specific error information:

- An error code that identifies the specific error
- A descriptive message explaining the error
- Request ID for support and debugging
- Additional details for some error types

Error Code Reference
--------------------

Authentication Errors
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Error Code
     - Description
   * - ``auth.expired_key``
     - The API key has expired
   * - ``auth.insufficient_permissions``
     - The API key doesn't have permission for the requested action
   * - ``auth.invalid_key``
     - The API key is invalid or improperly formatted

Rate Limit Errors
^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Error Code
     - Description
   * - ``rate_limit.quota_exceeded``
     - Account quota has been exceeded
   * - ``rate_limit.request_limit``
     - Too many requests in a short time period
   * - ``rate_limit.test_quota_exceeded``
     - Test-specific quota has been exceeded

Resource Errors
^^^^^^^^^^^^^^^

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Error Code
     - Description
   * - ``resource.conflict``
     - Resource already exists or conflicts with another resource
   * - ``resource.not_found``
     - The requested resource doesn't exist
   * - ``resource.policy_not_found``
     - The requested policy doesn't exist
   * - ``resource.score_run_not_found``
     - The requested score run doesn't exist
   * - ``resource.test_not_found``
     - The requested test doesn't exist

Validation Errors
^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Error Code
     - Description
   * - ``validation.invalid_format``
     - Input is in an invalid format
   * - ``validation.invalid_request``
     - Request is invalid
   * - ``validation.missing_field``
     - Required field is missing

Server Errors
^^^^^^^^^^^^^

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Error Code
     - Description
   * - ``server.internal_error``
     - Internal server error

Error Handling Examples
-----------------------

Handling specific error types:

.. code-block:: python

   from aymara_ai import AymaraAI
   from aymara_ai.core.errors import ResourceError, RateLimitError

   aymara = AymaraAI(api_key="your_api_key")

   try:
       aymara.get_test("non_existent_test_id")
   except ResourceError as e:
       print(f"Resource error: {e}")
       print(f"Error code: {e.code}")
       print(f"Request ID: {e.request_id}")
   except RateLimitError as e:
       print(f"Rate limit exceeded: {e}")
   except Exception as e:
       print(f"Unexpected error: {e}")

Handling all Aymara errors:

.. code-block:: python

   from aymara_ai import AymaraAI
   from aymara_ai.core.errors import AymaraError

   aymara = AymaraAI(api_key="your_api_key")

   try:
       # SDK operation
       results = aymara.score_test("test_id", student_answers)
   except AymaraError as e:
       print(f"Aymara API error: {e}")
       print(f"Error code: {e.code}")
       print(f"Request ID: {e.request_id}")
