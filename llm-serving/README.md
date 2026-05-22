First get the weights for Gemma as the rest of the demo scripts in this
directory depend on it. Do this by running `./get-models/get-gemma.sh`. This
will require you to set up a hugging face access token and get approval from
google as they require this.

Next get the vllm and openwebui containers by running the following

* ./get-containers/get-ollama.sh
* ./get-containers/get-vllm.sh
* ./get-containers/get-openwebui.sh

After that, you can do either test running these containers with the scripts
available in `./run-containers`.


