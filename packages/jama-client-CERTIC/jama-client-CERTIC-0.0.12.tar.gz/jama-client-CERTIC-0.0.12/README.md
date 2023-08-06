---
description: |
    API documentation for modules: jama_client.

lang: en

classoption: oneside
geometry: margin=1in
papersize: a4

linkcolor: blue
links-as-notes: true
...


    
# Module `jama_client` {#jama_client}

# Jama client library

## Installation

Use pip to install:

    pip install jama-client-CERTIC

## Quick start

    from jama_client import Client
    client = Client("https://acme.tld/rpc/", "secretapikeyhere")
    file_id = client.upload("/path/to/some/file.jpg")
    collection_id = client.add_collection("title of the collection")
    client.add_file_to_collection(file_id, collection_id)





    
## Classes


    
### Class `Client` {#jama_client.Client}




>     class Client(
>         endpoint: str,
>         api_key: str
>     )










    
#### Methods


    
##### Method `add_collection` {#jama_client.Client.add_collection}




>     def add_collection(
>         self,
>         title: str,
>         parent_id: int = None
>     ) ‑> Union[Dict, NoneType]


Create a new collection based on 'title'. If 'parent_id' is set,
will create new collection as child of parent. Otherwise, the new
collection is created at root.

Returns either the serialized new collection of null if parent does
not exist.

Example output:

```
{
    "id": 3,
    "title": "paintings",
    "resources_count": 0,
    "children_count": 0,
    "descendants_count": 0,
    "descendants_resources_count": 0,
    "parent": null,
    "children": null,
    "metas": [],
    "public_access": false,
    "tags": [],
}
```

    
##### Method `add_collection_from_path` {#jama_client.Client.add_collection_from_path}




>     def add_collection_from_path(
>         self,
>         path: str
>     ) ‑> List[Dict]


Will take take a path such as '/photos/arts/paintings/'
and build the corresponding hierarchy of collections. The hierarchy
is returned as a list of serialized collections.

Beware: Because the collections are serialized before their children,
all the children/descendants counts are set to 0.

Example output:

```
[
    {
        "id": 1,
        "title": "photos",
        "resources_count": 0,
        "children_count": 0,
        "descendants_count": 0,
        "descendants_resources_count": 0,
        "parent": null,
        "children": null,
        "metas": [],
        "public_access": false,
        "tags": [],
    },
    {
        "id": 2,
        "title": "arts",
        "resources_count": 0,
        "children_count": 0,
        "descendants_count": 0,
        "descendants_resources_count": 0,
        "parent": 1,
        "children": null,
        "metas": [],
        "public_access": false,
        "tags": [],
    },
    {
        "id": 3,
        "title": "paintings",
        "resources_count": 0,
        "children_count": 0,
        "descendants_count": 0,
        "descendants_resources_count": 0,
        "parent": 2,
        "children": null,
        "metas": [],
        "public_access": false,
        "tags": [],
    },
]
```

    
##### Method `add_file_to_collection` {#jama_client.Client.add_file_to_collection}




>     def add_file_to_collection(
>         self,
>         file_id: int,
>         collection_id: int
>     ) ‑> bool


DEPRECATED. Do not use. Will be removed later. Use add_resource_to_collection instead.

    
##### Method `add_meta_to_collection` {#jama_client.Client.add_meta_to_collection}




>     def add_meta_to_collection(
>         self,
>         collection_id: int,
>         meta_id: int,
>         meta_value: str
>     ) ‑> Union[int, bool]


Add a meta value to a collection given their ids.

    
##### Method `add_meta_to_file` {#jama_client.Client.add_meta_to_file}




>     def add_meta_to_file(
>         self,
>         file_id: int,
>         meta_id: int,
>         meta_value: str
>     ) ‑> Union[int, bool]


DEPRECATED. Do not use. Will be removed later. Use add_meta_to_resource instead.

    
##### Method `add_meta_to_resource` {#jama_client.Client.add_meta_to_resource}




>     def add_meta_to_resource(
>         self,
>         resource_id: int,
>         meta_id: int,
>         meta_value: str
>     ) ‑> Union[int, bool]


Add a meta value to a resource given their ids.

    
##### Method `add_metadata` {#jama_client.Client.add_metadata}




>     def add_metadata(
>         self,
>         title: str,
>         metas_set_id: int,
>         metadata_type_id: int = None
>     ) ‑> Union[int, bool]


Add a new metadata to metadata set.

Set optional 'metadata_type_id'

    
##### Method `add_metadataset` {#jama_client.Client.add_metadataset}




>     def add_metadataset(
>         self,
>         title: str
>     ) ‑> int


Create new metadata set from title.

    
##### Method `add_resource_to_collection` {#jama_client.Client.add_resource_to_collection}




>     def add_resource_to_collection(
>         self,
>         resource_id: int,
>         collection_id: int
>     ) ‑> bool


Add a resource to a collection given ids.

    
##### Method `add_tag_to_collection` {#jama_client.Client.add_tag_to_collection}




>     def add_tag_to_collection(
>         self,
>         tag_uid: str,
>         collection_id: int
>     ) ‑> bool


Add tag to a collection based on tag uid and collection id.

    
##### Method `add_tag_to_resource` {#jama_client.Client.add_tag_to_resource}




>     def add_tag_to_resource(
>         self,
>         tag_uid: str,
>         resource_id: int
>     ) ‑> bool


Add tag to a resource based on tag uid and resource id.

    
##### Method `advanced_search` {#jama_client.Client.advanced_search}




>     def advanced_search(
>         self,
>         search_terms: List[Dict]
>     ) ‑> Dict[str, List]


Performs a complex search using terms such as 'contains', 'is', 'does_not_contain'.

Multiple conditions can be added.

Example input:

```
[
    {"property": "title", "term": "contains", "value": "cherbourg"},
    {"meta": 123, "term": "is", "value": "35mm"},
    {"tags": ["PAINTINGS", "PHOTOS"]}
]
```

Example output:

```
{
    "collections": [],
    "resources": [
        {
        "id": 1,
        "title": "Cherbourg by night",
        "original_name": "cherbourg_by_night.jpg",
        "type": "image/jpeg",
        "hash": "0dd93a59aeaccfb6d35b1ff5a49bde1196aa90dfef02892f9aa2ef4087d8738e",
        "metas": null,
        "urls": [],
        "tags": [],
        }
    ]
}
```

    
##### Method `advanced_search_terms` {#jama_client.Client.advanced_search_terms}




>     def advanced_search_terms(
>         self
>     ) ‑> List[str]


Return terms conditions to be used in advanced search.

Example output:

```
[
    "is",
    "contains",
    "does_not_contain"
]
```

    
##### Method `ancestors_from_collection` {#jama_client.Client.ancestors_from_collection}




>     def ancestors_from_collection(
>         self,
>         collection_id: int,
>         include_self: bool = False
>     ) ‑> List[dict]


Get ancestors from collection id as a list of serialized collections.

If 'include_self' is true, will add the current collection at the begining.

Example output:

```
[
    {
        "id": 1,
        "title": "photos",
        "resources_count": 0,
        "children_count": 0,
        "descendants_count": 0,
        "descendants_resources_count": 0,
        "parent": null,
        "children": null,
        "metas": [],
        "public_access": false,
        "tags": [],
    },
    {
        "id": 2,
        "title": "arts",
        "resources_count": 0,
        "children_count": 0,
        "descendants_count": 0,
        "descendants_resources_count": 0,
        "parent": 1,
        "children": null,
        "metas": [],
        "public_access": false,
        "tags": [],
    },
    {
        "id": 3,
        "title": "paintings",
        "resources_count": 0,
        "children_count": 0,
        "descendants_count": 0,
        "descendants_resources_count": 0,
        "parent": 2,
        "children": null,
        "metas": [],
        "public_access": false,
        "tags": [],
    },
]
```

    
##### Method `ancestors_from_resource` {#jama_client.Client.ancestors_from_resource}




>     def ancestors_from_resource(
>         self,
>         resource_id: int
>     ) ‑> List[List[dict]]


Get ancestors from resource id as a list of serialized collections.

Example output:

```
[
    {
        "id": 1,
        "title": "photos",
        "resources_count": 0,
        "children_count": 0,
        "descendants_count": 0,
        "descendants_resources_count": 0,
        "parent": null,
        "children": null,
        "metas": [],
        "public_access": false,
        "tags": [],
    },
    {
        "id": 2,
        "title": "arts",
        "resources_count": 0,
        "children_count": 0,
        "descendants_count": 0,
        "descendants_resources_count": 0,
        "parent": 1,
        "children": null,
        "metas": [],
        "public_access": false,
        "tags": [],
    },
    {
        "id": 3,
        "title": "paintings",
        "resources_count": 0,
        "children_count": 0,
        "descendants_count": 0,
        "descendants_resources_count": 0,
        "parent": 2,
        "children": null,
        "metas": [],
        "public_access": false,
        "tags": [],
    },
]
```

    
##### Method `change_collection_meta_value` {#jama_client.Client.change_collection_meta_value}




>     def change_collection_meta_value(
>         self,
>         meta_value_id: int,
>         meta_value: str
>     ) ‑> bool


Change the value of a meta for a collection.

    
##### Method `change_resource_meta_value` {#jama_client.Client.change_resource_meta_value}




>     def change_resource_meta_value(
>         self,
>         meta_value_id: int,
>         meta_value: str
>     ) ‑> bool


Change the value of a meta for a resource

    
##### Method `collection` {#jama_client.Client.collection}




>     def collection(
>         self,
>         collection_id: int
>     ) ‑> Union[Dict, NoneType]


Get a particular collection given its id.

Example output:

```
{
    "id": 2,
    "title": "art works",
    "resources_count": 23,
    "children_count": 5,
    "descendants_count": 12,
    "descendants_resources_count": 58,
    "parent": 1,
    "children": None,
    "metas": [],
    "public_access": False,
    "tags": [],
}
```

    
##### Method `collections` {#jama_client.Client.collections}




>     def collections(
>         self,
>         parent_id: int = None,
>         recusive: bool = False
>     ) ‑> List[Dict]


Return the user's collections under the parent collection
specified by 'parent_id'. If 'parent_id' is null, will return
collections available at root. If 'recursive' is true, will
return all the descendants recusively in the 'children' key.
If recursive is false, 'children' is null.

Example output:

```
[
    {
        "id": 2,
        "title": "art works",
        "resources_count": 23,
        "children_count": 5,
        "descendants_count": 12,
        "descendants_resources_count": 58,
        "parent": 1,
        "children": None,
        "metas": [],
        "public_access": False,
        "tags": [],
    }
]
```

    
##### Method `delete_collection` {#jama_client.Client.delete_collection}




>     def delete_collection(
>         self,
>         collection_id: int,
>         recursive: bool = False
>     ) ‑> bool


Delete collection given its id.

Collection MUST be empty of any content (no children collections and no resources),
unless the 'recursive' parameter is set to True.

    
##### Method `delete_file` {#jama_client.Client.delete_file}




>     def delete_file(
>         self,
>         file_id: int
>     ) ‑> bool


DEPRECATED. Do not use. Will be removed later. Use delete_resource instead.

    
##### Method `delete_resource` {#jama_client.Client.delete_resource}




>     def delete_resource(
>         self,
>         resource_id: int
>     ) ‑> bool


Permanently delete a resource given its id.

    
##### Method `file` {#jama_client.Client.file}




>     def file(
>         self,
>         file_id: int
>     ) ‑> Union[Dict, NoneType]


DEPRECATED. Do not use. Will be removed later. Use resource instead.

    
##### Method `files` {#jama_client.Client.files}




>     def files(
>         self,
>         collection_id: int,
>         include_metas: bool = True
>     ) ‑> List[Dict]


DEPRECATED. Do not use. Will be removed later. Use resources instead.

    
##### Method `metadata` {#jama_client.Client.metadata}




>     def metadata(
>         self,
>         metadata_id: int
>     ) ‑> Union[Dict, NoneType]


Get one particular metadata given its id.

Example output:

```
{
    "id": 2,
    "title": "ICC_Profile:GrayTRC",
    "set_id": 1,
    "set_title": "exif metas",
    "rank": 1,
    "owner": "john",
}
```

    
##### Method `metadatas` {#jama_client.Client.metadatas}




>     def metadatas(
>         self,
>         metadata_set_id: int
>     ) ‑> List[Dict]


Get all metadatas given a metadata set id.

Metadatas MAY be ordered with the rank attribute.

Example output:

```
[
    {
        "id": 1,
        "title": "PNG:ProfileName",
        "set_id": 1,
        "set_title": "exif metas",
        "rank": 0,
        "owner": "john",
    },
    {
        "id": 2,
        "title": "ICC_Profile:GrayTRC",
        "set_id": 1,
        "set_title": "exif metas",
        "rank": 1,
        "owner": "john",
    }
]
```

    
##### Method `metadatasets` {#jama_client.Client.metadatasets}




>     def metadatasets(
>         self
>     ) ‑> List[Dict]


Get the list of all the user's metadata sets.
For each metadatas set, the number of metadatas is given in metas_count

Example output:

```
[
    {"id": 1, "title": "exif metas", "owner": "john", "metas_count": 23},
    {"id": 2, "title": "dublin core", "owner": "john", "metas_count": 17}
]
```

    
##### Method `metadatatypes` {#jama_client.Client.metadatatypes}




>     def metadatatypes(
>         self
>     ) ‑> List[dict]


Get a list of available data types

Example output:

```
[
    {"id": 1, "title": "text"},
    {"id": 2, "title": "numeric"},
]
```

    
##### Method `move_collection` {#jama_client.Client.move_collection}




>     def move_collection(
>         self,
>         child_collection_id: int,
>         parent_collection_id: int = None
>     ) ‑> bool


Move a collection from a parent to another.

Will return false in the following cases:

- 'child_collection_id' and 'parent_collection_id' are equal
- parent collection does not exist
- parent collection is a descendant of child collection

If 'parent_collection_id' is null, collection is moved to the root.

    
##### Method `ping` {#jama_client.Client.ping}




>     def ping(
>         self
>     ) ‑> str


This is a test method to ensure the server-client communication works.
Will return "pong [name authenticated of user]"

Example output:

```
pong john
```

    
##### Method `publish_collection` {#jama_client.Client.publish_collection}




>     def publish_collection(
>         self,
>         collection_id: int
>     ) ‑> bool


Mark a collection as public

    
##### Method `remove_file_from_collection` {#jama_client.Client.remove_file_from_collection}




>     def remove_file_from_collection(
>         self,
>         file_id: int,
>         collection_id: int
>     ) ‑> bool


DEPRECATED. Do not use. Will be removed later. Use remove_resource_from_collection instead.

    
##### Method `remove_meta_from_collection` {#jama_client.Client.remove_meta_from_collection}




>     def remove_meta_from_collection(
>         self,
>         collection_id: int,
>         meta_value_id: int
>     ) ‑> bool


Remove a meta from a collection given their ids.

    
##### Method `remove_meta_from_file` {#jama_client.Client.remove_meta_from_file}




>     def remove_meta_from_file(
>         self,
>         file_id: int,
>         meta_value_id: int
>     ) ‑> bool


DEPRECATED. Do not use. Will be removed later. Use remove_meta_from_resource instead.

    
##### Method `remove_meta_from_resource` {#jama_client.Client.remove_meta_from_resource}




>     def remove_meta_from_resource(
>         self,
>         resource_id: int,
>         meta_value_id: int
>     ) ‑> bool


Remove a meta from a resource given their ids.

    
##### Method `remove_resource_from_collection` {#jama_client.Client.remove_resource_from_collection}




>     def remove_resource_from_collection(
>         self,
>         resource_id: int,
>         collection_id: int
>     ) ‑> bool


Remove a resource from a collection given ids.

    
##### Method `remove_tag` {#jama_client.Client.remove_tag}




>     def remove_tag(
>         self,
>         uid: str
>     ) ‑> bool


Remove (delete) a tag based on its uid.

Beware: This will remove ALL associations with the tag.

    
##### Method `remove_tag_from_collection` {#jama_client.Client.remove_tag_from_collection}




>     def remove_tag_from_collection(
>         self,
>         tag_uid: str,
>         collection_id: int
>     ) ‑> bool


Remove tag from a collection based on tag uid and collection id.

    
##### Method `remove_tag_from_resource` {#jama_client.Client.remove_tag_from_resource}




>     def remove_tag_from_resource(
>         self,
>         tag_uid: str,
>         resource_id: int
>     ) ‑> bool


Remove tag from a resource based on tag uid and resource id.

    
##### Method `rename_collection` {#jama_client.Client.rename_collection}




>     def rename_collection(
>         self,
>         collection_id: int,
>         title: str
>     ) ‑> bool


Rename a collection (ie. change its title).

    
##### Method `rename_file` {#jama_client.Client.rename_file}




>     def rename_file(
>         self,
>         file_id: int,
>         title: str
>     ) ‑> bool


DEPRECATED. Do not use. Will be removed later. Use rename_resource instead.

    
##### Method `rename_meta` {#jama_client.Client.rename_meta}




>     def rename_meta(
>         self,
>         meta_id: int,
>         title: str
>     ) ‑> bool


Rename a metadata (ie. change its title).

    
##### Method `rename_resource` {#jama_client.Client.rename_resource}




>     def rename_resource(
>         self,
>         resource_id: int,
>         title: str
>     ) ‑> bool


Rename a resource (ie. change its title).

    
##### Method `resource` {#jama_client.Client.resource}




>     def resource(
>         self,
>         resource_id: int
>     ) ‑> Union[Dict, NoneType]


Get a resource given its id.

Example output (file resource):

```
{
    "id": 1,
    "title": "letter",
    "original_name": "letter.txt",
    "type": "text/plain",
    "hash": "0dd93a59aeaccfb6d35b1ff5a49bde1196aa90dfef02892f9aa2ef4087d8738e",
    "metas": null,
    "urls": [],
    "tags": [],
}
```

    
##### Method `resources` {#jama_client.Client.resources}




>     def resources(
>         self,
>         collection_id: int,
>         include_metas: bool = True
>     ) ‑> List[Dict]


Get all resources from a collection.

If 'include_metas' is true, will return the resources metadatas.
If 'include_metas' is false, 'metas' will be null.

Different resources types may have different object keys. The bare
minimum is 'id', 'title' and 'tags'.

Example output (file resource):

```
[
    {
        "id": 1,
        "title": "letter",
        "original_name": "letter.txt",
        "type": "text/plain",
        "hash": "0dd93a59aeaccfb6d35b1ff5a49bde1196aa90dfef02892f9aa2ef4087d8738e",
        "metas": null,
        "urls": [],
        "tags": [],
    }
]
```

    
##### Method `set_tag` {#jama_client.Client.set_tag}




>     def set_tag(
>         self,
>         uid: str,
>         label: str = None,
>         ark: str = None
>     ) ‑> dict


Get or create a Tag by uid (unique identifier). 'label' is an optional human-readable name.

Example output:

```
{
    "id": 1,
    "uid": "PAINTINGS",
    "label": "peintures",
    "ark": null,
}
```

    
##### Method `simple_search` {#jama_client.Client.simple_search}




>     def simple_search(
>         self,
>         query: str
>     ) ‑> Dict[str, List]


Performs a simple search on resources and collections, based on their titles.

Example output:

```
{
    "collections": [
        {
        "id": 1,
        "title": "photos",
        "resources_count": 0,
        "children_count": 0,
        "descendants_count": 0,
        "descendants_resources_count": 0,
        "parent": null,
        "children": null,
        "metas": [],
        "public_access": false,
        "tags": [],
        }
    ],
    "resources": [
        {
        "id": 1,
        "title": "letter",
        "original_name": "letter.txt",
        "type": "text/plain",
        "hash": "0dd93a59aeaccfb6d35b1ff5a49bde1196aa90dfef02892f9aa2ef4087d8738e",
        "metas": null,
        "urls": [],
        "tags": [],
        }
    ]
}
```

    
##### Method `supported_file_types` {#jama_client.Client.supported_file_types}




>     def supported_file_types(
>         self
>     ) ‑> List[Dict]


Get a list of all supported file type, complete with their mimes.

Example output:

```
[
    {
    "mime": "image/jpeg",
    "extensions": [".jpg", ".jpeg"],
    "iiif_support": true,
    }
]
```

    
##### Method `tags` {#jama_client.Client.tags}




>     def tags(
>         self
>     ) ‑> List[dict]


Returns all tags available to the current user.

Example output:

```
[
    {
    "id": 1,
    "uid": "PAINTINGS",
    "label": "peintures",
    "ark": null,
    },
    {
    "id": 2,
    "uid": "PHOTOS",
    "label": "photos",
    "ark": null,
    }
]
```

    
##### Method `unpublish_collection` {#jama_client.Client.unpublish_collection}




>     def unpublish_collection(
>         self,
>         collection_id: int
>     ) ‑> bool


Mark a collection as private

    
##### Method `upload` {#jama_client.Client.upload}




>     def upload(
>         self,
>         file_path: str,
>         chunk_size: int = 1048576,
>         file_name: str = None,
>         origin_dir_name: str = None
>     ) ‑> int


This methods uploads a file in multiple chunks, allowing
resumable uploads.

```file_path``` is the local path to the file.

```chunk_size``` is the number of bytes uploaded with each chunk of the file.

```file_name``` overides the name of the file, should you want a different name in Jama than
the local name.

```origin_dir_name``` is a directory path (```dirA/dirB/dirC```). This path triggers
the creation of the corresponding collections and sub-collections in Jama.

    
##### Method `upload_infos` {#jama_client.Client.upload_infos}




>     def upload_infos(
>         self,
>         sha256_hash: str
>     ) ‑> Dict


Get information for an upload based on the file hash.

Example output:

```
{
    "status": "not available",
    "id": null,
    "available_chunks":[]
}
```

"status" being one of "not available", "available" or "incomplete"

    
### Class `IncompleteUpload` {#jama_client.IncompleteUpload}




>     class IncompleteUpload(
>         *args,
>         **kwargs
>     )


Unspecified run-time error.


    
#### Ancestors (in MRO)

* [builtins.RuntimeError](#builtins.RuntimeError)
* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `ServiceError` {#jama_client.ServiceError}




>     class ServiceError(
>         message
>     )


Unspecified run-time error.


    
#### Ancestors (in MRO)

* [builtins.RuntimeError](#builtins.RuntimeError)
* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)







-----
Generated by *pdoc* 0.9.1 (<https://pdoc3.github.io>).
