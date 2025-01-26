import unittest
import multiprocessing
import time
from alfa1.chat_app.app.chat.models import ChatMessage
from alfa1.chat_app.app.message_process import message_process_main

class TestMessageProcessing(unittest.TestCase):
    def setUp(self):
        # Setup queues
        self.message_queue = multiprocessing.Queue()
        self.broadcast_queue = multiprocessing.Queue()
        self.log_queue = multiprocessing.Queue()

        # Start the message process
        self.process = multiprocessing.Process(target=message_process_main, args=(
            self.message_queue, self.broadcast_queue, self.log_queue, "config.yaml"
        ))
        self.process.start()

    def tearDown(self):
        # Terminate the process
        self.message_queue.put("SHUTDOWN")
        self.process.join()

    def test_process_valid_message(self):
        message = {"username": "TestUser", "content": "Hello World!"}
        self.message_queue.put(message)
        time.sleep(1)  # Give some time for processing

        # Check if broadcast_queue has the processed message
        self.assertFalse(self.broadcast_queue.empty())
        broadcasted = self.broadcast_queue.get()
        self.assertEqual(broadcasted["type"], "message")
        self.assertEqual(broadcasted["data"]["username"], "TestUser")
        self.assertEqual(broadcasted["data"]["content"], "Hello World!")

    def test_process_invalid_message(self):
        message = {"username": "TestUser", "content": "Hello §"}
        self.message_queue.put(message)
        time.sleep(1)  # Give some time for processing

        # Since the message is invalid, it should not be broadcasted
        self.assertTrue(self.broadcast_queue.empty())

if __name__ == '__main__':
    unittest.main()
