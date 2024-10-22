# Initialize index
$index = 1

# Read the contents of stories.txt
$stories = Get-Content "stories.txt"

# Initialize a variable for the current story
$currentStory = ""

foreach ($line in $stories) {
    
    # Replace commas and periods followed by spaces (e.g. ". " or ", ") with a newline character
    # This ensures that both punctuation and the following space will move to a new line
    $line = $line -replace '([,.])\s+', "$1`n"

    # Append the modified line to the current story
    $currentStory += $line + "`n"

    # Check for the story delimiter
    if ($line -like "*|*") {
        Write-Host "Saving story $index..."  # Indicate that a story is being saved
        
        # Remove the delimiter and save the current story to a file
        $currentStory = $currentStory -replace '\|', ''
        
        # Remove empty lines
        $currentStory = $currentStory -replace '^\s*[\r\n]+', ''
        
        Set-Content "Story_$index.txt" $currentStory
        
        # Increment the index and reset the current story
        $index++
        $currentStory = ""
    }
}

# Handle the last story if it doesn't end with a delimiter
if ($currentStory -ne "") {
    Write-Host "Saving final story $index..."  # Indicate that the last story is being saved
    $currentStory = $currentStory -replace '\|', ''
    
    # Remove empty lines
    $currentStory = $currentStory -replace '^\s*[\r\n]+', ''
    
    Set-Content "Story_$index.txt" $currentStory
}

Write-Host "Script completed!"  # Indicate that the script has finished
