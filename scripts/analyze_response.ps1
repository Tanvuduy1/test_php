param (
    [Parameter(Mandatory=$true)]
    [string]$TestCaseId,

    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

# Kiem tra file bang chung co ton tai khong
if (!(Test-Path -Path $FilePath)) {
    Write-Output "ERROR: Khong tim thay file bang chung tai: $FilePath"
    exit 1
}

$content = Get-Content -Path $FilePath -Raw -Encoding UTF8

# Cac tu khoa canh bao va loi PHP can bẫy
$phpErrorPatterns = @(
    "Fatal error",
    "Parse error",
    "Warning:",
    "Notice:",
    "Deprecated:",
    "Strict Standards:",
    "Undefined index",
    "Undefined variable",
    "Undefined array key",
    "Call to a member function",
    "Uncaught Error",
    "Uncaught Exception",
    "Stack trace:",
    "xdebug-error"
)

$foundErrors = @()

foreach ($pattern in $phpErrorPatterns) {
    if ($content -match $pattern) {
        $foundErrors += $pattern
    }
}

$status = "Pass"
$actualResult = ""
$feedback = ""

if ($foundErrors.Count -gt 0) {
    $status = "Fail"
    $errorListStr = ($foundErrors | Select-Object -Unique) -join ", "
    $actualResult = "Phat hien cac loi PHP trong Response: $errorListStr."
    
    # Trich xuat toi da 5 dong chua chuoi loi dau tien de lam bang chung tom tat
    $lines = $content -split "`r?`n"
    $sampleLines = @()
    foreach ($line in $lines) {
        foreach ($pattern in $foundErrors) {
            if ($line -match $pattern) {
                $sampleLines += $line.Trim()
                break
            }
        }
        if ($sampleLines.Count -ge 3) { break }
    }
    $feedback = "Chi tiet loi trich xuat: " + ($sampleLines -join " | ")
} else {
    $status = "Pass"
    $actualResult = "Response tra ve du lieu hop le, khong phat hien bat ky chuoi loi PHP (Warning/Notice/Deprecated/Fatal) nao."
    $feedback = "He thong xu ly on dinh, response sach loi backend."
}

# Xuat ket qua dang JSON nho gon de Agent nap vao bo nho (Tiet kiem toi da Token)
$result = [PSCustomObject]@{
    TestCaseId   = $TestCaseId
    FilePath     = $FilePath
    Status       = $status
    ActualResult = $actualResult
    Feedback     = $feedback
    HasPhpError  = ($status -eq "Fail")
    DetectedKeys = $foundErrors
}

$result | ConvertTo-Json -Compress
