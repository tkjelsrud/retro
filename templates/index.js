function openBoard() {
  $.ajax({
        url: '/retro/board/?board_id=' + 1,
        dataType: 'json',
        cache: false
    }).done(function(data){
      alert(data);
    //for(i = 0; i < data['notes'].length; i++) {
    //        nd = data['notes'][i];
    //        DrawNote(nd);
    //}
  });
}
