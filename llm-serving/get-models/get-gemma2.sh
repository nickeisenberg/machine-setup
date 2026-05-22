LLNL_USER=eisenbnt
SAVE_TO=${HOME}/models

mkdir -p $SAVE_TO

rsync -avP ${LLNL_USER}@matrix.llnl.gov:/p/lustre1/nova/llm-weights/ \
    ${SAVE_TO}/
