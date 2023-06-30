function postData() {
    var data1 = document.getElementById("dataInput1").value;
    var data2 = document.getElementById("dataInput2").value;
    var data3 = document.getElementById("dataInput3").value;

    // XMLHttpRequestオブジェクトを作成
    var xhr = new XMLHttpRequest();
  
    // POSTリクエストを作成
    xhr.open("POST", "src/generate_text.py");
  
    // リクエストヘッダを設定
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  
    // レスポンスが返ってきた時の処理
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        // レスポンスの処理
        var response = xhr.responseText;
        document.getElementById("result").innerHTML = response;
      }
    };
  
    // データを送信
    xhr.send("data1=" + encodeURIComponent(data1) + "&data2=" + encodeURIComponent(data2) + "&data3=" + encodeURIComponent(data3));
  }
  