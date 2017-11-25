APP_URL="http://localhost:5000"

#De-register all apps in the system
curl -XDELETE $APP_URL/apps/register

#Register git as an app
curl -XPOST $APP_URL/apps/register/git -H "Content-Type: application/json" \
    -d "{\"sourceUrl\":\"https://github.com/git-for-windows/git/releases/download/v2.15.0.windows.1/Git-2.15.0-32-bit.exe\", \"system\": \"Windows\"}"

#Register notepad++ as an app
curl -XPOST $APP_URL/apps/register/notepad++ -H "Content-Type: application/json" \
    -d "{\"sourceUrl\":\"https://notepad-plus-plus.org/repository/7.x/7.5.1/npp.7.5.1.Installer.exe\", \"system\": \"Windows\"}"