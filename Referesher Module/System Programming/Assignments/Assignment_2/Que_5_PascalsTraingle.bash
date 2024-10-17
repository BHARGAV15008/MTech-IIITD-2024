read -p "Enter the number of Rows: " rows

for (( i=0; i<rows; i++ )); do
    val=1
    for (( j=0; j<=i; j++ )); do
        echo -n "$val  "
        (( val = val * (i - j) / (j + 1) ))
    done
    echo
done
