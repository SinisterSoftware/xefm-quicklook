# QuickLook for XeFM（日本語）

XeFM でフォーカス中の項目を、Windows 用アプリ **QuickLook** でプレビューする拡張機能です。QuickLook 本体はこの拡張機能には含まれません。別途インストールし、`quicklook.exe` を PATH から起動できるようにしてください。

## 必要な環境

- **Windows**。この拡張機能は Windows 専用です。
- **XeFM 1.10.0 以降**。
- 別途インストール済みの QuickLook for Windows。`quicklook.exe` が PATH 上に必要です。
- 拡張機能が使う Python パッケージ `psutil` と `pywin32`。インストール時に依存パッケージの同期を求められたら許可してください。後から同期する場合は、XeFM の **Tools ▸ Advanced ▸ Sync Python Packages** を実行します。

## インストール

XeFM を使っている Windows 環境で、ターミナルから次を実行します。

```powershell
xefm ext install github:SinisterSoftware/xefm-quicklook
```

インストーラーが拡張機能の内容と依存パッケージを表示したら、内容を確認してインストールを承認してください。インストール後、**Tools ▸ Reload Configuration** を選ぶか XeFM を再起動します。

インストールを確認するには、次を実行します。

```powershell
xefm ext list
```

## 使い方

拡張機能が読み込まれると、アクション `quicklook.preview` が追加されます。XeFM のコマンドパレットからこのアクションを選ぶと、フォーカス中の項目を QuickLook で開きます。

この拡張機能は **Alt-Z** をキー候補として提案しますが、自動でキーに割り当てるわけではありません。キーで呼び出す場合は `~/.xefm/config.py` の `Config.KEY_BINDINGS` にアクション名と使いたいキーを追加します。たとえば次のように設定します。

```python
class Config:
    KEY_BINDINGS = {
        "quicklook.preview": ["Alt-Z"],
    }
```

既存の `Config` や `KEY_BINDINGS` がある場合は、新しい `Config` や辞書を重ねて定義せず、既存の設定に `'quicklook.preview': ['Alt-Z']` の項目を加えてください。Alt-Z が現在のキーマップや設定ですでに使われている場合は、競合しないキーを選ぶか、既存アクションの割り当ても調整してください。設定を変更した後は **Tools ▸ Reload Configuration** を選ぶか XeFM を再起動します。

## 表示位置

プレビューウィンドウは XeFM と同じモニターの作業領域（タスクバーを除いた範囲）に配置されます。左ペインがアクティブなら画面右側、右ペインがアクティブなら画面左側です。実装上のウィンドウ幅は 600 ピクセル、高さは最大 800 ピクセルです。

## 制限と注意

- 仮想フォルダー内の項目は開けません。対象のパスが仮想パスの場合、拡張機能はメッセージを表示して終了します。
- フォーカス中の項目がない場合は何もせず終了します。
- QuickLook が対応するファイル形式やプレビュー内容は、インストールしている QuickLook 本体とそのプラグインに依存します。
- 拡張機能は QuickLook の起動を待ってから対象パスを渡し、ウィンドウを配置します。環境によって QuickLook の起動やウィンドウ表示に時間がかかる場合、位置調整が間に合わないことがあります。

## トラブルシューティング

**「quicklook.exe」が見つからない、またはアクションを実行できない**

QuickLook for Windows がインストールされていることを確認し、`quicklook.exe` を含むフォルダーが PATH に登録されていることを確認してください。PATH を変更した後は XeFM を再起動してから、もう一度試してください。

**依存パッケージに関するエラーが出る**

XeFM の **Tools ▸ Advanced ▸ Sync Python Packages** を実行し、`psutil` と `pywin32` を同期してください。同期後にまだ読み込まれない場合は、XeFM を再起動してください。

**キーを押してもアクションが実行されない**

`quicklook.preview` が `KEY_BINDINGS` に正確に記載されていること、設定を再読み込みしたことを確認してください。また、同じキーが別のアクションに割り当てられていないか、使用中のキーマップと `config.py` の両方を確認してください。キー割り当てがなくても、コマンドパレットからアクションを実行できます。

**プレビューが表示されない、または位置が合わない**

仮想フォルダーではなく通常のファイルを選択していること、QuickLook が PATH から起動できることを確認してください。ファイル形式によっては QuickLook 側でプレビューできないことがあります。起動に時間がかかる環境では、QuickLook を先に起動してから再度アクションを実行すると改善する場合があります。

## 更新とアンインストール

更新可能なバージョンを確認して更新するには、次を実行します。

```powershell
xefm ext outdated
xefm ext upgrade quicklook
```

拡張機能を削除するには、次を実行します。

```powershell
xefm ext uninstall quicklook
```
