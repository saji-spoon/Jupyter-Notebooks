<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Illust.aspx.cs" Inherits="TrainingManagementWeb.Omake.Illust" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <link href="../Content/Global.css" rel="stylesheet" />
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title></title>
    <script type="text/javascript">
        var data = new Array()

        function start() {
            canvas = document.getElementById('test');

            if (canvas.getContext) {
                ctx = canvas.getContext('2d');
            }

            function clickPoint(event) {
                if (document.classForm.selectClass[0].checked) {
                    fill1 = "#AA0000"
                    fill2 = "#111111"
                    classID = 0
                }
                else {
                    fill1 = "#0000AA"
                    fill2 = "#111111"
                    classID = 1
                }

                var x = 0;
                var y = 0;
                x = event.clientX - canvas.offsetLeft;
                y = event.clientY - canvas.offsetTop;

                drawDot(x, y, fill1, 3)

                drawDot(x, y, fill2, 1)

                data.push([x, y, classID])

            }

            canvas.addEventListener('click', clickPoint, true);

            //console.log(document.classForm.selectClass[0].checked)
        }

        function drawDot(x, y, color, size) {
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(x, y, size, 0, 2 * Math.PI);
            ctx.fill();
        }

        function EncodeHtmlForm(dataDict) {
            var oneParamQuerys = [];

            for (var name in dataDict) {
                var value = dataDict[name];
                oneParamQuerys.push(encodeURIComponent(name) + "=" + encodeURIComponent(value));
            }

            return oneParamQuerys.join("&").replace(/%20/g, "+");

        }

        function ajaxTest() {
            try {
                // IEの場合
                xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
            }
            catch (e) {
                try {
                    xmlHttp = new XMLHttpRequest();
                }
                catch (e2) {
                    console.log(e2.message)
                    return
                }
            }

            xmlHttp.onreadystatechange = function () {

                //メッセージ表示用の領域
                var message = document.getElementById("message")

                if (xmlHttp.readyState == 1) {
                    console.log("ready...");
                    message.textContent = "計算中"
                }
                if (xmlHttp.readyState == 4) {
                    if (xmlHttp.status == 200) {
                        //console.log("recieved===");
                        ajaxData = xmlHttp.responseText;
                        //console.log(data)
                        var arrData = ajaxData.split("\n")
                        if (arrData[0] == "recieved") {
                            dataBody = arrData.slice(1)
                            for (var idx in dataBody) {
                                //console.log(item)

                                var dataArray = dataBody[idx].split(",")
                                var x = parseFloat(dataArray[0])
                                var y = parseFloat(dataArray[1])
                                //console.log(dataArray[0], dataArray[1])
                                var fill = "";
                                if (dataArray[2] == "0")
                                {
                                    fill = "#CC8888";
                                }
                                else
                                {
                                    fill = "#8888CC";
                                }

                                drawDot(canvas.width * x, y * canvas.height, fill, 3)
                                //console.log("draw:" + x * canvas.width)
                            }

                            for(var idx in data)
                            {
                                var fill = "";
                                if (data[idx][2] == "0") {
                                    fill = "#AA0000";
                                }
                                else {
                                    fill = "#0000AA";
                                }
                                drawDot(data[idx][0], data[idx][1], fill, 3)
                            }
                            message.textContent = "完了！"
                        }
                        else 
                        {
                            message.textContent = "Pythonサービスとの通信に失敗しました…"
                        }
                    }
                    else {
                        console.log("Server Communication Failed. Status Code:" + xmlHttp.status);
                        message.textContent = "Webサーバーとの通信に失敗しました…"
                    }
                }
            }

            var trainData = data.join("\n");

            var dict = { "trainData": trainData };

            xmlHttp.open("POST", "Illust", true);

            xmlHttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');


            xmlHttp.send(EncodeHtmlForm(dict));


        }

        function handleDownload() {
            var content = data.join('\n');
            var blob = new Blob([content], { "type": "text/plain" });

            if (window.navigator.msSaveBlob) {
                window.navigator.msSaveBlob(blob, "test.txt");
            } else {
                document.getElementById("download").href = window.URL.createObjectURL(blob);
            }
        }

    </script>

</head>
<body onload="start();">
    <canvas id="test" width="300" height="300"></canvas>

    <!--<a href="#" id="download" download="test.txt" onclick="handleDownload()">ダウンロード</a>-->

    <form name="classForm">
        <input type="radio" name="selectClass" value="0" checked="checked"/>赤
        <input type="radio" name="selectClass" value="1"/>青
        <p><span style="font-family:'MS Pゴシック'">(*ﾟーﾟ)＜</span><span id="message">　　　</span></p>
        <input id="btAjax" type="button" value="境界を見つける" onclick="ajaxTest()" />
    </form>

    <style type="text/css">
        canvas {
            border: 1px solid #808080;
        }
    </style>
</body>
</html>
