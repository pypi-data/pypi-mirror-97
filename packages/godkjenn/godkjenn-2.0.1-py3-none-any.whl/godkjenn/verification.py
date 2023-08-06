"""The core approval testing algorithm.

This is where we check the latest *received* data with the latest *accepted* data.
"""


def verify(vault, comparator, test_id, received):
    """Check if `received` matches the current accepted value for the test_id.

    If `received` doesn't match the accepted value, this will raise MismatchError§.

    Args:
        vault: A Vault instance.
        comparator: A Comparator instance.
        test_id: The ID of the test that produced `received`.
        received: An Artifact representing the received data.
    """
    vault.receive(test_id, received)

    try:
        accepted = vault.accepted(test_id)

        if comparator(accepted.data, received.data):
            vault.accept(test_id)
            return

        message = "Received data does not match accepted"
    except KeyError:
        accepted = None
        message = "There is no accepted data"

    raise MismatchError(message, received, accepted)


class MismatchError(Exception):
    def __init__(self, message, received, accepted):
        super().__init__(message)
        self._received = received
        self._accepted = accepted

    @property
    def message(self):
        return self.args[0]

    @property
    def received(self):
        return self._received

    @property
    def accepted(self):
        return self._accepted
