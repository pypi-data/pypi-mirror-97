<p align="center">
<img src="https://github.com/jina-ai/jina/blob/master/.github/logo-only.gif?raw=true" alt="Jina banner" width="200px">
</p>
<p align="center">
An easier way to build neural search on the cloud
</p>
<p align=center>
<a href="https://pypi.org/project/jina/"><img src="https://github.com/jina-ai/jina/blob/master/.github/badges/python-badge.svg?raw=true" alt="Python 3.7 3.8 3.9" title="Jina supports Python 3.7 and above"></a>
<a href="https://pypi.org/project/jina/"><img src="https://img.shields.io/pypi/v/jina?color=%23099cec&amp;label=PyPI&amp;logo=pypi&amp;logoColor=white" alt="PyPI"></a>
<a href="https://hub.docker.com/r/jinaai/jina/tags"><img src="https://img.shields.io/docker/v/jinaai/jina?color=%23099cec&amp;label=Docker&amp;logo=docker&amp;logoColor=white&amp;sort=semver" alt="Docker Image Version (latest semver)"></a>
<a href="https://github.com/jina-ai/jina/actions?query=workflow%3ACI"><img src="https://github.com/jina-ai/jina/workflows/CI/badge.svg" alt="CI"></a>
<a href="https://github.com/jina-ai/jina/actions?query=workflow%3ACD"><img src="https://github.com/jina-ai/jina/workflows/CD/badge.svg?branch=master" alt="CD"></a>
<a href="https://codecov.io/gh/jina-ai/jina"><img src="https://codecov.io/gh/jina-ai/jina/branch/master/graph/badge.svg" alt="codecov"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"><a>
</p>


Jina is a deep learning-powered search framework for building <strong>cross-/multi-modal search systems</strong> (e.g. text, images, video, audio) on the cloud.

⏱️ **Time Saver** - *The* design pattern of neural search systems, from zero to a production-ready system in minutes.

🍱 **Full-Stack Ownership** - Keep an end-to-end stack ownership of your solution, avoid the integration pitfalls with fragmented, multi-vendor, generic legacy tools.

🌌 **Universal Search** - Large-scale indexing and querying of unstructured data: video, image, long/short text, music, source code, etc.

🧠 **First-Class AI Models** - First-class support for [state-of-the-art AI models](https://docs.jina.ai/chapters/all_exec.html), easily usable and extendable with a Pythonic interface.

🌩️ **Fast & Cloud Ready** - Decentralized architecture from day one. Scalable & cloud-native by design: enjoy containerizing, distributing, sharding, async, REST/gRPC/WebSocket.

❤️  **Made with Love** - Never compromise on quality, actively maintained by a [passionate full-time, venture-backed team](https://jina.ai).

---

<p align="center">
<a href="http://docs.jina.ai">Docs</a> • <a href="#jina-hello-world-">Hello World</a> • <a href="#get-started">Quick Start</a> • <a href="#learn">Learn</a> • <a href="https://github.com/jina-ai/examples">Examples</a> • <a href="#contributing">Contribute</a> • <a href="https://jobs.jina.ai">Jobs</a> • <a href="http://jina.ai">Website</a> • <a href="http://slack.jina.ai">Slack</a>
</p>


## Installation

| 📦<br><sub><sup>x86/64,arm/v6,v7,[v8 (Apple M1)](https://github.com/jina-ai/jina/issues/1781)</sup></sub> | On Linux/macOS & Python 3.7/3.8/[3.9](https://github.com/jina-ai/jina/issues/1801) | Docker Users|
| --- | --- | --- |
| Standard | `pip install -U jina` | `docker run jinaai/jina:latest` |
| <sub><a href="https://api.jina.ai/daemon/">Daemon</a></sub> | <sub>`pip install -U "jina[daemon]"`</sub> | <sub>`docker run --network=host jinaai/jina:latest-daemon`</sub> |
| <sub>With Extras</sub> | <sub>`pip install -U "jina[devel]"`</sub> | <sub>`docker run jinaai/jina:latest-devel`</sub> |
| <sub>Dev/Pre-Release</sub> | <sub>`pip install --pre jina`</sub> | <sub>`docker run jinaai/jina:master`</sub> |

Version identifiers [are explained here](https://github.com/jina-ai/jina/blob/master/RELEASE.md). To install Jina with extra dependencies [please refer to the docs](https://docs.jina.ai/chapters/install/via-pip.html). Jina can run on [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10). We welcome the community to help us with [native Windows support](https://github.com/jina-ai/jina/issues/1252).

### YAML Completion in IDE

Developing Jina app often means writing YAML configs. We provide a [JSON Schema](https://json-schema.org/) for your IDE to enable code completion, syntax validation, members listing and displaying help text. Here is a [video tutorial](https://youtu.be/qOD-6mihUzQ) to walk you through the setup.

<table>
  <tr>
    <td>
<a href="https://www.youtube.com/watch?v=qOD-6mihUzQ&ab_channel=JinaAI"><img src="https://github.com/jina-ai/jina/blob/master/.github/images/pycharm-schema.gif?raw=true" /></a>
    </td>
    <td>

**PyCharm**

1. Click menu `Preferences` -> `JSON Schema mappings`;
2. Add a new schema, in the `Schema File or URL` write `https://api.jina.ai/schemas/latest.json`; select `JSON Schema Version 7`;
3. Add a file path pattern and link it to `*.jaml` and `*.jina.yml`.

</td>
</tr>
<tr>
    <td>
<a href="https://www.youtube.com/watch?v=qOD-6mihUzQ&ab_channel=JinaAI"><img src="https://github.com/jina-ai/jina/blob/master/.github/images/vscode-schema.gif?raw=true" /></a>
    </td>
    <td>

**VSCode**

1. Install the extension: `YAML Language Support by Red Hat`;
2. In IDE-level `settings.json` add:

```json
"yaml.schemas": {
    "https://api.jina.ai/schemas/latest.json": ["/*.jina.yml", "/*.jaml"],
}
```

</td>
</tr>
</table>


## Jina "Hello, World!" 👋🌍

Just starting out? Try Jina's "Hello, World" - `jina hello --help`

### 👗 Fashion Image Search


<a href="https://docs.jina.ai/">
<img align="right" width="25%" src="https://github.com/jina-ai/jina/blob/master/.github/images/hello-world.gif?raw=true" />
</a>

A simple image neural search demo for [Fashion-MNIST](https://hanxiao.io/2018/09/28/Fashion-MNIST-Year-In-Review/). No extra dependencies needed, simply run:

```bash
jina hello fashion  # more options in --help
```

...or even easier for Docker users, **no install required**:

```bash
docker run -v "$(pwd)/j:/j" jinaai/jina hello fashion --workdir /j && open j/hello-world.html
# replace "open" with "xdg-open" on Linux
```

<details>
<summary>Click here to see console output</summary>

<p align="center">
  <img src="https://github.com/jina-ai/jina/blob/master/.github/images/hello-world-demo.png?raw=true" alt="hello world console output">
</p>


</details>
This downloads the Fashion-MNIST training and test dataset and tells Jina to index 60,000 images from the training set. Then it randomly samples images from the test set as queries and asks Jina to retrieve relevant results. The whole process takes about 1 minute.


### 🤖 Covid-19 Chatbot

<a href="https://docs.jina.ai/">
<img align="right" width="25%" src="https://github.com/jina-ai/jina/blob/master/.github/images/helloworld-chatbot.gif?raw=true" />
</a>

For NLP engineers, we provide a simple chatbot demo for answering Covid-19 questions. To run that:
```bash
pip install "jina[chatbot]"

jina hello chatbot
```

This downloads [CovidQA dataset](https://www.kaggle.com/xhlulu/covidqa) and tells Jina to index 418 question-answer pairs with DistilBERT. The index process takes about 1 minute on CPU. Then it opens a web page where you can input questions and ask Jina.

<br><br>

### 🪆 Multimodal Document Search

<a href="https://youtu.be/B_nH8GCmBfc">
<img align="right" width="25%" src="https://github.com/jina-ai/jina/blob/master/.github/images/helloworld-multimodal.gif?raw=true" />
</a>

A multimodal-document contains multiple data types, e.g. a PDF document often contains figures and text. Jina lets you build a multimodal search solution in just minutes. To run our minimum multimodal document search demo:
```bash
pip install "jina[multimodal]"

jina hello multimodal
```

This downloads [people image dataset](https://www.kaggle.com/ahmadahmadzada/images2000) and tells Jina to index 2,000 image-caption pairs with MobileNet and DistilBERT. The index process takes about 3 minute on CPU. Then it opens a web page where you can query multimodal documents. We have prepared [a YouTube tutorial](https://youtu.be/B_nH8GCmBfc) to walk you through this demo.


<br><br><br>

## Get Started

|     |   |
| --- |---|
| 🥚  | [CRUD Functions](#crud-functions) • [Document](#document) • [Flow](#flow)  |
| 🐣  | [Feed Data](#feed-data) • [Fetch Result](#fetch-result) • [Add Logic](#add-logic) • [Inter & Intra Parallelism](#inter--intra-parallelism) • [Decentralize](#decentralized-flow) • [Asynchronous](#asynchronous-flow) |
| 🐥 | [Customize Encoder](#customize-encoder) • [Test Encoder](#test-encoder-in-flow) • [Parallelism & Batching](#parallelism--batching) • [Add Data Indexer](#add-data-indexer) • [Compose Flow from YAML](#compose-flow-from-yaml) • [Search](#search) • [Evaluation](#evaluation) • [REST Interface](#rest-interface) |

### 🥚 Fundamentals

#### CRUD Functions
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-basic-crud-functions.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

First we look at basic CRUD operations. In Jina, CRUD corresponds to four functions: `index` (create), `search` (read), `update`, and `delete`. With Documents below as an example:
```python
import numpy as np
from jina import Document
docs = [Document(id='🐲', embedding=np.array([0, 0]), tags={'guardian': 'Azure Dragon', 'position': 'East'}),
        Document(id='🐦', embedding=np.array([1, 0]), tags={'guardian': 'Vermilion Bird', 'position': 'South'}),
        Document(id='🐢', embedding=np.array([0, 1]), tags={'guardian': 'Black Tortoise', 'position': 'North'}),
        Document(id='🐯', embedding=np.array([1, 1]), tags={'guardian': 'White Tiger', 'position': 'West'})]
```

Let's build a Flow with a simple indexer:

```python
from jina import Flow
f = Flow().add(uses='_index')
```

`Document` and `Flow` are basic concepts in Jina, which will be explained later. `_index` is a built-in embedding + structured storage that you can use out of the box.

<table>
  <tr>
    <td>
    <b>Index</b>
    </td>
    <td>

```python
# save four docs (both embedding and structured info) into storage
with f:
    f.index(docs, on_done=print)
```

</td>
</tr>
  <tr>
    <td>
    <b>Search</b>
    </td>
    <td>

```python
# retrieve top-3 neighbours of 🐲, this print 🐲🐦🐢 with score 0, 1, 1 respectively
with f:
    f.search(docs[0], top_k=3, on_done=lambda x: print(x.docs[0].matches))
```

<sup>

```json
{"id": "🐲", "tags": {"guardian": "Azure Dragon", "position": "East"}, "embedding": {"dense": {"buffer": "AAAAAAAAAAAAAAAAAAAAAA==", "shape": [2], "dtype": "<i8"}}, "score": {"opName": "NumpyIndexer", "refId": "🐲"}, "adjacency": 1}
{"id": "🐦", "tags": {"position": "South", "guardian": "Vermilion Bird"}, "embedding": {"dense": {"buffer": "AQAAAAAAAAAAAAAAAAAAAA==", "shape": [2], "dtype": "<i8"}}, "score": {"value": 1.0, "opName": "NumpyIndexer", "refId": "🐲"}, "adjacency": 1}
{"id": "🐢", "tags": {"guardian": "Black Tortoise", "position": "North"}, "embedding": {"dense": {"buffer": "AAAAAAAAAAABAAAAAAAAAA==", "shape": [2], "dtype": "<i8"}}, "score": {"value": 1.0, "opName": "NumpyIndexer", "refId": "🐲"}, "adjacency": 1}
```
</sup>
</td>
</tr>
  <tr>
    <td>
    <b>Update</b>
    </td>
    <td>

```python
# update 🐲 embedding in the storage
docs[0].embedding = np.array([1, 1])
with f:
    f.update(docs[0])
```
</td>
</tr>
  <tr>
    <td>
    <b>Delete</b>
    </td>
    <td>

```python
# remove 🐦🐲 Documents from the storage
with f:
    f.delete(['🐦', '🐲'])
```
</td>
</tr>
</table>


#### Document
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-construct-document.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

`Document` is [Jina's primitive data type](https://hanxiao.io/2020/11/22/Primitive-Data-Types-in-Neural-Search-System/#primitive-types). It can contain text, image, array, embedding, URI, and be accompanied by rich meta information. To construct a Document, you can use:

```python
import numpy
from jina import Document

doc1 = Document(content=text_from_file, mime_type='text/x-python')  # a text document contains python code
doc2 = Document(content=numpy.random.random([10, 10]))  # a ndarray document
```

A Document can be recursed both vertically and horizontally to have nested Documents and matched Documents. To better see the Document's recursive structure, you can use `.plot()` function. If you are using JupyterLab/Notebook, all Document objects will be auto-rendered.

<table>
  <tr>
    <td>

```python
import numpy
from jina import Document

d0 = Document(id='🐲', embedding=np.array([0, 0]))
d1 = Document(id='🐦', embedding=np.array([1, 0]))
d2 = Document(id='🐢', embedding=np.array([0, 1]))
d3 = Document(id='🐯', embedding=np.array([1, 1]))

d0.chunks.append(d1)
d0.chunks[0].chunks.append(d2)
d0.matches.append(d3)

d0.plot()  # simply `d0` on JupyterLab
```

</td>
<td>
<img src="https://github.com/jina-ai/jina/blob/master/.github/images/four-symbol-docs.svg?raw=true"/>
</td>
</tr>
</table>

<details>
  <summary>Click here to see more about MultimodalDocument</summary>


#### MultimodalDocument

A `MultimodalDocument` is a document composed of multiple `Document` from different modalities (e.g. text, image, audio).

Jina provides multiple ways to build a multimodal Document. For example, you can provide the modality names and the content in a `dict`:

```python
from jina import MultimodalDocument
document = MultimodalDocument(modality_content_map={
    'title': 'my holiday picture',
    'description': 'the family having fun on the beach',
    'image': PIL.Image.open('path/to/image.jpg')
})
```

One can also compose a `MultimodalDocument` from multiple `Document` directly:

```python
from jina.types import Document, MultimodalDocument

doc_title = Document(content='my holiday picture', modality='title')
doc_desc = Document(content='the family having fun on the beach', modality='description')
doc_img = Document(content=PIL.Image.open('path/to/image.jpg'), modality='image')
doc_img.tags['date'] = '10/08/2019'

document = MultimodalDocument(chunks=[doc_title, doc_description, doc_img])
```

##### Fusion Embeddings from Different Modalities

To extract fusion embeddings from different modalities Jina provides `BaseMultiModalEncoder` abstract class, which has a unique `encode` interface.

```python
def encode(self, *data: 'numpy.ndarray', **kwargs) -> 'numpy.ndarray':
    ...
```

`MultimodalDriver` provides `data` to the `MultimodalDocument` in the correct expected order. In this example below, `image` embedding is passed to the encoder as the first argument, and `text` as the second.

```yaml
jtype: MyMultimodalEncoder
with:
  positional_modality: ['image', 'text']
requests:
  on:
    [IndexRequest, SearchRequest]:
      - jtype: MultiModalDriver {}
```

Interested readers can refer to [`jina-ai/example`: how to build a multimodal search engine for image retrieval using TIRG (Composing Text and Image for Image Retrieval)](https://github.com/jina-ai/examples/tree/master/multimodal-search-tirg) for the usage of `MultimodalDriver` and `BaseMultiModalEncoder` in practice.

</details>

#### Flow
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-create-flow.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

Jina provides a high-level Flow API to simplify building CRUD workflows. To create a new Flow:

```python
from jina import Flow
f = Flow().add()
```

This creates a simple Flow with one [Pod](https://101.jina.ai/#pod). You can chain multiple `.add()`s in a single Flow.

<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-visualize-a-flow.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

To visualize the Flow, simply chain it with `.plot('my-flow.svg')`. If you are using a Jupyter notebook, the Flow object will be displayed inline *without* `plot`.

<img src="https://github.com/jina-ai/jina/blob/master/.github/simple-flow0.svg?raw=true"/>

`Gateway` is the entrypoint of the Flow.

Get the vibe? Now we're talking! Let's learn more about the basic concepts and features of Jina:

---

|     |   |
| --- |---|
| 🥚  | [CRUD Functions](#crud-functions) • [Document](#document) • [Flow](#flow)  |
| 🐣  | [Feed Data](#feed-data) • [Fetch Result](#fetch-result) • [Add Logic](#add-logic) • [Inter & Intra Parallelism](#inter--intra-parallelism) • [Decentralize](#decentralized-flow) • [Asynchronous](#asynchronous-flow) |
| 🐥 | [Customize Encoder](#customize-encoder) • [Test Encoder](#test-encoder-in-flow) • [Parallelism & Batching](#parallelism--batching) • [Add Data Indexer](#add-data-indexer) • [Compose Flow from YAML](#compose-flow-from-yaml) • [Search](#search) • [Evaluation](#evaluation) • [REST Interface](#rest-interface) |


### 🐣 Basic

#### Feed Data
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-feed-data.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

To use a Flow, open it via `with` context manager, like you would open a file in Python. Now let's create some empty Documents and index them:

```python
from jina import Document

with Flow().add() as f:
    f.index((Document() for _ in range(10)))
```

Flow supports CRUD operations: `index`, `search`, `update`, `delete`. In addition, it also provides sugary syntax on `ndarray`, `csv`, `ndjson` and arbitrary files.


<table>
<tr>
    <td>
    Input
    </td>
    <td>
     Example of <code>index</code>/<code>search</code>
    </td>
<td>
Explain
</td>
</tr>
  <tr>
    <td>
    <code>numpy.ndarray</code>
    </td>
    <td>
      <sup>

```python
with f:
  f.index_ndarray(numpy.random.random([4,2]))
```

</sup>
  </td>
<td>

Input four `Document`s, each `document.blob` is an `ndarray([2])`

</td>
</tr>
<tr>
    <td>
    CSV
    </td>
    <td>
      <sup>

```python
with f, open('index.csv') as fp:
  f.index_csv(fp1, field_resolver={'pic_url': 'uri'})
```

</sup>
  </td>

<td>

Each line in `index.csv` is constructed as a `Document`, CSV field `pic_url` mapped to `document.uri`.

</td>
</tr>

<tr>
    <td>
    JSON Lines/<code>ndjson</code>/LDJSON
    </td>
    <td>
<sup>

```python
with f, open('index.ndjson') as fp:
  f.index_ndjson(fp1, field_resolver={'question_id': 'id'})
```

</sup>
  </td>
<td>

Each line in `index.ndjson` is constructed as a `Document`, JSON field `question_id` mapped to `document.id`.

</td>
</tr>
<tr>
    <td>
    Files with wildcards
    </td>
    <td>
      <sup>

```python
with f:
  f.index_files(['/tmp/*.mp4', '/tmp/*.pdf'])
```

</sup>
  </td>
<td>

Each file captured is constructed as a `Document`, and Document content (`text`, `blob`, `buffer`) is auto-guessed & filled.

</td>
</tr>

</table>

#### Fetch Result
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-fetch-result.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

Once a request is done, callback functions are fired. Jina Flow implements a Promise-like interface: You can add callback functions `on_done`, `on_error`, `on_always` to hook different events. In the example below, our Flow passes the message then prints the result when successful. If something goes wrong, it beeps. Finally, the result is written to `output.txt`.

```python
def beep(*args):
    # make a beep sound
    import os
    os.system('echo -n "\a";')

with Flow().add() as f, open('output.txt', 'w') as fp:
    f.index(numpy.random.random([4, 5, 2]),
            on_done=print, on_error=beep, on_always=lambda x: fp.write(x.json()))
```

#### Add Logic
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-add-logic.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

To add logic to the Flow, use the `uses` parameter to attach a Pod with an [Executor](https://101.jina.ai/#executor). `uses` accepts multiple value types including class name, Docker image, (inline) YAML or built-in shortcut.


```python
f = (Flow().add(uses='MyBertEncoder')  # class name of a Jina Executor
           .add(uses='docker://jinahub/pod.encoder.dummy_mwu_encoder:0.0.6-0.9.3')  # the image name
           .add(uses='myencoder.yml')  # YAML serialization of a Jina Executor
           .add(uses='!WaveletTransformer | {freq: 20}')  # inline YAML config
           .add(uses='_pass')  # built-in shortcut executor
           .add(uses={'__cls': 'MyBertEncoder', 'with': {'param': 1.23}}))  # dict config object with __cls keyword
```

The power of Jina lies in its decentralized architecture: Each `add` creates a new Pod, and these Pods can be run as a local thread/process, a remote process, inside a Docker container, or even inside a remote Docker container.

#### Inter & Intra Parallelism
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-inter-intra-parallelism.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

Chaining `.add()`s creates a sequential Flow. For parallelism, use the `needs` parameter:

```python
f = (Flow().add(name='p1', needs='gateway')
           .add(name='p2', needs='gateway')
           .add(name='p3', needs='gateway')
           .needs(['p1','p2', 'p3'], name='r1').plot())
```

<img src="https://github.com/jina-ai/jina/blob/master/.github/simple-plot3.svg?raw=true"/>

`p1`, `p2`, `p3` now subscribe to `Gateway` and conduct their work in parallel. The last `.needs()` blocks all Pods until they finish their work. Note: parallelism can also be performed inside a Pod using `parallel`:

```python
f = (Flow().add(name='p1', needs='gateway')
           .add(name='p2', needs='gateway')
           .add(name='p3', parallel=3)
           .needs(['p1','p3'], name='r1').plot())
```

<img src="https://github.com/jina-ai/jina/blob/master/.github/simple-plot4.svg?raw=true"/>

#### Decentralized Flow
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=decentralized-flow.ipynb"><img align="right" src="https://github.com/jina-ai/jina/blob/master/.github/badges/run-badge.svg?raw=true"/></a>

A Flow does not have to be local-only: You can put any Pod to remote(s). In the example below, with the `host` keyword `gpu-pod`, is put to a remote machine for parallelization, whereas other Pods stay local. Extra file dependencies that need to be uploaded are specified via the `upload_files` keyword.

<table>
    <tr>
    <td>123.456.78.9</td>
    <td>

```bash
# have docker installed
docker run --name=jinad --network=host -v /var/run/docker.sock:/var/run/docker.sock jinaai/jina:latest-daemon --port-expose 8000
# to stop it
docker rm -f jinad
```

</td>
</tr>
  <tr>
    <td>
    Local
    </td>
    <td>

```python
import numpy as np
from jina import Flow

f = (Flow()
     .add()
     .add(name='gpu_pod',
          uses='mwu_encoder.yml',
          host='123.456.78.9:8000',
          parallel=2,
          upload_files=['mwu_encoder.py'])
     .add())

with f:
    f.index_ndarray(np.random.random([10, 100]), output=print)
```
</tr>

</table>

We provide a demo server on `cloud.jina.ai:8000`, give the following snippet a try!

```python
from jina import Flow

with Flow().add().add(host='cloud.jina.ai:8000') as f:
    f.index(['hello', 'world'])
```

#### Asynchronous Flow
<a href="https://mybinder.org/v2/gh/jina-ai/jupyter-notebooks/main?filepath=basic-inter-intra-parallelism.ipynb"><img align="right" src="https://g