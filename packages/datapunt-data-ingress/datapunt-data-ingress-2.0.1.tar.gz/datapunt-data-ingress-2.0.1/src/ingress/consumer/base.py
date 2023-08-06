from abc import ABC, abstractmethod
from time import sleep

from django.db import transaction

from ingress.models import Collection, Message


class BaseConsumer(ABC):
    """
    Whether or not to immediately remove messages once consumption succeeds.
    If set to False, message.consume_succeeded_at will be set.
    """

    remove_message_on_consumed = True

    """
    Whether or not to set Message.consume_started_at immediately once consumption starts
    """
    set_consume_started_at = False

    @property
    @abstractmethod
    def collection_name(self):
        pass

    @abstractmethod
    def consume_raw_data(self, raw_data):
        """
        Implement consumption of one raw message.
        If it fails an exception must be raised.
        """
        pass

    def on_consume_start(self, message):
        if self.set_consume_started_at:
            message.set_consume_started(save_immediately=True)

    def on_consume_success(self, message):
        if self.remove_message_on_consumed:
            message.delete()
        else:
            message.set_consume_succeeded(save_immediately=True)

    def on_consume_error(self, message):
        message.move_to_failed_queue()

    def consume_message(self, message):
        if message.consume_started:
            return

        self.on_consume_start(message)

        try:
            # A try/except within an atomic transaction is not possible
            # For this reason we add another transaction within this try/except
            # https://docs.djangoproject.com/en/3.1/topics/db/transactions/#controlling-transactions-explicitly
            with transaction.atomic():
                self.consume_raw_data(message.raw_data)
                self.on_consume_success(message)

        except Exception:
            self.on_consume_error(message)

    def consume_iterator(self, message_iterator):
        for message in message_iterator:
            self.consume_message(message)

    def get_default_batch_size(self):
        return 100

    # flake8: noqa: C901
    def consume(
        self, end_at_empty_queue=False, end_at_disabled_consumer=False, batch_size=None
    ):
        if not batch_size:
            batch_size = self.get_default_batch_size()

        try:
            collection = Collection.objects.get(name=self.collection_name)
        except Collection.DoesNotExist:
            print(
                f"\n\tNo collection exists with the name '{self.collection_name}'."
                "\n\tDid you forget to create it? Run the command below to create it:"
                f"\n\tpython manage.py add_collection {self.collection_name}\n"
            )
            return

        while True:
            collection.refresh_from_db()
            if not collection.consumer_enabled:
                if end_at_disabled_consumer:
                    break  # For testing purposes
                sleep(10)
                continue

            with transaction.atomic():
                # This locks N records and iterates over them.
                # Parallel workers simply lock the next N records
                # Quote from https://www.postgresql.org/docs/11/sql-select.html :
                # "If a LIMIT is used, locking stops once enough rows have been
                # returned to satisfy the limit"
                messages = (
                    Message.objects.for_collection(collection)
                    .not_consumed()
                    .order_by("created_at")
                    .select_for_update(skip_locked=True)[:batch_size]
                )

                num_messages = messages.count()
                if num_messages > 0:
                    self.consume_iterator(messages.iterator())

                if num_messages < batch_size:
                    if end_at_empty_queue:
                        break  # For testing purposes
                    sleep(1)
