import datetime

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from ..models import Target, TargetTransaction
from ...pockets.constants import TransactionTypes
from ...pockets.models import Transaction, TransactionCategory


class TargetAPICRUDTestCase(TestCase):
    """Case for tests of API CRUD operations of target."""

    def setUp(self):
        self.api_client = APIClient()
        self.user = get_user_model().objects.create(
            username='root',
            email='root@root.com',
            password='root',
        )
        self.category = TransactionCategory.objects.create(
            name='Category',
            user=self.user,
        )
        Transaction.objects.create(
            transaction_date=datetime.date.today(),
            amount=Decimal(100000),
            category=None,
            transaction_type=TransactionTypes.INCOME,
            user=self.user,
        )
        self.api_client.force_authenticate(
            user=self.user,
        )
        self.data = {
            'name': 'Target1',
            'amount': Decimal(666),
            'category': self.category,
            'initial_deposit': Decimal(10),
            'deposit_term': 6,
            'percent': Decimal(50),
            'is_finished': False,
            'user': self.user,
        }
        self.count_transactions = Transaction.objects.count()
        self.count_targets = Target.objects.count()
        self.count_target_transactions = TargetTransaction.objects.count()

    def test_create_target(self):
        """Test for check correct create target."""
        data = self.data
        data['category'] = data['category'].id
        response = self.api_client.post(reverse('targets-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Target.objects.count(), self.count_targets + 1)
        self.assertEqual(
            Transaction.objects.count(),
            self.count_transactions + 1,
        )
        self.assertEqual(
            TargetTransaction.objects.count(),
            self.count_target_transactions + 1,
        )

    def test_update_target(self):
        """Test for check correct update target."""
        data = self.data
        data['category'] = data['category'].id
        response = self.api_client.post(reverse('targets-list'), data)
        data['name'] = 'New target name'
        data['id'] = response.data['id']
        response = self.api_client.put(
            reverse('targets-detail', kwargs={'pk': data['id']}),
            data,
        )
        self.assertTrue(
            Target.objects.filter(id=data['id'], name=data['name']).exists(),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Target.objects.count(), self.count_targets + 1)
        self.assertEqual(
            Transaction.objects.count(),
            self.count_transactions + 1,
        )
        self.assertEqual(
            TargetTransaction.objects.count(),
            self.count_target_transactions + 1,
        )

    def test_delete_target(self):
        """Test for check correct delete target."""
        data = self.data
        data['category'] = data['category'].id
        response = self.api_client.post(reverse('targets-list'), data)
        id = response.data['id']
        response = self.api_client.delete(
            reverse('targets-detail', kwargs={'pk': id}),
            data,
        )
        self.assertFalse(Target.objects.filter(id=id).exists())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Target.objects.count(), self.count_targets)
        self.assertEqual(
            Transaction.objects.count(), 
            self.count_transactions + 2,
    )
        self.assertEqual(
            TargetTransaction.objects.count(),
            self.count_target_transactions,
        )


class TargetAmountAPITestCase(TestCase):
    """Case for tests of operations with amount and API of target."""

    def setUp(self):
        self.api_client = APIClient()
        self.user = get_user_model().objects.create(
            username='root',
            email='root@root.com',
            password='root',
        )
        self.category = TransactionCategory.objects.create(
            name='Category',
            user=self.user,
        )
        Transaction.objects.create(
            transaction_date=datetime.date.today(),
            amount=Decimal(100000),
            category=None,
            transaction_type=TransactionTypes.INCOME,
            user=self.user,
        )
        self.api_client.force_authenticate(
            user=self.user,
        )
        initial_deposit = Decimal(10)
        self.data = {
            'name': 'Target1',
            'amount': Decimal(666),
            'category': self.category,
            'initial_deposit': Decimal(10),
            'deposit_term': 6,
            'percent': Decimal(50),
            'is_finished': False,
            'user': self.user,
        }
        self.target = Target.objects.create(**self.data)
        Transaction.objects.create(
            transaction_date=datetime.date.today(),
            amount=initial_deposit,
            transaction_type=TransactionTypes.EXPENSE,
            category=self.category,
            user=self.user,
        )
        TargetTransaction.objects.create(
            target=self.target,
            amount=initial_deposit,
        )
        self.count_transactions = Transaction.objects.count()
        self.count_targets = Target.objects.count()
        self.count_target_transactions = TargetTransaction.objects.count()

    def test_replenishment_target(self):
        """
        Test for check replenishment target.
        """
        amount = Decimal(10)
        data = {
            'target': self.target.id,
            'amount': amount,
        }
        response = self.api_client.post(
            reverse('target_transactions-replenishment'),
            data,
        )
        target = Target.objects.filter(id=self.target.id).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            target.current_amount,
            self.target.initial_deposit + amount,
        )
        self.assertTrue(
            TargetTransaction.objects.count(),
            self.count_target_transactions + 2
        )
        self.assertTrue(
            Transaction.objects.count(),
            self.count_transactions + 2,
        )

    def test_finish_target(self):
        """
        Test for check finish target.
        """
        data = {
            'target': self.target.id,
            'amount': Decimal(1000),
        }
        self.api_client.post(
            reverse('target_transactions-replenishment'),
            data,
        )
        response = self.api_client.post(
            reverse(
                'targets-finish',
                kwargs={'pk': self.target.id},
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Цель завершена')
        self.assertTrue(
            TargetTransaction.objects.count(),
            self.count_target_transactions + 1,
        )
        self.assertTrue(
            Transaction.objects.count(),
            self.count_transactions + 2,
        )


class TargetPercentTestCase(TestCase):
    """Case for tests with operations with percentof target."""

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='root',
            email='root@root.com',
            password='root',
        )
        self.category = TransactionCategory.objects.create(
            name='Category',
            user=self.user,
        )
        Transaction.objects.create(
            transaction_date=datetime.date.today(),
            amount=Decimal(100000),
            category=None,
            transaction_type=TransactionTypes.INCOME,
            user=self.user,
        )
        initial_deposit = Decimal(10)
        self.data = {
            'name': 'Target1',
            'amount': Decimal(666),
            'category': self.category,
            'initial_deposit': Decimal(10),
            'deposit_term': 6,
            'percent': Decimal(50),
            'is_finished': False,
            'user': self.user,
        }
        self.target = Target.objects.create(**self.data)
        Transaction.objects.create(
            transaction_date=datetime.date.today(),
            amount=initial_deposit,
            transaction_type=TransactionTypes.EXPENSE,
            category=self.category,
            user=self.user,
        )
        TargetTransaction.objects.create(
            target=self.target,
            amount=initial_deposit,
        )
        self.count_transactions = Transaction.objects.count()
        self.count_targets = Target.objects.count()
        self.count_target_transactions = TargetTransaction.objects.count()

    def test_up_correct_percent_on_target(self):
        """
        Test for check interest append on target.
        """
        amount = round(
            (self.target.initial_deposit * self.target.percent / 36500),
            2,
        )
        amount_before = self.target.current_amount
        TargetTransaction.interest_append()
        self.assertEqual(amount_before, self.target.initial_deposit)
        self.assertEqual(
            self.target.current_amount,
            self.target.initial_deposit + amount,
        )
        self.assertTrue(
            TargetTransaction.objects.count(),
            self.count_target_transactions + 2,
        )
        self.assertTrue(
            Transaction.objects.count(),
            self.count_transactions + 1,
        )

    def test_not_up_percent_on_finish_target(self):
        """
        Test for check interest append on finished target.
        """
        self.target.is_finished = True
        self.target.save()
        TargetTransaction.interest_append()
        target = Target.objects.filter(id=self.target.id).first()
        self.assertEqual(target.current_amount, self.target.initial_deposit)
        self.assertTrue(
            TargetTransaction.objects.count(),
            self.count_target_transactions + 2,
        )
        self.assertTrue(
            Transaction.objects.count(),
            self.count_transactions + 2,
        )
