# Usage

## Basic Usage
To use narrow-down in a project:
```pycon
>>> import asyncio
>>> import narrow_down as nd
>>> from narrow_down.data_types import StoredDocument
>>> strings_to_index = [
...     "Delicious!",
...     "Great Anytime of Day!",
...     "Very good!",
...     "Quaker Oats Oatmeal Raisin Mom Voxbox Review Courtesy of Influenster",
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
>>> async def index_documents(documents):
...     similarity_store = nd.similarity_store.SimilarityStore(
...         storage_level=nd.data_types.StorageLevel.Document,
...         similarity_threshold=0.8,
...         tokenize="char_ngrams(5)",
...     )
...     await similarity_store.initialize()
...     for i, doc in enumerate(documents):
...         await similarity_store.insert(doc.lower(), document_id=i)
...     return similarity_store
...
>>> similarity_store = asyncio.run(index_documents(strings_to_index))

>>> strings_to_search = [
...     "Awesome cookies",
...     "Soft and Delicious",
...     "Loving every bit of it!",
...     "Awesome!",
...     "Like Homemade!",
... ]

```

Now that the some data is indexed we can search:
```pycon
>>> search_result = asyncio.run(similarity_store.query("Awesome cookies".lower()))
>>> search_result == [StoredDocument(id_=14, document="awesome cookies")]
True

>>> search_result = asyncio.run(similarity_store.query("So Delicious".lower()))
>>> search_result == []
True

>>> search_result = asyncio.run(similarity_store.query("Awesome!".lower()))
>>> search_result == [StoredDocument(id_=14, document="awesome cookies")]
True

>>> search_result = asyncio.run(similarity_store.query("Like Homemade!".lower()))
>>> search_result == [
...     StoredDocument(
...         id_=19,
...         document="good, but not homemade.",
...     )
... ]
True

>>> search_result = asyncio.run(similarity_store.query("Loving every bit of it!".lower()))
>>> search_result == []
True

```

Another one:
```pycon
>>> print(5)
5

```
