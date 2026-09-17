# Lab01 Commands And Screenshot Plan

Цей файл описує не шаблонні команди з лабораторної, а фактичні команди та дії, які були використані під час виконання в цьому робочому середовищі.

Поточний робочий каталог для більшості команд:

```powershell
F:\sobol\ai-systems-design-course\training-project
```

Для команд `git`, які стосуються всього клону, також використовувався каталог:

```powershell
F:\sobol\ai-systems-design-course
```

Змінна для гарантованого запуску WinGet-версії `uv`:

```powershell
$WingetUv='C:\Users\lstar\AppData\Local\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uv.exe'
$env:Path='C:\Program Files\GitHub CLI;C:\Users\lstar\AppData\Local\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe;' + $env:Path
```

## Крок 0: Прочитати лабораторну та перевірити стартовий стан

Фактично використані команди:

```powershell
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
Get-Content -LiteralPath 'C:\Users\lstar\Downloads\01_AI_Engineering_Foundations_Lab_uk.md' -Encoding UTF8 -Raw
Get-ChildItem -LiteralPath 'F:\sobol\ai-systems-design-course' -Force
git status --short
git remote -v
git branch --show-current
```

Скріншот: `reports/lab01/screenshots/step00-lab-and-start-state.png`

Що має бути видно: файл лабораторної відкритий або прочитаний, робоча папка `ai-systems-design-course`, поточний Git-стан.

## Крок 1: Передпольотна перевірка лише для читання

Фактично використані команди:

```powershell
$PSVersionTable.PSVersion
[Environment]::OSVersion.Version
winget --version
winget configure --help
```

Результат: Windows build `10.0.26200`, WinGet `v1.29.290`, `winget configure` доступний.

Скріншот: `reports/lab01/screenshots/step01-preflight.png`

Що має бути видно: версія PowerShell, версія Windows, версія WinGet і довідка `winget configure`.

## Крок 2: Форк, віддалені репозиторії та особиста гілка

Клон і форк уже існували. Було перевірено, що `origin` вказує на форк `exideys`, а `upstream` - на репозиторій викладача.

Фактично використані команди:

```powershell
git --version
git config --global user.name
git config --global user.email
git remote -v
git branch --show-current
Test-Path '..\modules\01_AI_Engineering_Foundations'
Test-Path '.\fixtures\windows\lab01-workstation.dsc.yaml'
Test-Path '.\boundary-proposal.yaml'
git branch --list
git switch -c lab01/exideys
git branch --show-current
git -C 'F:\sobol\ai-systems-design-course' rev-parse HEAD
```

Результат: гілка `lab01/exideys`, коміт `e4fb5c6bbb2cb150c6000ed1406dff10b6854690`.

Скріншот: `reports/lab01/screenshots/step02-remotes-and-branch.png`

Що має бути видно: `git remote -v`, `git branch --show-current`, наявність файлів `modules\01...` і `fixtures\windows\lab01-workstation.dsc.yaml`.

## Крок 3: Застосувати конфігурацію робочої станції двічі

Фактично використані команди:

```powershell
Start-Transcript -Path .\provision.log -Force
winget configure --file .\fixtures\windows\lab01-workstation.dsc.yaml --accept-configuration-agreements
winget configure --file .\fixtures\windows\lab01-workstation.dsc.yaml --accept-configuration-agreements
winget list --id Git.Git --exact --source winget
winget list --id GitHub.cli --exact --source winget
winget list --id astral-sh.uv --exact --source winget
winget list --id Obsidian.Obsidian --exact --source winget
Stop-Transcript
```

Додатково, через те що поточний shell ще не підхопив новий PATH:

```powershell
Get-ChildItem -Path 'C:\Program Files','C:\Program Files (x86)','$env:LOCALAPPDATA\Programs' -Filter gh.exe -Recurse -ErrorAction SilentlyContinue
& 'C:\Program Files\GitHub CLI\gh.exe' --version
Get-ChildItem -Path "$env:LOCALAPPDATA\Microsoft\WinGet\Packages","$env:LOCALAPPDATA\Programs","$env:USERPROFILE\.local","C:\Program Files" -Filter uv.exe -Recurse -ErrorAction SilentlyContinue
```

Результат: Git `2.54.0`, GitHub CLI `2.101.0`, WinGet package `uv 0.12.15`, Obsidian `1.13.7`.

Скріншот: `reports/lab01/screenshots/step03-workstation-packages.png`

Що має бути видно: завершення другого `winget configure` і чотири `winget list` результати.

## Крок 4: Підготувати пропонувача

Antigravity CLI не використовувався. Перевірка показала:

```powershell
agy --help
```

Результат: `agy` недоступний у PATH.

Фактично використаний шлях пропонувача: наявний AI-агент OpenAI Codex у цій сесії. Він прочитав локальні файли й відредагував лише `reports/lab01/boundary-proposal.yaml`.

Скріншот: `reports/lab01/screenshots/step04-proposer-session.png`

Що має бути видно: ця Codex-сесія або інший доказ того, що AI редагував тільки `reports/lab01/boundary-proposal.yaml` і не виконував `decide` / `apply`. Не показувати токени, ключі, email, приватні облікові дані.

## Крок 5: Ініціалізувати студентські каталоги та зовнішнє сховище

Фактично використані команди:

```powershell
New-Item -ItemType Directory -Force .\student\design | Out-Null
New-Item -ItemType Directory -Force .\reports\lab01\screenshots | Out-Null
Copy-Item .\boundary-proposal.yaml .\reports\lab01\boundary-proposal.yaml -Force
if (-not (Test-Path .\reports\lab01\REPORT.md)) { New-Item -ItemType File .\reports\lab01\REPORT.md | Out-Null }
New-Item -ItemType Directory -Force 'C:\Users\lstar\OneDrive\ai-systems-learning-vault\sources' | Out-Null
git -C 'F:\sobol\ai-systems-design-course' rev-parse HEAD
```

Файли зовнішнього vault були створені через Codex `apply_patch`, а не через PowerShell-запис:

```text
C:\Users\lstar\OneDrive\ai-systems-learning-vault\README.md
C:\Users\lstar\OneDrive\ai-systems-learning-vault\sources\module-01-ai-engineering-foundations.md
```

Скріншот: `reports/lab01/screenshots/step05-obsidian-vault.png`

Що має бути видно: Obsidian або провідник/редактор із vault `ai-systems-learning-vault`, `README.md`, `sources/module-01-ai-engineering-foundations.md` і повною YAML-передмовою. Сховище має бути поза `F:\sobol\ai-systems-design-course`.

## Крок 6: Відтворити та протестувати середовище проєкту

Фактично використані команди:

```powershell
$WingetUv='C:\Users\lstar\AppData\Local\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uv.exe'
$env:Path='C:\Program Files\GitHub CLI;C:\Users\lstar\AppData\Local\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe;' + $env:Path
& $WingetUv --version
& $WingetUv sync
& $WingetUv run python -m unittest discover -s tests/public -v
& $WingetUv run learning-project doctor --output .\reports\lab01\environment-report.json
& $WingetUv run learning-project validate .\reports\lab01\boundary-proposal.yaml
& $WingetUv run learning-project apply .\reports\lab01\boundary-proposal.yaml --decision .\reports\lab01\boundary-decision.json --output .\student\design\learning-system-boundary.yaml
if (Test-Path .\student\design\learning-system-boundary.yaml) { 'accepted-boundary-created' } else { 'accepted-boundary-not-created' }
```

Важливо: повний `discover -s tests/public -v` у цьому опублікованому дереві також знаходить Lab02-тести, хоча в `modules/` є тільки модуль 01; ці Lab02-тести падають через відсутні матеріали модуля 02. Для чистого Lab01-свідчення було виконано:

```powershell
& $WingetUv run python -m unittest discover -s tests/public -p 'test_lab01*.py' -v
```

Результат Lab01: `Ran 18 tests ... OK`. Передчасний `apply` відмовив через відсутній `boundary-decision.json`.

Скріншоти:

```text
reports/lab01/screenshots/step06-lab01-tests-ok.png
reports/lab01/screenshots/step06-doctor-and-premature-apply.png
```

Що має бути видно: успішні Lab01-тести, створення `environment-report.json`, успішний `validate`, помилка premature `apply`, і рядок `accepted-boundary-not-created`.

## Крок 7: Підготувати обмежену пропозицію

Фактична дія: файл `reports/lab01/boundary-proposal.yaml` був змінений через Codex `apply_patch`.

Ключові значення, які були внесені:

```yaml
proposal_id: lab01-learning-knowledge-boundary
status: proposed
personal_domain: Software engineering study notes for backend application design.
```

Скріншот: `reports/lab01/screenshots/step07-proposal-edit.png`

Що має бути видно: відкритий `reports/lab01/boundary-proposal.yaml` після редагування зі `status: proposed`.

## Крок 8: Перевірити та розглянути пропозицію

Фактично використані команди:

```powershell
& $WingetUv run learning-project validate .\reports\lab01\boundary-proposal.yaml
git diff -- .\reports\lab01\boundary-proposal.yaml
git diff --no-index -- .\boundary-proposal.yaml .\reports\lab01\boundary-proposal.yaml
```

Примітка: `git diff -- .\reports\lab01\boundary-proposal.yaml` не показав diff, бо файл ще був untracked. Тому для видимого порівняння стартової та студентської пропозиції використовувався `git diff --no-index`.

Семантичний розгляд записано в `reports/lab01/REPORT.md` до запуску `decide`.

Скріншот: `reports/lab01/screenshots/step08-validate-and-review.png`

Що має бути видно: `Proposal lab01-learning-knowledge-boundary is valid` і частину семантичного розгляду в `REPORT.md`.

## Крок 9: Зафіксувати людське затвердження та застосувати контракт

Фактично використані команди:

```powershell
& $WingetUv run learning-project decide .\reports\lab01\boundary-proposal.yaml --approve --by "exideys" --decision .\reports\lab01\boundary-decision.json
& $WingetUv run learning-project apply .\reports\lab01\boundary-proposal.yaml --decision .\reports\lab01\boundary-decision.json --output .\student\design\learning-system-boundary.yaml
Get-Content .\reports\lab01\boundary-decision.json -Raw
Get-Content .\student\design\learning-system-boundary.yaml -Raw
```

Результат: approved decision для `lab01-learning-knowledge-boundary`, SHA-256 `fc85c066ad831023fa3d26f15985639a603650d21b4a76ebeb885c811b716d01`, прийнятий контракт створено.

Скріншот: `reports/lab01/screenshots/step09-decision-and-contract.png`

Що має бути видно: `boundary-decision.json` зі статусом `approved` і `learning-system-boundary.yaml` зі `status: approved`.

## Крок 10: Підготувати свідчення, перевірити та зафіксувати результат

Фактично використані команди:

```powershell
Copy-Item .\provision.log .\reports\lab01\provision.log -Force
Select-String -Path .\reports\lab01\provision.log -Pattern 'token|secret|password|authorization|bearer|ghp_|github_pat_|@' -CaseSensitive:$false
git status --short
git diff --check
```

Фінальна перевірка Lab01:

```powershell
& $WingetUv run python -m unittest discover -s tests/public -p 'test_lab01*.py' -v
& $WingetUv run learning-project doctor --output .\reports\lab01\environment-report.json
& $WingetUv run learning-project validate .\reports\lab01\boundary-proposal.yaml
& $WingetUv run learning-project apply .\reports\lab01\boundary-proposal.yaml --decision .\reports\lab01\boundary-decision.json --output .\student\design\learning-system-boundary.yaml
Get-Content .\reports\lab01\environment-report.json -Raw | ConvertFrom-Json | Out-Null
git remote -v
git branch --show-current
git diff --check
git status --short
```

Команди для коміту та push виконуються після створення цього файлу:

```powershell
git add student/design/learning-system-boundary.yaml reports/lab01
git commit -m "feat(lab01): establish governed AI system boundary"
git status --short
git rev-parse HEAD
git push -u origin HEAD
```

Скріншоти:

```text
reports/lab01/screenshots/step10-final-verification.png
reports/lab01/screenshots/step10-git-commit.png
```

Що має бути видно: фінальна перевірка, `git remote -v`, гілка `lab01/exideys`, `git diff --check`, `git status --short`, коміт і hash. Для Teams також потрібно окремо подати URL форку, назву гілки й точний hash коміту.
