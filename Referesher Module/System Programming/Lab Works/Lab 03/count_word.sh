if [ "$#" -ne 2 ]; then
    echo ""
    exit 1
fi

FILENAME="$1"
WORD="$2"

if [ ! -f "$FILENAME" ]; then
    echo "Error: File '$FILENAME' not found."
    exit 1
fi

COUNT=$(grep -o -w "$WORD" "$FILENAME" | wc -l)

if [ "$COUNT" -eq 0 ]; then
    echo "The word '$WORD' is not present in the file '$FILENAME'."
else
    echo "The word '$WORD' appears $COUNT times in the file '$FILENAME'."
fi

