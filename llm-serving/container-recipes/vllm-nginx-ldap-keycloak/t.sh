check_env_var_set() {
    val=$(eval "echo \"\$$1\"")

    if [ -z "$val" ]; then
        echo
    else
        echo "$val"
    fi
}


check_env_var_set USER
