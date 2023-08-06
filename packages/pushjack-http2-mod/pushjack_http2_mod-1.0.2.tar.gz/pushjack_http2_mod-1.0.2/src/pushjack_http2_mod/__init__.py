# -*- coding: utf-8 -*-
"""Pushjack module.
"""

from .__version__ import __version__

from .apns import (
    APNSClient,
    APNSSandboxClient,
    APNSResponse,
    APNSExpiredToken,
    APNSHTTP2Client,
    APNSHTTP2SandboxClient,
    APNSAuthToken,
)

from .gcm import (
    GCMClient,
    GCMResponse,
    GCMCanonicalID,
)

from .exceptions import (
    APNSError,
    APNSAuthError,
    APNSServerError,
    APNSProcessingError,
    APNSMissingTokenError,
    APNSMissingTopicError,
    APNSMissingPayloadError,
    APNSInvalidTokenSizeError,
    APNSInvalidTopicSizeError,
    APNSInvalidPayloadSizeError,
    APNSInvalidTokenError,
    APNSShutdownError,
    APNSProtocolError,
    APNSUnknownError,
    APNSTimeoutError,
    APNSUnsendableError,
    GCMError,
    GCMAuthError,
    GCMServerError,
    GCMMissingRegistrationError,
    GCMInvalidRegistrationError,
    GCMUnregisteredDeviceError,
    GCMInvalidPackageNameError,
    GCMMismatchedSenderError,
    GCMMessageTooBigError,
    GCMInvalidDataKeyError,
    GCMInvalidTimeToLiveError,
    GCMTimeoutError,
    GCMInternalServerError,
    GCMDeviceMessageRateExceededError,
    NotificationError,
    ServerError,
)

# Set default logging handler to avoid "No handler found" warnings.
import logging

try:  # Python 2.7+
    from logging import NullHandler  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


logging.getLogger(__name__).addHandler(NullHandler())
