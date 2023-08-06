from bmlx.utils import proc_utils
import unittest


class ProcUtilsTest(unittest.TestCase):
    d = 0

    def testRetry(self):
        d = 0

        @proc_utils.retry(
            retry_count=6, delay=0.05, allowed_exceptions=(KeyError)
        )
        def five_error_one_right():
            nonlocal d
            if d < 2:
                d += 1
                raise KeyError()

        five_error_one_right()
        self.assertEqual(d, 2)

    def testRetryUnexceptedError(self):
        @proc_utils.retry()
        def unexcept():
            raise Exception

        self.assertRaises(Exception, unexcept)

    def testPoll(self):
        d = 0

        def check():
            nonlocal d
            if d == 3:
                return True
            else:
                d += 1

        def cleanup(ret, exec_info=None):
            return

        proc_utils.poll_wait_until(check, cleanup, timeout=5)
        self.assertEqual(d, 3)

    def testTimeoutPool(self):
        d = 0

        def check():
            nonlocal d
            if d == 3:
                return True
            else:
                d += 1

        def cleanup(ret, exec_info=None):
            self.assertIsInstance(exec_info, proc_utils.TimeoutException)

        proc_utils.poll_wait_until(check, cleanup, timeout=2)
        self.assertEqual(d, 2)
