Search.setIndex({"docnames": ["api", "apidoc/narrow_down.hash", "apidoc/narrow_down.scylladb", "apidoc/narrow_down.similarity_store", "apidoc/narrow_down.sqlite", "apidoc/narrow_down.storage", "changelog", "index", "license", "narrow_down", "readme", "user_guide/basic_usage", "user_guide/configuration_of_indexing_and_search", "user_guide/storage_backends"], "filenames": ["api.rst", "apidoc/narrow_down.hash.rst", "apidoc/narrow_down.scylladb.rst", "apidoc/narrow_down.similarity_store.rst", "apidoc/narrow_down.sqlite.rst", "apidoc/narrow_down.storage.rst", "changelog.md", "index.rst", "license.rst", "narrow_down.rst", "readme.md", "user_guide/basic_usage.md", "user_guide/configuration_of_indexing_and_search.md", "user_guide/storage_backends.md"], "titles": ["API Documentation", "narrow_down.hash module", "narrow_down.scylladb module", "narrow_down.similarity_store module", "narrow_down.sqlite module", "narrow_down.storage module", "Changelog", "Narrow Down - Efficient near-duplicate search", "Apache Software License 2.0", "narrow_down package", "Narrow Down - Efficient near-duplicate search", "Basic Usage", "Configuration of Indexing and Search", "Storage Backends"], "terms": {"inform": 0, "specif": [0, 8], "function": [0, 1, 3, 6, 7, 10, 11], "class": [0, 1, 2, 3, 4, 5, 6, 11, 13], "method": [0, 2, 3, 4, 5, 6, 11, 12, 13], "narrow_down": [0, 6, 11, 12, 13], "packag": [0, 7, 10, 11], "hash": [0, 2, 4, 5, 6, 7, 10, 12], "modul": [0, 7, 10], "scylladb": [0, 6, 7, 10], "similarity_stor": [0, 11, 12, 13], "sqlite": [0, 2, 6, 7, 10], "storag": [0, 2, 3, 4, 6, 7, 10, 11], "gener": [1, 12, 13], "purpos": 1, "hashalgorithm": 1, "valu": [1, 2, 4, 5, 6, 12, 13], "sourc": [1, 2, 3, 4, 5], "base": [1, 2, 3, 4, 5, 6, 7, 10, 12, 13], "flag": [1, 5], "enum": [1, 13], "avail": [1, 3, 6, 7, 10, 12, 13], "algorithm": [1, 7, 10, 12], "murmur3_32bit": 1, "1": [1, 5, 12, 13], "xxhash_32bit": 1, "2": [1, 5, 12], "xxhash_64bit": 1, "4": [1, 5, 12], "": [1, 12, 13], "byte": [1, 2, 4, 5, 6], "int": [1, 2, 3, 4, 5], "calcul": [1, 6, 11, 12, 13], "32": 1, "bit": [1, 11], "murmur3": 1, "input": [1, 6, 11, 12, 13], "string": [1, 2, 3, 4, 5, 7, 10, 12, 13], "xxhash": 1, "64": 1, "backend": [2, 3, 4, 5, 6, 7, 10], "i": [2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13], "low": [2, 3, 12, 13], "latenc": 2, "distribut": [2, 6, 8, 13], "kei": [2, 4, 5, 6], "store": [2, 3, 4, 5, 6, 11, 12, 13], "compat": 2, "apach": [2, 13], "cassandra": [2, 6, 7, 10], "protocol": 2, "For": [2, 13], "detail": [2, 5, 13], "see": [2, 3, 8, 13], "http": [2, 7, 8, 10], "www": [2, 8], "com": [2, 7, 10], "scylladbstor": [2, 6, 13], "cluster_or_sess": 2, "keyspac": [2, 13], "table_prefix": [2, 6], "none": [2, 3, 4, 5, 13], "storagebackend": [2, 3, 4, 5, 13], "similaritystor": [2, 3, 4, 5, 6, 11, 12], "us": [2, 3, 5, 6, 7, 8, 10, 11], "paramet": [2, 3, 4, 5, 6, 7, 10, 12], "union": [2, 3], "cluster": [2, 13], "session": [2, 6, 13], "str": [2, 3, 4, 5], "__init__": [2, 3, 4, 5, 6], "creat": [2, 3, 4, 5, 6, 7, 10, 11, 12, 13], "new": [2, 3, 4, 5, 6, 13], "empti": [2, 4, 5, 6, 13], "connect": [2, 4, 13], "an": [2, 3, 4, 5, 6, 7, 8, 10, 11, 13], "exist": [2, 3, 4, 5, 6, 13], "databas": [2, 4, 5, 6, 7, 10, 13], "can": [2, 3, 5, 6, 7, 10, 11, 12, 13], "object": [2, 3, 4, 5, 6, 11, 13], "name": [2, 3, 5, 12, 13], "option": [2, 3, 4, 5, 6, 12, 13], "A": [2, 3, 4, 5, 6, 11, 12, 13], "prefix": 2, "all": [2, 3, 4, 5, 6, 7, 10, 11, 12, 13], "tabl": [2, 4, 6, 13], "rais": [2, 3, 4, 5], "valueerror": [2, 3], "when": [2, 3, 6, 7, 10, 13], "invalid": 2, "return": [2, 3, 4, 5, 11, 12, 13], "type": [2, 3, 4, 5, 12], "async": [2, 3, 4, 5], "initi": [2, 3, 4, 5, 6, 13], "file": [2, 4, 5, 6, 8, 13], "self": [2, 4, 5, 6], "insert_set": [2, 4, 5], "set": [2, 3, 4, 5, 6, 13], "pair": [2, 4, 5, 12], "query_set": [2, 4, 5], "queri": [2, 3, 4, 5, 6, 12, 13], "given": [2, 3, 4, 5, 12, 13], "The": [2, 3, 4, 5, 6, 7, 10, 11, 12, 13], "identifi": [2, 3, 4, 5, 13], "If": [2, 3, 4, 5, 7, 10, 13], "doe": [2, 3, 4, 5], "uniniti": [2, 4, 5], "driverexcept": 2, "In": [2, 3, 4, 5, 7, 10, 12, 13], "case": [2, 3, 4, 6, 12, 13], "fail": [2, 4], "ani": [2, 4, 5, 8, 11], "reason": [2, 4], "insert_docu": [2, 4, 5], "document": [2, 3, 4, 5, 6, 7, 10, 12, 13], "document_id": [2, 3, 4, 5, 11], "add": [2, 4, 5], "data": [2, 3, 4, 5, 6, 7, 10, 11, 13], "its": [2, 4, 5], "id": [2, 3, 4, 5, 13], "query_docu": [2, 4, 5, 6], "get": [2, 4, 5, 13], "belong": [2, 4, 5], "thi": [2, 3, 4, 5, 6, 7, 8, 10, 11, 13], "under": [2, 3, 4, 5, 8], "keyerror": [2, 3, 4, 5], "multipl": [2, 4, 5, 6, 7, 10, 13], "list": [2, 3, 4, 5, 12], "which": [2, 3, 4, 5, 6, 11, 12, 13], "wa": [2, 3, 4, 5, 6, 7, 10, 12], "found": [2, 3, 4, 5, 12], "least": [2, 3, 4, 5, 11], "one": [2, 4, 5, 6, 12, 13], "remove_docu": [2, 4, 5], "remov": [2, 3, 4, 5], "from": [2, 3, 4, 5, 6, 11, 12], "add_document_to_bucket": [2, 4, 5], "bucket_id": [2, 4, 5], "document_hash": [2, 4, 5], "link": [2, 4, 5], "bucket": [2, 4, 5], "query_ids_from_bucket": [2, 4, 5], "certain": [2, 4, 5], "iter": [2, 4, 5], "remove_id_from_bucket": [2, 4, 5], "high": [3, 7, 10], "level": [3, 5, 6, 9, 11, 12], "api": [3, 7, 10, 11, 13], "index": [3, 6, 7, 10, 13], "retriev": [3, 13], "fuzzi": [3, 5, 12, 13], "search": [3, 5, 11, 13], "classmethod": [3, 5], "storage_level": [3, 5, 11, 13], "storagelevel": [3, 5, 11, 13], "minim": [3, 5, 13], "token": [3, 6, 11], "max_false_negative_proba": [3, 12], "0": [3, 11, 12, 13], "05": [3, 12], "max_false_positive_proba": [3, 12], "similarity_threshold": [3, 11, 12], "75": [3, 11, 12], "persist": [3, 5, 13], "per": [3, 13], "default": [3, 5, 12, 13], "memori": [3, 6, 7, 10, 12, 13], "granular": 3, "intern": [3, 5, 6, 12, 13], "mechan": 3, "noth": 3, "than": [3, 6, 13], "ar": [3, 6, 11, 12, 13], "callabl": 3, "collect": [3, 6, 7, 10, 12], "split": [3, 11, 12], "smaller": 3, "part": [3, 13], "e": [3, 5, 12, 13], "g": [3, 5, 12, 13], "mai": [3, 8, 12, 13], "word": [3, 6], "charact": [3, 6, 11], "n": [3, 6], "gram": [3, 6, 11], "3": [3, 11, 12], "built": [3, 13], "pass": [3, 12, 13], "word_ngram": [3, 12], "enabl": 3, "ngram": 3, "_token": [3, 12], "char_ngram": [3, 6, 11, 12], "c": [3, 8, 12, 13], "It": [3, 7, 10, 12, 13], "also": [3, 5, 6, 7, 10, 11, 12, 13], "possibl": [3, 5, 6, 12, 13], "custom": 3, "itself": 3, "need": [3, 5, 7, 10, 13], "taken": 3, "care": [3, 13], "specifi": [3, 5], "same": [3, 13], "again": [3, 6, 13], "save": [3, 6], "re": [3, 13], "float": 3, "target": [3, 11, 12], "probabl": [3, 12], "fals": [3, 6, 12, 13], "neg": [3, 12], "higher": [3, 5, 11, 12], "decreas": 3, "risk": 3, "find": [3, 6, 7, 10, 12], "similar": [3, 6, 11, 12], "lead": [3, 6], "slower": [3, 13], "process": [3, 12, 13], "more": [3, 6, 12, 13], "consumpt": [3, 6, 12], "posit": [3, 6, 12], "realiti": 3, "minimum": [3, 6, 12], "jaccard": [3, 11, 12], "threshold": [3, 11, 12], "two": [3, 12, 13], "being": 3, "cannot": [3, 13], "alreadi": 3, "load_from_storag": [3, 13], "load": 3, "must": 3, "have": [3, 5, 6, 11, 12, 13], "been": 3, "befor": [3, 12], "origin": 3, "init": [3, 6], "typeerror": [3, 6], "miss": 3, "corrupt": 3, "deseri": [3, 5, 6], "insert": [3, 5, 6, 11, 12, 13], "exact_part": [3, 5, 6, 13], "assign": 3, "exact": [3, 13], "match": [3, 5, 7, 10, 12, 13], "addit": [3, 5, 13], "payload": [3, 5, 13], "togeth": [3, 5, 13], "remove_by_id": [3, 6], "check_if_exist": 3, "structur": [3, 5, 6, 13], "bool": 3, "toolowstoragelevel": [3, 5], "too": 3, "fingerprint": [3, 5, 13], "note": [3, 13], "onli": [3, 5, 6, 7, 10, 13], "usabl": [3, 7, 10], "valid": [3, 6], "item": [3, 12], "should": [3, 5, 12, 13], "exactli": [3, 5, 13], "whether": 3, "result": [3, 5, 6, 12, 13], "realli": 3, "abov": [3, 12], "done": [3, 6], "otherwis": [3, 6], "storeddocu": [3, 5, 6, 11], "element": 3, "estim": [3, 7, 10, 12], "query_top_n": [3, 6], "top": [3, 9], "number": [3, 6, 12], "most": [3, 6], "like": [3, 6, 7, 10, 12], "probabilist": 3, "assum": 3, "candid": 3, "thei": [3, 5, 12], "But": [3, 11, 13], "actual": [3, 5, 12, 13], "themselv": 3, "might": 3, "differ": [3, 6, 7, 10, 11, 12, 13], "howev": 3, "true": [3, 11], "order": [3, 6, 13], "correct": 3, "becaus": [3, 6, 13], "compar": [3, 6, 7, 10], "each": [3, 7, 10], "other": [3, 7, 10, 11, 12, 13], "sqlitestor": [4, 13], "db_filenam": 4, "partit": [4, 6], "128": 4, "sqlite3": 4, "operationalerror": 4, "interfac": [5, 6, 7, 10, 13], "except": [5, 6, 8], "featur": 5, "necessari": [5, 13], "perform": [5, 6, 7, 10, 13], "minhash": [5, 6, 7, 10, 12, 13], "whole": [5, 11, 13], "full": [5, 7, 10, 12, 13], "7": 5, "everyth": 5, "repres": [5, 13], "oper": [5, 6, 13], "alia": 5, "ndarrai": 5, "dtype": 5, "uint32": 5, "id_": [5, 11, 13], "combin": 5, "field": 5, "distinguish": 5, "ident": [5, 6], "content": 5, "unprocess": 5, "sentenc": [5, 12], "serial": [5, 6, 13], "static": 5, "doc": [5, 11], "without": [5, 6, 8, 11, 12, 13], "attribut": [5, 13], "copi": [5, 8], "left": 5, "out": [5, 6, 13], "leav": 5, "so": [5, 11, 13], "abc": 5, "inmemorystor": [5, 6], "rust": [5, 6, 7, 10], "implement": [5, 6, 7, 10, 13], "rustmemorystor": 5, "messagepack": [5, 6, 13], "somewher": 5, "to_fil": [5, 13], "file_path": 5, "path": 5, "msgpack": [5, 13], "from_fil": [5, 13], "notabl": 6, "project": 6, "format": [6, 13], "keep": 6, "adher": 6, "semant": [6, 12], "version": [6, 8], "do": [6, 13], "now": [6, 11], "leverag": [6, 13], "economi": 6, "scale": [6, 7, 10], "onc": 6, "public": 6, "librari": 6, "declar": 6, "stabl": 6, "henc": 6, "readi": [6, 11], "fulli": [6, 11], "give": 6, "speedup": 6, "2x": 6, "lsh": [6, 7, 10, 12], "instead": [6, 13], "run": [6, 11], "concurr": [6, 13], "wrong": 6, "preced": 6, "incorrect": 6, "pars": 6, "argument": [6, 13], "pad": [6, 12], "improv": 6, "63": 6, "led": 6, "62": 6, "permut": [6, 12], "avoid": 6, "artifact": 6, "describ": [6, 12], "61": 6, "accept": 6, "data_typ": 6, "were": 6, "move": 6, "call": [6, 11], "time": [6, 11, 13], "issu": 6, "counter": 6, "typehint": 6, "broke": 6, "mypi": 6, "check": 6, "direct": 6, "peak": 6, "de": 6, "via": 6, "detour": 6, "python": [6, 7, 10], "top_n_queri": 6, "allow": [6, 11, 13], "limit": [6, 8, 13], "offer": [6, 7, 10, 13], "score": 6, "factori": 6, "coroutin": [6, 11], "first": [6, 11, 13], "make": [6, 13], "usag": [6, 13], "straight": 6, "forward": 6, "longer": [6, 12], "dictionari": 6, "rather": [6, 11, 13], "extens": [6, 7, 10], "reduc": [6, 7, 10], "footprint": [6, 13], "lot": [6, 12], "wai": [6, 12, 13], "db": 6, "contain": [6, 12], "user": [6, 7, 10, 13], "doesn": 6, "t": [6, 7, 10, 12], "elsewher": 6, "protobuf": 6, "increas": 6, "speed": 6, "where": 6, "reus": 6, "great": [6, 11], "benefit": 6, "integ": 6, "overflow": 6, "qualiti": 6, "depend": [6, 12, 13], "effect": [6, 12, 13], "max_uint32": 6, "prime": 6, "modulo": 6, "asyncsqlitestor": 6, "turn": 6, "aiosqlit": 6, "reli": 6, "guarante": 6, "tri": [6, 12], "write": [6, 8, 13], "lock": 6, "thrown": 6, "As": [6, 11], "anywai": 6, "wors": 6, "expect": 6, "take": [6, 13], "optim": [6, 7, 10], "disk": [6, 13], "synchron": [6, 11], "asynchron": [6, 11, 13], "ci": 6, "url": 6, "test": 6, "pypi": 6, "therefor": [6, 13], "build": 6, "system": [6, 13], "maturin": 6, "releas": 6, "flexibl": [7, 10, 13], "easi": [7, 10, 13], "veri": [7, 10, 11, 13], "larg": [7, 10, 12], "dataset": [7, 10, 12], "o": [7, 10], "n\u00b2": [7, 10], "problem": [7, 10], "linear": [7, 10], "approxim": [7, 10, 12], "local": [7, 10, 12, 13], "sensit": [7, 10, 12], "github": [7, 10], "repo": [7, 10], "chr1st1ank": [7, 10], "git": [7, 10], "io": [7, 10], "thank": [7, 10], "nativ": [7, 10], "autom": [7, 10], "tune": [7, 10, 12], "work": [7, 10, 11], "exchang": [7, 10], "current": [7, 10], "defin": [7, 10, 11, 13], "small": [7, 10], "asyncio": [7, 10, 11], "pip": [7, 10], "some": [7, 10, 11, 12, 13], "heavier": [7, 10], "pylsh": [7, 10], "good": [7, 10, 11], "classic": [7, 10], "scheme": [7, 10], "cython": [7, 10], "you": [7, 8, 10], "don": [7, 10, 12], "choic": [7, 10, 12], "datasketch": [7, 10], "interest": [7, 10], "sketch": [7, 10], "cardin": [7, 10, 12], "k": [7, 10], "nearest": [7, 10], "neighbour": [7, 10], "highli": [7, 10], "well": [7, 10, 11], "rich": [7, 10], "milvu": [7, 10], "stack": [7, 10], "vector": [7, 10], "approach": [7, 10], "fast": [7, 10, 13], "appli": [7, 10, 12], "text": [7, 10, 12, 13], "embed": [7, 10], "word2vec": [7, 10], "bert": [7, 10], "cookiecutt": [7, 10], "fedejaur": [7, 10], "modern": [7, 10], "pypackag": [7, 10], "templat": [7, 10], "copyright": 8, "2021": 8, "christian": 8, "krudewig": 8, "complianc": 8, "obtain": 8, "org": 8, "unless": 8, "requir": 8, "applic": [8, 13], "law": 8, "agre": 8, "AS": 8, "basi": 8, "warranti": 8, "OR": 8, "condit": 8, "OF": 8, "kind": [8, 13], "either": [8, 13], "express": 8, "impli": 8, "languag": 8, "govern": 8, "permiss": 8, "narrow": [9, 12, 13], "down": [9, 12, 13], "increment": 11, "both": [11, 13], "demonstr": [11, 12], "section": 11, "below": [11, 12, 13], "That": 11, "mean": 11, "relev": 11, "directli": [11, 13], "await": [11, 12, 13], "code": [11, 13], "littl": 11, "overhead": 11, "establish": 11, "event": 11, "loop": 11, "better": [11, 13], "often": 11, "chain": 11, "block": 11, "show": [11, 12, 13], "how": [11, 12, 13], "configur": [11, 13], "here": 11, "we": [11, 13], "choos": 11, "want": 11, "To": [11, 12], "preprocess": 11, "import": [11, 12, 13], "nd": 11, "fill": 11, "exampl": [11, 12, 13], "review": 11, "popular": 11, "oatmeal": 11, "cooki": 11, "strings_to_index": 11, "delici": 11, "anytim": 11, "dai": 11, "quick": 11, "simpl": [11, 13], "healthi": 11, "snack": 11, "kiddo": 11, "quaker": 11, "soft": 11, "bake": 11, "yummi": 11, "wow": 11, "chewi": 11, "bomb": 11, "awesom": 11, "home": 11, "tast": 11, "fuss": 11, "grain": 11, "amaz": 11, "homemad": 11, "love": 11, "especi": [11, 13], "kid": 11, "my": 11, "them": 11, "lunchbox": 11, "stapl": 11, "deliou": 11, "over": [11, 13], "product": 11, "yum": 11, "foil": 11, "packet": 11, "handi": 11, "total": 11, "enumer": 11, "lower": 11, "execut": [11, 13], "search_result": 11, "13": 11, "24": 11, "20": 11, "everi": [11, 12, 13], "There": 11, "between": [11, 12], "train": 11, "predict": 11, "phase": 11, "42": 11, "further": 12, "handl": 12, "less": 12, "benefici": 12, "descript": 12, "length": 12, "let": 12, "look": 12, "coupl": 12, "wuzzi": 12, "bear": 12, "had": 12, "hair": 12, "wasn": 12, "he": 12, "def": 12, "show_first": 12, "print": 12, "6": 12, "With": [12, 13], "fu": 12, "air": 12, "5": 12, "uzzi": 12, "f": 12, "zzy": 12, "w": 12, "fuz": 12, "y": 12, "asn": 12, "produc": 12, "represent": 12, "uniqu": [12, 13], "harder": 12, "On": [12, 13], "hand": [12, 13], "sens": 12, "common": [12, 13], "extrem": 12, "almost": 12, "frequent": 12, "webpag": 12, "newspap": 12, "articl": 12, "shorter": 12, "short": 12, "address": 12, "follow": [12, 13], "final": [12, 13], "raw_str": 12, "comma": 12, "leskovec": 12, "rajaraman": 12, "ullman": 12, "mine": 12, "massiv": 12, "chapter": 12, "heurist": 12, "bodi": 12, "ones": 12, "happen": 12, "condens": 12, "share": 12, "although": 12, "automat": 12, "row": 12, "band": 12, "reach": 12, "cpu": 12, "abstract": 13, "start": 13, "lifetim": 13, "bound": 13, "chang": 13, "storage_backend": 13, "dataclass": 13, "rest": 13, "mostli": 13, "usecas": 13, "prefer": 13, "sometim": 13, "enough": 13, "just": 13, "abl": 13, "second": 13, "later": 13, "simplest": 13, "fastest": 13, "access": 13, "within": 13, "hold": 13, "effici": 13, "binari": 13, "advantag": 13, "setup": 13, "disadvantag": 13, "size": 13, "physic": 13, "tmp": 13, "reimplement": 13, "beyond": 13, "boundari": 13, "singl": 13, "across": 13, "servic": 13, "server": 13, "cassandra_clust": 13, "contact_point": 13, "localhost": 13, "port": 13, "9042": 13, "IF": 13, "NOT": 13, "test_k": 13, "WITH": 13, "replic": 13, "simplestrategi": 13, "replication_factor": 13, "AND": 13, "durable_writ": 13, "cassandra_storag": 13, "manag": 13, "outsid": 13, "after": 13, "anymor": 13, "support": 13, "amount": 13, "exce": 13, "fairli": 13, "linux": 13, "cach": 13, "window": 13, "slow": 13, "commit": 13, "flush": 13, "documentend": 13, "extern": 13, "reopen": 13, "continu": 13, "design": 13, "plug": 13, "box": 13, "inherit": 13, "serv": 13, "unsupport": 13, "effort": 13, "typic": 13, "100": 13, "200": 13, "line": 13}, "objects": {"": [[9, 0, 0, "-", "narrow_down"]], "narrow_down": [[1, 0, 0, "-", "hash"], [2, 0, 0, "-", "scylladb"], [3, 0, 0, "-", "similarity_store"], [4, 0, 0, "-", "sqlite"], [5, 0, 0, "-", "storage"]], "narrow_down.hash": [[1, 1, 1, "", "HashAlgorithm"], [1, 3, 1, "", "murmur3_32bit"], [1, 3, 1, "", "xxhash_32bit"], [1, 3, 1, "", "xxhash_64bit"]], "narrow_down.hash.HashAlgorithm": [[1, 2, 1, "", "Murmur3_32bit"], [1, 2, 1, "", "Xxhash_32bit"], [1, 2, 1, "", "Xxhash_64bit"]], "narrow_down.scylladb": [[2, 1, 1, "", "ScyllaDBStore"]], "narrow_down.scylladb.ScyllaDBStore": [[2, 4, 1, "", "__init__"], [2, 4, 1, "", "add_document_to_bucket"], [2, 4, 1, "", "initialize"], [2, 4, 1, "", "insert_document"], [2, 4, 1, "", "insert_setting"], [2, 4, 1, "", "query_document"], [2, 4, 1, "", "query_documents"], [2, 4, 1, "", "query_ids_from_bucket"], [2, 4, 1, "", "query_setting"], [2, 4, 1, "", "remove_document"], [2, 4, 1, "", "remove_id_from_bucket"]], "narrow_down.similarity_store": [[3, 1, 1, "", "SimilarityStore"]], "narrow_down.similarity_store.SimilarityStore": [[3, 4, 1, "", "create"], [3, 4, 1, "", "insert"], [3, 4, 1, "", "load_from_storage"], [3, 4, 1, "", "query"], [3, 4, 1, "", "query_top_n"], [3, 4, 1, "", "remove_by_id"]], "narrow_down.sqlite": [[4, 1, 1, "", "SQLiteStore"]], "narrow_down.sqlite.SQLiteStore": [[4, 4, 1, "", "__init__"], [4, 4, 1, "", "add_document_to_bucket"], [4, 4, 1, "", "initialize"], [4, 4, 1, "", "insert_document"], [4, 4, 1, "", "insert_setting"], [4, 4, 1, "", "query_document"], [4, 4, 1, "", "query_documents"], [4, 4, 1, "", "query_ids_from_bucket"], [4, 4, 1, "", "query_setting"], [4, 4, 1, "", "remove_document"], [4, 4, 1, "", "remove_id_from_bucket"]], "narrow_down.storage": [[5, 5, 1, "", "Fingerprint"], [5, 1, 1, "", "InMemoryStore"], [5, 1, 1, "", "StorageBackend"], [5, 1, 1, "", "StorageLevel"], [5, 1, 1, "", "StoredDocument"], [5, 6, 1, "", "TooLowStorageLevel"]], "narrow_down.storage.InMemoryStore": [[5, 4, 1, "", "__init__"], [5, 4, 1, "", "add_document_to_bucket"], [5, 4, 1, "", "deserialize"], [5, 4, 1, "", "from_file"], [5, 4, 1, "", "insert_document"], [5, 4, 1, "", "insert_setting"], [5, 4, 1, "", "query_document"], [5, 4, 1, "", "query_ids_from_bucket"], [5, 4, 1, "", "query_setting"], [5, 4, 1, "", "remove_document"], [5, 4, 1, "", "remove_id_from_bucket"], [5, 4, 1, "", "serialize"], [5, 4, 1, "", "to_file"]], "narrow_down.storage.StorageBackend": [[5, 4, 1, "", "add_document_to_bucket"], [5, 4, 1, "", "initialize"], [5, 4, 1, "", "insert_document"], [5, 4, 1, "", "insert_setting"], [5, 4, 1, "", "query_document"], [5, 4, 1, "", "query_documents"], [5, 4, 1, "", "query_ids_from_bucket"], [5, 4, 1, "", "query_setting"], [5, 4, 1, "", "remove_document"], [5, 4, 1, "", "remove_id_from_bucket"]], "narrow_down.storage.StorageLevel": [[5, 2, 1, "", "Document"], [5, 2, 1, "", "Fingerprint"], [5, 2, 1, "", "Full"], [5, 2, 1, "", "Minimal"]], "narrow_down.storage.StoredDocument": [[5, 2, 1, "", "data"], [5, 4, 1, "", "deserialize"], [5, 2, 1, "", "document"], [5, 2, 1, "", "exact_part"], [5, 2, 1, "", "fingerprint"], [5, 2, 1, "", "id_"], [5, 4, 1, "", "serialize"], [5, 4, 1, "", "without"]]}, "objtypes": {"0": "py:module", "1": "py:class", "2": "py:attribute", "3": "py:function", "4": "py:method", "5": "py:data", "6": "py:exception"}, "objnames": {"0": ["py", "module", "Python module"], "1": ["py", "class", "Python class"], "2": ["py", "attribute", "Python attribute"], "3": ["py", "function", "Python function"], "4": ["py", "method", "Python method"], "5": ["py", "data", "Python data"], "6": ["py", "exception", "Python exception"]}, "titleterms": {"api": 0, "document": [0, 11], "narrow_down": [1, 2, 3, 4, 5, 9], "hash": 1, "modul": [1, 2, 3, 4, 5], "scylladb": [2, 13], "similarity_stor": 3, "sqlite": [4, 13], "storag": [5, 13], "changelog": 6, "unreleas": 6, "1": 6, "0": [6, 8], "2022": 6, "05": 6, "17": 6, "ad": [6, 11], "chang": 6, "fix": 6, "10": 6, "08": 6, "9": 6, "3": 6, "04": 6, "2": [6, 8], "03": 6, "29": 6, "25": 6, "13": 6, "8": 6, "02": 6, "23": 6, "7": 6, "06": 6, "6": 6, "01": 6, "remov": 6, "5": 6, "4": 6, "16": 6, "14": 6, "09": 6, "2021": 6, "12": 6, "30": 6, "narrow": [7, 10], "down": [7, 10], "effici": [7, 10], "duplic": [7, 10], "search": [7, 10, 12], "featur": [7, 10], "instal": [7, 10], "extra": [7, 10], "similar": [7, 10], "project": [7, 10], "credit": [7, 10], "apach": 8, "softwar": 8, "licens": 8, "packag": 9, "basic": 11, "usag": 11, "index": [11, 12], "queri": 11, "more": 11, "configur": 12, "token": 12, "word": 12, "n": 12, "gram": 12, "charact": 12, "choos": 12, "right": 12, "function": 12, "custom": [12, 13], "precis": 12, "set": 12, "backend": 13, "us": 13, "explicitli": 13, "specifi": 13, "load": 13, "similaritystor": 13, "from": 13, "storeddocu": 13, "level": 13, "inmemorystor": 13, "cassandra": 13}, "envversion": {"sphinx.domains.c": 2, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 6, "sphinx.domains.index": 1, "sphinx.domains.javascript": 2, "sphinx.domains.math": 2, "sphinx.domains.python": 3, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx.ext.intersphinx": 1, "sphinx.ext.viewcode": 1, "sphinx": 56}})