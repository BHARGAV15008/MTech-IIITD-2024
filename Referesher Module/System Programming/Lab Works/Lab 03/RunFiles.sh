if [["$#" != 2]]; then
    echo ""
    exit 1
fi

fileName1 = "$1"
fileName2 = "$2"

if [ ! -f "$fileName1" or ! -f "$fileName1" ]; then
    echo "Error: File not found."
    exit 1
fi