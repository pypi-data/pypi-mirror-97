"""Simple file-system based implementation of a vault.
"""

from enum import Enum
from pathlib import Path

from godkjenn.artifact import Artifact


class FSVault:
    """File-system implementation of a vault.

    This just keeps accepted data in files with the "accepted" suffix and received data in files suffixed with
    "received". Id's in this vault are simply paths.

    This assumes it has complete control over the files under `root_directory`.

    Args:
        root_path: The root directory under which this will store received and accepted data.
    """

    def __init__(self, root_path):
        self._root_path = Path(root_path)

    @property
    def root_path(self):
        "Root path of the vault."
        return self._root_path

    def accepted(self, test_id):
        """Get the current accepted value for `test_id`.

        Args:
            test_id: ID of the test.

        Returns: An Artifact instance.

        Raises:
            KeyError: `test_id` does not have accepted data in the vault.
        """
        return self._get(test_id, _Kind.accepted)

    def accept(self, test_id):
        """Accept the current received data for `test_id`.

        Args:
            test_id: The ID of the test to accept.

        Raises:
            KeyError: There is no received data for `test_id`.
        """
        artifact = self.received(test_id)

        self._put(test_id, _Kind.accepted, artifact)

        p = self._full_path(test_id, _Kind.received)
        if p.exists():
            p.unlink()

    def received(self, test_id):
        """Get the current received value for `test_id`.

        Args:
            test_id: ID of test.

        Returns: An Artifact describing the received data `test_id`.

        Raises:
            KeyError: There is no received data for `test_id`.
        """
        return self._get(test_id, _Kind.received)

    def receive(self, test_id, artifact):
        """Set new received data for a test.

        Args:
            test_id: ID of the test for which to receive data.
            artifact: Artifact describing received data for the test.
        """
        self._put(test_id, _Kind.received, artifact)

    def ids(self):
        """Get all IDs in the vault.

        This is all IDs that have either or both of accepted and received data. There is no
        order to the results. Each ID is included only once in the output, even if it has both
        received and accepted data.

        Returns: An iterable of all test IDs.
        """
        return set(
            str(path.parent.relative_to(self._root_path))
            for kind in _Kind
            for path in self._root_path.glob('**/{}'.format(kind.value)))

    def _full_path(self, path, kind):
        return self._root_path / path / kind.value

    def _get(self, path, kind):
        full_path = self._full_path(path, kind)

        if not full_path.exists():
            raise KeyError('no {} data: {}'.format(kind.value, path))

        with full_path.open(mode='rb') as handle:
            data = handle.read()

        return Artifact(data)

    def _put(self, path, kind, artifact):
        full_path = self._full_path(path, kind)

        full_path.parent.mkdir(parents=True, exist_ok=True)

        with full_path.open(mode='wb') as handle:
            handle.write(artifact.data)


class _Kind(Enum):
    accepted = 'accepted'
    received = 'received'
