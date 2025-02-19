pascalTraingle() {
    local num=$1

    for (( i = 0; i <= num; i++ )); do
        local n=1

        for (( j = 0; j <= i; j++ )); do
            echo -n "$n "
            n=$(( n * (i - j) / (j + 1) ))
        done
        echo
    done
}

# Takes input from the user
echo "Enter the number of rows: "
read num

pascalTraingle $num