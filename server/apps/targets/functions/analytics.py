def get_user_analytics(user) -> dict:
    """Get analytics info about current user."""
    targets = user.targets.all()
    not_finish_targets = targets.filter(is_finished=False)
    categories = user.categories.all()
    data = {
        'count_not_finished_targets': (
            not_finish_targets.count()
        ),
        'success_category': (
            categories.get_success_category()
        ),
        'populary_category': (
            categories.get_popular_category()
        ),
        'immediate_target': (
            not_finish_targets.get_immediate_target()
        ),
    }
    data.update(not_finish_targets.get_amount_not_finished_targets())
    data.update(targets.get_all_income_percent())
    data.update(not_finish_targets.get_income_percent_month())
    return data
