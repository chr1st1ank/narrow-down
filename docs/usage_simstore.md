# SimilarityStore

The class [SimilarityStore](narrow_down.similarity_store.SimilarityStore) allows to incrementally index and search documents.

The API is fully asynchronous. That means it can directly called with `await` from coroutine functions. But it can also be called from synchronous code with [asyncio.run()](asyncio.run). This creates a little overhead to establish an event loop. So it is better to call `run()` not to often but rather on a higher level in the call chain. 

## Indexing
The code block below shows how to create and configure a SimilarityStore() object. 

Here we choose the [StorageLevel](narrow_down.data_types.StorageLevel) `Document`, so that the whole document is stored in the `SimilarityStore` and can be returned from it. If the documents are large, also the default storage level `Minimal` can be used. Then the documents can be referenced to by id.

```pycon
>>> import asyncio
>>> import narrow_down as nd
>>> from narrow_down.data_types import StoredDocument

>>> similarity_store = nd.similarity_store.SimilarityStore(
...     storage_level=nd.data_types.StorageLevel.Document,
...     similarity_threshold=0.8,
...     tokenize="char_ngrams(5)",
... )
>>> asyncio.run(similarity_store.initialize()) is None
True

```

Now the object can be filled with documents. As example reviews of a popular oatmeal cookie are used:
```pycon
>>> strings_to_index = [
...     "Delicious!",
...     "Great Anytime of Day!",
...     "Very good!",
...     "Quick, simple HEALTHY snack for the kiddos!!!",
...     "Quaker Soft Baked Oatmeal Cookies",
...     "Yummy",
...     "Wow!!!!!",
...     "soft, chewy, yummy!",
...     "so soft and good",
...     "Chewy deliciousness",
...     "the bomb",
...     "Deliciousness",
...     "Yummy",
...     "awesome cookies",
...     "Home-baked taste without the fuss",
...     "Yummy Whole Grain Goodness!!!",
...     "Yummy",
...     "Amazing Cookies!",
...     "Good, but not homemade.",
...     "Very Good Oatmeal Cookie",
...     "Very good cookie",
...     "Love these cookies especially for the kids",
...     "My kids loved them.",
...     "Lunchbox or Work Staple",
...     "So Delious",
...     "Over-Packaged Product",
...     "yum",
...     "Great taste",
...     "Yummy!!",
...     "Well, the foil packet is handy...",
...     "TOTALLY DIFFERENT!",
... ]

>>> async def index_documents(similarity_store, documents):
...     for i, doc in enumerate(documents):
...         await similarity_store.insert(doc.lower(), document_id=i)

>>> asyncio.run(index_documents(similarity_store, strings_to_index))

```

Now that the some data is indexed, the SimilarityStore is ready to execute searches:
```pycon
>>> search_result = asyncio.run(similarity_store.query("Awesome cookies".lower()))
>>> search_result == [StoredDocument(id_=13, document="awesome cookies")]
True

>>> search_result = asyncio.run(similarity_store.query("So Delicious".lower()))
>>> search_result == []
True

>>> search_result = asyncio.run(similarity_store.query("Awesome!".lower()))
>>> search_result == [StoredDocument(id_=13, document="awesome cookies")]
True

>>> search_result = asyncio.run(similarity_store.query("Like Homemade!".lower()))
>>> search_result == [
...     StoredDocument(
...         id_=18,
...         document="good, but not homemade.",
...     )
... ]
True

>>> search_result = asyncio.run(similarity_store.query("Loving every bit of it!".lower()))
>>> search_result == []
True

```

More documents can be added at any time:
```pycon
>>> asyncio.run(similarity_store.insert('Good cookie', document_id=42))
42

```
