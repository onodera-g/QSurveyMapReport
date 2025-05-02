# QSurveyMapReport
## 概要
QSurveyMapReportは、写真ファイルのEXIF情報を解析し、QGIS上への点シンボルとして出力、写真をまとめたPDFレポートを作成する機能を備えたQGISプラグインです。
出力された点シンボルとPDFレポートと合わせることで、簡易な調査報告書を作成することが可能です。

![image](https://github.com/user-attachments/assets/c0af08d4-817f-490d-8c3d-1c8448938f36)


![a](https://github.com/user-attachments/assets/e8f72265-1bab-4d23-a822-3ec66d0dd0b3)



## 主な機能
- 写真ファイルに保存されたEXIFメタデータ（GPS座標・撮影方位など）の解析及びCSVファイルへの出力
- 出力したCSVをQGISに読み込み、点シンボルとして出力
- 2行×3列のレイアウトによる写真、文章を含むPDFレポートの作成

## インストール方法
1. リリースページから最新のプラグイン本体(ZIPファイル)をダウンロード
2.  **プラグイン > プラグインの管理とインストール > ZIPからインストール**より、ダウンロードしたZIPファイルを選択し、インストール
3. QGISを再起動
4. **プラグイン > プラグインの管理とインストール** から「QSurveyMapReport」を有効化

## 使い方
1. QSurveyMapReportツールバーまたはメニューからプラグインを起動
2. **フォルダ選択** ボタンで、JPEG/PNG画像が格納されたディレクトリを指定
3. 画像一覧が表示されるので、**前へ/次へ** ボタンで切り替えながら説明文を入力
4. **CSV保存** でEXIFメタデータをCSVに出力
5. **CSVをQGISに読み込み** で地図上に点レイヤとして表示
6. **PDF作成** で注釈付き画像をまとめたPDFレポートを出力

![スクリーンショット 2025-04-28 130334](https://github.com/user-attachments/assets/999a6467-b6cd-45b5-9af3-ec75ebf487c1)

## 必要要件
- QGIS 3.x以降


