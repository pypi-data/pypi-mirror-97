"""Improved version of Pact, that fixes interaction order issues."""

from typing import TYPE_CHECKING, Any, cast

from outcome.devkit_api.pact.pactman.mock.mock_urlopen import MockURLOpenHandler
from pactman import Pact as OriginalPact

if TYPE_CHECKING:  # pragma: no cover
    from pactman.mock.pact import V3Interaction, JSONType  # noqa: WPS433
else:
    V3Interaction = Any  # noqa: WPS440
    JSONType = Any  # noqa: WPS440


class Pact(OriginalPact):  # pragma: no cover
    # This is a fix - the official pactman library inserts new interactions at the beginning
    # of the _interactions array, but then uses the last item in the array when using `and_given`
    # This override addresses the index alignment issue.
    def and_given(self, provider_state: str, **params: JSONType):

        self.semver

        if self.semver.major < 3:
            raise ValueError('pact v2 only allows a single provider state')
        elif not self._interactions:
            raise ValueError('only invoke and_given() after given()')

        # We know that we're dealing with V3
        most_recent_interaction = cast(V3Interaction, self._interactions[0])
        most_recent_interaction['providerStates'].append({'name': provider_state, 'params': params})
        return self

    # We need to override the `OriginalPact` `start_mocking` method to use our custom `MockURLOpenHandler`
    # that changes the way Pactman gets interactions.
    def start_mocking(self):
        if self.use_mocking_server:
            super().start_mocking()
        else:
            # Pactman comment: ain't no port, we're monkey-patching (but the URLs we generate still need to look correct)
            self._mock_handler = MockURLOpenHandler(self)
