//イベント
$(function() {
    //右へ要素を追加する。
    $('#left-btn').click(rightMove);
    
    //カテゴリ削除イベント
    $('#right-btn').click(leftMove);
});
 
//右へ要素を追加する。
function rightMove() {
    
    //左リストで選択している要素のIDを取得する。
    value = $("#leftList").children("option:selected").val();
 
    //要素が選択されている場合、以下を行う。
    if(value !== void 0){
 
        //左リストで選択している要素を取得する。
        element = $("#leftList").children("option:selected").html();
 
        //選択した要素を左リストから削除する。
        $("#" + value).remove();
 
        //選択した要素を、右リストへ追加する。
        $("#rightList").append('<option value = ' + value + ' id = ' + value + '>' + element + '</option>');
        
        //選択状態を開放する。
        $("#rightList").removeAttr("option:selected");
    }
}
 
//左へ要素を追加する。
function leftMove() {
    
    //右リストで選択している要素のIDを取得する。
    value = $("#rightList").children("option:selected").val();
 
    //要素が選択されている場合、以下を行う。
    if(value !== void 0){
 
        //右リストで選択している要素を取得する。
        element = $("#rightList").children("option:selected").html();
 
        //選択した要素を右リストから削除する。
        $("#" + value).remove();
 
        //選択した要素を、左リストへ追加する。
        $("#leftList").append('<option value = ' + value + ' id = ' + value + '>' + element + '</option>');
        
        //選択状態を開放する。
        $("#leftList").removeAttr("option:selected");
    }
}
//イベント
$(function() {
    //右へ要素を追加する。
    $('#left-btn').click(rightMove);
    
    //カテゴリ削除イベント
    $('#right-btn').click(leftMove);
});