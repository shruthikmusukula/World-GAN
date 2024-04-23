param(
    [Parameter(Mandatory=$true)]
    [string]$objDirectory = "",

    [Parameter(Mandatory=$false)]
    [single]$orthScale = 14.5,

    [Parameter(Mandatory=$false)]
    [int]$view = 0
)

# Loop through all .obj files in the directory specified by the first script argument
foreach ($file in Get-ChildItem "$objDirectory\*.obj") {
    # Run Blender with specified parameters
    & "C:\Program Files\Blender Foundation\Blender\blender.exe" -b --python "minecraft\blender_scripts\CyclesMineways.py" -- $file.FullName $orthScale $view
}

# Create the renders directory if it doesn't exist
$renderDir = Join-Path $objDirectory "..\renders"
if (-not (Test-Path $renderDir)) {
    New-Item -ItemType Directory -Path $renderDir
}

# Loop through all render-$view.png files in the directory
foreach ($file in Get-ChildItem "$objDirectory\*render-$view.png") {
    # Copy each file to the renders directory
    Copy-Item -Path $file.FullName -Destination $renderDir -Force

    # Delete the original file after copying
    Remove-Item -Path $file.FullName -Force
}