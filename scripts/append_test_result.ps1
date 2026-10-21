param (
    [Parameter(Mandatory=$true)]
    [string]$TestCaseId,

    [Parameter(Mandatory=$true)]
    [string]$Status,

    [Parameter(Mandatory=$true)]
    [string]$ActualResult,

    [Parameter(Mandatory=$true)]
    [string]$EvidenceFile,

    [string]$Feedback = ""
)

$csvPath = "D:\Tan\work\test_php\Test_case_D.Tan_30_9 - Test_case.csv"
$specPath = "D:\Tan\work\test_php\docs\02_TEST_SPEC.md"

if (!(Test-Path -Path $csvPath)) {
    Write-Output "ERROR: Khong tim thay file CSV tai: $csvPath"
    exit 1
}

# Doc spec de lay Module, Chuc nang, Mo ta va Cac buoc
$specContent = Get-Content -Path $specPath -Raw -Encoding UTF8

# Trich xuat block cua TestCaseId
$pattern = "(?s)### $TestCaseId:\s*(.*?)\r?\n- \*\*Module / Chức năng:\*\*\s*(.*?)\s*/\s*(.*?)\r?\n- \*\*Mô tả:\*\*\s*(.*?)\r?\n- \*\*Các bước thực hiện:\*\*\s*(.*?)\r?\n- \*\*Expected Result:\*\*\s*(.*?)\r?\n"

if ($specContent -match $pattern) {
    $module = $matches[2].Trim()
    $chucNang = $matches[3].Trim()
    $moTa = $matches[4].Trim()
    $cacBuoc = $matches[5].Trim()
    $expected = $matches[6].Trim()
} else {
    Write-Output "ERROR: Khong tim thay thong tin dac ta cua $TestCaseId trong 02_TEST_SPEC.md"
    exit 1
}

# Format dong CSV chuan
$cacBuocCsv = '"' + ($cacBuoc -replace '"', '""') + '"'
$expectedCsv = '"' + ($expected -replace '"', '""') + '"'
$actualCsv = '"' + ($ActualResult -replace '"', '""') + '"'
$feedbackCsv = '"' + ($Feedback -replace '"', '""') + '"'
$evidenceCsv = $EvidenceFile

# Ghi vao CSV
$newLine = "$TestCaseId,$module,$chucNang,$moTa,$cacBuocCsv,$expectedCsv,$actualCsv,$evidenceCsv,-,$Status,$feedbackCsv,,,,,"

Add-Content -Path $csvPath -Value $newLine -Encoding UTF8

Write-Output "SUCCESS: Da ghi thanh cong $TestCaseId vao $csvPath"
