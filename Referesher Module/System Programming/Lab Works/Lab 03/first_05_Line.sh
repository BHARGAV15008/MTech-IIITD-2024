if [["$#" != 2]]; then
    echo ""
    exit 1
fi

FILENAME="$1"

if [ ! -f "$FILENAME" ]; then
    echo "Error: File '$FILENAME' not found."
    exit 1
fi

if [ $(wc -l < first_05_Line.sh) -lt 5 ]; then
  head "$FILENAME"
fi # file end

head -n 5 "$FILENAME"
