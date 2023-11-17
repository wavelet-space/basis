from essence.messaging.actor import Message


def test_message_equality():
    m1 = Message(1)
    m2 = Message(1)
    assert m1 == m2
