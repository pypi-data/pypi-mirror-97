import pandas as pd
import time

from threading import Lock
from azure.core.exceptions import ResourceExistsError

from remotedict.utils.serialization import unserialize, serialize


class AzureIndex:
    def __init__(self, index_file, autocreate=True):
        self._index_file = index_file
        self._content = None
        self._etag = None
        self._lease = None
        self._lease_count = 0
        self._lock = Lock()

        if autocreate and not self._index_file.exists():
            self._content = pd.DataFrame({"name": []}, index=pd.Index([], name="index"))
            self.write(self._content)

    def __enter__(self):
        with self._lock:
            while self._lease is None:
                try:
                    self._lease = self._index_file.acquire_lease(15)
                except ResourceExistsError:
                    time.sleep(0.1)

            self._lease_count += 1
        return self

    def __len__(self):
        return self.read().shape[0]

    def clear(self):
        with self:
            self._content = pd.DataFrame({"name": []}, index=pd.Index([], name="index"))
            self.write(self._content)

    def __exit__(self, t, value, traceback):
        with self._lock:
            if self._lease is not None:
                self._lease.release()

                self._lease_count -= 1

            if self._lease_count == 0:
                self._lease = None

    def read(self):
        remote_etag = self._index_file.get_blob_properties()['etag']

        if remote_etag != self._etag:
            self._content = unserialize(self._index_file.download_blob().readall())
            self._etag = remote_etag

        return self._content

    def insert(self, index, real_index):

        with self:
            index_df = self.read()
            index_to_join = pd.DataFrame({"name": real_index}, index=pd.Index(index, name="index"))
            joined_index_df = pd.concat([index_df, index_to_join], axis=1)

            if len(joined_index_df.columns) > 1:
                ix = ~joined_index_df.iloc[:, 1].isna()
                joined_index_df.loc[ix] = index_to_join

            index_df = joined_index_df.iloc[:, 0]
            self._content = index_df
            self.write(index_df)

    def remove(self, index):
        with self:
            index_df = self.read()
            index_df.drop(index, inplace=True)
            self.write(index_df)

    @property
    def keys(self):
        return self.read().index

    def get(self, index):
        index_df = self.read()

        try:
            real_indexes = index_df.loc[index]

        except KeyError as e:
            missing_keywords = e.args[0].split("The following labels were missing: Index([")[1].split(
                "], dtype='object', name='index'). See https://")[0].replace("'", "").split(", ")
            error = KeyError(f'Missing keywords: {missing_keywords}')
            error.missing_keywords = {'missing_keywords': missing_keywords}
            raise error from None

        return real_indexes

    def write(self, index_df):
        self._etag = self._index_file.upload_blob(serialize(index_df), overwrite=True, lease=self._lease)['etag']

    def __str__(self):
        return str(self.read())

    def __repr__(self):
        return self.read().__repr__()
