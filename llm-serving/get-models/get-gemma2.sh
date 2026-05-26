LLNL_USER=eisenbnt
SAVE_TO=${HOME}/models
MODEL="gemma-3-270m-it"

mkdir -p $SAVE_TO

scp -r ${LLNL_USER}@matrix.llnl.gov:/p/lustre1/nova/llm-weights/${MODEL} \
    ${SAVE_TO}/
