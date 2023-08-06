class InMemoryVault:
    """In-memory implementation of a vault.

    NB: This is not persistent. It's intended for use in tests, not in production.
    """

    def __init__(self):
        self._accepted = {}
        self._received = {}

    def accepted(self, test_id):
        """Get the current accepted value for `test_id`.

        Args:
            test_id: ID of the test.

        Returns: An Artifact instance.

        Raises:
            KeyError: `test_id` does not have accepted data in the vault.
        """
        return self._accepted[test_id]

    def accept(self, test_id):
        """Accept the current received data for `test_id`.

        Args:
            test_id: The ID of the test to accept.

        Raises:
            KeyError: There is no received data for `test_id`.
        """
        artifact = self._received.pop(test_id)
        self._accepted[test_id] = artifact

    def received(self, test_id):
        """Get the current received value for `test_id`.

        Args:
            test_id: ID of test.

        Returns: An Artifact describing the received data `test_id`.

        Raises:
            KeyError: There is no received data for `test_id`.
        """
        return self._received[test_id]

    def receive(self, test_id, artifact):
        """Set new received data for a test.

        Args:
            test_id: ID of the test for which to receive data.
            artifact: Artifact describing received data for the test.
        """
        self._received[test_id] = artifact

    def ids(self):
        """Get all IDs in the vault.

        This is all IDs that have either or both of accepted and received data. There is no
        order to the results. Each ID is included only once in the output, even if it has both
        received and accepted data.

        Returns: An iterable of all test IDs.
        """
        yield from self._received
        yield from self._accepted
