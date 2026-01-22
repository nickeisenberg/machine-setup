if ! hf version > /dev/null 2>&1; then
	echo "INFO: You must pip install huggingface_hub"
	exit 1
fi

if [[ -z $HF_TOKEN ]]; then
	echo "INFO: Set the HF_TOKEN env var so that you can download gemma. Google requires this."
	exit 1
fi

SAVE_TO=${HOME}/models/gemma-3-1b-it

mkdir -p $SAVE_TO

hf download google/gemma-3-1b-it --local-dir ${SAVE_TO} --token ${HF_TOKEN}
