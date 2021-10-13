from django.test import TestCase

# Create your tests here.
#
#
#  Running tests
# In the terminal, we can run our test:
# $ python manage.py test polls

import datetime
from django.utils import timezone 
from .models import Question

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self): 
        """
        was_published_recently() returns False for questions whose pub_date is in the future.

        A django.test.TestCase subclass with a method that creates a Question instance with a pub_date in the future. 
        We then check the output of was_published_recently() - which ought to be False.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time) 
        self.assertIs(future_question.was_published_recently(), False)
        """
        what happens in this : 
            - manage.py test polls looked for tests in the polls application
            - it found a subclass of the django.test.TestCase class
            - it created a special database for the purpose of testing
            - it looked for test methods - ones whose names begin with test
            - in test_was_published_recently_with_future_question it created a Question 
              instance whose pub_date field is 30 days in the future
            - ... and using the assertIs() method, it discovered that its was_published_recently() returns True, 
              though we wanted it to return False

        The test informs us which test failed and even the line on which the failure occurred.
        """