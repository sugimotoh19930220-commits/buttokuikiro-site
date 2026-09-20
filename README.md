# 麺屋 ぶっとく生きろ。公式サイト

このリポジトリは、[麺屋 ぶっとく生きろ。公式サイト](https://buttokuikiro.com/)のソースコードと変更履歴を管理する正本です。

## 管理対象

- 日本語トップページ: `public/index.html`
- 英語: `public/en/index.html`
- 韓国語: `public/ko/index.html`
- 中国語簡体字: `public/zh-hans/index.html`
- 中国語繁体字: `public/zh-hant/index.html`
- 求人ページ: `public/recruit/index.html`
- 画像・動画・検索エンジン向けファイル: `public/`
- 多言語ページ生成: `tools/build_i18n.py`
- Cloudflare Workers設定: `wrangler.jsonc`

## 役割分担

- GitHub: ソースコード、変更履歴、承認、復旧の正本
- ChatGPT: 依頼内容の整理、編集、検証、変更案の作成
- Cloudflare Workers: 公開サイトの配信
- ChatGPTプロジェクト「検索対策｜ウェブサイト作成｜3店舗（新宿亭 以外）」: 変更依頼と判断履歴の窓口

## 標準の変更手順

1. 杉本さんがChatGPTへ日本語で変更を依頼する
2. ChatGPTが`main`の最新版と公開サイトを確認する
3. 作業用ブランチで編集する
4. 日本語・多言語・構造化データ・スマートフォン表示を確認する
5. Pull Requestで変更前後と確認結果を提示する
6. 杉本さんの承認後に`main`へ反映する
7. Cloudflareへの公開結果と実サイトを確認する

`main`への直接編集と強制更新は行いません。

## 依頼例

> ぶっとく生きろ。の営業時間を変更してください。公開サイトとGitHubの最新版を確認し、まずプレビューと変更箇所を見せてください。本番公開は私の承認後に行ってください。スマートフォン表示と多言語ページも確認してください。

## セキュリティ

APIキー、パスワード、GitHubトークン、Cloudflareトークンなどはリポジトリへ保存しません。必要な認証情報は各サービスの秘密情報管理機能に保存します。

詳しい運用は [docs/OPERATIONS.md](docs/OPERATIONS.md) を参照してください。
