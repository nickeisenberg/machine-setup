LLNL_USER=eisenbnt
SAVE_TO=${HOME}/models/gemma-3-1b-it

mkdir -p $SAVE_TO

scp -r \
    ${LLNL_USER}@matrix.llnl.gov:/p/lustre2/eisenbnt/.local/share/huggingface/models/gemma-3-1b-it \
	${SAVE_TO}
