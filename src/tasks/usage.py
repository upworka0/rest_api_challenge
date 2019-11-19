from src.models.usages import DataUsage
from src.models.subscriptions import Subscription, SubscriptionStatus
from src.models.cycles import BillingCycle
from src.models.service_codes import *
from src.models.base import db


def get_current_usages(sub):
    """
    Get usages by subscription and current cycle
    :param sub: Subscription object
    :return: Usage objects
    """
    cycle = BillingCycle.get_current_cycle()
    try:
        usages = DataUsage.query.join(Subscription) \
            .filter(DataUsage.from_date > cycle.start_date) \
            .filter(Subscription.status != SubscriptionStatus.new) \
            .filter(DataUsage.subscription_id == sub.id) \
            .all()
    except Exception as e:
        usages = []
    return usages


def check_subscription(sub):
    """
    checks if subscription is over their allotted data usage for the current billing cycle
    :param sub: Subscription object
    :return: Boolean
    """
    usages = get_current_usages(sub)
    total = 0
    for usage in usages:
        total += usage.mb_used

    if total < sub.plan.mb_available or sub.plan.is_unlimited:
        return False
    else:
        return True


def check_subscriptions():
    """
    Check if subscriptions are over their allotted data usage for the current billing cycle
    :param subscriptions:
    :return: None
    """
    subscriptions = Subscription.query.filter()

    for sub in subscriptions:
        if check_subscription(sub):
            code = ServiceCode.query.filter(ServiceCode.name == 'Data Block').first()
            sub.service_codes.append(code)
            # db.session.add(sub)
            db.session.commit()
