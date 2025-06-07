# QSurveyMapReport
## 概要 Overview  
QSurveyMapReportは、写真ファイルのEXIF情報を解析し、QGIS上への点シンボルとして出力、写真をまとめたPDFレポートを作成する機能を備えたQGISプラグインです。
出力された点シンボルとPDFレポートと合わせることで、簡易な調査報告書を作成することが可能です。
 
QSurveyMapReport is a QGIS plugin that parses EXIF metadata from photo files, exports them as point symbols in QGIS, and compiles selected photos into a PDF report. By combining the exported point symbols and the PDF report, you can quickly generate a basic field survey report.


## 主な機能 Key features  
- 写真ファイルに保存されたEXIFメタデータ（GPS座標・撮影方位など）の解析及びCSVファイルへの出力
- 出力したCSVをQGISに読み込み、点シンボルとして出力
- 2行×3列のレイアウトによる写真、文章を含むPDFレポートの作成

--
- Parse EXIF metadata (GPS coordinates, camera direction, etc.) from image files and export to CSV  
- Load the generated CSV into QGIS and render as point symbols on the map  
- Create a PDF report with a 2×3 grid layout that includes photos and descriptive text  

## インストール方法 Installation  
1. リリースページから最新のプラグインをダウンロード
2.  **プラグイン > プラグインの管理とインストール > ZIPからインストール**より、ダウンロードしたZIPファイルを選択し、インストール
3. QGISを再起動
4. **プラグイン > プラグインの管理とインストール** から「QSurveyMapReport」を有効化

--
1. Download the latest plugin
2. In QGIS go to **Plugins > Manage and Install Plugins > Install from ZIP** and select the downloaded ZIP  
3. Restart QGIS  
4. Enable “QSurveyMapReport” under **Plugins > Manage and Install Plugins**

## 使い方 Usage  
1. QSurveyMapReportツールバーまたはメニューからプラグインを起動
2. **フォルダ選択** ボタンで、JPEG/PNG画像が格納されたディレクトリを指定
3. 画像一覧が表示されるので、**前へ/次へ** ボタンで切り替えながら説明文を入力
4. **CSV保存** でEXIFメタデータをCSVに出力
5. **CSVをQGISに読み込み** で地図上に点レイヤとして表示
6. **PDF作成** で注釈付き画像をまとめたPDFレポートを出力

--
1. Launch QSurveyMapReport from the QGIS toolbar or menu  
2. Click **Select Directory** and choose the folder containing JPEG/PNG images  
3. Browse images with **Previous/Next** buttons and enter descriptive text  
4. Click **Save CSV** to export EXIF metadata to CSV  
5. Click **Load CSV into QGIS** to display the CSV as a point layer on the map  
6. Click **Create PDF** to generate an annotated photo PDF report  


## 必要要件 Requirements  
- QGIS 3.x以降
- QGIS 3.x or later  

## ライセンス 
MIT License. 詳しくは [LICENSE](LICENSE) ファイルをご覧ください。  
MIT License. See the [LICENSE](LICENSE) file for details.