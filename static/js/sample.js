$(function(){
 
  // 画面読込時に実行する。
  $("#controlArea").hide(); // 初期表示で隠しておく

  // 指定ボタンを押下すると処理を開始する
  $("#btn1").on("click", function() {
    $("#controlArea").show(); // div領域を表示
  });
 
  // 指定ボタンを押下すると処理を開始する
  $("#btn2").on("click", function() {
    $("#controlArea").hide(); // div領域を隠す
  });
 
});