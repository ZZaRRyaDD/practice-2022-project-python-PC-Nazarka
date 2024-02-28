from django.db.models import (
    Count,
    DecimalField,
    F,
    IntegerField,
    Q,
    QuerySet,
    Sum,
)
from django.db.models.functions import Coalesce

from ...constants import COUNT_CATEGORIES


class TransactionCategoryQuerySet(QuerySet):
    def annotate_with_transaction_sums(self):
        """
        :return: TransactionCategoryQuerySet
        """

        return self.annotate(
            transactions_sum=Coalesce(
                Sum('transactions__amount'),
                0,
                output_field=DecimalField(),
            ),
        )

    def get_top_categories(self) -> list:
        """Get data for reponse of top categories."""
        data = list(
            self[:COUNT_CATEGORIES].values(
                'name',
                'transactions_sum',
            ),
        )
        transactions_sum = sum(
            [
                category.transactions_sum
                for category in self[COUNT_CATEGORIES:]
            ],
        )
        new_item = {
            'name': 'Другое',
            'transactions_sum': transactions_sum,
        }
        data.append(new_item)
        return data

    def get_popular_category(self):
        """Get popular category by count targets."""
        populary_category = self.annotate(
            count_targets=Count(
                F('targets'),
            ),
        )
        populary_category = sorted(
            populary_category,
            key=lambda t: t.count_targets,
            reverse=True,
        )
        return (
            {'name': populary_category[0].name}
            if populary_category else None
        )

    def get_success_category(self):
        """Get success categories by count finished targets."""
        success_category = self.annotate(
            count_finished_targets=Coalesce(
                Count(
                    F('targets'),
                    filter=Q(targets__is_finished=True),
                ),
                0,
                output_field=IntegerField(),
            ),
        )
        success_category = sorted(
            success_category,
            key=lambda x: x.count_finished_targets,
            reverse=True,
        )
        return (
            {'name': success_category[0].name}
            if success_category else None
        )
