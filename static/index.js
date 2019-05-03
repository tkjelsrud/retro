function openBoard(id) {
  $.ajax({
        url: '/retro/board/' + id,
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
