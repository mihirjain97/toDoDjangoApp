
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


def createQuestion(questionText, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(questionText=questionText, pubDate=time)

class QuestionIndexViewTests(TestCase):
    def testNoQuestions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def testPastQuestion(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        createQuestion(questionText="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])
    
    def testFutureQuestion(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        createQuestion(questionText="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    
    def testFutureQuestionAndPastQuestion(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        createQuestion(questionText="Past question.", days=-30)
        createQuestion(questionText="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def testTwoPastQuestions(self):
        """
        The questions index page may display multiple questions.
        """
        createQuestion(questionText="Past question 1.", days=-30)
        createQuestion(questionText="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question 2.>', '<Question: Past question 1.>'])


class QuestionDetailViewTests(TestCase):
    def testFutureQuestion(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        futureQuestion = createQuestion(questionText='Future question.', days=5)
        url = reverse('polls:detail', args=(futureQuestion.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def testPastQuestion(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        pastQuestion = createQuestion(questionText='Past Question.', days=-5)
        url = reverse('polls:detail', args=(pastQuestion.id,))
        response = self.client.get(url)
        self.assertContains(response, pastQuestion.questionText)
class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pubDate = time)
        self.assertIs(future_question.was_published_recently(),False)
        
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns false for questions whose pubDate
        is older than one day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pubDate=time)
        self.assertIs(old_question.was_published_recently(), False)
    
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns true for questions whose pubDate 
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pubDate=time)
        self.assertIs(recent_question.was_published_recently(), True) 

