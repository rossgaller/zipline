"""
Reference implementation for buyback auth loaders.
"""

from ..data.buyback_auth import (
    CashBuybackAuthorizations,
    ShareBuybackAuthorizations
)
from .events import EventsLoader
from zipline.pipeline.common import (
    BUYBACK_ANNOUNCEMENT_FIELD_NAME,
    CASH_FIELD_NAME,
    SHARE_COUNT_FIELD_NAME
)
from zipline.utils.memoize import lazyval


class CashBuybackAuthorizationsLoader(EventsLoader):
    """
    Reference loader for
    :class:`zipline.pipeline.data.CashBuybackAuthorizations`.

    events_by_sid: dict[sid -> pd.DataFrame(knowledge date,
    event date, cash value)]

    """

    def __init__(self,
                 all_dates,
                 events_by_sid,
                 infer_timestamps=False,
                 dataset=CashBuybackAuthorizations):
        super(CashBuybackAuthorizationsLoader, self).__init__(
            all_dates,
            events_by_sid,
            infer_timestamps=infer_timestamps,
            dataset=dataset,
        )

    @property
    def expected_cols(self):
        return frozenset([BUYBACK_ANNOUNCEMENT_FIELD_NAME, CASH_FIELD_NAME])

    @lazyval
    def previous_value_loader(self):
        return self._previous_event_value_loader(
            self.dataset.previous_value,
            BUYBACK_ANNOUNCEMENT_FIELD_NAME,
            CASH_FIELD_NAME
        )

    @lazyval
    def previous_announcement_date_loader(self):
        return self._previous_event_date_loader(
            self.dataset.previous_announcement_date,
            BUYBACK_ANNOUNCEMENT_FIELD_NAME,
        )


class ShareBuybackAuthorizationsLoader(EventsLoader):
    """
    Reference loader for
    :class:`zipline.pipeline.data.ShareBuybackAuthorizations`.

    Does not currently support adjustments to the dates of known buyback
    authorizations.

    events_by_sid: dict[sid -> pd.DataFrame(knowledge date,
     event date, share value)]

    """

    def __init__(self,
                 all_dates,
                 events_by_sid,
                 infer_timestamps=False,
                 dataset=ShareBuybackAuthorizations):
        super(ShareBuybackAuthorizationsLoader, self).__init__(
            all_dates,
            events_by_sid,
            infer_timestamps=infer_timestamps,
            dataset=dataset,
        )

    @property
    def expected_cols(self):
        return frozenset([BUYBACK_ANNOUNCEMENT_FIELD_NAME,
                          SHARE_COUNT_FIELD_NAME])

    @lazyval
    def previous_share_count_loader(self):
        return self._previous_event_value_loader(
            self.dataset.previous_share_count,
            BUYBACK_ANNOUNCEMENT_FIELD_NAME,
            SHARE_COUNT_FIELD_NAME
        )

    @lazyval
    def previous_announcement_date_loader(self):
        return self._previous_event_date_loader(
            self.dataset.previous_announcement_date,
            BUYBACK_ANNOUNCEMENT_FIELD_NAME,
        )
