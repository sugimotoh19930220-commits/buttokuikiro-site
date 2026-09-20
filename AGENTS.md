# Repository instructions

このリポジトリは「麺屋 ぶっとく生きろ。」公式サイトの本番ソースです。

## Before editing

- `README.md` と `docs/OPERATIONS.md` を読む。
- `main`、公開サイト、依頼内容の3点を照合する。
- 公開情報の営業時間、価格、住所、電話、求人条件は推測で変更しない。
- 本番公開は杉本さんの明示的な承認後に行う。
- `main`へ直接コミットせず、作業ブランチとPull Requestを使う。

## Source rules

- 日本語トップは `public/index.html` が正本。
- 多言語ページは原則 `tools/build_i18n.py` の文言を変更して再生成する。
- 生成後は英語・韓国語・中国語簡体字・繁体字の全ページを確認する。
- 求人ページは `public/recruit/index.html` を個別確認する。
- canonical、hreflang、JSON-LD、sitemap、robots.txtを壊さない。
- GA4の測定IDとイベント名を依頼なく変更しない。
- 画像・動画の権利関係と出典表記を削除・変更しない。
- APIキー、トークン、認証ファイル、個人用設定をコミットしない。

## Required verification

- 変更対象の文言とリンク
- 日本語と対象多言語
- 構造化データ
- スマートフォン幅とデスクトップ幅
- 内部リンクと主要外部リンク
- 求人、営業時間、価格など重要情報の整合
- 公開後の実サイト

## Deployment safety

- 現時点ではCloudflareの自動デプロイ接続が未確認。
- 接続状態を確認するまで、リポジトリ更新だけで公開完了と判断しない。
- 強制push、履歴改変、資格情報の追加、ドメイン・DNS変更を行わない。
- ロールバックは履歴を消さず、revertで行う。
