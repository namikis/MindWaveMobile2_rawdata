# MindWaveMobile2_rawdata
<p>研究室のシェア用。</p>
<p>thinkgearモジュールを使ってneurosky社のMindWaveMobile2で取得した脳波の生データと1秒おきのスペクトルデータをcsvファイルで出力します。</p>
<p>Python2.7でしか動かないので注意。</p>


$ docker build -t my-python-app .
$ docker run -it --rm --name my-running-app my-python-app
