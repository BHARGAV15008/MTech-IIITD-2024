targetDir="copied_files_dir"
copiedFileList="copied_files.txt"

if [ ! -d "$targetDir" ]; then
    mkdir -p "$targetDir"
fi

if [ ! -f "$copiedFileList" ]; then
    > "$targetDir/$copiedFileList"
fi

for file in "./"/*; do
    if [ -f "$file" ]; then
        baseName=$(basename "$file")
        cp "$file" "$targetDir"
        echo "$baseName" >> "$copiedFileList"
    fi
done