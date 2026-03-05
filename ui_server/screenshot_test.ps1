# 使用 PowerShell 和 Edge WebDriver 来截图
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# 等待用户手动打开浏览器并导航到页面
Write-Host "请按以下步骤操作:" -ForegroundColor Yellow
Write-Host "1. 在浏览器中打开: http://127.0.0.1:8000/test_preview" -ForegroundColor Cyan
Write-Host "2. 等待 3 秒让数据加载完成" -ForegroundColor Cyan
Write-Host "3. 按 Enter 键继续截图..." -ForegroundColor Cyan
Read-Host

Write-Host "正在截取屏幕..." -ForegroundColor Green

# 获取屏幕尺寸
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$width = $screen.Width
$height = $screen.Height

# 创建位图
$bitmap = New-Object System.Drawing.Bitmap $width, $height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)

# 截取屏幕
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)

# 保存截图
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$screenshotPath = Join-Path $PSScriptRoot "screenshot_test_preview_$timestamp.png"
$bitmap.Save($screenshotPath, [System.Drawing.Imaging.ImageFormat]::Png)

# 清理
$graphics.Dispose()
$bitmap.Dispose()

Write-Host "截图已保存到: $screenshotPath" -ForegroundColor Green
Write-Host ""
Write-Host "现在请:" -ForegroundColor Yellow
Write-Host "1. 在浏览器中导航到: http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host "2. 按 Enter 键继续截图主页..." -ForegroundColor Cyan
Read-Host

Write-Host "正在截取主页..." -ForegroundColor Green

# 第二次截图
$bitmap2 = New-Object System.Drawing.Bitmap $width, $height
$graphics2 = [System.Drawing.Graphics]::FromImage($bitmap2)
$graphics2.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)

$screenshotPath2 = Join-Path $PSScriptRoot "screenshot_main_page_$timestamp.png"
$bitmap2.Save($screenshotPath2, [System.Drawing.Imaging.ImageFormat]::Png)

$graphics2.Dispose()
$bitmap2.Dispose()

Write-Host "主页截图已保存到: $screenshotPath2" -ForegroundColor Green
Write-Host ""
Write-Host "完成! 两张截图已保存。" -ForegroundColor Green

# 打开文件资源管理器显示截图
explorer.exe /select,$screenshotPath
