function postData() {
    var lower = document.getElementById("lower-limit").value;
    var upper = document.getElementById("upper-limit").value;

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
    xhr.send(
      "lower=" + encodeURIComponent(lower) + "&upper=" + encodeURIComponent(upper)
    );
  }
  