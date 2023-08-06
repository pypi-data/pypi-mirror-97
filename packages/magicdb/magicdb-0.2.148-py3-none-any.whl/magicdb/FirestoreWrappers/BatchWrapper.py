import magicdb
from magicdb.database import db
from magicdb.utils.Serverless.span import safe_span
import threading
from pydantic import BaseModel
from enum import Enum
from typing import List, Dict, Tuple, Any

MAX_BATCH_SIZE = 400


class OperationType(str, Enum):
    SET = "set"
    UPDATE = "update"
    DELETE = "delete"


class BatchCommand(BaseModel):
    operation_type: OperationType
    args: tuple = ()
    kwargs: dict = {}


class BatchWrapper:
    def __init__(self, *args, max_batch_size=MAX_BATCH_SIZE, **kwargs):
        self.max_batch_size = max_batch_size
        if self.max_batch_size != MAX_BATCH_SIZE:
            print(f"{self.max_batch_size=}")
        self._init_args: tuple = args
        self._init_kwargs: dict = kwargs
        self._batch_commands: List[BatchCommand] = []

    def set(self, *args, **kwargs):
        self._batch_commands.append(
            BatchCommand(operation_type=OperationType.SET, args=args, kwargs=kwargs)
        )

    def update(self, *args, **kwargs):
        self._batch_commands.append(
            BatchCommand(operation_type=OperationType.UPDATE, args=args, kwargs=kwargs)
        )

    def delete(self, *args, **kwargs):
        self._batch_commands.append(
            BatchCommand(operation_type=OperationType.DELETE, args=args, kwargs=kwargs)
        )

    @staticmethod
    def commit_batch(batch, i=None):
        with safe_span("batch_commit"):
            batch.commit()
            print(f"Batch number {'?' if i is None else i} committed!")

    def commit_batch_async(self, batch, i=None):
        t = threading.Thread(target=self.commit_batch, args=(batch, i))
        t.start()
        return t

    def commit_batches(self, batches: List[magicdb.WriteBatch], sync=False):
        if not sync:
            ts = [self.commit_batch_async(batch, i) for i, batch in enumerate(batches)]
            [t.join() for t in ts]
        else:
            [self.commit_batch(batch, i) for i, batch in enumerate(batches)]

    def commit(self, sync=False):
        batches: List[magicdb.WriteBatch] = self.make_batches()
        self.commit_batches(batches=batches, sync=sync)

    def commit_async(self, *args, **kwargs):
        t = threading.Thread(target=self.commit, args=args, kwargs=kwargs)
        t.start()
        return t

    def make_batches(self) -> List[magicdb.WriteBatch]:
        chunks = self.chunk_array(
            arr=self._batch_commands, chunk_size=self.max_batch_size
        )
        batches: List[magicdb.WriteBatch] = []
        for i, chunk in enumerate(chunks):
            batch: magicdb.WriteBatch = db.conn.batch(
                *self._init_args, **self._init_kwargs
            )
            for batch_command in chunk:
                batch_command: BatchCommand
                if batch_command.operation_type == OperationType.SET:
                    batch.set(*batch_command.args, **batch_command.kwargs)
                elif batch_command.operation_type == OperationType.UPDATE:
                    batch.update(*batch_command.args, **batch_command.kwargs)
                elif batch_command.operation_type == OperationType.DELETE:
                    batch.delete(*batch_command.args, **batch_command.kwargs)

            batches.append(batch)
        return batches

    @staticmethod
    def chunk_array(arr, chunk_size):
        return [arr[i : i + chunk_size] for i in range(0, len(arr), chunk_size)]
