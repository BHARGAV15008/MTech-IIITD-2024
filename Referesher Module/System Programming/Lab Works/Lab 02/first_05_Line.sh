# Check if file has fewer than 5 lines
if [ $(wc -l < first_05_Line.sh) -lt 5 ]; then
  echo "File has fewer than 5 lines."
fi # file end

# Print the first 5 lines of the file by using head commands
head -n 5 first_05_Line.sh
