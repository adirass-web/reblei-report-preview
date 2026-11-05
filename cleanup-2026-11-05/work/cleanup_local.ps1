$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath '.').Path
$expectedRoot='V:\Codex\2026-11-04\referenced-chatgpt-conversation-this-is-an-3'
if ($taskRoot -ne $expectedRoot) { throw 'Wrong cleanup workspace' }
$keep=(Resolve-Path -LiteralPath 'outputs/ReBlei-migration').Path
$logRoot=Join-Path $keep 'investigations/2026-11-04-official-records/cleanup-2026-11-05'
$inv=Get-Content -LiteralPath (Join-Path $logRoot 'local-inventory.json') -Raw | ConvertFrom-Json
$preflight=python (Join-Path $logRoot 'work/preflight_cleanup.py')
if ($LASTEXITCODE -ne 0) { throw 'Pre-deletion verification failed' }
$proof=$preflight | ConvertFrom-Json
$targets=@($inv.cleanup_targets)+@(Join-Path $taskRoot 'outputs/ReBlei-remote-verification')
$checked=@()
foreach ($raw in $targets) {
 $target=(Resolve-Path -LiteralPath $raw).Path
 $outsideTemp=$target -eq 'V:\Codex\editorial-skill-input.json'
 if (-not $outsideTemp -and -not $target.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Path outside intended workspace' }
 if ($target -eq $taskRoot -or $target -eq $keep -or $target.StartsWith($keep+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Protected working checkout' }
 $item=Get-Item -LiteralPath $target -Force
 $all=@($item)
 if ($item.PSIsContainer) { $all+=@(Get-ChildItem -LiteralPath $target -Recurse -Force) }
 if (@($all | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) { throw 'Refuse reparse point in cleanup tree' }
 $files=@($all | Where-Object { -not $_.PSIsContainer })
 $sum=($files | Measure-Object -Property Length -Sum).Sum
 $checked+=@{path=$target;files=$files.Count;bytes=$sum;directory=$item.PSIsContainer}
}
$removed=@()
try {
 foreach ($entry in $checked) {
  if ($entry.directory) { Remove-Item -LiteralPath $entry.path -Recurse -Force } else { Remove-Item -LiteralPath $entry.path -Force }
  if (Test-Path -LiteralPath $entry.path) { throw 'Target still exists' }
  $removed+=$entry
 }
} finally {
 $receipt=@{completed_at_utc=[DateTime]::UtcNow.ToString('o');preflight=$proof;removed=$removed;removed_files=($removed | Measure-Object -Property files -Sum).Sum;removed_bytes=($removed | Measure-Object -Property bytes -Sum).Sum;retained_checkout=$keep;all_targets_removed=($removed.Count -eq $checked.Count);free_bytes_on_v=(Get-PSDrive V).Free}
 $receipt | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $logRoot 'cleanup-receipt.json') -Encoding utf8
}
$receipt | Select-Object removed_files,removed_bytes,all_targets_removed,retained_checkout,free_bytes_on_v | ConvertTo-Json
