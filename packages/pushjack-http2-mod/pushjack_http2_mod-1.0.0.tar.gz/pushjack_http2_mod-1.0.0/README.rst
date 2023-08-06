********
pushjack
********


Push notifications for APNS (iOS) and GCM (Android). It provides HTTP/2 network protocol based APNS client.

Quickstart
==========

Install using pip:


::

    pip install pushjack-http2-mod


Whether using ``APNS`` or ``GCM``, pushjack provides clients for each. It also provides
a HTTP/2 based APNS client.


APNS (using certificates)
-------------------------

Send notifications using the ``APNSClient`` class:


.. code-block:: python

    from pushjack_http2 import APNSClient

    client = APNSClient(certificate='<path/to/certificate.pem>',
                        default_error_timeout=10,
                        default_expiration_offset=2592000,
                        default_batch_size=100,
                        default_retries=5)

    token = '<device token>'
    alert = 'Hello world.'

    # Send to single device.
    # NOTE: Keyword arguments are optional.
    res = client.send(token,
                      alert,
                      badge='badge count',
                      sound='sound to play',
                      category='category',
                      content_available=True,
                      title='Title',
                      title_loc_key='t_loc_key',
                      title_loc_args='t_loc_args',
                      action_loc_key='a_loc_key',
                      loc_key='loc_key',
                      launch_image='path/to/image.jpg',
                      extra={'custom': 'data'})

    # Send to multiple devices by passing a list of tokens.
    client.send([token], alert, **options)


Access response data.

.. code-block:: python

    # List of all tokens sent.
    res.tokens

    # List of errors as APNSServerError objects
    res.errors

    # Dict mapping errors as token => APNSServerError object.
    res.token_errors


Override defaults for error_timeout, expiration_offset, and batch_size.

.. code-block:: python

    client.send(token,
                alert,
                expiration=int(time.time() + 604800),
                error_timeout=5,
                batch_size=200)


Send a low priority message.

.. code-block:: python

    # The default is low_priority == False
    client.send(token, alert, low_priority=True)


Get expired tokens.

.. code-block:: python

    expired_tokens = client.get_expired_tokens()


Close APNS connection.

.. code-block:: python

    client.close()


For the APNS sandbox, use ``APNSSandboxClient`` instead:


.. code-block:: python

    from pushjack_http2 import APNSSandboxClient

APNS (using Auth tokens)
------------------------

Send notifications using the ``APNSHTTP2Client`` class:


.. code-block:: python

    from pushjack_http2 import APNSHTTP2Client

    key = "my_key"

    token = apns.APNSAuthToken(
        token=key,
        team_id="my_team_id",
        key_id="my_key_id",
    )

    client = apns.APNSHTTP2Client(
        token=token,
        bundle_id='my_bundle_id',
    )

    response = client.send_message(
        device_id="my_device_id",
        message="message",
        content_available=True,
        title="title"
    )


Close APNS connection.

.. code-block:: python

    client.conn.close()


For the APNS sandbox, use ``APNSHTTP2SandboxClient`` instead:


.. code-block:: python

    from pushjack_http2 import APNSHTTP2SandboxClient


GCM
---

Send notifications using the ``GCMClient`` class:


.. code-block:: python

    from pushjack_http2 import GCMClient

    client = GCMClient(api_key='<api-key>')

    registration_id = '<registration id>'
    alert = 'Hello world.'
    notification = {'title': 'Title', 'body': 'Body', 'icon': 'icon'}

    # Send to single device.
    # NOTE: Keyword arguments are optional.
    res = client.send(registration_id,
                      alert,
                      notification=notification,
                      collapse_key='collapse_key',
                      delay_while_idle=True,
                      time_to_live=604800)

    # Send to multiple devices by passing a list of ids.
    client.send([registration_id], alert, **options)


Alert can also be be a dictionary with data fields.

.. code-block:: python

    alert = {'message': 'Hello world', 'custom_field': 'Custom Data'}


Alert can also contain the notification payload.

.. code-block:: python

    alert = {'message': 'Hello world', 'notification': notification}


Send a low priority message.

.. code-block:: python

    # The default is low_priority == False
    client.send(registration_id, alert, low_priority=True)


Access response data.

.. code-block:: python

    # List of requests.Response objects from GCM Server.
    res.responses

    # List of messages sent.
    res.messages

    # List of registration ids sent.
    res.registration_ids

    # List of server response data from GCM.
    res.data

    # List of successful registration ids.
    res.successes

    # List of failed registration ids.
    res.failures

    # List of exceptions.
    res.errors

    # List of canonical ids (registration ids that have changed).
    res.canonical_ids
