function postData() {
    var data = document.getElementById("dataInput").value;
  
    // XMLHttpRequestオブジェクトを作成
    var xhr = new XMLHttpRequest();
  
    // POSTリクエストを作成
    xhr.open("POST", "src/generate_text.py", true);
  
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
    xhr.send("data=" + encodeURIComponent(data));
  }
  