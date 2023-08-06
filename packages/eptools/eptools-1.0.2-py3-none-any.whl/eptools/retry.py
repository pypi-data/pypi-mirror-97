import time
import slackNotifications
from functools import wraps



def retry(ExceptionToCheck, tries=4, delay=1, backoff=1, logger=None, slack_svc_name = None):
    """Retry calling the decorated function using an exponential backoff.

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            
            while mtries > 0:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = slack_svc_name +  " %s, Retrying in %d seconds..." % (str(e), mdelay)
                    print(mtries)
                    if mtries == 1:
                        slackNotifications.errorNotification(slack_svc_name, "After " + str(tries - mtries) + " attempts\n"+ str(e)
                        + "\nPlease check logs")
                        print('time to output msg')
 
                    if logger:
                       logger.error(msg)

                    print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff

            return f(*args, **kwargs)
              

        return f_retry # true decorator
       

    return deco_retry

