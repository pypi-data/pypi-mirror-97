
from concurrent.futures import ThreadPoolExecutor
from time import sleep

from azure.core.exceptions import ResourceExistsError, HttpResponseError
from azure.storage.blob import BlobServiceClient

from remotedict.azure.index.azure_index import AzureIndex
from remotedict.exceptions.item_locked_exception import ItemLockedException
from remotedict.utils.serialization import serialize, unserialize


class AzureDictionary:

    def __init__(self, connection_string, container_name, folder_name, background_pool_size=16):
        self._service_client = BlobServiceClient.from_connection_string(connection_string)
        self._container_name = container_name
        self._folder_name = folder_name
        self._container = self._service_client.get_container_client(container_name)

        try:
            self._container.create_container()
        except ResourceExistsError:
            pass

        self._index = AzureIndex(self._container.get_blob_client(f"index/{folder_name}/main_index"))
        self._background = ThreadPoolExecutor(background_pool_size)
        self._name_prefix = "default/" if folder_name is None else folder_name + "/"
        self._leases = {}

    @property
    def index(self):
        return self._index

    def lock_item(self, item, duration=15, wait=True):
        """
        Locks an item for the given duration in seconds.

        This ensures that no other process can ever lock this same item while it is locked, effectively "reserving" the property of the item.

        Note that the item can still be read by other processes, but they cannot modify or lock it.

        :param item:
            Item to block

        :param duration:
            Duration in seconds of the lock

        :param wait:
            Waits for the lock to be released (in case lease was acquired by other process)
        """
        item_index = self.index.get(item)
        done = False

        while not done:

            try:
                try:
                    self._leases[item_index] = self._container.get_blob_client(item_index).acquire_lease(duration)
                    done = True

                except HttpResponseError as e:
                    if 'There is already a lease present' in str(e):
                        raise ItemLockedException("Item is already locked by other process", item)
                    else:
                        raise e

            except ItemLockedException as e:
                if wait:
                    sleep(0.5)
                else:
                    raise e from None

    def unlock_item(self, item):
        item_index = self.index.get(item)
        self._leases[item_index].release()
        del self._leases[item_index]

    def __delitem__(self, item):
        self.index.remove(item)

    def __setitem__(self, item, value):
        if type(item) is not list:
            item = [item]
            value = [value]

        real_items = [self._name_prefix + i for i in item]
        self._background.submit(self._index.insert, item, real_items)

        results = [self._background.submit(self._put_single_item, i, v) for i, v in zip(real_items, value)]
        results = [result.result() for result in results]

    def __getitem__(self, item):
        was_single_item = type(item) is not list
        items = [item] if was_single_item else item

        # Obtenemos los índices de los ítems
        indexes = self.index.get(items).to_numpy()

        results = [self._background.submit(self._get_single_item, i) for i in indexes]

        results = [result.result() for result in results]

        if len(results) == 1 and was_single_item:
            results = results[0]

        return results

    def _put_single_item(self, item, value):
        blob_client = self._container.get_blob_client(item)
        blob_client.upload_blob(serialize(value), overwrite=True, lease=self._leases.get(item, None))

    def _get_single_item(self, item):
        blob_client = self._container.get_blob_client(item)
        return unserialize(blob_client.download_blob().readall())

    def __iter__(self):
        index = self.index
        yield from index.keys

    def keys(self):
        return list(self)

    def values(self):
        for item in self:
            yield self[item]

    def items(self):
        for k in self:
            yield k, self[k]

    def clear(self):
        self.index.clear()

    def __len__(self):
        index = self._index
        return len(index)

    def __str__(self):
        return f"Azure Blob Storage. Container: \"{self._container_name}\"; Folder: \"{self._folder_name}\"; Num elements: {len(self)}"

    def __repr__(self):
        return str(self)
