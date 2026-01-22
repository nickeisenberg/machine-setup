First get the weights for Gemma as the rest of the demo scripts in this
directory depend on it. Do this by running get-gemma.sh. This will require
you to set up a hugging face access token and get approval from google as
they require this.

First get the vllm and openwebui containers by running the following

* ./openwebui-container/get-openwebui-container.sh
* ./vllm-container/get-vllm-container.sh

after that, you can run each of these separately with

* ./openwebui-container/run.sh
* ./vllm-container/run.sh

Or you can use podman compose. To do this, `cd` into
vllm-openwebui-podman-compose and then run `podman compose up`.

After this, openwebui will be available at localhost:8080 and you
should be able to interact with gemma as well through the UI.
