# Relying on existing $env:CONSTELLATION_ACCESS_KEY
cd "C:\Users\autismo\Documents\GitHub\GodBrain"
if (Test-Path constellation.json) { Remove-Item constellation.json }
$answers = @(
    "proj:b286d06d91714be3a57229e5e19d092f", # Project ID
    "master",                                # Branch
    "python, javascript",                    # Languages (guessing if it asks)
    "y"                                      # Save?
)
$inputString = $answers -join "`n"
echo $inputString | npx -y @constellationdev/cli init
